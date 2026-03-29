# Guardrails and Preventive Checklists

This reference contains pre-built checklists and guardrails for high-risk tasks. Copy and adapt these to your specific workflows.

## Table of Contents

1. [Search/Lookup Task Guardrails](#searchlookup-task-guardrails)
2. [Code Generation Guardrails](#code-generation-guardrails)
3. [List/Table Creation Guardrails](#listtable-creation-guardrails)
4. [Aggregation/Summarization Guardrails](#aggregationsummarization-guardrails)
5. [Writing and Documentation Guardrails](#writing-and-documentation-guardrails)
6. [Response Composition Guardrails](#response-composition-guardrails)
7. [Creating Custom Guardrails](#creating-custom-guardrails)

---

## Search/Lookup Task Guardrails

**When to use**: Before sending search results, product lookups, information retrieval, or any task where sources are important.

**Risk**: Missing URLs, incomplete results, inconsistent formatting.

### Guardrail: Pre-Send Validation Checklist

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

**Format expectation**:
```
1. [Title] - [Source name]
   URL: [full URL]
   [Snippet/description]
```

**Common slip-ups**: Forgetting URL, truncating URL, inconsistent formatting
```

### Guardrail: Search Result Template

Use this template to ensure consistency:

```markdown
## [Query]: [Number] Results

[Result 1]
- **Title**: [Clear, descriptive title]
- **Source**: [Source name]
- **URL**: [Full, complete URL]
- **Snippet**: [1-2 sentence summary of content]

[Result 2]
- ... (repeat for all results)

[Verification summary]
- Returned: X results (requested Y)
- All URLs included and functional
- All sources clear and consistent
```

---

## Code Generation Guardrails

**When to use**: Before sending code samples, scripts, functions, or any executable code.

**Risk**: Missing imports, incomplete functions, syntax errors, untested code.

### Guardrail: Code Completeness Checklist

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

**Common slip-ups**: Missing imports, incomplete functions, no usage example
```

### Guardrail: Code Sample Template

```python
# [Code title/description]
# Usage: [Brief explanation of how to use this code]

# Required imports
import [module]
from [module] import [function]

# Main code
def main():
    """[Brief description of what this does]"""
    # [Implementation]
    return [result]

# Example usage
if __name__ == "__main__":
    result = main()
    print(result)
```

---

## List/Table Creation Guardrails

**When to use**: Before sending lists, tables, enumerations, or any structured data collections.

**Risk**: Wrong count, missing items, inconsistent formatting, missing columns.

### Guardrail: List/Table Verification Checklist

```markdown
## List/Table Verification Checklist

**Before sending lists or tables to user:**

- [ ] **Count correct**: Promised N items, have exactly N items
- [ ] **All items present**: No missing or skipped items
- [ ] **Format consistent**: All items follow the same format
- [ ] **Columns complete**: All promised columns are present
- [ ] **Data types match**: Data is consistent (all are strings, numbers, etc.)
- [ ] **Sorting correct**: Items are sorted as promised (alphabetical, by importance, etc.)
- [ ] **Headers clear**: Column headers are descriptive
- [ ] **No duplicates**: Each item appears exactly once
- [ ] **No truncation**: Long items aren't cut off
- [ ] **No blank rows**: No empty items or separators

**Common slip-ups**: Wrong count, missing items, inconsistent formatting, truncation at the end
```

### Guardrail: Table Template

```markdown
## [Title]: [Count] Items

| [Column 1] | [Column 2] | [Column 3] |
|---|---|---|
| [data] | [data] | [data] |
| [data] | [data] | [data] |

**Summary**: Returned [N] items as requested
```

---

## Aggregation/Summarization Guardrails

**When to use**: Before sending summaries, compilations, combined data, or any task that pulls from multiple sources.

**Risk**: Missed items, incorrect totals, duplicates, lost details.

### Guardrail: Aggregation Verification Checklist

```markdown
## Aggregation Verification Checklist

**Before sending aggregated data to user:**

- [ ] **Item count**: Do I have all items from all sources?
- [ ] **Source verification**: Did I check all promised sources?
- [ ] **No duplicates**: Have I removed or flagged duplicates?
- [ ] **Total correct**: Summary total matches sum of parts
- [ ] **Details preserved**: Important details weren't lost in aggregation
- [ ] **Consistency**: All items use the same format/structure
- [ ] **Completeness**: No truncated or partial items
- [ ] **Ordering logical**: Items are sorted or grouped sensibly
- [ ] **Source attribution**: Can user trace each item to its source?
- [ ] **Verification summary**: I can explain how I verified completeness

**Verification approach**:
- List all sources checked
- Count items from each source
- Verify total = sum of counts
- Check against original requirement

**Common slip-ups**: Missed a source, forgot to count, duplicates included
```

### Guardrail: Aggregation Template

```markdown
## [Aggregation title]

**Sources checked**:
- Source 1: X items
- Source 2: Y items
- Source 3: Z items

**Total**: X + Y + Z = [total] items

[Aggregated data here]

**Verification**:
- All sources checked ✓
- No duplicates ✓
- Count verified ✓
```

---

## Writing and Documentation Guardrails

**When to use**: Before sending written documents, guides, explanations, or structured writing.

**Risk**: Missing sections, incomplete explanations, unclear structure.

### Guardrail: Document Structure Checklist

```markdown
## Document Completeness Checklist

**Before sending written content to user:**

- [ ] **Title/heading**: Clear main heading present
- [ ] **Overview**: Brief explanation of what this is
- [ ] **All sections**: All promised or expected sections are present
- [ ] **Introduction**: Reader knows what to expect
- [ ] **Main content**: Core information is comprehensive
- [ ] **Examples**: Concrete examples clarify abstract concepts
- [ ] **Conclusion/summary**: Clear takeaway or next steps
- [ ] **Formatting**: Structure is clear (headings, bullets, etc.)
- [ ] **Clarity**: Writing is clear and unambiguous
- [ ] **Completeness**: No trailing "..." or [TODO] sections

**Expected sections** (adjust per context):
- Title
- Overview/Introduction
- Main content (detailed)
- Examples or case studies
- Summary or next steps
```

---

## Response Composition Guardrails

**When to use**: Before finalizing any response to a user.

**Risk**: Missing required information, unclear structure, incomplete answers.

### Guardrail: Pre-Send Response Checklist

```markdown
## Pre-Send Response Checklist

**Before sending any response to user:**

- [ ] **Addresses the question**: Response directly answers what was asked
- [ ] **Complete**: All necessary information is included
- [ ] **Required elements**: Does this response type have required elements? Are they all present?
- [ ] **Examples included**: Abstract concepts have concrete examples
- [ ] **Clear structure**: Reader can navigate the response easily
- [ ] **Links/references**: Required links or references are included
- [ ] **Context provided**: Reader has enough context to understand
- [ ] **No assumptions**: Or assumptions are stated explicitly
- [ ] **Tone appropriate**: Matches the context and relationship
- [ ] **Ready to send**: I would send this without hesitation

**Required elements by response type**:
- **Search results**: Title, URL, snippet
- **Code samples**: Imports, complete function, usage example
- **Lists**: Count verification, consistent format
- **Explanations**: Overview, details, examples
- **Instructions**: Steps, prerequisites, examples
- **Recommendations**: Rationale, options, tradeoffs
```

---

## Creating Custom Guardrails

### Template for Custom Guardrails

When you identify a new high-risk task, create a custom guardrail:

```markdown
## [Task Name] Guardrail

**Description**: [What task is this for?]

**Risk**: [What commonly goes wrong?]

**Before [task action], verify**:

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]
- [ ] [Requirement 4]
- [ ] [Requirement 5]

**Common slip-ups**: [What mistakes happen most often?]

**Verification approach**:
[Concrete steps to verify each requirement]

**Example**:
```
[Concrete example of correct vs. incorrect]
```
```

### Example: Creating a Custom Guardrail

**Your mistake**: You forgot to include version numbers in a requirements list.

**Analysis**:
- Task: Generate software requirements lists
- Risk: Missing version numbers, missing compatibility notes
- Root cause: Process gap (no validation)

**Creating the guardrail**:

```markdown
## Requirements List Guardrail

**Description**: Before sending a software requirements list.

**Risk**: Missing version numbers, unclear compatibility, incomplete specs.

**Before sending requirements, verify**:

- [ ] Each requirement has a clear name
- [ ] Each requirement lists the version or version constraint
- [ ] Compatibility requirements are explicit (Python 3.8+, Node 16+, etc.)
- [ ] All dependencies are listed (nothing assumed as "obvious")
- [ ] Examples or installation instructions provided
- [ ] Optional vs. required is clearly marked
- [ ] No [TODO] or placeholder text

**Common slip-ups**: Forgetting versions, assuming stdlib items are known, missing optional items

**Verification approach**:
- Read through each requirement
- Confirm every requirement has a version
- Check that nothing is assumed
- Verify optional items are marked as such
```

### Where to Store Custom Guardrails

Add custom guardrails to this file in the appropriate section, or create a new section. Over time, your guardrails library will grow and become your personal prevention system.

---

## Using Guardrails Effectively

### Daily Integration

1. **Before important outputs**: Check the relevant guardrail from this list
2. **During the task**: Use the guardrail to structure your work
3. **Before sending**: Verify against the checklist one final time
4. **Log the lesson**: If you notice a guardrail prevented a mistake, that's success

### Iterating Guardrails

Guardrails are living documents. Update them when:
- You make the same mistake twice despite having a guardrail (guardrail needs strengthening)
- You notice a new risk pattern (add a new guardrail)
- A guardrail becomes too cumbersome (simplify it)

### Key Principle

The goal is not perfection, but awareness and prevention. A guardrail that actually prevents 80% of mistakes is more valuable than an ideal checklist that's too long to use.
