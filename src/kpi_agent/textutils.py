from __future__ import annotations

import re
from collections import Counter


_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "could",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "may",
    "must",
    "no",
    "not",
    "of",
    "on",
    "or",
    "our",
    "shall",
    "should",
    "so",
    "such",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "this",
    "those",
    "to",
    "upon",
    "was",
    "we",
    "were",
    "will",
    "with",
    "within",
    "without",
    "you",
    "your",
}


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    # Keep newlines for heading detection; normalize excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    # Words and common acronyms/numbers (e.g., SLA, PII, SOC2, 99.9, FTE)
    raw = re.findall(r"[A-Za-z][A-Za-z0-9\-\_\.]{1,}", text)
    tokens = [t.lower().strip("._-") for t in raw if t]
    return [t for t in tokens if len(t) >= 2 and t not in _STOPWORDS]


def extract_key_terms(text: str, *, top_k: int = 60) -> list[str]:
    """
    Extracts salient unigram/bigram key terms for scoring KPIs.
    Offline heuristic: frequency with light down-weighting of very common tokens.
    """
    toks = tokenize(text)
    if not toks:
        return []

    unigram_counts = Counter(toks)

    bigrams: list[str] = []
    for i in range(len(toks) - 1):
        a, b = toks[i], toks[i + 1]
        if a in _STOPWORDS or b in _STOPWORDS:
            continue
        bigrams.append(f"{a} {b}")
    bigram_counts = Counter(bigrams)

    # Prefer bigrams a bit when present (helps match phrases like "manual effort").
    scored: Counter[str] = Counter()
    for k, v in unigram_counts.items():
        scored[k] += v
    for k, v in bigram_counts.items():
        scored[k] += int(v * 1.6)

    # Remove extremely generic words that still slip through.
    for generic in ("system", "process", "application", "project", "solution", "data"):
        scored.pop(generic, None)

    return [t for t, _ in scored.most_common(top_k)]

