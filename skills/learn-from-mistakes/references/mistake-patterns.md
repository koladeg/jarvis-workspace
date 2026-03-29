# Common Mistake Patterns and Root Causes

This reference documents frequently occurring mistake patterns, their underlying causes, and how to recognize them.

## Table of Contents

1. [Output Detail Omission](#output-detail-omission)
2. [Process Gaps](#process-gaps)
3. [Context Loss](#context-loss)
4. [Logic Errors](#logic-errors)
5. [Truncation and Incompleteness](#truncation-and-incompleteness)
6. [Assumption Errors](#assumption-errors)
7. [Task Type Summary](#task-type-summary)

---

## Output Detail Omission

**Description**: Forgetting to include required information in the final output.

**Symptoms**:
- User asks "Where's the link?" or "Where's the code?"
- Output is incomplete but appears complete at first glance
- Information exists in your working context but didn't make it to the response

**Common Instances**:
- Search results without URLs
- Code samples without imports or setup
- Product lists without prices
- Instructions without examples
- Links without explanatory text

**Root Causes**:
- **Process gap**: No systematic check before finalizing output
- **Attention slip**: Focus on one part of output, miss another
- **Mental model mismatch**: Assumed something was already included
- **Task complexity**: Large output causes oversight of details

**Prevention**:
- Create a pre-send checklist (what MUST be in this output type?)
- Use a template format that forces inclusion of all required fields
- Review output against a mental checklist before sending
- For lists/tables, verify column headers match requirements

**Example**:
```
Mistake: Truck search results without URLs
Checklist that would prevent it:
☐ Title included?
☐ URL included?
☐ Source name included?
☐ Snippet/description included?
```

---

## Process Gaps

**Description**: No systematic procedure exists, leading to inconsistent or incomplete work.

**Symptoms**:
- First time you made this mistake, but it could happen again
- No validation step exists to catch the error
- Task feels ad-hoc without clear stages
- Mistakes vary (sometimes you remember, sometimes not)

**Common Instances**:
- No pre-send validation for responses
- No confirmation step for important decisions
- No checklist for multi-step workflows
- No review step before finalizing complex tasks

**Root Causes**:
- Task is new or infrequent, so no pattern exists yet
- Process feels "obvious" but actually requires explicit steps
- No automation to enforce consistency
- Process not documented, so it's memory-dependent

**Prevention**:
- Document the workflow as steps
- Create explicit validation or review checkpoints
- Build checklists for recurring task types
- Automate checks when possible (scripts, validators)

**Example**:
```
Before: "Just send search results"
After: "Before sending search results, verify: title, URL, snippet"
```

---

## Context Loss

**Description**: Losing or forgetting key information during a long or complex task.

**Symptoms**:
- You started with clear understanding but lost track partway through
- User reminds you of requirements you acknowledged earlier
- Output doesn't align with stated objectives
- You remember the requirement only after the mistake is pointed out

**Common Instances**:
- Long sessions where early requirements fade from focus
- Complex tasks where intermediate steps cause distraction
- Multi-step processes where later steps override earlier ones
- Large outputs where early requirements get deprioritized

**Root Causes**:
- **Attention shift**: Moved focus to a new subtask and forgot the original requirement
- **Context window pressure**: Working with large context causes some details to fade
- **No external anchor**: Requirement not written down or linked to current work
- **Assumption of persistence**: Thought "I'll remember this" but didn't

**Prevention**:
- Write down key requirements before starting
- Reference the requirement again before finalizing
- Use external anchors (checklist, template, reference doc)
- For long tasks, periodically re-read the original requirement

**Example**:
```
Requirement: "Include the URL in search results"
Long task: Generate results, format them, write explanation...
Mistake: Focused on writing explanation, forgot the URL requirement
Prevention: Add checklist step "Verify original requirement" before finalizing
```

---

## Logic Errors

**Description**: Flawed reasoning or incorrect understanding of requirements.

**Symptoms**:
- Your logic made sense to you but was incorrect
- User points out a flaw in your approach
- Output is logically inconsistent
- You followed a procedure but the procedure was wrong

**Common Instances**:
- Misunderstanding what "include" means (include in response? include in summary?)
- Incorrect prioritization (do X first vs. do Y first)
- Wrong scope (does this apply to all items or just some?)
- Backward logic (should exclude, not include)

**Root Causes**:
- **Ambiguous requirement**: Requirement could mean multiple things
- **False assumption**: Assumed something about the task that isn't true
- **Incomplete mental model**: Didn't fully understand the domain or workflow
- **Overlooked constraint**: Missed a constraint that changes the approach

**Prevention**:
- Ask for clarification on ambiguous requirements
- Explicitly state assumptions and ask if they're correct
- Research or review domain knowledge before starting
- Break down the logic step-by-step and verify each step

**Example**:
```
Misunderstanding: "Include search results"
Interpretation 1: Include them in the response (this is correct)
Interpretation 2: Include them in my working memory (incorrect)
Prevention: Clarify "In what form should I include them? In the response to the user."
```

---

## Truncation and Incompleteness

**Description**: Output is cut off, incomplete, or missing trailing sections.

**Symptoms**:
- Last item in a list is incomplete
- Text ends abruptly mid-sentence
- Table has missing rows at the end
- Code snippet ends without closing braces

**Common Instances**:
- Long lists that exceed context window limits
- Streaming responses that get cut off
- Aggregations that miss the last item
- Code generation that stops before completion

**Root Causes**:
- **Context limit**: Task output exceeded available context
- **Timeout**: Processing took too long and was terminated
- **Attention loss**: Finished generating content without verifying completeness
- **Streaming interruption**: Output delivery was interrupted mid-stream

**Prevention**:
- Verify the output is complete (check for trailing context indicators)
- For lists, confirm count matches expectations (promised 10 items, show 10)
- For code, verify syntax is complete (all braces matched, no hanging statements)
- Test truncation-prone tasks with smaller inputs first

**Example**:
```
Output: "Here are 5 results: 1. Item A, 2. Item B, 3. Item C"
Problem: Promised 5, only gave 3
Prevention: Before finalizing, verify "I promised N items, do I have N items?"
```

---

## Assumption Errors

**Description**: Making incorrect assumptions about what was done or what is required.

**Symptoms**:
- You thought something was already done when it wasn't
- You assumed a requirement without asking
- User corrects an assumption you made
- Output is based on an incorrect mental model

**Common Instances**:
- Assuming a URL exists when it doesn't
- Assuming a field is present in data when it's optional
- Assuming the user wants the default approach
- Assuming something was included in a previous step

**Root Causes**:
- **Mental shortcut**: Made a reasonable assumption without verifying
- **Incomplete specification**: Requirement wasn't fully detailed
- **Domain knowledge gap**: Unfamiliar with domain conventions
- **No verification step**: Didn't check the assumption

**Prevention**:
- State assumptions explicitly and ask for confirmation
- Verify assumptions before committing to them
- Research conventions if unfamiliar with a domain
- Use templates or checklists that force verification

**Example**:
```
Assumption: "Search results have URLs"
Reality: Sometimes search results don't have clickable URLs (like local results)
Prevention: Explicitly list what each result SHOULD include, then verify it's there
```

---

## Task Type Summary

### High-Risk Task Types

These task types are especially prone to mistakes:

| Task Type | Common Mistake | Typical Root Cause | Prevention |
|-----------|---|---|---|
| Search/lookup | Missing URLs or sources | Output detail omission | Pre-send checklist |
| Code generation | Missing imports or setup | Incompleteness | Template or validation script |
| List creation | Wrong count or format | Process gap | Verify count before sending |
| Aggregation | Missed items or duplicates | Context loss | Documented checklist |
| Writing | Missing sections or details | Assumption error | Template with required sections |
| Research | Incomplete results | Truncation | Verify count matches request |

### Prevention Strategy by Task Type

**Search/Lookup Tasks**:
- Use: "Search result template" checklist
- Verify: Title, URL, source, snippet all present
- Check: URL is not truncated and is functional

**Code Generation Tasks**:
- Use: Code completeness template (imports, function signature, body, examples)
- Verify: Code is syntactically complete
- Check: All dependencies are listed

**List/Table Creation**:
- Use: Column/field verification checklist
- Verify: All promised items are present (count check)
- Check: Format is consistent across all items

**Aggregation/Summarization**:
- Use: Item checklist (did I include everything?)
- Verify: No duplicates, no missed items
- Check: Summary count matches source count

---

## Learning from Your Mistakes

When you make a mistake:

1. **Identify the pattern** - Does this match one of the above?
2. **Find the root cause** - Which underlying cause applies?
3. **Create prevention** - Which prevention strategy fits?
4. **Log the lesson** - Store it in your mistakes log
5. **Build the guardrail** - Create a checklist or process to prevent repetition

Example:
```
Mistake: Forgot URL in search results
Pattern: Output detail omission
Root cause: Process gap (no pre-send validation)
Prevention: Pre-send checklist for search tasks
Guardrail: Create "Search Results Checklist" in guardrails.md
Log: Add entry with date, pattern, root cause, guardrail link
```
