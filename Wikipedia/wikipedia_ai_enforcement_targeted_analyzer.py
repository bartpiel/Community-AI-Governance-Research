#!/usr/bin/env python3
"""
Wikipedia AI Enforcement Analyzer - Targeted Approach

Instead of random sampling, this script SEARCHES for articles that have
AI-related enforcement activity in their edit history, then analyzes them
in detail.

Approach: Search edit summaries for AI-related phrases, then analyze those
articles' complete edit history and talk pages.
"""

import requests
import json
import time
from datetime import datetime
import re
import csv
from collections import defaultdict

class TargetedAIEnforcementAnalyzer:
    """Analyzer that finds and analyzes articles with AI enforcement activity"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia AI Enforcement Research Tool (Educational Research)'
        })

        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.request_delay = 1

        # Specific AI enforcement phrases
        self.enforcement_phrases = [
            'AI-generated',
            'AI generated',
            'ChatGPT',
            'GPT-3',
            'GPT-4',
            'suspected AI',
            'suspected automation',
            'WP:NOTAI',
            'machine-generated',
            'bot-generated content',
            'automated content',
            'language model'
        ]

        # Start date for analysis
        self.start_date = datetime(2023, 1, 1)

        self.articles_found = []
        self.edit_data = []
        self.talk_data = []

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def search_for_ai_enforcement_edits(self, phrase, limit=50):
        """Search for edits containing specific AI-related phrases"""
        self.log(f"Searching for edits with phrase: '{phrase}'")

        edits_found = []

        try:
            # Use search API to find edit summaries
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': f'insource:/{phrase}/',
                'srnamespace': 0,  # Main namespace
                'srlimit': limit,
                'srwhat': 'text'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'search' in data['query']:
                for result in data['query']['search']:
                    article_title = result['title']

                    # Check if we already have this article
                    if not any(a['title'] == article_title for a in self.articles_found):
                        self.articles_found.append({
                            'title': article_title,
                            'search_phrase': phrase
                        })
                        edits_found.append(article_title)

            self.log(f"  Found {len(edits_found)} new articles")
            return edits_found

        except Exception as e:
            self.log(f"  Error searching: {e}")
            return []

    def search_recent_changes_for_ai(self, limit=100):
        """Search recent changes for AI-related edit summaries"""
        self.log("Searching recent changes for AI-related edits...")

        found_articles = set()

        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'recentchanges',
                'rcnamespace': 0,
                'rclimit': limit,
                'rcprop': 'title|comment|timestamp|user|ids',
                'rcstart': datetime.now().isoformat(),
                'rcend': self.start_date.isoformat()
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'recentchanges' in data['query']:
                for rc in data['query']['recentchanges']:
                    comment = rc.get('comment', '').lower()

                    # Check if comment contains any enforcement phrase
                    for phrase in self.enforcement_phrases:
                        if phrase.lower() in comment:
                            article_title = rc['title']
                            if article_title not in found_articles:
                                found_articles.add(article_title)
                                self.articles_found.append({
                                    'title': article_title,
                                    'search_phrase': phrase,
                                    'found_via': 'recent_changes'
                                })

            self.log(f"  Found {len(found_articles)} articles in recent changes")

        except Exception as e:
            self.log(f"  Error searching recent changes: {e}")

    def get_wikiproject_ai_cleanup_articles(self):
        """Get articles tagged by WikiProject AI Cleanup"""
        self.log("Fetching WikiProject AI Cleanup articles...")

        try:
            # Try to get articles from WikiProject AI Cleanup categories/pages
            # First, try getting the project page content
            params = {
                'action': 'query',
                'format': 'json',
                'titles': 'Wikipedia:WikiProject AI Cleanup',
                'prop': 'revisions|links',
                'rvprop': 'content',
                'pllimit': 500
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            articles_found_count = 0

            if 'query' in data and 'pages' in data['query']:
                page = list(data['query']['pages'].values())[0]

                # Get linked articles
                if 'links' in page:
                    for link in page['links']:
                        title = link['title']
                        # Only main namespace articles
                        if ':' not in title or title.startswith('Talk:'):
                            if not any(a['title'] == title for a in self.articles_found):
                                self.articles_found.append({
                                    'title': title.replace('Talk:', ''),
                                    'search_phrase': 'WikiProject AI Cleanup',
                                    'found_via': 'wikiproject_links'
                                })
                                articles_found_count += 1

            self.log(f"  Found {articles_found_count} articles from WikiProject AI Cleanup")

        except Exception as e:
            self.log(f"  Error fetching WikiProject articles: {e}")

    def analyze_edit_history(self, article_title):
        """Analyze complete edit history for AI-related content"""
        self.log(f"  Analyzing edit history: {article_title}")

        ai_edits = []

        try:
            # Get revisions since start_date
            params = {
                'action': 'query',
                'format': 'json',
                'titles': article_title,
                'prop': 'revisions',
                'rvprop': 'timestamp|user|comment|ids|size',
                'rvlimit': 500,
                'rvstart': datetime.now().isoformat(),
                'rvend': self.start_date.isoformat()
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page = list(data['query']['pages'].values())[0]

                if 'revisions' in page:
                    for rev in page['revisions']:
                        comment = rev.get('comment', '')

                        # Check for AI-related phrases
                        ai_mentioned = False
                        for phrase in self.enforcement_phrases:
                            if phrase.lower() in comment.lower():
                                ai_mentioned = True
                                break

                        if ai_mentioned:
                            # Determine action type
                            is_revert = bool(re.search(r'revert|undid|undo|rv\b', comment, re.IGNORECASE))
                            is_warning = bool(re.search(r'warn|notice|tag', comment, re.IGNORECASE))
                            is_removal = bool(re.search(r'remov|delet|blank', comment, re.IGNORECASE))

                            # Extract policy mentions
                            policies = self.extract_policy_mentions(comment)

                            action_type = []
                            if is_revert: action_type.append('revert')
                            if is_warning: action_type.append('warning')
                            if is_removal: action_type.append('removal')
                            if not action_type: action_type.append('other')

                            ai_edits.append({
                                'article': article_title,
                                'timestamp': rev['timestamp'],
                                'user': rev['user'],
                                'revid': rev['revid'],
                                'size': rev.get('size', 0),
                                'edit_summary': comment,
                                'action_type': ', '.join(action_type),
                                'policies_cited': ', '.join(policies) if policies else 'None'
                            })

            self.log(f"    Found {len(ai_edits)} AI-related edits")
            return ai_edits

        except Exception as e:
            self.log(f"    Error analyzing edits: {e}")
            return []

    def analyze_talk_page(self, article_title):
        """Analyze talk page for AI discussions"""
        talk_title = f"Talk:{article_title}"
        self.log(f"  Analyzing talk page: {talk_title}")

        ai_discussions = []

        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': talk_title,
                'prop': 'revisions',
                'rvprop': 'content|timestamp',
                'rvlimit': 1
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page = list(data['query']['pages'].values())[0]

                if 'revisions' in page and page['revisions']:
                    content = page['revisions'][0].get('*', '')

                    # Parse sections
                    sections = self.parse_talk_sections(content)

                    for section in sections:
                        # Check for AI phrases
                        ai_mentioned = False
                        matching_phrases = []
                        for phrase in self.enforcement_phrases:
                            if phrase.lower() in section['content'].lower():
                                ai_mentioned = True
                                matching_phrases.append(phrase)

                        if ai_mentioned:
                            # Extract policy mentions
                            policies = self.extract_policy_mentions(section['content'])

                            # Get excerpt
                            excerpt = section['content'][:300].replace('\n', ' ').strip()

                            ai_discussions.append({
                                'article': article_title,
                                'section_title': section['title'],
                                'matching_phrases': ', '.join(matching_phrases),
                                'policies_cited': ', '.join(policies) if policies else 'None',
                                'excerpt': excerpt,
                                'section_length': len(section['content'])
                            })

            self.log(f"    Found {len(ai_discussions)} AI-related discussions")
            return ai_discussions

        except Exception as e:
            self.log(f"    Error analyzing talk page: {e}")
            return []

    def parse_talk_sections(self, content):
        """Parse talk page into sections"""
        sections = []
        header_pattern = r'^(={2,})\s*([^=]+?)\s*\1\s*$'
        lines = content.split('\n')

        current_section = {'title': 'Introduction', 'content': ''}

        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                if current_section['content']:
                    sections.append(current_section)
                current_section = {
                    'title': match.group(2).strip(),
                    'content': ''
                }
            else:
                current_section['content'] += line + '\n'

        if current_section['content']:
            sections.append(current_section)

        return sections

    def extract_policy_mentions(self, text):
        """Extract Wikipedia policy mentions"""
        policies = []

        policy_patterns = {
            'WP:BOT': r'\bWP:BOT\b|bot policy',
            'WP:V': r'\bWP:V\b|\bWP:VERIFY\b|verifiability',
            'WP:RS': r'\bWP:RS\b|reliable source',
            'WP:NOR': r'\bWP:NOR\b|no original research',
            'WP:NOTAI': r'\bWP:NOTAI\b',
            'WP:AI': r'\bWP:AI\b(?!Cleanup)',
            'WP:COPIED': r'\bWP:COPIED\b|copyright',
            'WP:SPAM': r'\bWP:SPAM\b',
            'WP:COI': r'\bWP:COI\b|conflict of interest',
            'WP:PROMO': r'\bWP:PROMO\b|promotional'
        }

        for policy, pattern in policy_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                policies.append(policy)

        return policies

    def collect_articles(self, max_articles=30):
        """Collect articles with AI enforcement activity"""
        self.log("=" * 70)
        self.log("COLLECTING ARTICLES WITH AI ENFORCEMENT ACTIVITY")
        self.log("=" * 70)

        # Method 1: WikiProject AI Cleanup
        self.get_wikiproject_ai_cleanup_articles()
        time.sleep(self.request_delay)

        # Method 2: Recent changes
        self.search_recent_changes_for_ai(limit=500)
        time.sleep(self.request_delay)

        # Limit to requested number
        self.articles_found = self.articles_found[:max_articles]

        self.log(f"\nTotal articles to analyze: {len(self.articles_found)}")

    def analyze_all_articles(self):
        """Analyze all collected articles"""
        self.log("\n" + "=" * 70)
        self.log("ANALYZING ARTICLES")
        self.log("=" * 70)

        for i, article_info in enumerate(self.articles_found, 1):
            title = article_info['title']

            self.log(f"\n[{i}/{len(self.articles_found)}] {title}")
            self.log(f"  Found via: {article_info.get('found_via', article_info.get('search_phrase', 'N/A'))}")

            # Analyze edit history
            edits = self.analyze_edit_history(title)
            self.edit_data.extend(edits)
            time.sleep(self.request_delay)

            # Analyze talk page
            discussions = self.analyze_talk_page(title)
            self.talk_data.extend(discussions)
            time.sleep(self.request_delay)

    def generate_statistics(self):
        """Generate summary statistics"""
        self.log("\n" + "=" * 70)
        self.log("ANALYSIS RESULTS")
        self.log("=" * 70)

        # Edit statistics
        total_edits = len(self.edit_data)
        articles_with_edits = len(set(e['article'] for e in self.edit_data))

        self.log(f"\nEDIT HISTORY ANALYSIS:")
        self.log(f"  Total articles analyzed: {len(self.articles_found)}")
        self.log(f"  Articles with AI-related edits: {articles_with_edits}")
        self.log(f"  Total AI-related edits found: {total_edits}")

        if self.edit_data:
            # Action types
            action_counts = defaultdict(int)
            for edit in self.edit_data:
                for action in edit['action_type'].split(', '):
                    action_counts[action] += 1

            self.log(f"\n  Actions taken:")
            for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
                self.log(f"    {action}: {count}")

            # Policy citations
            policy_counts = defaultdict(int)
            for edit in self.edit_data:
                if edit['policies_cited'] != 'None':
                    for policy in edit['policies_cited'].split(', '):
                        policy_counts[policy] += 1

            if policy_counts:
                self.log(f"\n  Policies cited in edits:")
                for policy, count in sorted(policy_counts.items(), key=lambda x: x[1], reverse=True):
                    self.log(f"    {policy}: {count}")

            # Temporal analysis
            edits_by_year = defaultdict(int)
            for edit in self.edit_data:
                year = edit['timestamp'][:4]
                edits_by_year[year] += 1

            self.log(f"\n  Edits by year:")
            for year in sorted(edits_by_year.keys()):
                self.log(f"    {year}: {edits_by_year[year]}")

        # Talk page statistics
        total_discussions = len(self.talk_data)
        articles_with_discussions = len(set(d['article'] for d in self.talk_data))

        self.log(f"\nTALK PAGE ANALYSIS:")
        self.log(f"  Articles with AI discussions: {articles_with_discussions}")
        self.log(f"  Total AI-related discussion sections: {total_discussions}")

        if self.talk_data:
            # Policy citations in discussions
            policy_counts = defaultdict(int)
            for discussion in self.talk_data:
                if discussion['policies_cited'] != 'None':
                    for policy in discussion['policies_cited'].split(', '):
                        policy_counts[policy] += 1

            if policy_counts:
                self.log(f"\n  Policies cited in discussions:")
                for policy, count in sorted(policy_counts.items(), key=lambda x: x[1], reverse=True):
                    self.log(f"    {policy}: {count}")

    def save_results(self):
        """Save results to CSV files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save article list
        article_filename = f'ai_enforcement_targeted_articles_{timestamp}.csv'
        with open(article_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'found_via', 'search_phrase'])
            writer.writeheader()
            for article in self.articles_found:
                writer.writerow({
                    'title': article['title'],
                    'found_via': article.get('found_via', 'search'),
                    'search_phrase': article.get('search_phrase', 'N/A')
                })
        self.log(f"\nArticle list saved to: {article_filename}")

        # Save edit data
        if self.edit_data:
            edit_filename = f'ai_enforcement_targeted_edits_{timestamp}.csv'
            with open(edit_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.edit_data[0].keys())
                writer.writeheader()
                writer.writerows(self.edit_data)
            self.log(f"Edit data saved to: {edit_filename}")
        else:
            self.log("No edit data to save")

        # Save talk data
        if self.talk_data:
            talk_filename = f'ai_enforcement_targeted_discussions_{timestamp}.csv'
            with open(talk_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.talk_data[0].keys())
                writer.writeheader()
                writer.writerows(self.talk_data)
            self.log(f"Talk data saved to: {talk_filename}")
        else:
            self.log("No talk data to save")

def main():
    """Main execution function"""
    analyzer = TargetedAIEnforcementAnalyzer()

    # Collect articles with AI enforcement
    analyzer.collect_articles(max_articles=30)

    # Analyze collected articles
    if analyzer.articles_found:
        analyzer.analyze_all_articles()

        # Generate statistics
        analyzer.generate_statistics()

        # Save results
        analyzer.save_results()
    else:
        print("\nNo articles with AI enforcement found!")

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
