from __future__ import annotations

from dataclasses import dataclass

from .kpi_library import KPI


@dataclass(frozen=True)
class ScoredKPI:
    kpi: KPI
    score: float
    matched_terms: list[str]


def _term_set(key_terms: list[str]) -> set[str]:
    return {t.lower().strip() for t in key_terms if t and t.strip()}


def score_kpis(
    *,
    key_terms: list[str],
    kpis: list[KPI],
) -> list[ScoredKPI]:
    """
    Very small, interpretable scoring:
    - KPI score = weighted overlap between extracted terms and KPI applicability keywords
    - penalize anti-keywords
    """
    terms = _term_set(key_terms)
    if not terms:
        return [ScoredKPI(kpi=k, score=0.0, matched_terms=[]) for k in kpis]

    scored: list[ScoredKPI] = []
    for k in kpis:
        kw = [w.lower() for w in k.applicability_keywords]
        anti = [w.lower() for w in k.anti_keywords]

        matched = []
        for w in kw:
            if w in terms:
                matched.append(w)
            else:
                # crude containment to allow matches like "service level" vs "sla"
                if any((w in t) or (t in w) for t in terms if len(t) >= 4):
                    matched.append(w)

        anti_hits = [w for w in anti if w in terms]

        if kw:
            base = len(set(matched)) / len(set(kw))
        else:
            base = 0.0

        # Reward multiple matches slightly, but keep in [0,1] range.
        boost = min(0.25, 0.05 * max(0, len(set(matched)) - 1))
        penalty = min(0.35, 0.12 * len(set(anti_hits)))
        score = max(0.0, min(1.0, base + boost - penalty))

        scored.append(
            ScoredKPI(
                kpi=k,
                score=score,
                matched_terms=sorted(set(matched)),
            )
        )

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored


def select_relevant_kpis(
    *,
    scored: list[ScoredKPI],
    min_score: float,
    max_per_bucket: int,
) -> dict[str, list[ScoredKPI]]:
    out: dict[str, list[ScoredKPI]] = {}
    for s in scored:
        if s.score < min_score:
            continue
        out.setdefault(s.kpi.bucket, [])
        if len(out[s.kpi.bucket]) < max_per_bucket:
            out[s.kpi.bucket].append(s)
    return out

