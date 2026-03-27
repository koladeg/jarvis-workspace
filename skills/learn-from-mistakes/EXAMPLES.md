# Usage Examples - learn-from-mistakes Skill

This file shows concrete examples of how to use the skill in real situations.

---

## Example 1: Logging the Truck Search Mistake

**Situation**: You (Jarvis) generated truck search results but forgot to include the URL/link. Kolade asked for the link and you realized the mistake.

**Step 1: Capture and log the mistake**

```bash
python scripts/analyze-mistake.py \
  --mistake "Forgot to include URL in truck search results" \
  --context "Web search task for Kolade - searching for truck listings" \
  --root-cause "Process gap: no systematic validation check before sending search results" \
  --pattern "Output detail omission" \
  --guardrail "Add URL-inclusion check to pre-send validation for search tasks" \
  --severity high
```

**Output**:
```
✓ Logged to: mistakes-log.json
✓ Markdown log: mistakes-log.md

Mistake Summary:
  What: Forgot to include URL in truck search results
  When: Web search task for Kolade - searching for truck listings
  Why: Process gap: no systematic validation check before sending search results
  Pattern: Output detail omission
  Guardrail: Add URL-inclusion check to pre-send validation for search tasks
  Severity: high

Next steps:
  1. Review references/mistake-patterns.md for 'Output detail omission' pattern
  2. Review references/guardrails.md for relevant checklists
  3. Create or update a guardrail in references/guardrails.md
  4. Add the guardrail to your workflow for future prevention
```

**Step 2: Review the mistake pattern**

Read `references/mistake-patterns.md` section on "Output Detail Omission":
- You see this is a common pattern caused by process gaps
- The prevention strategy is to create a pre-send checklist

**Step 3: Review the guardrail**

Read `references/guardrails.md` section on "Search/Lookup Task Guardrails":
```markdown
## Search Results Validation Checklist

**Before sending search results to user:**

- [ ] **Count verification**: Promised N results, have exactly N results
- [ ] **URL inclusion**: Each result has a source URL/link
- [ ] **URL format**: URLs are complete and not truncated
- [ ] **URL functionality**: URLs would work if clicked (not partial paths)
- [ ] **Title present**: Each result has a clear, descriptive title
- [ ] **Snippet quality**: Each result has meaningful text (not just "...")
- [ ] **Snippet length**: Snippets are substantive (>20 characters)
- [ ] **Consistency**: All results follow the same format
- [ ] **Source clarity**: User can identify where each result came from
- [ ] **No duplicates**: Each result is unique
```

**Step 4: Going forward**

Before sending search results next time:
```bash
python scripts/validate-checklist.py \
  --checklist search-results \
  --interactive
```

This will ask you:
```
1. Do you have the requested number of results?
   Answer (yes/no/skip): yes
   ✓ Passed

2. Does each result have a URL?
   Answer (yes/no/skip): yes
   ✓ Passed

... (all other checks)
```

---

## Example 2: Code Generation Missing Imports

**Situation**: You generated a Python code sample for Kolade but forgot to include the required `import requests` statement at the top.

**Step 1: Log the mistake**

```bash
python scripts/analyze-mistake.py \
  --mistake "Code sample missing import statement (requests)" \
  --context "Python code generation - HTTP request example" \
  --root-cause "Incomplete output: generated function without verifying all imports were included" \
  --guardrail "Use code completeness checklist before sending code samples"
```

**Pattern auto-detected**: Truncation/Incompleteness

**Step 2: Check the guardrail**

From `guardrails.md` → "Code Generation Guardrails":
```markdown
## Code Generation Verification Checklist

**Before sending code to user:**

- [ ] **All imports present**: Does the code include all required imports?
- [ ] **All dependencies listed**: Are external libraries documented?
- [ ] **Function complete**: Does the function have a complete body (not pseudocode)?
- [ ] **Syntax valid**: Code is syntactically complete (all braces, quotes, parentheses matched)
- [ ] **Entry point clear**: User knows how to run or use the code
- [ ] **Error handling**: Code handles edge cases or errors appropriately
- [ ] **Comments included**: Unclear sections are commented
- [ ] **Example provided**: User has an example of how to use it
- [ ] **Return statement**: Functions return what they promise
- [ ] **No placeholder text**: No [TODO], [...], or incomplete sections
```

