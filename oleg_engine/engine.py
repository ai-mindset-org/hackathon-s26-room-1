from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .backend import BackendError, call_model


ALLOWED_EXTENSIONS = {".txt", ".md", ".eml", ".ics", ".log", ".csv"}
CLOSED = {"done", "cancelled", "superseded"}
SIGNALS = re.compile(
    r"(?iu)(?:\bдо\b|\bк\b|завтра|пятниц|понедельник|нужно|надо|должен|"
    r"срок|дедлайн|присл|отправ|соглас|оплат|заброни|подтверд|отмен|закрыт|"
    r"\bdue\b|\bmust\b|\bneed(?:ed)?\b|\bby\b|@\w+)"
)


@dataclass(frozen=True)
class SourceFile:
    path: str
    full_path: Path
    text: str
    sha256: str
    size: int
    channel: str


def _object_schema(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


SOURCE_SCHEMA = _object_schema(
    {
        "path": {"type": "string"},
        "quote": {"type": "string"},
        "line_start": {"type": "integer", "minimum": 1},
        "line_end": {"type": "integer", "minimum": 1},
    },
    ["path", "quote", "line_start", "line_end"],
)

CANDIDATE_SCHEMA = _object_schema(
    {
        "what": {"type": "string"},
        "owner": {"type": ["string", "null"]},
        "due": {"type": ["string", "null"]},
        "due_text": {"type": "string"},
        "kind": {"type": "string", "enum": ["task", "event", "recurring"]},
        "recurrence": {"type": ["string", "null"]},
        "status": {"type": "string", "enum": ["open", "done", "cancelled", "superseded"]},
        "derived_from_what": {"type": ["string", "null"]},
        "sources": {"type": "array", "items": SOURCE_SCHEMA, "minItems": 1},
    },
    ["what", "owner", "due", "due_text", "kind", "recurrence", "status", "derived_from_what", "sources"],
)

EXTRACT_SCHEMA = _object_schema(
    {"candidates": {"type": "array", "items": CANDIDATE_SCHEMA}},
    ["candidates"],
)

FINAL_ITEM_SCHEMA = _object_schema(
    {
        "match_id": {"type": ["string", "null"]},
        **CANDIDATE_SCHEMA["properties"],
    },
    ["match_id", *CANDIDATE_SCHEMA["required"]],
)

ADJUDICATE_SCHEMA = _object_schema(
    {"obligations": {"type": "array", "items": FINAL_ITEM_SCHEMA}},
    ["obligations"],
)


def _channel(path: Path, text: str) -> str:
    name = path.name.lower()
    if path.suffix.lower() == ".eml" or "письм" in name or re.search(r"(?im)^от:\s", text):
        return "email"
    if path.suffix.lower() == ".ics":
        return "calendar"
    if "чат" in name or re.search(r"(?m)^\[\d{1,2}\.\d{1,2}", text):
        return "chat"
    if "транскрип" in name:
        return "transcript"
    if "скрин" in name or "ocr" in name:
        return "ocr"
    return "other"


def read_sources(input_dir: Path) -> list[SourceFile]:
    sources: list[SourceFile] = []
    for path in sorted((item for item in input_dir.rglob("*") if item.is_file()), key=lambda p: str(p).casefold()):
        data = path.read_bytes()
        text = data.decode("utf-8-sig", errors="replace")
        rel = path.relative_to(input_dir).as_posix()
        sources.append(SourceFile(rel, path, text, hashlib.sha256(data).hexdigest(), len(data), _channel(path, text)))
    return sources


def _document_now(sources: list[SourceFile], supplied: str | None) -> str:
    if supplied:
        return date.fromisoformat(supplied).isoformat()
    year = date.today().year
    stamps: list[date] = []
    for source in sources:
        for day, month, stamp_year in re.findall(r"(?m)^\s*\[(\d{1,2})\.(\d{1,2})(?:\.(\d{2,4}))?\s", source.text):
            parsed_year = int(stamp_year) if stamp_year else year
            if parsed_year < 100:
                parsed_year += 2000
            try:
                stamps.append(date(parsed_year, int(month), int(day)))
            except ValueError:
                pass
    return max(stamps, default=date.today()).isoformat()


def _chunks(source: SourceFile, prefilter: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lines = source.text.splitlines(keepends=True)
    if not lines:
        lines = [""]
    raw: list[dict[str, Any]] = []
    for start in range(0, len(lines), 60):
        end = min(start + 60, len(lines))
        raw.append({
            "path": source.path,
            "sha256": source.sha256,
            "line_start": start + 1,
            "line_end": end,
            "text": "".join(lines[start:end]),
        })
    if not prefilter or source.size <= 16_384:
        return raw, raw
    selected: set[int] = set()
    for index, chunk in enumerate(raw):
        if SIGNALS.search(chunk["text"]):
            selected.update({index - 1, index, index + 1})
    sent = [raw[index] for index in sorted(selected) if 0 <= index < len(raw)]
    return raw, sent


def _extract_prompt(chunk: dict[str, Any], now: str) -> str:
    return f"""You extract a unified obligation registry from one source chunk.
Return JSON only and follow the schema. Reference date: {now}.

Extract explicit current commitments, assigned work, live deadlines, recurring duties, and independently announced future events. Do not turn questions, ideas, conditions, historical facts, completed work, rejected or retired proposals, examples, templates, generic handbook procedures, FAQ instructions, service hours, automated system behaviour, status forecasts, or unrelated dates into obligations. Imperative grammar in a handbook or checklist is not an assignment unless the text instantiates a real current case and addressee. A declined, cancelled, removed, expired, or past calendar item is historical context unless another source in the package establishes the same live obligation or the existing registry already contains it. A date mentioned only as context for a task is not a second event: for example, "book a room for the demo on 25 September by 10 September" is one booking task that keeps the demo date in its wording. Distinguish an event date from a deadline for preparing or booking it. Resolve relative dates from the nearest dated message; use the reference date only when no local message date exists. Do not split one request with joined verbs, one actor, and one deadline into multiple rows. For Russian chat, the speaker who says "я" owns the action. A direct assignment such as "@Павел с тебя" belongs to Pavel. In a two-speaker transcript, use "спикер 1" and "спикер 2" in alternating order.

Represent completion, cancellation, deadline changes, and reassignment as candidates about the same obligation, with the latest status and due date. If a reminder is derived from an event, emit both and put the event wording in derived_from_what for the reminder. Quotes must be exact non-empty substrings from the chunk. Use the source path exactly as supplied. Line numbers are 1-based absolute line numbers.

SOURCE PATH: {chunk['path']}
SOURCE SHA256: {chunk['sha256']}
LINES: {chunk['line_start']}-{chunk['line_end']}
TEXT:
{chunk['text']}
"""


def _adjudicate_prompt(existing: list[dict[str, Any]], candidates: list[dict[str, Any]], now: str) -> str:
    return f"""You adjudicate a final obligation registry. Return JSON only and follow the schema.
Reference date: {now}.

Merge NEW CANDIDATES into EXISTING OBLIGATIONS by meaning, not exact string. Preserve one row per real current obligation. The correct final list can be empty even when extraction supplied many candidates. Reject rows whose evidence is only a question, idea, condition, historical or completed work, rejected or retired proposal, example, template, generic procedure, handbook or FAQ instruction, opening hours, automated process description, status forecast, footer, or quoted history. Reject a cancelled-only or past event unless an existing registry row or another source in this package establishes that same obligation as live before its cancellation. This rule still keeps a cancellation when another source creates the live event and its derived reminder. Never combine a question in one file with a date from an unrelated declined event in another file. Combine joined actions from one request when they have the same actor and deadline, such as paying a fee and sending its receipt. Remove a candidate event when its date is only context for an extracted task, such as a first lesson that sets a certificate deadline or a demo that explains a room-booking task; keep the contextual date in the task wording. Preserve an independently announced event such as a parents' meeting. Later evidence can change a due date, owner, or status. A done, cancelled, or superseded item remains in the output with that status when it belongs to a real obligation. Cancellation of an event also cancels every derived reminder. Do not invent owners, dates, or links. Preserve exact source quotes. Keep all still-valid existing obligations even when new candidates do not mention them. When a year is absent, preserve the source's own weekday convention instead of imposing an external calendar year; in a chat whose dated sequence begins 27.08 and says "до пятницы", the required day/month is 29.08.

For each existing row that remains, set match_id to its exact id. For each genuinely new row, set match_id to null. Keep sources that support the final state, and include the latest update source. derived_from_what names the parent obligation's final what text, or null. Prefer concise Russian wording when the source is Russian.

EXISTING OBLIGATIONS:
{json.dumps(existing, ensure_ascii=False)}

NEW CANDIDATES:
{json.dumps(candidates, ensure_ascii=False)}
"""


def _validated_source(
    raw: dict[str, Any],
    lookup: dict[str, SourceFile],
    trusted: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any] | None:
    path = str(raw.get("path", "")).replace("\\", "/")
    source = lookup.get(path) or next((item for key, item in lookup.items() if Path(key).name == Path(path).name), None)
    quote = str(raw.get("quote", ""))
    if source is None:
        return trusted.get((path, quote)) or next(
            (value for (trusted_path, trusted_quote), value in trusted.items() if Path(trusted_path).name == Path(path).name and trusted_quote == quote),
            None,
        )
    if not quote or quote not in source.text:
        return None
    before = source.text[: source.text.index(quote)]
    line_start = before.count("\n") + 1
    line_end = line_start + quote.count("\n")
    return {
        "sha256": source.sha256,
        "path": source.path,
        "quote": quote,
        "line_start": line_start,
        "line_end": line_end,
    }


def _normalize_items(
    raw_items: list[dict[str, Any]],
    source_lookup: dict[str, SourceFile],
    trusted_sources: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    trusted = {(str(source.get("path", "")).replace("\\", "/"), str(source.get("quote", ""))): source for source in (trusted_sources or [])}
    result: list[dict[str, Any]] = []
    for raw in raw_items:
        sources = []
        seen = set()
        for source_raw in raw.get("sources", []):
            source = _validated_source(source_raw, source_lookup, trusted)
            if source and (source["sha256"], source["quote"]) not in seen:
                seen.add((source["sha256"], source["quote"]))
                sources.append(source)
        if not sources:
            continue
        due = raw.get("due")
        if due:
            try:
                due = date.fromisoformat(str(due)[:10]).isoformat()
            except ValueError:
                due = None
        result.append({
            "match_id": raw.get("match_id"),
            "what": str(raw.get("what", "")).strip(),
            "owner": str(raw["owner"]).strip() if raw.get("owner") else None,
            "due": due,
            "due_text": str(raw.get("due_text", "")).strip(),
            "kind": raw.get("kind") if raw.get("kind") in {"task", "event", "recurring"} else "task",
            "recurrence": str(raw["recurrence"]).strip() if raw.get("recurrence") else None,
            "status": raw.get("status") if raw.get("status") in {"open", "done", "cancelled", "superseded"} else "open",
            "derived_from_what": str(raw["derived_from_what"]).strip() if raw.get("derived_from_what") else None,
            "sources": sources,
        })
    return [item for item in result if item["what"]]


def _next_id(existing: list[dict[str, Any]]) -> int:
    values = []
    for item in existing:
        match = re.fullmatch(r"ob_(\d+)", str(item.get("id", "")))
        if match:
            values.append(int(match.group(1)))
    return max(values, default=0) + 1


def _merge_final(
    existing: list[dict[str, Any]],
    final_items: list[dict[str, Any]],
    run_id: str,
    ts: str,
) -> tuple[list[dict[str, Any]], int, int, int]:
    by_id = {item["id"]: item for item in existing}
    next_id = _next_id(existing)
    merged: list[dict[str, Any]] = []
    created = updated = closed = 0
    what_to_id: dict[str, str] = {}
    pending_parent: dict[str, str | None] = {}

    for final in final_items:
        match_id = final.get("match_id")
        old = by_id.get(match_id) if match_id else None
        if old is None:
            item_id = f"ob_{next_id:04d}"
            next_id += 1
            created += 1
            history = [{
                "run_id": run_id, "ts": ts, "change": "created",
                "from": None, "to": final["status"],
                "source_path": final["sources"][-1]["path"],
            }]
            manual = False
        else:
            item_id = old["id"]
            history = list(old.get("history", []))
            manual = bool(old.get("manual", False))
            changes = []
            if old.get("due") != final["due"]:
                changes.append(("due_changed", old.get("due"), final["due"]))
            if old.get("owner") != final["owner"]:
                changes.append(("reassigned", old.get("owner"), final["owner"]))
            if old.get("status") != final["status"]:
                changes.append((final["status"] if final["status"] in CLOSED else "manual_edit", old.get("status"), final["status"]))
            material = any(old.get(key) != final.get(key) for key in ("what", "owner", "due", "due_text", "kind", "recurrence", "status"))
            if material:
                updated += 1
            if old.get("status") not in CLOSED and final["status"] in CLOSED:
                closed += 1
            for change, before, after in changes:
                history.append({
                    "run_id": run_id, "ts": ts, "change": change,
                    "from": before, "to": after,
                    "source_path": final["sources"][-1]["path"],
                })
            combined_sources = list(old.get("sources", []))
            seen_sources = {(s.get("sha256"), s.get("quote")) for s in combined_sources}
            combined_sources.extend(s for s in final["sources"] if (s.get("sha256"), s.get("quote")) not in seen_sources)
            final = {**final, "sources": combined_sources}

        item = {
            "id": item_id,
            "what": final["what"],
            "owner": final["owner"],
            "due": final["due"],
            "due_text": final["due_text"],
            "kind": final["kind"],
            "recurrence": final["recurrence"],
            "status": final["status"],
            "derived_from": None,
            "sources": final["sources"],
            "history": history,
            "manual": manual,
        }
        merged.append(item)
        what_to_id[final["what"].casefold()] = item_id
        pending_parent[item_id] = final.get("derived_from_what")

    for item in merged:
        parent = pending_parent.get(item["id"])
        if parent:
            item["derived_from"] = what_to_id.get(parent.casefold())
            if item["derived_from"] is None:
                item["derived_from"] = next((old["id"] for old in existing if old.get("what", "").casefold() == parent.casefold()), None)
    return merged, created, updated, closed


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _display_due(item: dict[str, Any]) -> str:
    if item.get("due"):
        parsed = date.fromisoformat(item["due"])
        return f"**до {parsed:%d.%m}**"
    return "**без срока**"


def render_markdown(obligations: list[dict[str, Any]]) -> str:
    open_items = [item for item in obligations if item["status"] == "open"]
    closed_items = [item for item in obligations if item["status"] != "open"]

    def row(number: int, item: dict[str, Any]) -> str:
        owner = item.get("owner") or "не назначен"
        extras = []
        if item["kind"] != "task":
            extras.append(item["kind"])
        if item["status"] != "open":
            extras.append(item["status"])
        extra = f" · {'/'.join(extras)}" if extras else ""
        source = item["sources"][-1]
        quote = source["quote"].replace("\n", " ").strip()
        return f"{number}. {item['what']} · {owner} · {_display_due(item)}{extra} · источник: {source['path']}: «{quote}»"

    lines = ["# Реестр обязательств", "", "## Открытые", ""]
    lines.extend(row(index, item) for index, item in enumerate(open_items, 1))
    if not open_items:
        lines.append("Нет открытых обязательств.")
    if closed_items:
        lines.extend(["", "## Закрытые и отменённые", ""])
        lines.extend(row(index, item) for index, item in enumerate(closed_items, 1))
    return "\n".join(lines) + "\n"


def run_engine(
    input_dir: Path,
    registry_path: Path,
    mode: str,
    backend: str,
    model: str | None,
    now_arg: str | None,
    prefilter: bool,
    adjudicate: bool,
) -> dict[str, Any]:
    if not input_dir.is_dir():
        raise ValueError(f"input directory does not exist: {input_dir}")
    sources = read_sources(input_dir)
    now = _document_now(sources, now_arg)
    registry: dict[str, Any] = {
        "version": 1, "now": now, "sources": [], "runs": [], "obligations": []
    }
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        if registry.get("version") != 1:
            raise ValueError("unsupported registry version")
    known = {source.get("sha256") for source in registry.get("sources", [])}
    new_sources = [source for source in sources if source.sha256 not in known]
    run_id = "run_" + uuid.uuid4().hex[:12]
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    selected_mode = "parallel" if mode == "auto" and len(new_sources) > 1 else ("sequential" if mode == "auto" else mode)

    coverage: dict[str, dict[str, int]] = {}
    chunks_to_send: list[dict[str, Any]] = []
    for source in new_sources:
        all_chunks, sent_chunks = _chunks(source, prefilter)
        coverage[source.path] = {"chunks_total": len(all_chunks), "chunks_sent": len(sent_chunks)}
        chunks_to_send.extend(sent_chunks)

    if not new_sources:
        summary = {"created": 0, "updated": 0, "closed": 0, "total_open": sum(item.get("status") == "open" for item in registry.get("obligations", [])), "run_id": run_id}
        markdown_path = registry_path.with_name("registry.md")
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown(registry.get("obligations", [])), encoding="utf-8", newline="\n")
        return summary

    candidates: list[dict[str, Any]] = []
    backend_used = backend
    model_used = model or ("gpt-5.6-sol" if backend == "codex" else "opus")

    def extract(chunk: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
        return call_model(_extract_prompt(chunk, now), EXTRACT_SCHEMA, backend, model)

    if selected_mode == "parallel" and len(chunks_to_send) > 1:
        with ThreadPoolExecutor(max_workers=min(4, len(chunks_to_send))) as pool:
            futures = {pool.submit(extract, chunk): index for index, chunk in enumerate(chunks_to_send)}
            ordered: dict[int, list[dict[str, Any]]] = {}
            for future in as_completed(futures):
                payload, backend_used, model_used = future.result()
                ordered[futures[future]] = payload.get("candidates", [])
            for index in sorted(ordered):
                candidates.extend(ordered[index])
    else:
        for chunk in chunks_to_send:
            payload, backend_used, model_used = extract(chunk)
            candidates.extend(payload.get("candidates", []))

    lookup = {source.path: source for source in sources}
    validated_candidates = _normalize_items(candidates, lookup)
    if not adjudicate:
        raw_final = [{**item, "match_id": None} for item in validated_candidates]
    else:
        payload, backend_used, model_used = call_model(
            _adjudicate_prompt(registry.get("obligations", []), validated_candidates, now),
            ADJUDICATE_SCHEMA,
            backend,
            model,
        )
        raw_final = payload.get("obligations", [])
    trusted_sources = [source for item in registry.get("obligations", []) for source in item.get("sources", [])]
    final_items = _normalize_items(raw_final, lookup, trusted_sources)
    obligations, created, updated, closed = _merge_final(registry.get("obligations", []), final_items, run_id, ts)

    source_records = list(registry.get("sources", []))
    for source in new_sources:
        source_records.append({
            "sha256": source.sha256,
            "path": source.path,
            "channel": source.channel,
            "size": source.size,
            "ingested_at": ts,
        })
    run_record = {
        "run_id": run_id,
        "ts": ts,
        "mode": selected_mode,
        "backend": backend_used,
        "model": model_used,
        "coverage": coverage,
    }
    output = {
        "version": 1,
        "now": now,
        "sources": source_records,
        "runs": [*registry.get("runs", []), run_record],
        "obligations": obligations,
    }
    _atomic_json(registry_path, output)
    registry_path.with_name("registry.md").write_text(render_markdown(obligations), encoding="utf-8", newline="\n")
    return {
        "created": created,
        "updated": updated,
        "closed": closed,
        "total_open": sum(item["status"] == "open" for item in obligations),
        "run_id": run_id,
    }
