"""Focused tests for the demo server's registry view."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from demo import serve


# Reduced from one real run of examples/01-разнородный-вход on 2026-08-28.
REGISTRY_FIXTURE = r"""
{
  "nodes": {
    "source": [
      {"id": "src-email", "kind": "email", "name": "письмо-школа.txt"},
      {"id": "src-call", "kind": "transcript", "name": "транскрипт-созвона.txt"}
    ],
    "chunk": [
      {"id": "ch-1", "quote": "Оплатить кружок до 5 сентября.", "source_id": "src-email"},
      {"id": "ch-2", "text": "Я отправляю договор завтра утром.", "source_id": "src-call"},
      {"id": "ch-3", "quote": "Зал бронируй до десятого.", "source_id": "src-call"}
    ],
    "commitment": [
      {"id": "c-1", "key": "pay", "what": "Оплатить кружок", "owner": "Анна",
       "due": "2026-09-05", "status": "open", "kind": "task", "basket": "work",
       "deadline": {"raw": "до 5 сентября", "precision": "exact", "boundary": "before"}},
      {"id": "c-2", "key": "contract", "what": "Отправить договор", "owner": "Игорь",
       "due": "2026-08-29", "status": "open", "kind": "task", "basket": "work",
       "deadline": {"raw": "завтра утром", "precision": "day", "boundary": "by"}},
      {"id": "c-3", "key": "room", "what": "Забронировать зал", "owner": "Павел",
       "due": "2026-09-10", "status": "open", "kind": "task", "basket": "work",
       "deadline": {"raw": "до десятого", "precision": "day", "boundary": "before"}}
    ]
  },
  "edges": [
    {"src": "c-1", "type": "EVIDENCED_BY", "dst": "ch-1"},
    {"src": "c-2", "type": "EVIDENCED_BY", "dst": "ch-2"},
    {"src": "c-3", "type": "EVIDENCED_BY", "dst": "ch-3"}
  ]
}
"""


class ServeTests(unittest.TestCase):
    def _write_fixture(self, directory: str) -> Path:
        path = Path(directory) / "registry.json"
        path.write_text(REGISTRY_FIXTURE, encoding="utf-8")
        return path

    def test_flatten_returns_one_complete_row_per_commitment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cards = serve._flatten(self._write_fixture(directory))

        self.assertEqual(3, len(cards))
        self.assertEqual(3, len({card["id"] for card in cards}))
        for card in cards:
            self.assertTrue(card["what"])
            self.assertIn("owner", card)
            self.assertIn("due", card)
            self.assertTrue(card["status"])
            self.assertTrue(card["evidence"])
            self.assertTrue(card["evidence"][0]["quote"])
            self.assertNotEqual("—", card["evidence"][0]["source"])

    def test_diff_marks_updated_same_and_new_without_duplicate_ids(self) -> None:
        cards = [
            {"id": "changed", "what": "A", "due": "2026-09-06", "status": "open"},
            {"id": "same", "what": "B", "due": "2026-09-07", "status": "open"},
            {"id": "new", "what": "C", "due": None, "status": "open"},
        ]
        before = {
            "changed": {"what": "A", "due": "2026-09-05", "status": "open"},
            "same": {"what": "B", "due": "2026-09-07", "status": "open"},
        }

        serve._diff(before, cards)

        by_id = {card["id"]: card for card in cards}
        self.assertEqual(len(cards), len(by_id))
        self.assertEqual("updated", by_id["changed"]["change"])
        self.assertEqual(["due"], by_id["changed"]["changed_fields"])
        self.assertEqual("same", by_id["same"]["change"])
        self.assertEqual("new", by_id["new"]["change"])

    def test_run_summary_count_matches_returned_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "registry.json"

            def fake_run(command, **_kwargs):
                target = Path(command[command.index("--registry") + 1])
                target.write_text(REGISTRY_FIXTURE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, b"fixture written", b"")

            state = {"registry": registry, "before": {}, "log": []}
            with patch.dict(serve.STATE, state, clear=True), patch(
                "demo.serve.subprocess.run", side_effect=fake_run
            ) as mocked_run:
                result = serve.do_run("01")

        self.assertTrue(result["ok"])
        self.assertEqual(len(result["cards"]), result["count"])
        self.assertEqual(result["count"], result["log"][-1]["count"])
        self.assertEqual(len(result["cards"]), len({c["id"] for c in result["cards"]}))
        mocked_run.assert_called_once()

    @unittest.expectedFailure
    def test_unknown_example_returns_readable_error_without_traceback(self) -> None:
        """MEDIUM defect: an unknown example leaks a traceback in the API response."""
        captured = {}
        handler = object.__new__(serve.Handler)
        handler._json = lambda code, payload: captured.update(code=code, payload=payload)

        with tempfile.TemporaryDirectory() as directory, patch.object(
            serve, "EXAMPLES", Path(directory)
        ):
            handler._api("/api/run", {"example": ["99"]})

        self.assertEqual(500, captured["code"])
        self.assertIn("Нет примера", captured["payload"]["error"])
        self.assertIn("99", captured["payload"]["error"])
        self.assertNotIn("Traceback", captured["payload"]["error"])
        self.assertNotIn("trace", captured["payload"])


if __name__ == "__main__":
    unittest.main()
