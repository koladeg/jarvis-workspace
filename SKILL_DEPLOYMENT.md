# learn-from-mistakes Skill - Deployment Report

**Status**: ✅ Complete and Ready for Use  
**Created**: 2026-03-25  
**Location**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes/`  
**Packaged**: `learn-from-mistakes.skill` (17KB)

---

## What Was Created

A complete, production-ready AgentSkill that helps systematically review mistakes, document lessons, and build preventive guardrails.

### Skill Contents

```
learn-from-mistakes/
├── SKILL.md                                    (7.0 KB)
│   ├── Metadata: name, description
│   ├── Overview and when to use
│   ├── 5-step workflow (Capture → Analyze → Pattern → Guardrail → Store)
│   ├── Quick start guide
│   └── Reference to bundled resources
│
├── references/
│   ├── mistake-patterns.md                     (10.4 KB)
│   │   ├── 7 common mistake patterns
│   │   ├── Root causes for each pattern
│   │   ├── Symptoms, prevention strategies
│   │   └── High-risk task type summary
│   │
│   └── guardrails.md                           (12.1 KB)
│       ├── Pre-built checklists for 6 task types
│       ├── Guardrail templates (copy & customize)
│       ├── Usage patterns and integration
│       └── How to create custom guardrails
│
└── scripts/
    ├── analyze-mistake.py                      (7.4 KB)
    │   ├── Log mistakes with root cause, pattern, guardrail
    │   ├── Auto-categorize patterns from root cause
    │   ├── Save to JSON log (persistent)
    │   ├── Generate markdown mistakes log
    │   └── Suggest next steps
    │
    └── validate-checklist.py                   (8.9 KB)
        ├── Interactive checklist validation
        ├── 5 built-in checklists (search-results, code, list, aggregation, document)
        ├── Content-based heuristic validation
        └── Pre-send validation before finalizing output
```

---

## Key Features

### 1. **Systematic Mistake Analysis**
- Capture what went wrong with context and evidence
- Analyze root causes (7 common patterns identified)
- Identify systemic patterns across mistakes
- Understand why mistakes happen, not just what

### 2. **Preventive Guardrails**
- Pre-built checklists for 6 high-risk task types
- Templates for creating custom guardrails
- Integration into your workflow as pre-send validation
- Mechanical checks to prevent repeating the same error

### 3. **Persistent Lessons Log**
- `mistakes-log.json`: Machine-readable log for tracking
- `mistakes-log.md`: Human-readable markdown for review
- Timestamped entries with severity levels
- Linked to patterns and guardrails

### 4. **Automation & Tools**
- `analyze-mistake.py`: Log mistakes systematically with pattern auto-detection
- `validate-checklist.py`: Validate output before sending against guardrails
- Both scripts are fully functional and tested

---

## Concrete Example

**The Problem**: I (Jarvis) generated truck search results but forgot to include the URL/link in my response to Kolade. When Kolade asked for the link, I couldn't find it.

**Using This Skill**:

```bash
# Step 1: Log the mistake
python scripts/analyze-mistake.py \
  --mistake "Forgot to include URL in truck search results" \
  --context "Web search task for Kolade" \
  --root-cause "Process gap: no pre-send validation check" \
  --pattern "Output detail omission" \
  --guardrail "Add URL-inclusion check to search results response" \
  --severity high
```

**Output**:
```
✓ Logged to: mistakes-log.json
✓ Markdown log: mistakes-log.md

Mistake Summary:
  What: Forgot to include URL in truck search results
  When: Web search task for Kolade
  Why: Process gap: no pre-send validation check
  Pattern: Output detail omission
  Guardrail: Add URL-inclusion check to search results response
  Severity: high

Next steps:
  1. Review references/mistake-patterns.md for 'Output detail omission' pattern
  2. Review references/guardrails.md for relevant checklists
  3. Create or update a guardrail in references/guardrails.md
  4. Add the guardrail to your workflow for future prevention
```

**Step 2**: Review the "Search Results Validation Checklist" in `references/guardrails.md`

**Step 3**: Use it before next search result task:
```bash
python scripts/validate-checklist.py \
  --checklist search-results \
  --interactive
