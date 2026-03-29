#!/usr/bin/env python3
"""
Validate Checklist - Verify outputs against pre-defined guardrail checklists.

Usage:
    python validate-checklist.py \
      --checklist-name "Search Results" \
      --items "Title, URL, Snippet" \
      --content "output.txt or direct text"

This script helps verify that output meets the checklist requirements before
sending it to the user.

Supported checklists (from references/guardrails.md):
  - search-results: Verify search result structure
  - code-sample: Verify code completeness
  - list-table: Verify list/table structure
  - aggregation: Verify aggregated data completeness
  - document: Verify document structure
"""

import argparse
import re
from pathlib import Path


# Checklist definitions (maps to guardrails.md)
CHECKLISTS = {
    'search-results': {
        'description': 'Search results validation',
        'required_checks': [
            'count_verification',
            'url_present',
            'url_complete',
            'title_present',
            'snippet_present',
            'no_duplicates',
        ],
        'questions': [
            'Do you have the requested number of results?',
            'Does each result have a URL?',
            'Are URLs complete (not truncated)?',
            'Does each result have a title?',
            'Does each result have a snippet/description?',
            'Are there any duplicate results?',
        ]
    },
    'code-sample': {
        'description': 'Code completeness validation',
        'required_checks': [
            'imports_present',
            'function_complete',
            'syntax_valid',
            'example_provided',
        ],
        'questions': [
            'Are all required imports present?',
            'Is the function complete (not pseudocode)?',
            'Is the syntax valid (balanced brackets, quotes)?',
            'Is there a usage example?',
        ]
    },
    'list-table': {
        'description': 'List/table structure validation',
        'required_checks': [
            'count_correct',
            'format_consistent',
            'no_duplicates',
            'no_truncation',
        ],
        'questions': [
            'Do you have the correct number of items?',
            'Is the format consistent across all items?',
            'Are there any duplicate items?',
            'Are any items truncated or cut off?',
        ]
    },
    'aggregation': {
        'description': 'Aggregation completeness validation',
        'required_checks': [
            'all_sources_checked',
            'no_duplicates',
            'count_verified',
        ],
        'questions': [
            'Did you check all promised sources?',
            'Are there any duplicate items?',
            'Does the total count match your verification?',
        ]
    },
    'document': {
        'description': 'Document structure validation',
        'required_checks': [
            'title_present',
            'intro_present',
            'sections_complete',
            'examples_provided',
        ],
        'questions': [
            'Is there a clear title/heading?',
            'Is there an introduction explaining what this is?',
            'Are all promised sections present?',
            'Are there concrete examples?',
        ]
    },
}


def run_interactive_checklist(checklist_name):
    """Run an interactive checklist validation."""
    if checklist_name not in CHECKLISTS:
        print(f"Error: Unknown checklist '{checklist_name}'")
        print(f"Available checklists: {', '.join(CHECKLISTS.keys())}")
        return False
    
    checklist = CHECKLISTS[checklist_name]
    print(f"\n{'='*60}")
    print(f"Checklist: {checklist['description'].upper()}")
    print(f"{'='*60}\n")
    
    passed = 0
    failed = 0
    
    for i, question in enumerate(checklist['questions'], 1):
        print(f"{i}. {question}")
        response = input("   Answer (yes/no/skip): ").strip().lower()
        
        if response == 'skip':
            print("   ⊘ Skipped\n")
            continue
        elif response in ('yes', 'y'):
            print("   ✓ Passed\n")
            passed += 1
        elif response in ('no', 'n'):
            print("   ✗ FAILED\n")
            failed += 1
        else:
            print("   ? Please answer 'yes', 'no', or 'skip'\n")
    
    # Summary
    total = passed + failed
    print(f"{'='*60}")
    print(f"Results: {passed}/{total} checks passed")
    
    if failed == 0 and total > 0:
        print("✓ All checks passed! Output is ready to send.")
        return True
    elif failed > 0:
        print(f"✗ {failed} check(s) failed. Review and fix before sending.")
        return False
    else:
        print("⊘ No checks completed. Aborting.")
        return False


def validate_from_content(checklist_name, content):
    """Validate output against checklist based on content analysis."""
    if checklist_name not in CHECKLISTS:
        print(f"Error: Unknown checklist '{checklist_name}'")
        return False
    
    checklist = CHECKLISTS[checklist_name]
    print(f"\nValidating: {checklist['description']}")
    
    results = {}
    
    # Basic heuristic validation
    if checklist_name == 'search-results':
        # Check for URL patterns
        urls = re.findall(r'https?://\S+', content)
        results['urls_found'] = len(urls) > 0
        
        # Check for line breaks (indicates multiple results)
        lines = content.strip().split('\n')
        results['multiple_results'] = len(lines) > 3
        
        print(f"  URLs found: {results['urls_found']}")
        print(f"  Multiple results: {results['multiple_results']}")
    
    elif checklist_name == 'code-sample':
        # Check for import statements
        has_imports = 'import ' in content or 'from ' in content
        results['imports'] = has_imports
        
        # Check for function definition
        has_function = 'def ' in content or 'function ' in content
        results['function'] = has_function
        
        # Check for balanced brackets
        balanced = content.count('{') == content.count('}')
        results['balanced'] = balanced
        
        print(f"  Imports found: {results['imports']}")
        print(f"  Function definition: {results['function']}")
        print(f"  Balanced brackets: {results['balanced']}")
    
    elif checklist_name == 'list-table':
        # Count items (heuristic: newlines or dashes)
        items = [l for l in content.split('\n') if l.strip()]
        results['item_count'] = len(items)
        
        # Check for duplicates
        seen = set()
        has_dupes = False
        for item in items:
            if item in seen:
                has_dupes = True
                break
            seen.add(item)
        results['duplicates'] = has_dupes
        
        print(f"  Items found: {results['item_count']}")
        print(f"  Duplicates detected: {results['duplicates']}")
    
    # Print summary
    print(f"\n{'='*60}")
    if all(results.values()):
        print("✓ All automated checks passed.")
        print("\nNote: Some checks still require manual verification.")
        print("Run with --interactive for full checklist.")
        return True
    else:
        print("✗ Some checks failed or inconclusive.")
        print("Recommendations:")
        for check, passed in results.items():
            if not passed:
                print(f"  - Review: {check}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate output against guardrail checklists before sending.'
    )
    
    parser.add_argument('--checklist', required=True,
                       choices=list(CHECKLISTS.keys()),
                       help='Checklist type to validate against')
    parser.add_argument('--interactive', action='store_true',
                       help='Run interactive validation (ask questions)')
    parser.add_argument('--file', help='File to validate')
    parser.add_argument('--content', help='Direct content to validate')
    
    args = parser.parse_args()
    
    # Validate has content
    if not args.interactive and not args.file and not args.content:
        print("Error: Provide --content, --file, or use --interactive")
        return 1
    
    if args.interactive:
        success = run_interactive_checklist(args.checklist)
    else:
        # Load content
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"Error: File not found: {args.file}")
                return 1
        else:
            content = args.content
        
        success = validate_from_content(args.checklist, content)
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
