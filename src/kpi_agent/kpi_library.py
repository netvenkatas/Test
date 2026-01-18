from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KPI:
    id: str
    bucket: str  # cost_savings, cost_avoidance, efficiency_gains, quality_improvements, regulatory_compliance, intangible_benefits
    name: str
    definition: str
    formula: str
    unit: str
    data_sources: list[str]
    applicability_keywords: list[str]
    anti_keywords: list[str]


BUCKETS = [
    "cost_savings",
    "cost_avoidance",
    "efficiency_gains",
    "quality_improvements",
    "regulatory_compliance",
    "intangible_benefits",
]


def _k(
    *,
    id: str,
    bucket: str,
    name: str,
    definition: str,
    formula: str,
    unit: str,
    data_sources: list[str],
    applicability_keywords: list[str],
    anti_keywords: list[str] | None = None,
) -> KPI:
    return KPI(
        id=id,
        bucket=bucket,
        name=name,
        definition=definition,
        formula=formula,
        unit=unit,
        data_sources=data_sources,
        applicability_keywords=[k.lower() for k in applicability_keywords],
        anti_keywords=[k.lower() for k in (anti_keywords or [])],
    )


def get_kpi_library() -> list[KPI]:
    """
    Curated, cross-industry KPI library with applicability keywords.
    The agent selects only KPIs that score high against the document scope.
    """
    return [
        # ----------------------- COST SAVINGS -----------------------
        _k(
            id="cs_opex_reduction",
            bucket="cost_savings",
            name="Operational cost reduction (OPEX)",
            definition="Reduction in run/operate costs attributable to the project (labor + vendor + infra).",
            formula="(Baseline monthly run cost) - (Post-go-live monthly run cost)",
            unit="currency/month",
            data_sources=["Finance/GL", "Vendor invoices", "Cloud billing"],
            applicability_keywords=[
                "cost reduction",
                "opex",
                "run cost",
                "cloud cost",
                "infrastructure",
                "vendor",
                "license",
                "decommission",
            ],
        ),
        _k(
            id="cs_fte_savings",
            bucket="cost_savings",
            name="FTE hours saved (convertible to cost savings)",
            definition="Reduction in human effort due to automation/streamlining (can be monetized if capacity is removed or repurposed).",
            formula="(Baseline effort hours) - (Post-go-live effort hours)",
            unit="hours/month",
            data_sources=["Time tracking", "Process logs", "Work management tools"],
            applicability_keywords=[
                "automation",
                "manual",
                "manual effort",
                "fte",
                "headcount",
                "hours saved",
                "workflow",
                "ops",
            ],
        ),
        _k(
            id="cs_tool_consolidation",
            bucket="cost_savings",
            name="Tool / license consolidation savings",
            definition="Savings from reducing duplicate tools/licenses due to the project.",
            formula="(Baseline license spend) - (Post-go-live license spend)",
            unit="currency/month",
            data_sources=["Software asset management", "Vendor invoices"],
            applicability_keywords=[
                "license",
                "tool",
                "consolidation",
                "legacy",
                "platform",
                "vendor",
            ],
        ),
        # ----------------------- COST AVOIDANCE -----------------------
        _k(
            id="ca_penalty_avoidance",
            bucket="cost_avoidance",
            name="Penalty / fine avoidance",
            definition="Avoided penalties due to improved compliance, audit readiness, or SLA adherence.",
            formula="Expected penalties (baseline risk) - Expected penalties (post-go-live risk)",
            unit="currency/year",
            data_sources=["Risk register", "Audit findings", "Compliance reports"],
            applicability_keywords=[
                "penalty",
                "fine",
                "audit finding",
                "non-compliance",
                "sla breach",
                "regulatory",
                "compliance",
            ],
        ),
        _k(
            id="ca_outage_avoidance",
            bucket="cost_avoidance",
            name="Avoided downtime cost",
            definition="Avoided cost of outages or service disruption due to reliability/observability improvements.",
            formula="(Baseline downtime hours * cost per downtime hour) - (Post-go-live downtime hours * cost per downtime hour)",
            unit="currency/year",
            data_sources=["Incident management", "Monitoring/uptime", "Finance estimates"],
            applicability_keywords=[
                "availability",
                "uptime",
                "incident",
                "outage",
                "resilience",
                "sla",
                "reliability",
                "dr",
                "bcp",
            ],
        ),
        _k(
            id="ca_legacy_risk_retirement",
            bucket="cost_avoidance",
            name="Legacy risk retirement (security/maintenance)",
            definition="Avoided costs due to retiring unsupported systems and reducing security exposure/patch burden.",
            formula="(Baseline legacy maintenance + expected security incident cost) - (Post-go-live equivalents)",
            unit="currency/year",
            data_sources=["App inventory", "Security reports", "Maintenance contracts"],
            applicability_keywords=[
                "legacy",
                "end of life",
                "eol",
                "unsupported",
                "security",
                "patching",
                "vulnerability",
                "retire",
            ],
        ),
        # ----------------------- EFFICIENCY GAINS -----------------------
        _k(
            id="eg_cycle_time",
            bucket="efficiency_gains",
            name="Process cycle time reduction",
            definition="Reduction in end-to-end time to complete a business process in scope.",
            formula="(Baseline median cycle time) - (Post-go-live median cycle time)",
            unit="minutes/hours/days",
            data_sources=["Workflow system logs", "Ticketing/CRM", "Process mining"],
            applicability_keywords=[
                "turnaround time",
                "cycle time",
                "lead time",
                "sla",
                "workflow",
                "approval",
                "processing time",
            ],
        ),
        _k(
            id="eg_throughput",
            bucket="efficiency_gains",
            name="Throughput increase",
            definition="Increase in items processed per period due to automation/optimization.",
            formula="(Post-go-live items processed per period) - (Baseline items processed per period)",
            unit="items/day or items/week",
            data_sources=["Transaction logs", "Workflow system", "CRM/ERP"],
            applicability_keywords=[
                "throughput",
                "volume",
                "transactions",
                "cases",
                "requests",
                "scale",
                "capacity",
            ],
        ),
        _k(
            id="eg_first_time_right",
            bucket="efficiency_gains",
            name="First-time-right rate improvement (less rework)",
            definition="Increase in % of work items completed without rework/returns.",
            formula="(First-time-right items / total items) * 100",
            unit="percent",
            data_sources=["QA results", "Workflow/ticket status", "Returns/rework logs"],
            applicability_keywords=[
                "rework",
                "returns",
                "first time right",
                "quality gate",
                "defect",
            ],
        ),
        # ----------------------- QUALITY IMPROVEMENTS -----------------------
        _k(
            id="qi_error_rate",
            bucket="quality_improvements",
            name="Error/defect rate reduction",
            definition="Reduction in errors/defects in the in-scope process/system (production defects, data errors, failed validations).",
            formula="(Baseline errors per 1,000 transactions) - (Post-go-live errors per 1,000 transactions)",
            unit="errors per 1,000 transactions",
            data_sources=["Application logs", "QA/defect tracker", "Data quality checks"],
            applicability_keywords=[
                "error",
                "defect",
                "bug",
                "data quality",
                "validation",
                "accuracy",
                "exception",
            ],
        ),
        _k(
            id="qi_sla_attainment",
            bucket="quality_improvements",
            name="SLA attainment improvement",
            definition="Increase in % of in-scope requests completed within SLA.",
            formula="(Requests within SLA / total requests) * 100",
            unit="percent",
            data_sources=["Ticketing/ITSM", "Workflow logs", "Reporting dashboards"],
            applicability_keywords=[
                "sla",
                "service level",
                "breach",
                "turnaround",
                "response time",
            ],
        ),
        _k(
            id="qi_customer_issues",
            bucket="quality_improvements",
            name="Reduction in customer-reported issues for in-scope journey",
            definition="Decrease in tickets/complaints attributable to the in-scope system or journey.",
            formula="(Baseline issues per month) - (Post-go-live issues per month)",
            unit="count/month",
            data_sources=["Customer support", "CRM", "Contact center platform"],
            applicability_keywords=[
                "customer",
                "complaint",
                "ticket",
                "support",
                "call center",
                "incident",
            ],
        ),
        # ----------------------- REGULATORY COMPLIANCE -----------------------
        _k(
            id="rc_audit_findings",
            bucket="regulatory_compliance",
            name="Audit findings reduction (in-scope control set)",
            definition="Reduction in audit issues/findings related to the project scope controls.",
            formula="(Baseline # findings) - (Post-go-live # findings)",
            unit="count/audit",
            data_sources=["Audit reports", "GRC tools", "Control evidence repository"],
            applicability_keywords=[
                "audit",
                "sox",
                "soc2",
                "iso",
                "pci",
                "gdpr",
                "hipaa",
                "glba",
                "control",
                "evidence",
                "policy",
            ],
        ),
        _k(
            id="rc_time_to_produce_evidence",
            bucket="regulatory_compliance",
            name="Time to produce compliance evidence",
            definition="Reduction in time to gather/produce required evidence for audits/regulatory reporting.",
            formula="(Baseline median time to produce evidence) - (Post-go-live median time to produce evidence)",
            unit="hours",
            data_sources=["GRC workflows", "Audit request tracker", "Document repository logs"],
            applicability_keywords=[
                "evidence",
                "audit request",
                "compliance reporting",
                "regulatory reporting",
                "attestation",
            ],
        ),
        # ----------------------- INTANGIBLE BENEFITS -----------------------
        _k(
            id="ib_csat",
            bucket="intangible_benefits",
            name="CSAT/NPS uplift for in-scope journey",
            definition="Improvement in customer satisfaction for the in-scope process/journey (measured via CSAT or NPS).",
            formula="(Post-go-live CSAT/NPS) - (Baseline CSAT/NPS)",
            unit="points",
            data_sources=["Survey tool", "CRM", "Voice-of-customer program"],
            applicability_keywords=[
                "csat",
                "nps",
                "customer experience",
                "ux",
                "satisfaction",
            ],
        ),
        _k(
            id="ib_employee_experience",
            bucket="intangible_benefits",
            name="Employee experience improvement (in-scope users)",
            definition="Improvement in internal user satisfaction due to better tooling/usability.",
            formula="(Post-go-live internal satisfaction score) - (Baseline score)",
            unit="points",
            data_sources=["Internal surveys", "Adoption analytics"],
            applicability_keywords=[
                "usability",
                "user experience",
                "agent assist",
                "employee",
                "training",
                "adoption",
            ],
        ),
        _k(
            id="ib_risk_reduction",
            bucket="intangible_benefits",
            name="Operational risk reduction (qualitative-to-quantified)",
            definition="Reduction in operational risk severity/likelihood for in-scope risks (can be mapped to risk score).",
            formula="(Baseline risk score) - (Post-go-live risk score)",
            unit="risk score points",
            data_sources=["Risk register", "Ops reviews", "Security posture reports"],
            applicability_keywords=[
                "risk",
                "control",
                "security",
                "privacy",
                "pii",
                "fraud",
                "governance",
            ],
        ),
    ]

