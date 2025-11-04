#!/usr/bin/env python3
"""
Wikipedia AI Talk Discussion Analyzer
Analyzes AI-related discussions in various Wikipedia discussion spaces
"""

import requests
import time
import json
import re
from datetime import datetime
from collections import Counter, defaultdict

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {'User-Agent': 'WikipediaAIResearch/1.0 (Educational Research)'}

# AI-related keywords for discussion search
AI_KEYWORDS = [
    'AI-generated',
    'ChatGPT',
    'GPT',
    'language model',
    'LLM',
    'artificial intelligence',
    'bot-written',
    'machine-generated',
    'automated content',
    'AI writing',
    'suspected AI',
    'looks like AI',
    'sounds like AI'
]

def search_village_pump_policy(start_date='2023-01-01', max_results=50):
    """Search Village Pump (Policy) for AI discussions"""
    print(f"\n{'='*60}")
    print("SEARCHING VILLAGE PUMP (POLICY) FOR AI DISCUSSIONS")
    print(f"{'='*60}\n")

    discussions = []

    for keyword in AI_KEYWORDS[:5]:  # Sample key terms
        print(f"Searching for: '{keyword}'...", end=" ", flush=True)

        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': f'"{keyword}"',
            'srnamespace': 4,  # Wikipedia namespace
            'srtitle': 'Wikipedia:Village pump (policy)',
            'format': 'json',
            'srlimit': 10,
            'srwhat': 'text'
        }

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            data = response.json()

            results = data.get('query', {}).get('search', [])
            print(f"Found {len(results)} results")

            for result in results:
                discussions.append({
                    'title': result['title'],
                    'snippet': result['snippet'],
                    'keyword': keyword,
                    'timestamp': result.get('timestamp', ''),
                    'wordcount': result.get('wordcount', 0)
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")

    return discussions

def search_wikiproject_ai_cleanup_talk(max_results=50):
    """Search WikiProject AI Cleanup talk pages"""
    print(f"\n{'='*60}")
    print("SEARCHING WIKIPROJECT AI CLEANUP TALK PAGES")
    print(f"{'='*60}\n")

    discussions = []

    pages_to_search = [
        'Wikipedia talk:WikiProject AI Cleanup',
        'Wikipedia:WikiProject AI Cleanup/Guide',
        'Wikipedia:WikiProject AI Cleanup/Policies'
    ]

    for page in pages_to_search:
        print(f"Analyzing: {page}...", end=" ", flush=True)

        params = {
            'action': 'parse',
            'page': page,
            'format': 'json',
            'prop': 'sections'
        }

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            data = response.json()

            if 'parse' in data:
                sections = data['parse'].get('sections', [])
                print(f"Found {len(sections)} sections")

                for section in sections:
                    discussions.append({
                        'page': page,
                        'section': section['line'],
                        'level': section['level'],
                        'index': section['index']
                    })
            else:
                print("Not found or error")

            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")

    return discussions

def search_ai_generated_content_talk():
    """Get discussions from Wikipedia:AI-generated content talk page"""
    print(f"\n{'='*60}")
    print("SEARCHING AI-GENERATED CONTENT POLICY TALK PAGE")
    print(f"{'='*60}\n")

    page = 'Wikipedia talk:AI-generated content'

    params = {
        'action': 'parse',
        'page': page,
        'format': 'json',
        'prop': 'sections|wikitext'
    }

    try:
        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        if 'parse' in data:
            sections = data['parse'].get('sections', [])
            wikitext = data['parse'].get('wikitext', {}).get('*', '')

            print(f"Found {len(sections)} discussion sections")
            print(f"Total text length: {len(wikitext):,} characters\n")

            discussions = []
            for section in sections:
                discussions.append({
                    'title': section['line'],
                    'level': section['level'],
                    'index': section['index']
                })

            return discussions, wikitext
        else:
            print("Page not found or error")
            return [], ""

    except Exception as e:
        print(f"Error: {e}")
        return [], ""

def search_afd_ai_discussions(limit=30):
    """Search Articles for Deletion discussions mentioning AI"""
    print(f"\n{'='*60}")
    print("SEARCHING ARTICLES FOR DELETION (AfD) FOR AI MENTIONS")
    print(f"{'='*60}\n")

    discussions = []

    keywords = ['AI-generated', 'ChatGPT', 'GPT', 'language model', 'suspected AI']

    for keyword in keywords:
        print(f"Searching AfD for: '{keyword}'...", end=" ", flush=True)

        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': f'"{keyword}" prefix:Wikipedia:Articles for deletion/',
            'srnamespace': 4,  # Wikipedia namespace
            'format': 'json',
            'srlimit': 10,
            'srwhat': 'text'
        }

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            data = response.json()

            results = data.get('query', {}).get('search', [])
            print(f"Found {len(results)} results")

            for result in results:
                discussions.append({
                    'title': result['title'],
                    'snippet': result['snippet'],
                    'keyword': keyword,
                    'timestamp': result.get('timestamp', ''),
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")

    return discussions

def analyze_discussion_content(discussions):
    """Analyze the content of discussions"""
    print(f"\n{'='*60}")
    print("DISCUSSION ANALYSIS")
    print(f"{'='*60}\n")

    # Keyword frequency
    keyword_counts = Counter()
    for disc in discussions:
        keyword_counts[disc.get('keyword', 'N/A')] += 1

    print("Discussions by keyword:")
    for keyword, count in keyword_counts.most_common():
        print(f"  {keyword}: {count}")

    return keyword_counts

def main():
    print("\n" + "="*60)
    print("Wikipedia AI Talk Discussion Analysis")
    print("Focus: Discussion spaces (not edit summaries)")
    print("="*60)

    results = {
        'village_pump': [],
        'wikiproject_talk': [],
        'ai_policy_talk': [],
        'afd_discussions': []
    }

    # 1. Village Pump (Policy)
    results['village_pump'] = search_village_pump_policy()

    # 2. WikiProject AI Cleanup talk pages
    results['wikiproject_talk'] = search_wikiproject_ai_cleanup_talk()

    # 3. AI-generated content policy talk
    ai_discussions, ai_wikitext = search_ai_generated_content_talk()
    results['ai_policy_talk'] = ai_discussions
    results['ai_policy_wikitext'] = ai_wikitext

    # 4. Articles for Deletion
    results['afd_discussions'] = search_afd_ai_discussions()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}\n")

    print(f"Village Pump discussions: {len(results['village_pump'])}")
    print(f"WikiProject AI Cleanup sections: {len(results['wikiproject_talk'])}")
    print(f"AI policy talk sections: {len(results['ai_policy_talk'])}")
    print(f"AfD discussions with AI mentions: {len(results['afd_discussions'])}")

    total = (len(results['village_pump']) +
             len(results['wikiproject_talk']) +
             len(results['ai_policy_talk']) +
             len(results['afd_discussions']))

    print(f"\nTotal discussion spaces found: {total}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"wikipedia_ai_talk_discussions_{timestamp}.json"

    # Make serializable
    results_serializable = {
        'village_pump': results['village_pump'],
        'wikiproject_talk': results['wikiproject_talk'],
        'ai_policy_talk': results['ai_policy_talk'],
        'afd_discussions': results['afd_discussions'],
        'ai_policy_wikitext_length': len(results.get('ai_policy_wikitext', '')),
        'analysis_date': timestamp,
        'total_discussions': total
    }

    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    # Print sample Village Pump discussions
    if results['village_pump']:
        print(f"\n{'='*60}")
        print("SAMPLE VILLAGE PUMP DISCUSSIONS")
        print(f"{'='*60}\n")

        for disc in results['village_pump'][:5]:
            print(f"Title: {disc['title']}")
            print(f"Keyword: {disc['keyword']}")
            print(f"Snippet: {disc['snippet'][:200]}...")
            print()

    # Print AI policy talk sections
    if results['ai_policy_talk']:
        print(f"\n{'='*60}")
        print("AI POLICY TALK PAGE SECTIONS")
        print(f"{'='*60}\n")

        for disc in results['ai_policy_talk'][:10]:
            print(f"{'  ' * (int(disc['level']) - 1)}{disc['title']}")

    # Print sample AfD discussions
    if results['afd_discussions']:
        print(f"\n{'='*60}")
        print("SAMPLE AFD DISCUSSIONS WITH AI MENTIONS")
        print(f"{'='*60}\n")

        for disc in results['afd_discussions'][:5]:
            print(f"Article: {disc['title'].replace('Wikipedia:Articles for deletion/', '')}")
            print(f"Keyword: {disc['keyword']}")
            print(f"Snippet: {disc['snippet'][:200]}...")
            print()

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
