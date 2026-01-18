from __future__ import annotations

import json
from dataclasses import asdict

from .scoring import ScoredKPI


def to_json(
    *,
    selected: dict[str, list[ScoredKPI]],
    source_path: str,
    scope_sections: list[str],
    key_terms: list[str],
) -> str:
    payload = {
        "source_path": source_path,
        "scope_sections_used": scope_sections,
        "key_terms": key_terms,
        "kpis": [
            {
                "bucket": bucket,
                "items": [
                    {
                        "id": s.kpi.id,
                        "name": s.kpi.name,
                        "definition": s.kpi.definition,
                        "formula": s.kpi.formula,
                        "unit": s.kpi.unit,
                        "data_sources": s.kpi.data_sources,
                        "relevance_score": round(s.score, 4),
                        "matched_terms": s.matched_terms,
                    }
                    for s in items
                ],
            }
            for bucket, items in selected.items()
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def to_markdown(
    *,
    selected: dict[str, list[ScoredKPI]],
    source_path: str,
    scope_sections: list[str],
) -> str:
    def bucket_title(b: str) -> str:
        return {
            "cost_savings": "Cost savings",
            "cost_avoidance": "Cost avoidance",
            "efficiency_gains": "Efficiency gains",
            "quality_improvements": "Quality improvements",
            "regulatory_compliance": "Regulatory compliance",
            "intangible_benefits": "Intangible benefits",
        }.get(b, b)

    lines: list[str] = []
    lines.append(f"## Project Value Realisation KPIs\n")
    lines.append(f"- **Source**: `{source_path}`")
    if scope_sections and scope_sections != ["DOCUMENT"]:
        lines.append(f"- **Scope evidence sections used**: {', '.join([f'`{s}`' for s in scope_sections])}")
    lines.append("")

    if not selected:
        lines.append(
            "No KPIs met the relevance threshold for this document. "
            "This typically happens when the document has limited scope/objective details or is mostly boilerplate."
        )
        return "\n".join(lines).strip() + "\n"

    # Stable ordering by expected business narrative
    order = [
        "cost_savings",
        "cost_avoidance",
        "efficiency_gains",
        "quality_improvements",
        "regulatory_compliance",
        "intangible_benefits",
    ]
    for bucket in order:
        items = selected.get(bucket) or []
        if not items:
            continue
        lines.append(f"### {bucket_title(bucket)}")
        for s in items:
            lines.append(f"- **{s.kpi.name}**")
            lines.append(f"  - Definition: {s.kpi.definition}")
            lines.append(f"  - Formula: `{s.kpi.formula}`")
            lines.append(f"  - Unit: {s.kpi.unit}")
            if s.kpi.data_sources:
                lines.append(f"  - Data sources: {', '.join(s.kpi.data_sources)}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"

