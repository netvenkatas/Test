# Value Realisation KPI Agent

An offline-friendly agent that analyzes an uploaded **requirements document / HLDD / project charter**
and generates **project value realisation KPIs** that are **relevant to the project scope**.

It produces KPIs across:
- Cost savings
- Cost avoidance
- Efficiency gains
- Quality improvements
- Regulatory compliance
- Intangible benefits

## Quickstart

### 1) Setup

```bash
cd /workspace
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run

```bash
python3 -m kpi_agent --input /path/to/your/document.pdf --format markdown
```

Other formats:

```bash
python3 -m kpi_agent --input /path/to/your/document.docx --format json
```

## What it does

1. Extracts text from PDF/DOCX/TXT/MD.
2. Tries to isolate *scope/objectives/deliverables* sections when present.
3. Extracts salient keywords and phrases.
4. Scores a curated KPI library and returns only KPIs whose applicability matches the project scope.

## Notes / Assumptions

- The default mode is **no external LLM dependency** (works offline).
- If the document text is too sparse or has no scope signals, the agent will return **fewer or no KPIs**
  (to avoid generating irrelevant KPIs).

