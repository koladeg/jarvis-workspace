# learn-from-mistakes Skill - Complete Index

## Quick Navigation

This is your complete guide to the new "learn-from-mistakes" AgentSkill.

---

## 📍 Where to Find Everything

### The Skill Itself
- **Folder**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes/`
- **Packaged**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes.skill` (17KB)
- **Ready to use**: Copy the folder to OpenClaw or install the .skill file

### Documentation Files (in workspace root)
- **SKILL_DEPLOYMENT.md** ← Start here! Complete overview and deployment guide
- **LEARN_FROM_MISTAKES_INDEX.md** ← You are here

### Examples (in workspace root)
- **skills/learn-from-mistakes/EXAMPLES.md** ← 6 real-world usage scenarios

---

## 🎯 What This Skill Does

This skill helps you **systematically learn from mistakes** by:

1. **Capturing** what went wrong with context and evidence
2. **Analyzing** root causes (7 common patterns identified)
3. **Identifying** systemic patterns across mistakes
4. **Creating** preventive guardrails (checklists for high-risk tasks)
5. **Storing** lessons persistently for future reference

---

## 📂 Skill Contents at a Glance

| File | Size | Purpose |
|------|------|---------|
| **SKILL.md** | 7.0 KB | Main skill documentation + workflow |
| **references/mistake-patterns.md** | 10.4 KB | 7 patterns, root causes, prevention |
| **references/guardrails.md** | 12.1 KB | 6 pre-built checklists + templates |
| **scripts/analyze-mistake.py** | 7.4 KB | Log mistakes with auto-categorization |
| **scripts/validate-checklist.py** | 8.9 KB | Pre-send validation tool |
| **EXAMPLES.md** | 12.9 KB | Real-world usage examples |

---

## 🚀 Quick Start (5 Minutes)

### 1. Log a Mistake
```bash
cd /home/claw/.openclaw/workspace/skills/learn-from-mistakes

python scripts/analyze-mistake.py \
  --mistake "What you forgot or got wrong" \
  --context "Task or situation" \
  --root-cause "Why it happened"
```

**Output**: Creates `mistakes-log.json` and `mistakes-log.md`

### 2. Review the Pattern
Open `references/mistake-patterns.md` and find your pattern category.

### 3. Find a Guardrail
Open `references/guardrails.md` and find the relevant checklist.

### 4. Validate Next Time
```bash
python scripts/validate-checklist.py \
  --checklist search-results \
  --interactive
```

---

## 📖 Complete Reading Guide

