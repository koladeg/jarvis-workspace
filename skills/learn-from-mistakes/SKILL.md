---
name: learn-from-mistakes
description: "Review, document, and learn from mistakes in your own work. Use when: (1) you notice you made an error and need to capture the lesson, (2) you want to analyze patterns in repeated mistakes, (3) you need to create guardrails or checklists to prevent future errors, (4) you're preparing a session summary and want to log important failures. This skill helps build systematic awareness of errors, root causes, and preventive measures."
---

# Learn From Mistakes

## Overview

This skill enables systematic review of mistakes and errors, transforming them into documented lessons and preventive guardrails. Rather than repeating the same errors, you can analyze what went wrong, understand why, identify patterns, and build checks to prevent recurrence.

## When to Use This Skill

Use this skill when:

- You notice you made an error (forgot a detail, logic was flawed, process failed)
- You want to prevent the same mistake from happening again
- You need to identify patterns across multiple similar errors
- You're analyzing a session and want to log lessons learned
- You want to create a quick checklist for high-risk task types

## Workflow: From Mistake to Lesson

### 1. Capture the Mistake

Describe what went wrong clearly:

- **What happened**: The specific error or failure
- **When**: In which task or interaction did it occur?
- **Evidence**: What shows it was a mistake? (e.g., user asked for missing information)

Example:
```
Mistake: Forgot to include the URL/link in truck search results response
When: Search results generation task for Kolade
Evidence: Kolade asked "What's the link?" and I couldn't provide it
```

### 2. Analyze Root Cause

Understand why the mistake happened. Common root causes:

- **Forgetfulness**: Forgot a step or detail
- **Process gap**: No systematic check existed
- **Unclear logic**: Misunderstood the requirement
- **Attention slip**: Context loss or distraction
- **Incomplete output**: Truncation or missing processing step
- **Assumption error**: Assumed something was done when it wasn't

Example:
```
Root cause: Process gap + Attention slip
- I generated search results without a systematic check for "must include URL"
- The results were long and I focused on the text content, not the full output requirement
```

### 3. Identify Patterns

Look across mistakes to spot patterns:

- Is this the 3rd time you forgot links in responses?
- Do you consistently miss details in certain task types?
- Are certain conditions (late session, complex task, long context) correlated with errors?

Example:
```
Pattern: Missing output details in information-heavy tasks
- Search results → forgot URL
- Product listings → might forget prices
- Code samples → might forget imports or setup instructions
Related condition: Happens when output is text-heavy and manual (not automated)
```

### 4. Create a Guardrail

Design a simple, mechanical check to prevent repetition:

- A checklist before sending responses
- A verification script to validate output
- A rule about mandatory inclusion (e.g., "Always include source URL in search results")
- A prompt reminder in high-risk workflows

Example:
```
Guardrail: Pre-response checklist for search/lookup tasks

Before sending search results:
☐ Did I include the source URL for each result?
☐ Is the URL format correct (not truncated)?
☐ Could the user access this URL without additional context?
```

### 5. Store the Lesson

Use the mistakes log and guardrails file to persist learnings for future reference.

## Quick Start: Logging a Mistake

Use the `analyze-mistake.py` script to log a mistake systematically:

```bash
python scripts/analyze-mistake.py \
  --mistake "Forgot to include URL in search results" \
  --context "Truck search results for Kolade" \
  --root-cause "Process gap: no pre-send validation check" \
  --guardrail "Add URL-inclusion check before sending search results"
```

This creates an entry in your mistakes log with timestamp, category, and linked guardrail.

## Building Your Mistakes Log

Your mistakes log (`memory/mistakes-log.md`) is the persistent record:

```markdown
# Mistakes Log

## 2026-03-25: Search Results Missing URL
- **What**: Forgot to include URL in truck search results response
- **Context**: Web search task
- **Root cause**: Process gap - no validation check before sending
- **Pattern**: Missing output details in information-heavy tasks
- **Guardrail**: URL-inclusion checklist for search tasks
- **Status**: Logged, awaiting prevention implementation
```

The log captures the lesson so you can:
- Review patterns over time
- Identify which guardrails are most needed
- Know when a mistake is a one-off vs. systemic

## Creating Guardrails: Checklists for High-Risk Tasks

Some tasks are high-risk for specific mistakes. Create guardrails for them:

### Common High-Risk Task Types

1. **Search/lookup tasks** - Risk: Missing source URLs, incomplete results
2. **Code generation** - Risk: Missing imports, incomplete functions, no error handling
3. **List/table creation** - Risk: Missing columns, inconsistent formatting, wrong data types
4. **Aggregation tasks** - Risk: Missed items, duplicates, incorrect summaries
5. **Response composition** - Risk: Forgotten requirements, truncated output, missing sections

### Checklist Pattern

Each guardrail is a simple pre-send or pre-output checklist:

```markdown
## Task: Web Search Results

**Before sending response:**
- [ ] Each result includes: title, URL, snippet, source name
- [ ] URLs are complete and functional (not truncated)
- [ ] Total result count matches what was requested
- [ ] No placeholder or partial results included
- [ ] Snippets are meaningful (>20 characters, not just "...")
```

See `references/guardrails.md` for the complete guardrails library and patterns for your most common mistakes.

## Reference Materials

- **Common Mistakes & Root Causes** (`references/mistake-patterns.md`) - Detailed patterns and why they happen
- **Guardrails Library** (`references/guardrails.md`) - Pre-built checklists for high-risk tasks
- **Mistakes Log** (`memory/mistakes-log.md`) - Your persistent record of lessons learned

## Example: Putting It All Together

**Mistake**: "I generated truck search results but forgot the URL."

**Analysis**:
1. Capture: What happened? Why did the user ask for the link? → I didn't include it in the response
2. Root cause: Process gap - no validation check existed for "must include URL"
3. Pattern: This is the first time, but it's part of a larger pattern of missing output details
4. Guardrail: Create a checklist for search result tasks
5. Store: Log the lesson and link it to the guardrail

**Going forward**:
- Before sending search results, check the guardrail checklist
- If you create more search result tasks, the guardrail prevents repetition
- If you notice the same gap in other task types, update the pattern analysis

---

**Key Insight**: Mistakes are data. Each one tells you something about your process. The goal is not to be perfect, but to systematically turn errors into improvements.
