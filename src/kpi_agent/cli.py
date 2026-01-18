from __future__ import annotations

import argparse
import sys

from rich.console import Console

from .agent import AgentConfig, analyze_document
from .output import to_json, to_markdown


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="kpi-agent",
        description=(
            "Analyze a requirements/HLDD/project charter document and output "
            "project-scope-relevant value realisation KPIs."
        ),
    )
    p.add_argument("--input", required=True, help="Path to .pdf/.docx/.txt/.md document")
    p.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    p.add_argument(
        "--min-score",
        type=float,
        default=0.18,
        help="Relevance threshold (higher = fewer/stricter KPIs)",
    )
    p.add_argument(
        "--max-per-bucket",
        type=int,
        default=5,
        help="Max KPIs per benefit bucket",
    )
    p.add_argument(
        "--top-k-terms",
        type=int,
        default=60,
        help="How many key terms to extract from scope text",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    console = Console()

    cfg = AgentConfig(
        min_score=float(args.min_score),
        max_per_bucket=int(args.max_per_bucket),
        top_k_terms=int(args.top_k_terms),
    )
    result = analyze_document(args.input, config=cfg)

    if args.format == "json":
        out = to_json(
            selected=result.selected,
            source_path=result.source_path,
            scope_sections=result.scope_sections_used,
            key_terms=result.key_terms,
        )
    else:
        out = to_markdown(
            selected=result.selected,
            source_path=result.source_path,
            scope_sections=result.scope_sections_used,
        )

    console.print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

