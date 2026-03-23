# Ollama Usage Guide

**Setup Date:** 2026-03-23  
**Status:** ✅ Running, ready to use  
**Cost:** FREE (local CPU inference)

---

## Overview

Ollama provides local LLM inference without API calls. Use it for **lightweight, routine tasks** to reduce API spend and improve speed.

---

## Available Models

| Model | Size | Speed | Best For | Cost |
|-------|------|-------|----------|------|
| `llama3.2:3b` | 2.0 GB | Fast (~5-10s) | Quick summaries, git status, log analysis, formatting | ✅ FREE |
| `nomic-embed-text` | 274 MB | Very fast | Memory embeddings (auto) | ✅ FREE |

---

## When to Use Ollama

### ✅ Good Use Cases
- Git status checks (`git status`, `git log`)
- Quick file summaries (read a file, summarize in 1-2 sentences)
- Log file analysis (errors, patterns)
- Simple text formatting (markdown, restructuring)
- Quick classification (is this important? yes/no)
- Heartbeat checks (is anything broken?)
- Simple JSON generation (structured output)

### ❌ Not Suitable For
- Complex reasoning or multi-step logic
- Creative writing or nuanced language
- Code generation (use Codex instead)
- Tasks requiring current information
- Large context windows (memory-heavy)
- Anything that needs "think carefully"

---

## How to Use Ollama

### Via Command Line

```bash
# Check if Ollama is running
curl -s http://localhost:11434/api/tags | head -20

# Run inference
ollama run llama3.2:3b "Summarize this in one sentence: [your text]"

# Multi-line prompt
echo "What is the status of this log file?
[your log content]" | ollama run llama3.2:3b
```

### Via Script

```bash
#!/bin/bash

# Example: Analyze a log file
LOG_FILE="logs/my.log"

PROMPT="Analyze this log file and tell me if there are any errors:

$(tail -50 "$LOG_FILE")"

RESPONSE=$(ollama run llama3.2:3b "$PROMPT")
echo "Analysis: $RESPONSE"
```

### Via Python/Node

```python
import requests
import json

def ollama_query(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

result = ollama_query("Summarize this in one sentence: " + my_text)
print(result)
```

---

## Example Tasks

### 1. Git Status Summary

```bash
ollama run llama3.2:3b "Summarize the status in 1 sentence:

$(cd /home/claw/.openclaw/workspace && git status --short)"
```

**Output:** "3 modified files and 10 untracked files, mostly log and script updates."

### 2. Log File Analysis

```bash
TAIL=$(tail -30 logs/adugboinsure-funding.log)
ollama run llama3.2:3b "Did this job succeed? Yes/No with one reason:

$TAIL"
```

**Output:** "Yes. Last line shows 'Telegram post sent'."

### 3. Quick Summarization

```bash
FILE_CONTENT=$(cat important_file.md)
ollama run llama3.2:3b "Summarize this in 3 bullet points:

$FILE_CONTENT"
```

---

## Integration with Scripts

### Heartbeat Automation

In `HEARTBEAT.md`, use Ollama for routine checks:

```bash
#!/bin/bash

# Check git status
GIT_STATUS=$(cd /workspace && git status --short)
if [ -n "$GIT_STATUS" ]; then
  SUMMARY=$(echo "$GIT_STATUS" | ollama run llama3.2:3b "Summarize: $_")
  echo "Uncommitted changes: $SUMMARY"
fi

# Check logs for errors
if [ -f logs/main.log ]; then
  ERRORS=$(tail -50 logs/main.log | grep -i error || true)
  if [ -n "$ERRORS" ]; then
    ANALYSIS=$(echo "$ERRORS" | ollama run llama3.2:3b "Is this critical? Y/N: $_")
    echo "Error status: $ANALYSIS"
  fi
fi
```

### Scheduled Tasks

```bash
#!/bin/bash
# Every morning, analyze yesterday's logs

YESTERDAY=$(date -d yesterday +%Y-%m-%d)
LOG_FILE="logs/automation-$YESTERDAY.log"

if [ -f "$LOG_FILE" ]; then
  SUMMARY=$(ollama run llama3.2:3b "Summarize this automation log (issues, stats):
  
$(cat "$LOG_FILE")")
  
  # Send summary somewhere
  echo "Yesterday's summary: $SUMMARY"
fi
```

---

## Performance & Cost

### Speed
- **First run:** ~3-5 seconds (model loads to memory)
- **Subsequent runs:** ~1-2 seconds per query
- **Streaming:** Fast enough for real-time use

### Cost Savings
- **Ollama query:** $0.00 (free)
- **Haiku query:** ~$0.001 per query (small)
- **Saving per 100 queries:** ~$0.10

**Example:** 10 daily heartbeat checks = $0.10/day saved = **$3/month in API costs**

### Resource Usage
- **CPU:** Minimal on modern systems (3B model is lightweight)
- **Memory:** ~2GB (model) + ~500MB overhead
- **Disk:** 2.3GB total for both models

---

## Troubleshooting

### Ollama Not Responding

```bash
# Check if service is running
curl -s http://localhost:11434/api/tags

# If error: start Ollama
ollama serve

# If still failing: check logs
journalctl -u ollama -n 50
```

### Model Not Available

```bash
# List available models
ollama list

# Pull a model if missing
ollama pull llama3.2:3b
```

### Response Quality Issues

- **Too short/long:** Add constraints ("in 1-2 sentences")
- **Wrong tone:** Be specific in the prompt ("analyze critically" vs "summarize")
- **Irrelevant:** 3B models have limited reasoning; give clear examples in the prompt

---

## Integration with Jarvis Automation

### Proposed Workflow (2026-03-23+)

1. **Heartbeat (every 30 min):**
   - Git status check → Ollama
   - Log file scan → Ollama
   - Quick health check → Ollama

2. **Daily Automation:**
   - Summarize yesterday's runs → Ollama
   - Flag errors/warnings → Ollama

3. **Routine Tasks:**
   - Format output → Ollama
   - Classify results → Ollama
   - Generate simple summaries → Ollama

4. **Cloud Models (when needed):**
   - Complex tasks → Codex
   - Creative work → Sonnet
   - Hard reasoning → Opus

---

## Future Upgrades

### Possible Additions
- `llama3.2:7b` or `llama2:70b` for more complex reasoning (if needed)
- `neural-chat` or `orca` for instruction following
- Quantized versions for faster inference

### When to Consider
- If Ollama tasks start failing frequently
- If you need reasoning beyond basic tasks
- If you want to reduce cloud API usage even further

---

## Cost Tracking

**Baseline (before Ollama, 2026-03-20):**
- ~30 API calls/day (mix of models)
- Estimated daily cost: ~$0.15-0.30

**With Ollama (2026-03-23+):**
- ~10 API calls/day (only complex tasks)
- ~20 Ollama queries/day (free)
- **New daily cost:** ~$0.05-0.10
- **Monthly savings:** ~$3-7/month

---

## Summary

✅ **Use Ollama for:**
- Quick checks, summaries, analysis
- Routine log/file processing
- Simple formatting & structuring

❌ **Use Cloud Models for:**
- Complex reasoning
- Code generation
- Creative or nuanced work
- Major tasks (use Codex)

**Bottom line:** Ollama handles 20% of our work for 0% cost. Keep it working!