```

---

## Design Principles

### 1. **Progressive Disclosure**
- Metadata (name, description) always available
- SKILL.md loaded when skill triggers
- Detailed references loaded on-demand
- Scripts can run without loading into context

### 2. **Token Efficiency**
- SKILL.md is concise (7KB) with clear workflow
- Detailed patterns & guardrails in separate reference files
- Scripts are executable, not just documentation
- No redundant documentation files (no README, no INSTALLATION_GUIDE, etc.)

### 3. **Actionable & Concrete**
- Every pattern has concrete examples
- Every guardrail is a working checklist
- Scripts work immediately without setup
- Clear next steps after each action

### 4. **Built for Reuse**
- Checklists are copy-paste ready
- Mistake patterns are generalizable
- Scripts auto-categorize and suggest improvements
- Logs grow over time, showing patterns

---

## Usage Patterns

### Pattern 1: "I Just Made a Mistake"
1. Run `analyze-mistake.py` with the mistake details
2. Get auto-categorized pattern and suggested guardrail
3. Review the relevant pattern in `mistake-patterns.md`
4. Copy the relevant checklist from `guardrails.md`
5. Use the checklist going forward

### Pattern 2: "Prevent a Known Mistake Type"
1. Before starting a task, check `guardrails.md`
2. Find the relevant task type checklist
3. Run `validate-checklist.py --interactive` before sending
4. Verify against checklist items
5. Send only after all checks pass

### Pattern 3: "Review Weekly Patterns"
1. Read through `mistakes-log.md` (most recent entries first)
2. Identify recurring patterns
3. Identify which guardrails need strengthening
4. Update or create new guardrails in `guardrails.md`

### Pattern 4: "Session Review / Lessons Learned"
1. At end of session, log important mistakes
2. Use `analyze-mistake.py` to capture each one
3. Update `MEMORY.md` with high-level lessons
4. Link to guardrails for future prevention

---

## Task Types Covered

1. **Search/Lookup Tasks** → Risk: Missing URLs, incomplete results
2. **Code Generation** → Risk: Missing imports, incomplete functions
3. **List/Table Creation** → Risk: Wrong count, format inconsistency
4. **Aggregation/Summarization** → Risk: Missed items, duplicates
5. **Writing/Documentation** → Risk: Missing sections, unclear structure
6. **Response Composition** → Risk: Missing required information

Each has a pre-built checklist. Create custom guardrails for tasks not covered.

---

## Integration with Your Workflow

### Daily Use
- Before sending important outputs, check `guardrails.md` for relevant checklist
- Run `validate-checklist.py --interactive` if uncertain
- Keep checklist visible while composing output

### Weekly Review
- Read `mistakes-log.md` to review recent errors
- Identify patterns (same mistake multiple times?)
- Strengthen guardrails that didn't prevent a mistake
- Add new guardrails for new risk types

### Session Summary
- Log important mistakes with `analyze-mistake.py`
- Update `MEMORY.md` with high-level lessons
- Note which guardrails helped prevent mistakes

---

## File Sizes & Resources

| File | Size | Purpose |
|------|------|---------|
| SKILL.md | 7.0 KB | Main skill documentation |
| mistake-patterns.md | 10.4 KB | Reference: 7 patterns + root causes |
| guardrails.md | 12.1 KB | Reference: 6 task type checklists + templates |
| analyze-mistake.py | 7.4 KB | Script: Log mistakes systematically |
| validate-checklist.py | 8.9 KB | Script: Validate output against checklists |
| **Total skill** | ~46 KB | **All files uncompressed** |
| **Packaged** | 17 KB | **learn-from-mistakes.skill** (zip) |

---

## Testing & Validation

✅ **All components tested**:
- SKILL.md: Validated against AgentSkills spec
- Scripts: Both `--help` and functional runs verified
- Example run: `analyze-mistake.py` successfully logged the truck search mistake
- Output generation: Both JSON and markdown logs created correctly
- Packaging: `package_skill.py` completed without errors

---

## Next Steps for Jarvis

1. **Integrate into workflow**: Copy relevant checklists from `guardrails.md` to your memory or quick-reference files
2. **First use**: Log the truck search mistake that triggered this skill
3. **Build guardrails**: Create a "Search Results Checklist" for your workflow
4. **Weekly reviews**: Use `mistakes-log.md` to track patterns and improve guardrails
5. **Customize**: Add custom guardrails in `references/guardrails.md` for your most common high-risk tasks

---

## File Locations

- **Skill folder**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes/`
- **Packaged skill**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes.skill`
- **To use**: Copy the skill folder or the .skill file to your OpenClaw skills directory

---

## Key Design Principles

1. **Mistakes are data** - Each error teaches you something about your process
2. **Prevention beats perfection** - A good guardrail prevents 80% of mistakes better than aiming for 100%
3. **Mechanical checks work** - Checklists catch more errors than memory or intuition
4. **Log lessons persistently** - Session memory isn't enough; write it down
5. **Build over time** - Your guardrails library grows stronger as you add to it

---

**Deliverable Status**: ✅ Ready to Use

The skill is complete, packaged, and ready for immediate integration into your workflow. All scripts are functional, all documentation is comprehensive, and the skill follows all AgentSkills specifications.
