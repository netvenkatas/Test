from __future__ import annotations

from dataclasses import dataclass

from .kpi_library import get_kpi_library
from .parsers import parse_document
from .scope import extract_scope_text
from .scoring import ScoredKPI, score_kpis, select_relevant_kpis
from .textutils import extract_key_terms, normalize_text


@dataclass(frozen=True)
class AgentConfig:
    min_score: float = 0.18
    max_per_bucket: int = 5
    top_k_terms: int = 60


@dataclass(frozen=True)
class AgentResult:
    source_path: str
    scope_sections_used: list[str]
    key_terms: list[str]
    selected: dict[str, list[ScoredKPI]]


def analyze_document(path: str, *, config: AgentConfig | None = None) -> AgentResult:
    cfg = config or AgentConfig()
    parsed = parse_document(path)
    text = normalize_text(parsed.text)

    scope = extract_scope_text(text)
    scope_text = scope.scope_text or text

    key_terms = extract_key_terms(scope_text, top_k=cfg.top_k_terms)

    kpis = get_kpi_library()
    scored = score_kpis(key_terms=key_terms, kpis=kpis)
    selected = select_relevant_kpis(
        scored=scored,
        min_score=cfg.min_score,
        max_per_bucket=cfg.max_per_bucket,
    )

    return AgentResult(
        source_path=parsed.source_path,
        scope_sections_used=scope.evidence_sections,
        key_terms=key_terms,
        selected=selected,
    )

