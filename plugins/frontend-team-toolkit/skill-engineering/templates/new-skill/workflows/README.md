# Workflows Directory

Dynamic orchestration scripts for this Skill.

## Purpose

Workflows provide **deterministic execution** of Skill orchestration patterns, complementing the static knowledge in `SKILL.md`.

## Workflow Types

| File | Pattern | When to Use |
|------|---------|-------------|
| `serial-workflow.js` | Serial | Sub-skills have sequential dependencies |
| `parallel-workflow.js` | Parallel | Sub-skills can run independently |
| `conditional-workflow.js` | Classify-and-Act | Route to different sub-skills based on input |
| `loop-workflow.js` | Loop until Done | Unknown amount of work, repeat until condition |
| `adversarial-workflow.js` | Adversarial Verification | Verify output quality with independent agent |

## Workflow vs SKILL.md

| Component | SKILL.md | Workflows |
|-----------|----------|-----------|
| **Purpose** | Static knowledge (when, what, rules) | Dynamic execution (how to run) |
| **Format** | Markdown | JavaScript |
| **Execution** | Claude interprets | Script executes deterministically |
| **Validation** | output Eval | trajectory Eval |

## How to Use

1. **Claude auto-selects**: Based on trigger keywords in SKILL.md
2. **User specifies**: "Use parallel workflow to..."
3. **Eval validates**: trajectory Eval checks execution process

## Validation

Each workflow should have corresponding `trajectory-evals.json` to validate:
- Agent spawn order (serial/parallel)
- Routing correctness (conditional)
- Iteration limits (loop)

## Template Files

Copy from `skill-engineering/templates/new-skill/workflows/` and replace placeholders:
- `{{SKILL_NAME}}` → Your skill name
- `{{AGENT_X_NAME}}` → Agent names
- `{{INPUT_VAR}}` → Input variable names
- `{{ROUTE_CONDITION_X}}` → Routing conditions

---

*See `skill-engineering/docs/lifecycle-quickref.md` for workflow creation workflow.*