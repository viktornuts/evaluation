# Glossary

## Dataset

A dataset is a set of examples used to measure product quality.

In this project, one dataset example contains a user scenario and expected properties of a good generated agent.

## Expected Properties

Expected properties describe what a good answer should contain or avoid. They are not always exact text.

Examples:

- required sections;
- required tools;
- forbidden actions;
- safety rules;
- expected behavior;
- minimum level of detail.

## Grader

A grader is a checker that evaluates one product output.

Examples:

- parse the output as JSON;
- check required fields;
- check that forbidden tools are not used;
- ask an LLM judge to rate completeness.

## Parser

A parser reads structured output and turns it into data the graders can inspect.

For example, if the product returns JSON, the parser loads it and validates it.

## LLM-as-Judge

LLM-as-judge means using another language model to evaluate the output according to a rubric.

It is useful for subjective criteria, but it should not be the only evaluator.

## Insufficient Detail

Insufficient detail means the answer is too shallow or generic to be useful.

Example:

```text
The agent should answer tickets and help users.
```

This is insufficient because it does not describe ticket types, tools, escalation, safety rules, or fallback behavior.

## Eval Run

An eval run is one full execution of the dataset through the product and graders.

It produces metrics such as pass rate, safety violations, missing required fields, cost, and latency.

