#!/usr/bin/env python3
"""
Wikipedia AfD AI Detection Pattern Analyzer
Deep analysis of Articles for Deletion discussions about AI-generated content
"""

import requests
import time
import json
import re
from datetime import datetime
from collections import Counter, defaultdict

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {'User-Agent': 'WikipediaAIResearch/1.0 (Educational Research)'}

def get_afd_discussions_ai(limit=50):
    """Get AfD discussions mentioning AI"""
    print(f"\n{'='*60}")
    print("FETCHING AFD DISCUSSIONS WITH AI MENTIONS")
    print(f"{'='*60}\n")

    all_discussions = []
    keywords = ['AI-generated', 'ChatGPT', 'GPT', 'language model', 'suspected AI', 'looks like AI', 'AI writing']

    seen_titles = set()

    for keyword in keywords:
        print(f"Searching for: '{keyword}'...", end=" ", flush=True)

        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': f'"{keyword}" prefix:Wikipedia:Articles for deletion/',
            'srnamespace': 4,
            'format': 'json',
            'srlimit': 20,
            'srwhat': 'text'
        }

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            data = response.json()

            results = data.get('query', {}).get('search', [])
            new_results = 0

            for result in results:
                if result['title'] not in seen_titles:
                    seen_titles.add(result['title'])
                    all_discussions.append({
                        'title': result['title'],
                        'snippet': result['snippet'],
                        'keyword': keyword,
                        'timestamp': result.get('timestamp', ''),
                        'wordcount': result.get('wordcount', 0)
                    })
                    new_results += 1

            print(f"Found {len(results)} results ({new_results} new)")
            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")

    print(f"\nTotal unique AfD discussions: {len(all_discussions)}")
    return all_discussions

def fetch_afd_full_text(afd_title):
    """Fetch the full text of an AfD discussion"""
    params = {
        'action': 'parse',
        'page': afd_title,
        'format': 'json',
        'prop': 'wikitext'
    }

    try:
        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        if 'parse' in data:
            return data['parse']['wikitext']['*']
        else:
            return None

    except Exception as e:
        print(f"Error fetching {afd_title}: {e}")
        return None

def analyze_afd_text(text, article_name):
    """Analyze an AfD discussion for AI detection patterns"""

    if not text:
        return None

    analysis = {
        'article': article_name,
        'text_length': len(text),
        'detection_indicators': [],
        'tools_mentioned': [],
        'outcomes': [],
        'arguments': [],
        'voters': [],
        'policies_cited': []
    }

    # Detection indicators
    indicators = [
        'AI-generated', 'ChatGPT', 'GPT', 'language model', 'LLM',
        'sounds like AI', 'looks like AI', 'reads like AI',
        'AI slop', 'AI writing', 'AI-written', 'machine-generated',
        'bot-written', 'automated', 'hallucinated', 'hallucination',
        'word salad', 'generic', 'non-human', 'robotic'
    ]

    for indicator in indicators:
        if re.search(indicator, text, re.IGNORECASE):
            # Find context around the indicator
            pattern = re.compile(f'.{{0,100}}{re.escape(indicator)}.{{0,100}}', re.IGNORECASE | re.DOTALL)
            matches = pattern.findall(text)
            if matches:
                analysis['detection_indicators'].append({
                    'indicator': indicator,
                    'count': len(matches),
                    'examples': [m.replace('\n', ' ')[:200] for m in matches[:2]]
                })

    # Detection tools
    tools = ['GPTZero', 'AI detector', 'detection tool', 'AI checker']
    for tool in tools:
        if re.search(tool, text, re.IGNORECASE):
            analysis['tools_mentioned'].append(tool)

    # Outcomes
    outcomes = [
        'delete', 'keep', 'redirect', 'merge', 'withdrawn',
        'closed', 'speedily deleted', 'no consensus'
    ]

    # Look for "The result was" which indicates closure
    result_match = re.search(r"The result was '''([^']+)'''", text, re.IGNORECASE)
    if result_match:
        analysis['outcomes'].append({
            'type': 'formal_result',
            'decision': result_match.group(1)
        })

    # Policy citations
    policies = re.findall(r'\[\[WP:([A-Z]+)\]\]', text)
    policies += re.findall(r'\[\[Wikipedia:([A-Za-z\s]+)\]\]', text)
    if policies:
        analysis['policies_cited'] = list(set(policies))[:10]  # Top 10 unique

    # Arguments (look for bullet points with Delete/Keep)
    votes = re.findall(r"^\*\s*'''(Delete|Keep|Redirect|Merge)'''(.{0,300})", text, re.MULTILINE | re.IGNORECASE)
    analysis['voters'] = len(votes)

    if votes:
        for vote_type, reasoning in votes[:5]:  # First 5 votes
            reasoning_clean = reasoning.replace('\n', ' ').strip()
            if 'AI' in reasoning_clean or 'GPT' in reasoning_clean:
                analysis['arguments'].append({
                    'vote': vote_type,
                    'reasoning': reasoning_clean[:200]
                })

    return analysis

