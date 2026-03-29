#!/usr/bin/env python3
"""
Analyze Mistake - Log and categorize mistakes with root causes and guardrails.

Usage:
    python analyze-mistake.py \
      --mistake "What went wrong" \
      --context "Task context" \
      --root-cause "Why it happened" \
      [--pattern "Pattern category"] \
      [--guardrail "How to prevent it"] \
      [--severity high|medium|low] \
      [--log-file path/to/log.md]

Example:
    python analyze-mistake.py \
      --mistake "Forgot to include URL in search results" \
      --context "Truck search results for Kolade" \
      --root-cause "Process gap: no pre-send validation check" \
      --pattern "Output detail omission" \
      --guardrail "Add URL-inclusion check before sending search results" \
      --severity high
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def load_mistakes_log(log_file):
    """Load existing mistakes log as JSON array or create new."""
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Warning: Could not read {log_file}, starting fresh")
            return []
    return []


def save_mistakes_log(log_file, mistakes):
    """Save mistakes log as JSON array."""
    # Create parent directory if needed
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
    
    with open(log_file, 'w') as f:
        json.dump(mistakes, f, indent=2)


def create_markdown_log(log_file, mistakes):
    """Create or update markdown mistakes log."""
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
    
    markdown_content = "# Mistakes Log\n\n"
    markdown_content += "_Persistent record of lessons learned and guardrails created._\n\n"
    
    # Group by date (newest first)
    by_date = {}
    for mistake in sorted(mistakes, key=lambda m: m['timestamp'], reverse=True):
        date = mistake['timestamp'].split('T')[0]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(mistake)
    
    # Format markdown
    for date in sorted(by_date.keys(), reverse=True):
        markdown_content += f"## {date}\n\n"
        
        for mistake in by_date[date]:
            # Extract time from ISO format timestamp
            time = mistake['timestamp'].split('T')[1][:5]
            title = mistake['mistake']
            
            markdown_content += f"### {time} - {title}\n"
            markdown_content += f"- **Context**: {mistake['context']}\n"
            markdown_content += f"- **Root cause**: {mistake['root_cause']}\n"
            
            if mistake.get('pattern'):
                markdown_content += f"- **Pattern**: {mistake['pattern']}\n"
            
            if mistake.get('guardrail'):
                markdown_content += f"- **Guardrail**: {mistake['guardrail']}\n"
            
            if mistake.get('severity'):
                markdown_content += f"- **Severity**: {mistake['severity']}\n"
            
            markdown_content += f"- **Status**: Logged\n\n"
    
    with open(log_file, 'w') as f:
        f.write(markdown_content)


def categorize_pattern(root_cause):
    """Suggest pattern category based on root cause."""
    root_cause_lower = root_cause.lower()
    
    patterns = {
        'output detail': 'Output detail omission',
        'missing': 'Output detail omission',
        'forgot': 'Process gap',
        'no check': 'Process gap',
        'no validation': 'Process gap',
        'no procedure': 'Process gap',
        'process gap': 'Process gap',
        'attention': 'Attention slip / Context loss',
        'lost track': 'Context loss',
        'forgot': 'Context loss',
        'long session': 'Context loss',
        'logic': 'Logic error',
        'flawed': 'Logic error',
        'misunderstand': 'Logic error',
        'assumption': 'Assumption error',
        'assumed': 'Assumption error',
        'truncat': 'Truncation/Incompleteness',
        'incomplete': 'Truncation/Incompleteness',
        'cut off': 'Truncation/Incompleteness',
    }
    
    for keyword, category in patterns.items():
        if keyword in root_cause_lower:
            return category
    
    return 'Unclassified'


def main():
    parser = argparse.ArgumentParser(
        description='Log and analyze a mistake with root cause and guardrail.'
    )
    parser.add_argument('--mistake', required=True, help='What went wrong (required)')
    parser.add_argument('--context', required=True, help='Task context (required)')
    parser.add_argument('--root-cause', required=True, help='Why it happened (required)')
    parser.add_argument('--pattern', default=None, help='Pattern category (auto-detected if not provided)')
    parser.add_argument('--guardrail', default=None, help='How to prevent it')
    parser.add_argument('--severity', choices=['high', 'medium', 'low'], default='medium',
                       help='Severity level (default: medium)')
    parser.add_argument('--log-file', default='mistakes-log.json',
                       help='Path to mistakes log file (default: mistakes-log.json)')
    parser.add_argument('--markdown', default=None,
                       help='Also save as markdown to this file')
    parser.add_argument('--json-only', action='store_true',
                       help='Only save JSON, do not create markdown')
    
    args = parser.parse_args()
    
    # Auto-detect pattern if not provided
    pattern = args.pattern or categorize_pattern(args.root_cause)
    
    # Create mistake entry
    mistake_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'mistake': args.mistake,
        'context': args.context,
        'root_cause': args.root_cause,
        'pattern': pattern,
        'guardrail': args.guardrail or None,
        'severity': args.severity,
    }
    
    # Load existing log
    mistakes = load_mistakes_log(args.log_file)
    mistakes.append(mistake_entry)
    
    # Save JSON log
    save_mistakes_log(args.log_file, mistakes)
    print(f"✓ Logged to: {args.log_file}")
    
    # Optionally create markdown version
    markdown_path = args.markdown
    if not args.json_only:
        if not markdown_path:
            # Default markdown path is same as JSON but with .md extension
            markdown_path = args.log_file.replace('.json', '.md')
        
        if markdown_path:
            create_markdown_log(markdown_path, mistakes)
            print(f"✓ Markdown log: {markdown_path}")
    
    # Print summary
    print(f"\nMistake Summary:")
    print(f"  What: {args.mistake}")
    print(f"  When: {args.context}")
    print(f"  Why: {args.root_cause}")
    print(f"  Pattern: {pattern}")
    if args.guardrail:
        print(f"  Guardrail: {args.guardrail}")
    print(f"  Severity: {args.severity}")
    
    # Suggest reference materials
    print(f"\nNext steps:")
    print(f"  1. Review references/mistake-patterns.md for '{pattern}' pattern")
    print(f"  2. Review references/guardrails.md for relevant checklists")
    print(f"  3. Create or update a guardrail in references/guardrails.md")
    print(f"  4. Add the guardrail to your workflow for future prevention")
    
    return 0


if __name__ == '__main__':
    exit(main())
