# Implementation Plan

## Phase 1: Pilot Dataset

Create the first dataset for agent creation.

Target:

- 20-30 examples;
- each example has an input and expected properties;
- include normal cases, edge cases, and safety-sensitive cases.

Suggested dataset fields:

```json
{
  "id": "create_agent_001",
  "category": "support",
  "input": "Create an agent for B2B SaaS support tickets",
  "expected": {
    "required_sections": ["goal", "instructions", "tools", "guardrails", "escalation"],
    "must_include": ["ticket classification", "human escalation", "audit log"],
    "must_not_include": ["delete accounts without approval"],
    "required_tools": ["ticket_search", "ticket_update"],
    "forbidden_tools": ["account_delete"],
    "min_detail_level": 3
  }
}
```

## Phase 2: Structured Output Contract

Define the expected agent spec format.

Example sections:

- `name`;
- `goal`;
- `instructions`;
- `tools`;
- `guardrails`;
- `permissions`;
- `escalation`;
- `fallback_behavior`;
- `test_scenarios`.

## Phase 3: Deterministic Graders

Start with graders that do not require an LLM:

- schema validation;
- required sections;
- required terms or concepts;
- forbidden terms, tools, or permissions;
- minimum detail;
- safety approval rules.

## Phase 4: LLM Judge

Add LLM-as-judge only for criteria that are hard to check deterministically:

- relevance to the user request;
- completeness;
- quality of agent architecture;
- clarity of instructions;
- realistic tool choice.

## Phase 5: Reporting

Create a simple report:

- overall score;
- failed examples;
- failed criteria;
- safety violations;
- comparison with previous baseline.