def categorize_detection_patterns(all_analyses):
    """Categorize how editors detect AI content"""
    print(f"\n{'='*60}")
    print("AI DETECTION PATTERN ANALYSIS")
    print(f"{'='*60}\n")

    # Detection indicator frequency
    all_indicators = defaultdict(int)
    all_tools = Counter()
    all_outcomes = []
    all_policies = Counter()

    for analysis in all_analyses:
        if not analysis:
            continue

        for indicator in analysis['detection_indicators']:
            all_indicators[indicator['indicator'].lower()] += indicator['count']

        for tool in analysis['tools_mentioned']:
            all_tools[tool.lower()] += 1

        for outcome in analysis['outcomes']:
            all_outcomes.append(outcome['decision'])

        for policy in analysis['policies_cited']:
            all_policies[policy] += 1

    # Print top indicators
    print("TOP AI DETECTION INDICATORS:")
    print("-" * 60)
    sorted_indicators = sorted(all_indicators.items(), key=lambda x: x[1], reverse=True)
    for i, (indicator, count) in enumerate(sorted_indicators[:15], 1):
        print(f"{i:2}. {indicator:30} : {count:3} mentions")

    # Print tools used
    print(f"\n{'='*60}")
    print("AI DETECTION TOOLS MENTIONED:")
    print("-" * 60)
    if all_tools:
        for tool, count in all_tools.most_common():
            print(f"  {tool:30} : {count} times")
    else:
        print("  No detection tools explicitly mentioned")

    # Print outcomes
    print(f"\n{'='*60}")
    print("DISCUSSION OUTCOMES:")
    print("-" * 60)
    outcome_counts = Counter(all_outcomes)
    for outcome, count in outcome_counts.most_common():
        print(f"  {outcome:30} : {count} cases")

    # Print policies
    print(f"\n{'='*60}")
    print("MOST CITED POLICIES IN AI AfD DISCUSSIONS:")
    print("-" * 60)
    if all_policies:
        for policy, count in all_policies.most_common(15):
            print(f"  {policy:30} : {count} citations")
    else:
        print("  No policies explicitly cited")

    return {
        'indicators': dict(sorted_indicators),
        'tools': dict(all_tools),
        'outcomes': dict(outcome_counts),
        'policies': dict(all_policies)
    }

def extract_detection_arguments(all_analyses):
    """Extract specific arguments editors make about AI detection"""
    print(f"\n{'='*60}")
    print("SAMPLE AI DETECTION ARGUMENTS")
    print(f"{'='*60}\n")

    delete_args = []
    keep_args = []

    for analysis in all_analyses:
        if not analysis or not analysis.get('arguments'):
            continue

        for arg in analysis['arguments']:
            if arg['vote'].lower() == 'delete':
                delete_args.append({
                    'article': analysis['article'],
                    'reasoning': arg['reasoning']
                })
            elif arg['vote'].lower() == 'keep':
                keep_args.append({
                    'article': analysis['article'],
                    'reasoning': arg['reasoning']
                })

    print("DELETE ARGUMENTS (mentioning AI):")
    print("-" * 60)
    for i, arg in enumerate(delete_args[:10], 1):
        print(f"{i}. Article: {arg['article']}")
        print(f"   Argument: {arg['reasoning']}")
        print()

    if keep_args:
        print(f"\n{'='*60}")
        print("KEEP ARGUMENTS (mentioning AI):")
        print("-" * 60)
        for i, arg in enumerate(keep_args[:5], 1):
            print(f"{i}. Article: {arg['article']}")
            print(f"   Argument: {arg['reasoning']}")
            print()

    return {'delete': delete_args, 'keep': keep_args}

def main():
    print("\n" + "="*60)
    print("Wikipedia AfD AI Detection Pattern Analysis")
    print("Deep dive into how editors identify AI-generated content")
    print("="*60)

    # Get AfD discussions
    afd_list = get_afd_discussions_ai(limit=50)

    # Analyze top discussions (limit to avoid too many API calls)
    print(f"\n{'='*60}")
    print(f"ANALYZING TOP {min(30, len(afd_list))} AFD DISCUSSIONS")
    print(f"{'='*60}\n")

    all_analyses = []

    for i, afd in enumerate(afd_list[:30], 1):
        article_name = afd['title'].replace('Wikipedia:Articles for deletion/', '')
        print(f"{i:2}. Analyzing: {article_name[:50]:50}...", end=" ", flush=True)

        text = fetch_afd_full_text(afd['title'])

        if text:
            analysis = analyze_afd_text(text, article_name)
            all_analyses.append(analysis)

            indicators = len(analysis['detection_indicators']) if analysis else 0
            print(f"✓ ({indicators} AI indicators)")
        else:
            print("✗ (not found)")
            all_analyses.append(None)

        time.sleep(0.5)  # Rate limiting

    # Categorize patterns
    patterns = categorize_detection_patterns(all_analyses)

    # Extract arguments
    arguments = extract_detection_arguments(all_analyses)

    # Statistics
    print(f"\n{'='*60}")
    print("STATISTICS")
    print(f"{'='*60}\n")

    valid_analyses = [a for a in all_analyses if a]
    total_indicators = sum(len(a['detection_indicators']) for a in valid_analyses)
    total_tools = sum(len(a['tools_mentioned']) for a in valid_analyses)
    total_policies = sum(len(a['policies_cited']) for a in valid_analyses)
    total_voters = sum(a['voters'] for a in valid_analyses)

    print(f"AfD discussions analyzed: {len(valid_analyses)}")
    print(f"Total AI detection indicators: {total_indicators}")
    print(f"Discussions mentioning detection tools: {total_tools}")
    print(f"Total policy citations: {total_policies}")
    print(f"Total voters (Delete/Keep): {total_voters}")
    print(f"Average voters per discussion: {total_voters/len(valid_analyses):.1f}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"wikipedia_afd_ai_patterns_{timestamp}.json"

    results = {
        'afd_discussions': afd_list,
        'analyses': [a for a in all_analyses if a],
        'patterns': patterns,
        'arguments': arguments,
        'statistics': {
            'total_analyzed': len(valid_analyses),
            'total_indicators': total_indicators,
            'total_tools': total_tools,
            'total_policies': total_policies,
            'total_voters': total_voters
        },
        'analysis_date': timestamp
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
