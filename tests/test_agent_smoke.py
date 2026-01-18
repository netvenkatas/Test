from kpi_agent.agent import AgentConfig, analyze_document


def test_smoke_example_charter_selects_relevant_buckets(tmp_path):
    # Copy example into temp path to avoid relying on repo-relative paths in some runners
    content = (
        "PROJECT CHARTER\n\n"
        "OBJECTIVES\n"
        "- Automate invoice processing for AP team.\n"
        "- Reduce manual data entry errors and rework.\n"
        "- Improve turnaround time.\n"
        "- Provide audit trail.\n"
    )
    p = tmp_path / "charter.txt"
    p.write_text(content, encoding="utf-8")

    res = analyze_document(
        str(p),
        config=AgentConfig(min_score=0.12, max_per_bucket=5, top_k_terms=60),
    )

    # Expect efficiency + quality; may also pull compliance depending on term overlap.
    assert "efficiency_gains" in res.selected
    assert "quality_improvements" in res.selected