### First Time Reading (30 minutes)
1. Read this index (you're doing it!)
2. Read **SKILL_DEPLOYMENT.md** for complete overview
3. Skim **EXAMPLES.md** for usage patterns

### When You Make a Mistake (10 minutes)
1. Run `analyze-mistake.py` to log it
2. Read relevant section in **references/mistake-patterns.md**
3. Copy relevant checklist from **references/guardrails.md**

### When You Want to Use a Guardrail (5 minutes)
1. Open **references/guardrails.md**
2. Find your task type (search, code, list, aggregation, writing)
3. Run `validate-checklist.py --checklist [type] --interactive`

### Weekly Review (15 minutes)
1. Read your `mistakes-log.md` (most recent entries first)
2. Identify recurring patterns
3. Update or strengthen relevant guardrails

---

## 🎬 Real-World Example

**Your mistake**: Truck search results without URL/link

**Using the skill**:

```bash
# 1. Log it
python scripts/analyze-mistake.py \
  --mistake "Forgot to include URL in truck search results" \
  --context "Web search task for Kolade" \
  --root-cause "Process gap: no pre-send validation check"

# 2. Review the pattern
# → Read: references/mistake-patterns.md (Output Detail Omission section)

# 3. Find the guardrail
# → Read: references/guardrails.md (Search/Lookup Task Guardrails section)

# 4. Next time, validate before sending
python scripts/validate-checklist.py \
  --checklist search-results \
  --interactive
```

The checklist will ask:
- Do you have the requested number of results?
- Does each result have a URL?
- Are URLs complete (not truncated)?
- Does each result have a title?
- Does each result have a snippet?
- ... and more

**Result**: Mistake prevented before Kolade even sees it. ✅

---

## 🔍 Task Types Covered

Each has a pre-built checklist in `guardrails.md`:

| Task Type | Common Risk | Checklist Command |
|-----------|---|---|
| **Search/Lookup** | Missing URLs, incomplete results | `--checklist search-results` |
| **Code Generation** | Missing imports, incomplete functions | `--checklist code-sample` |
| **List/Table Creation** | Wrong count, format issues | `--checklist list-table` |
| **Aggregation** | Missed items, duplicates | `--checklist aggregation` |
| **Writing/Docs** | Missing sections, unclear structure | `--checklist document` |

Plus: General response composition checklist.

---

## 🛠️ How to Use the Scripts

### analyze-mistake.py
```bash
python scripts/analyze-mistake.py \
  --mistake "What went wrong" \
  --context "When/where it happened" \
  --root-cause "Why it happened" \
  [--pattern "Category"] \
  [--guardrail "How to prevent it"] \
  [--severity high|medium|low]
```

**Features**:
- Auto-detects pattern from root cause
- Creates JSON log for persistence
- Generates markdown log for review
- Suggests next steps

### validate-checklist.py
```bash
python scripts/validate-checklist.py \
  --checklist [search-results|code-sample|list-table|aggregation|document] \
  --interactive
```

**Features**:
- Interactive mode asks questions
- Content-based heuristic validation
- Clear pass/fail results

---

## 📋 Key Design Principles

1. **Mistakes are data** → Each error teaches you something
2. **Prevention over perfection** → 80% guardrail beats 100% effort
3. **Mechanical checks work** → Checklists catch more than memory
4. **Persist lessons** → Write it down, don't rely on memory
5. **Build over time** → Your guardrails get stronger each week

---

## 🔄 Your Weekly Workflow

### Monday-Friday: During work
- Before sending outputs, check `guardrails.md` for relevant checklist
- Run `validate-checklist.py --interactive` before important responses
- Keep a checklist visible while composing

### Friday: Weekly review
- Read `mistakes-log.md` to see what went wrong
- Identify recurring patterns (same mistake 3x = systemic problem)
- Strengthen guardrails that didn't prevent mistakes
- Add guardrails for new risk types

### End of session: Session summary
- Log important mistakes with `analyze-mistake.py`
- Update `MEMORY.md` with high-level lessons
- Note which guardrails helped prevent errors

---

## 📁 File Organization

```
workspace/
├── SKILL_DEPLOYMENT.md          ← Complete deployment overview
├── LEARN_FROM_MISTAKES_INDEX.md ← You are here
│
└── skills/learn-from-mistakes/
    ├── SKILL.md                 ← Main skill documentation
    ├── EXAMPLES.md              ← 6 real-world scenarios
    │
    ├── references/
    │   ├── mistake-patterns.md  ← 7 patterns + prevention
    │   └── guardrails.md        ← 6 task type checklists
    │
    └── scripts/
        ├── analyze-mistake.py   ← Log mistakes tool
        └── validate-checklist.py ← Validation tool
```

---

## ✅ Verification Checklist

Before you start using the skill, verify:

- [ ] Skill folder exists: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes/`
- [ ] SKILL.md exists and is readable
- [ ] `references/mistake-patterns.md` exists
- [ ] `references/guardrails.md` exists
- [ ] `scripts/analyze-mistake.py` is executable
- [ ] `scripts/validate-checklist.py` is executable
- [ ] Run: `python scripts/analyze-mistake.py --help` (should work)
- [ ] Run: `python scripts/validate-checklist.py --help` (should work)

All verified? ✅ You're ready to use the skill!

---

## 🎓 Learning Path

### Beginner (First Time)
1. Read this index
2. Read SKILL_DEPLOYMENT.md
3. Run `analyze-mistake.py --help`
4. Make a test log entry

### Intermediate (Using It)
1. Log real mistakes
2. Read mistake-patterns.md to understand yours
3. Use guardrails.md checklists before important outputs
4. Run validate-checklist.py --interactive

### Advanced (Building Guardrails)
1. Weekly review of mistakes-log.md
2. Identify patterns
3. Create custom guardrails in guardrails.md
4. Integrate guardrails into your workflow

---

## 🆘 Troubleshooting

### Script won't run
```bash
# Ensure it's executable
chmod +x scripts/analyze-mistake.py
chmod +x scripts/validate-checklist.py

# Try with python3 explicitly
python3 scripts/analyze-mistake.py --help
```

### Can't find a pattern
- Check `references/mistake-patterns.md` table of contents
- Patterns are categorized: Output Detail, Process Gap, Context Loss, Logic Error, Truncation, Assumption

### Need a custom checklist
- Copy the "Creating Custom Guardrails" template from `guardrails.md`
- Add your checklist to the file
- Use it with `validate-checklist.py` or manually

### Want to see examples
- Read `EXAMPLES.md` for 6 real scenarios
- Each shows the full workflow from mistake to prevention

---

## 📞 Next Steps

1. **Right now**: Read SKILL_DEPLOYMENT.md (complete overview)
2. **Soon**: Review EXAMPLES.md (see it in action)
3. **Today**: Run `analyze-mistake.py` to test it
4. **This week**: Create your first custom guardrail
5. **Ongoing**: Use the skill for every mistake you notice

---

**Status**: ✅ Skill is complete, packaged, and ready to use  
**Location**: `/home/claw/.openclaw/workspace/skills/learn-from-mistakes/`  
**Package**: `learn-from-mistakes.skill` (17KB)

Start with **SKILL_DEPLOYMENT.md** →
