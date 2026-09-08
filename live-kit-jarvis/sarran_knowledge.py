"""Small vectorless retriever for the Sarran AI website knowledge base."""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


def _read_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".html":
        parser = _TextExtractor()
        parser.feed(content)
        return parser.text()
    return " ".join(content.split())


def _knowledge_documents() -> list[tuple[str, str]]:
    root = Path(os.getenv("SARRAN_KNOWLEDGE_DIR", "../sarran-ai")).resolve()
    allowed = {".html", ".md", ".txt"}
    documents = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in allowed:
            text = _read_file(path)
            if text:
                documents.append((str(path.relative_to(root)), text))
    return documents


def search_knowledge(query: str, limit: int = 4) -> str:
    """Return the most keyword-relevant approved source passages."""
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    if not terms:
        return "No approved source matched that question."

    ranked = []
    for name, text in _knowledge_documents():
        words = set(re.findall(r"[a-z0-9]+", text.lower()))
        score = len(terms & words)
        if score:
            ranked.append((score, name, text[:3500]))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    if not ranked:
        return "No approved source matched that question. Do not guess; offer a human handoff."

    return "\n\n".join(
        f"Source: {name}\n{passage}" for _, name, passage in ranked[:limit]
    )
