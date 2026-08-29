from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


class BackendError(RuntimeError):
    pass


def _search_path() -> str:
    extra: list[str] = []
    for base in (os.environ.get("USERPROFILE"), os.environ.get("HOME")):
        if base:
            extra += [os.path.join(base, "bin"), os.path.join(base, ".local", "bin")]
    if os.environ.get("APPDATA"):
        extra.append(os.path.join(os.environ["APPDATA"], "npm"))
    return os.pathsep.join([os.environ.get("PATH", ""), *extra])


def _executable(name: str) -> tuple[str, bool]:
    """Resolve a CLI; returns (command, use_shell). use_shell is the last resort when nothing resolves."""
    candidates = [name + ".cmd", name + ".exe", name] if os.name == "nt" else [name]
    path = _search_path()
    for candidate in candidates:
        resolved = shutil.which(candidate, path=path)
        if resolved:
            return resolved, False
    return name, True


def _decode_json(text: str) -> Any:
    text = text.strip()
    fence_start = text.find("```json")
    if fence_start < 0:
        fence_start = text.find("```")
    if fence_start >= 0:
        content_start = text.find("\n", fence_start)
        fence_end = text.find("```", content_start + 1)
        if content_start >= 0 and fence_end > content_start:
            return _decode_json(text[content_start + 1 : fence_end])
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        value = None
        for start, character in enumerate(text):
            if character != "{":
                continue
            try:
                candidate, _ = decoder.raw_decode(text[start:])
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                value = candidate
                break
        if value is None:
            raise
    if isinstance(value, dict) and isinstance(value.get("result"), str):
        return _decode_json(value["result"])
    return value


def _coerce_response(value: Any, schema: dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        array_properties = [
            name
            for name, definition in schema.get("properties", {}).items()
            if definition.get("type") == "array"
        ]
        if len(array_properties) == 1:
            return {array_properties[0]: value}
    raise ValueError("backend response does not match the requested top-level object")


def _run_codex(prompt: str, schema: dict[str, Any], model: str) -> dict[str, Any]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="oleg-engine-") as temp:
        temp_path = Path(temp)
        schema_path = temp_path / "schema.json"
        output_path = temp_path / "answer.json"
        schema_path.write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")
        codex, use_shell = _executable("codex")
        command = [
            codex, "exec", "-m", model,
            "-c", "model_reasoning_effort=high",
            "--skip-git-repo-check", "--sandbox", "read-only",
            "--ignore-rules", "--disable", "default_mode_request_user_input",
            "--output-schema", str(schema_path), "-o", str(output_path), "-",
        ]
        for attempt in range(2):
            output_path.unlink(missing_ok=True)
            try:
                completed = subprocess.run(
                    command,
                    input=prompt,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=420,
                    check=False,
                    shell=use_shell,
                )
                if completed.returncode != 0:
                    failures.append(f"attempt {attempt + 1}: exit {completed.returncode}: {completed.stderr[-300:]!r}")
                    continue
                raw = output_path.read_text(encoding="utf-8") if output_path.exists() else completed.stdout
                return _coerce_response(_decode_json(raw), schema)
            except FileNotFoundError as exc:
                failures.append(f"attempt {attempt + 1}: FileNotFoundError: {exc}; searched PATH={_search_path()}")
            except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError) as exc:
                failures.append(f"attempt {attempt + 1}: {type(exc).__name__}: {exc}")
    raise BackendError("codex failed twice: " + "; ".join(failures))


def _run_claude(prompt: str, model: str, schema: dict[str, Any]) -> dict[str, Any]:
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    claude, use_shell = _executable("claude")
    command = [
        claude, "-p", "--model", model,
        "--output-format", "json",
        "--mcp-config", '{"mcpServers":{}}', "--strict-mcp-config",
    ]
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=420,
        check=False,
        env=env,
        shell=use_shell,
    )
    if completed.returncode != 0:
        raise BackendError(f"claude failed: exit {completed.returncode}: {completed.stderr[-500:]}")
    try:
        return _coerce_response(_decode_json(completed.stdout), schema)
    except (ValueError, json.JSONDecodeError) as exc:
        raise BackendError(
            f"claude returned invalid JSON: {exc}: stdout[:300]={completed.stdout[:300]!r}; stderr tail={completed.stderr[-200:]!r}"
        ) from exc


def call_model(
    prompt: str,
    schema: dict[str, Any],
    backend: str,
    model: str | None,
) -> tuple[dict[str, Any], str, str]:
    if backend == "claude":
        selected = model or "opus"
        return _run_claude(prompt, selected, schema), "claude", selected

    selected = model or "gpt-5.6-sol"
    try:
        return _run_codex(prompt, schema, selected), "codex", selected
    except BackendError as codex_error:
        try:
            return _run_claude(prompt, "opus", schema), "claude", "opus"
        except BackendError as claude_error:
            raise BackendError(f"{codex_error}; fallback {claude_error}") from claude_error