**Step 3: Next time, before sending code**

```bash
python scripts/validate-checklist.py \
  --checklist code-sample \
  --interactive
```

The script will ask about imports, function completeness, syntax validity, examples, etc.

---

## Example 3: List Creation with Wrong Count

**Situation**: You promised to provide 5 product recommendations but only sent 3 in the list.

**Step 1: Log the mistake**

```bash
python scripts/analyze-mistake.py \
  --mistake "Product recommendation list has wrong count (promised 5, sent 3)" \
  --context "Product recommendations task" \
  --root-cause "No verification step: didn't count items before sending"
```

**Output**:
```
Pattern: Output detail omission (auto-detected from "wrong count")
```

**Step 2: Check the guardrail**

From `guardrails.md` → "List/Table Creation Guardrails":
```markdown
## List/Table Verification Checklist

**Before sending lists or tables to user:**

- [ ] **Count correct**: Promised N items, have exactly N items
- [ ] **All items present**: No missing or skipped items
- [ ] **Format consistent**: All items follow the same format
... (and more)
```

**Step 3: Next time, before sending lists**

```bash
python scripts/validate-checklist.py \
  --checklist list-table \
  --interactive
```

First question will be: "Do you have the correct number of items?"
This prevents the same mistake.

---

## Example 4: Creating a Custom Guardrail for a New Task Type

**Situation**: You notice you're making mistakes in "API response documentation" tasks - sometimes missing field descriptions, parameter types, or examples.

**Step 1: Log mistakes**

```bash
python scripts/analyze-mistake.py \
  --mistake "API documentation missing parameter types and descriptions" \
  --context "API reference documentation" \
  --root-cause "Process gap: no template or checklist for API docs"
```

Repeat for other similar mistakes you notice.

**Step 2: Create a custom guardrail**

In `references/guardrails.md`, add a new section:

```markdown
## API Documentation Guardrails

**Description**: Before sending API reference documentation.

**Risk**: Missing field descriptions, incomplete parameter lists, missing examples.

**Before sending API docs, verify**:

- [ ] **Endpoint name**: Clear endpoint URL path
- [ ] **HTTP method**: GET, POST, PUT, DELETE, etc. clearly stated
- [ ] **Description**: What does this endpoint do?
- [ ] **Parameters**: All parameters listed with name, type, required/optional
- [ ] **Parameter descriptions**: Each parameter has a human-readable description
- [ ] **Request example**: Code example showing how to call the endpoint
- [ ] **Response structure**: Documented what the response looks like
- [ ] **Response fields**: Each field in response documented with type
- [ ] **Error cases**: What errors can occur and what they mean
- [ ] **Status codes**: HTTP status codes documented (200, 400, 404, etc.)

**Common slip-ups**: Forgetting field types, missing parameter descriptions, no examples

**Example**:
```
GOOD:
```
GET /api/users/{userId}
- Parameter: userId (integer, required) - The unique identifier of the user
- Response: { id, name, email, createdAt }
- Example: GET /api/users/123
```

BAD:
```
GET /api/users/{userId}
- Returns user info
```
```
```

**Step 3: Going forward**

Use this checklist before sending API documentation:
```bash
# Create a custom validation or just use the checklist manually
# Reference: custom-api-docs guardrail in guardrails.md
```

---

## Example 5: Weekly Review - Identifying Patterns

**Situation**: It's Friday. You want to review the week's mistakes and see if there are recurring patterns.

**Step 1: Check your mistakes log**

```bash
cat mistakes-log.md
```

Output shows:
```
# Mistakes Log

## 2026-03-25

### 09:18 - Forgot to include URL in truck search results
- Pattern: Output detail omission

### 11:30 - Code sample missing import
- Pattern: Truncation/Incompleteness

### 14:45 - List had wrong count
- Pattern: Output detail omission

## 2026-03-24

### 10:00 - Product recommendation missing details
- Pattern: Output detail omission
```

