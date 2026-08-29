from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .engine import SourceFile, _chunks, _document_now, _normalize_items


class EngineBoundaryTests(unittest.TestCase):
    def test_chat_timestamp_controls_reference_date_not_future_deadline(self) -> None:
        source = SourceFile("chat.txt", Path("chat.txt"), "[27.08 14:02] deadline 25.09\n", "abc", 35, "chat")
        self.assertEqual(_document_now([source], None)[5:], "08-27")

    def test_small_file_prefilter_still_sends_all_chunks(self) -> None:
        source = SourceFile("quiet.txt", Path("quiet.txt"), "ordinary context\n" * 70, "abc", 100, "other")
        all_chunks, sent = _chunks(source, True)
        self.assertEqual(len(all_chunks), len(sent))

    def test_invalid_quote_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "source.txt"
            path.write_text("exact source sentence\n", encoding="utf-8")
            source = SourceFile("source.txt", path, path.read_text(encoding="utf-8"), "abc", path.stat().st_size, "other")
            raw = [{
                "what": "invented", "owner": None, "due": None, "due_text": "",
                "kind": "task", "recurrence": None, "status": "open",
                "derived_from_what": None,
                "sources": [{"path": "source.txt", "quote": "not present", "line_start": 1, "line_end": 1}],
            }]
            self.assertEqual(_normalize_items(raw, {"source.txt": source}), [])


if __name__ == "__main__":
    unittest.main()
