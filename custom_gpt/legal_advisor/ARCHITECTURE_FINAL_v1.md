# LEGAL OS - FINAL ARCHITECTURE v1

## OVERVIEW

System: Legal Advisor (Family Court)
Model: Custom GPT
Mode: Knowledge-driven + Repo-driven

Architecture:
- Advisor (Legal)
- Execution (GitHub API)
- Dashboard (Python Interpreter)
- Reasoning Engine (JSON)
- LLM Reasoning (optional)

## LAYERS

1. ADVISOR LAYER

Role:
- analiza sprawy
- buduje strategie
- generuje pisma

2. EXECUTION LAYER

Role:
 - GitHub REST API
 - repository_dispatch
 - zapis act

#3. DASHOARD LAYER

Role:
- build dashboard (python)
- visualizacja danych
- input do reasoning

4. REACONING ENGINE

Role:
 - execute reasoning_engine.json
- deterministyczna logika

5. LLM REASONING
ole:
- gleboka analiza
- real argumentacja
- optional trygger

## FLOW

START GPP
- load system_context
- load active_case
- fetch data from repo
- build dashboard (python)
- display dashboard
- execute reasoning_engine.json
- optional llm reasoning
- generate motion
- wait approval
- dispatch to repo

## RESPONSE FORMAT

Dashboard
Reasoning (JSON)
Advisor
Motion
Status

## KNOWLEDGE_DRIVEN LAYER

folder: custom_gpt/legal_advisor/knowledge_driven/

content:
- DASHBOARD_SPEC.md
- reasoning_rules.json
- dashboard_builder.py
- templates/

## RULES

- GPT must use engine
- No free analysis
- Dashboard first
- Structured output
