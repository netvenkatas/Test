from __future__ import annotations

import re
from dataclasses import dataclass

from .textutils import normalize_text


@dataclass(frozen=True)
class ScopeExtraction:
    scope_text: str
    evidence_sections: list[str]


_HEADING_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*(?:\d+\.)*\s*(scope|in scope|out of scope)\s*$", re.I),
    re.compile(r"^\s*(?:\d+\.)*\s*(objectives|goal|goals)\s*$", re.I),
    re.compile(r"^\s*(?:\d+\.)*\s*(business case|value|benefits)\s*$", re.I),
    re.compile(r"^\s*(?:\d+\.)*\s*(deliverables|requirements)\s*$", re.I),
    re.compile(r"^\s*(?:\d+\.)*\s*(assumptions|constraints)\s*$", re.I),
]


def _split_into_sections(text: str) -> list[tuple[str, str]]:
    """
    Very small "sectionizer":
    - Detects headings as standalone short lines.
    - Returns list of (heading, body) pairs.
    """
    lines = text.split("\n")
    sections: list[tuple[str, list[str]]] = []
    current_heading = "DOCUMENT"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_heading, current_body
        body = "\n".join(current_body).strip()
        if body:
            sections.append((current_heading, current_body.copy()))
        current_body = []

    for line in lines:
        stripped = line.strip()
        is_heading = (
            0 < len(stripped) <= 80
            and stripped == stripped.upper()
            and len(stripped.split()) <= 8
        )
        if not is_heading:
            # Also treat common headings that aren't all caps.
            for pat in _HEADING_PATTERNS:
                if pat.match(stripped):
                    is_heading = True
                    break

        if is_heading:
            flush()
            current_heading = stripped or "SECTION"
        else:
            current_body.append(line)

    flush()
    return [(h, "\n".join(b).strip()) for h, b in sections]


def extract_scope_text(text: str) -> ScopeExtraction:
    text = normalize_text(text)
    if not text:
        return ScopeExtraction(scope_text="", evidence_sections=[])

    sections = _split_into_sections(text)
    if not sections:
        return ScopeExtraction(scope_text=text, evidence_sections=["DOCUMENT"])

    selected: list[tuple[str, str]] = []
    for heading, body in sections:
        h = heading.lower()
        if any(
            k in h
            for k in (
                "scope",
                "objective",
                "goal",
                "business case",
                "benefit",
                "deliverable",
                "requirement",
            )
        ):
            if body:
                selected.append((heading, body))

    if not selected:
        # Fall back to entire doc to avoid missing content when headings aren't recognized.
        return ScopeExtraction(scope_text=text, evidence_sections=["DOCUMENT"])

    scope_text = "\n\n".join([f"{h}\n{b}" for h, b in selected]).strip()
    return ScopeExtraction(scope_text=scope_text, evidence_sections=[h for h, _ in selected])