**Step 2: Identify the pattern**

You notice:
- "Output detail omission" appears 3 times in 2 days
- Pattern: Information-heavy outputs where you focus on one aspect and miss another
- Common condition: Happens when output is long and manual (not automated)

**Step 3: Strengthen guardrails**

The existing "Search Results Validation Checklist" is good, but you need one more checklist for general "Information-Heavy Output" tasks.

Add to `guardrails.md`:

```markdown
## Information-Heavy Output Guardrail

**When to use**: Before sending any output with multiple required details (search results, product lists, documentation, etc.)

**Risk**: Missing one detail while focusing on others

**Before sending information-heavy output, verify**:

- [ ] **Required details identified**: What must be included in each item?
- [ ] **All required details present**: Does each item have ALL required parts?
- [ ] **Sample check**: Pick one item and verify it has everything. Then assume all items do.
- [ ] **Spot check random items**: Verify 2-3 random items have all required details
- [ ] **No assumptions**: Don't assume "of course I included X" - verify it's actually there
```

**Step 4: Going forward**

Before any information-heavy output, use this checklist. Your mistakes log helped you identify the pattern and create a preventive guardrail.

---

## Example 6: Recovering from a Pattern

**Situation**: You've now created the "Search Results Validation Checklist". Two weeks later, you use it and actually catch a mistake before sending.

**What happened**:
1. You generated 5 search results
2. Before sending, you ran the checklist
3. You checked "URL inclusion: Each result has a source URL/link"
4. You realized result #3 was missing the URL!
5. You fixed it before Kolade even saw it

**This is success**: The guardrail prevented the mistake from reaching the user.

**Log this win**:
```bash
# You don't log this as a mistake - you log it as a prevented mistake
# Add to mistakes-log.md manually:

### 09:45 - Prevented: Missing URL in search result #3
- Context: Search results - checklist caught it before sending
- Guardrail: Search Results Validation Checklist
- Status: Prevented (thanks to guardrail!)
```

Over time, your mistakes log becomes a record of:
- What went wrong initially
- What guardrails you built
- What guardrails actually prevented problems

This shows you which guardrails are working and which need improvement.

---

## Quick Reference: Common Task Types

### Search/Lookup Results
- **Common mistake**: Missing URLs
- **Guardrail**: "Search Results Validation Checklist" in guardrails.md
- **Script**: `python scripts/validate-checklist.py --checklist search-results --interactive`

### Code Samples
- **Common mistake**: Missing imports, incomplete functions
- **Guardrail**: "Code Generation Verification Checklist" in guardrails.md
- **Script**: `python scripts/validate-checklist.py --checklist code-sample --interactive`

### Lists/Tables
- **Common mistake**: Wrong count, inconsistent format
- **Guardrail**: "List/Table Verification Checklist" in guardrails.md
- **Script**: `python scripts/validate-checklist.py --checklist list-table --interactive`

### Aggregations
- **Common mistake**: Missed items, duplicates
- **Guardrail**: "Aggregation Verification Checklist" in guardrails.md
- **Script**: `python scripts/validate-checklist.py --checklist aggregation --interactive`

### Documentation
- **Common mistake**: Missing sections, incomplete explanations
- **Guardrail**: "Document Completeness Checklist" in guardrails.md
- **Script**: `python scripts/validate-checklist.py --checklist document --interactive`

---

## The Workflow in Action

1. **Make a mistake** → Log it with `analyze-mistake.py`
2. **Review the pattern** → Read relevant section in `mistake-patterns.md`
3. **Get a guardrail** → Find or create checklist in `guardrails.md`
4. **Validate next time** → Use `validate-checklist.py --interactive` before sending
5. **Weekly review** → Read `mistakes-log.md` to identify recurring patterns
6. **Improve guardrails** → Strengthen checklists that didn't work, create new ones for new patterns

The goal: Transform errors into systematic improvement, one mistake at a time.
