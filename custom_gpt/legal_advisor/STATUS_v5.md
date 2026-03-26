LEGAL ADVISOR STATUS V5

SYSTEM: Legal OS (Family Court Advisor)
MODE: Event-driven + Stateful
STATE: STABLE CORE

ARCHITECTURE:
Custom GPT -> GitHub API -> Actions -> Repo (acta) -> Pipeline -> System Context

FLOW:
START GPT -> LOAD context -> LOAD case -> ANALYSIS -> MOTION -> APPROVAL -> SAVE

FUNCTIONS:
- Add document
- Add note
- Analysis
- Generate motion
- Approval flow

NOTES:
- Repo = acta sprawy
- No auto save
- Human in the loop

STATUS: MVP+ ready