#!/usr/bin/env python3
"""
Wikipedia Policy Citation Analyzer
Analyzes frequency of AI-related policy citations vs all policy citations in 2025
"""

import requests
import time
import json
import re
from datetime import datetime
from collections import Counter, defaultdict

# Wikipedia API endpoint
API_URL = "https://en.wikipedia.org/w/api.php"

# Headers for API requests
HEADERS = {
    'User-Agent': 'WikipediaPolicyAnalyzer/1.0 (Educational Research; Python/requests)'
}

# AI-related policy patterns
AI_POLICY_PATTERNS = [
    r'WP:NOTAI',
    r'WP:AI',
    r'Wikipedia:AI',
    r'Wikipedia:AI[-_]generated',
    r'WP:CHATGPT',
    r'WP:LLM',
    r'WP:BOTS?(?:\b|[^A-Z])',  # WP:BOT or WP:BOTS (but not BOTTOM, etc.)
    r'MOS:AI',
]

# Pattern to match any Wikipedia policy citation
POLICY_PATTERN = r'(?:WP|Wikipedia|MOS):[A-Z][A-Z0-9]*(?:[-_][A-Z0-9]+)*'

def search_edit_summaries_2025(limit_per_batch=500, max_batches=20):
    """
    Search recent changes from 2025 for edit summaries containing policy citations
    """
    print(f"\n{'='*60}")
    print("SEARCHING 2025 EDIT SUMMARIES FOR POLICY CITATIONS")
    print(f"{'='*60}\n")

    all_policies = Counter()
    ai_policies = Counter()
    total_edits_checked = 0
    edits_with_policies = 0

    # Start from November 4, 2025 and go back to January 1, 2025
    params = {
        'action': 'query',
        'list': 'recentchanges',
        'rcstart': '2025-11-04T23:59:59Z',
        'rcend': '2025-01-01T00:00:00Z',
        'rcprop': 'comment|timestamp|title',
        'rclimit': limit_per_batch,
        'format': 'json',
        'rcnamespace': 0,  # Main namespace (articles)
    }

    batch_num = 0

    while batch_num < max_batches:
        batch_num += 1
        print(f"Batch {batch_num}/{max_batches}...", end=" ", flush=True)

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            response.raise_for_status()
            data = response.json()

            changes = data.get('query', {}).get('recentchanges', [])

            if not changes:
                print("No more changes found.")
                break

            # Process this batch
            for change in changes:
                total_edits_checked += 1
                comment = change.get('comment', '')

                if not comment:
                    continue

                # Find all policy citations in this edit summary
                policies_in_comment = re.findall(POLICY_PATTERN, comment, re.IGNORECASE)

                if policies_in_comment:
                    edits_with_policies += 1

                    for policy in policies_in_comment:
                        # Normalize policy name
                        policy_normalized = policy.upper()
                        all_policies[policy_normalized] += 1

                        # Check if it's AI-related
                        for ai_pattern in AI_POLICY_PATTERNS:
                            if re.search(ai_pattern, policy, re.IGNORECASE):
                                ai_policies[policy_normalized] += 1
                                break

            print(f"Found {len(changes)} edits. Total policies: {sum(all_policies.values())}, AI policies: {sum(ai_policies.values())}")

            # Check for continuation
            if 'continue' not in data:
                print("No more data to fetch.")
                break

            params['rccontinue'] = data['continue']['rccontinue']
            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"\nError in batch {batch_num}: {e}")
            break

    return {
        'all_policies': all_policies,
        'ai_policies': ai_policies,
        'total_edits_checked': total_edits_checked,
        'edits_with_policies': edits_with_policies,
        'batches_processed': batch_num
    }

def print_results(results):
    """Print analysis results"""
    print(f"\n{'='*60}")
    print("ANALYSIS RESULTS")
    print(f"{'='*60}\n")

    total_edits = results['total_edits_checked']
    edits_with_policies = results['edits_with_policies']
    all_policies = results['all_policies']
    ai_policies = results['ai_policies']

    total_policy_citations = sum(all_policies.values())
    total_ai_citations = sum(ai_policies.values())

    print(f"Total 2025 edits checked: {total_edits:,}")

    if total_edits > 0:
        print(f"Edits with policy citations: {edits_with_policies:,} ({edits_with_policies/total_edits*100:.2f}%)")
    else:
        print(f"Edits with policy citations: {edits_with_policies:,}")
        print("\nWARNING: No edits were retrieved. Check API access.")
        return

    print(f"\nTotal policy citations found: {total_policy_citations:,}")
    print(f"AI-related policy citations: {total_ai_citations:,}")

    if total_policy_citations > 0:
        ai_percentage = (total_ai_citations / total_policy_citations) * 100
        print(f"\n{'*'*60}")
        print(f"AI POLICY RATIO: {ai_percentage:.3f}%")
        print(f"({total_ai_citations} AI citations out of {total_policy_citations:,} total)")
        print(f"{'*'*60}")

    # Top 20 most cited policies overall
    print(f"\n{'='*60}")
    print("TOP 20 MOST CITED POLICIES (2025)")
    print(f"{'='*60}\n")

    for i, (policy, count) in enumerate(all_policies.most_common(20), 1):
        is_ai = policy in ai_policies
        ai_marker = " [AI-RELATED]" if is_ai else ""
        percentage = (count / total_policy_citations) * 100
        print(f"{i:2}. {policy:30} : {count:5,} citations ({percentage:5.2f}%){ai_marker}")

    # AI-related policies breakdown
    if ai_policies:
        print(f"\n{'='*60}")
        print("AI-RELATED POLICY CITATIONS")
        print(f"{'='*60}\n")

        for policy, count in ai_policies.most_common():
            percentage = (count / total_policy_citations) * 100
            ai_pct = (count / total_ai_citations) * 100
            print(f"{policy:30} : {count:5,} citations ({percentage:5.2f}% of all, {ai_pct:5.1f}% of AI)")
    else:
        print(f"\n{'='*60}")
        print("NO AI-RELATED POLICY CITATIONS FOUND")
        print(f"{'='*60}\n")
        print("This could mean:")
        print("1. AI policies are very rarely cited in edit summaries")
        print("2. AI enforcement happens without explicit policy citation")
        print("3. Our AI policy patterns need refinement")

    # Statistics
    print(f"\n{'='*60}")
    print("STATISTICS")
    print(f"{'='*60}\n")
    print(f"Unique policies cited: {len(all_policies)}")
    print(f"Unique AI policies cited: {len(ai_policies)}")
    print(f"Average citations per policy: {total_policy_citations/len(all_policies):.2f}")
    print(f"Batches processed: {results['batches_processed']}")

def main():
    print("\n" + "="*60)
    print("Wikipedia Policy Citation Frequency Analysis")
    print("Period: January 1 - November 4, 2025")
    print("="*60)

    # Search for policy citations in 2025
    results = search_edit_summaries_2025(limit_per_batch=500, max_batches=20)

    # Print results
    print_results(results)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"wikipedia_policy_citations_2025_{timestamp}.json"

    # Convert Counter objects to dicts for JSON serialization
    results_serializable = {
        'all_policies': dict(results['all_policies']),
        'ai_policies': dict(results['ai_policies']),
        'total_edits_checked': results['total_edits_checked'],
        'edits_with_policies': results['edits_with_policies'],
        'batches_processed': results['batches_processed'],
        'analysis_date': timestamp,
        'period': '2025-01-01 to 2025-11-04'
    }

    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
