#!/usr/bin/env python3
"""
Wikipedia AI Rule Enforcement Analyzer

Analyzes how Wikipedia's AI policies are implemented in practice by examining:
1. Edit history (revisions with AI-related edit summaries)
2. Talk page discussions (AI-related discussions)

Sample: 30 articles (10 recent, 10 high-traffic, 10 medium-traffic)
Time period: Since January 1, 2023
"""

import requests
import json
import time
from datetime import datetime, timedelta
import re
import csv
from collections import defaultdict

class AIEnforcementAnalyzer:
    """Analyzer for AI rule enforcement in Wikipedia"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia AI Enforcement Research Tool (Educational Research)'
        })

        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.request_delay = 1

        # AI-related keywords
        self.ai_keywords = [
            r'\bAI\b', r'\bA\.I\.\b',
            r'ChatGPT', r'GPT', r'GPT-[0-9]',
            r'artificial intelligence',
            r'machine learning', r'\bML\b',
            r'AI-generated', r'AI generated',
            r'bot-generated', r'auto-generated',
            r'LLM', r'large language model',
            r'neural network',
            r'automated content', r'automated edit'
        ]

        self.ai_pattern = re.compile('|'.join(self.ai_keywords), re.IGNORECASE)

        # Start date for analysis
        self.start_date = datetime(2023, 1, 1)

        self.edit_data = []
        self.talk_data = []
        self.article_list = []

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_recent_articles(self, count=10):
        """Get recently created articles"""
        self.log(f"Fetching {count} recently created articles...")

        articles = []

        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'recentchanges',
                'rctype': 'new',
                'rcnamespace': 0,  # Main namespace
                'rclimit': 500,
                'rcshow': '!redirect'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'recentchanges' in data['query']:
                for rc in data['query']['recentchanges']:
                    if len(articles) >= count:
                        break

                    title = rc['title']
                    timestamp = rc['timestamp']
                    articles.append({
                        'title': title,
                        'created': timestamp,
                        'category': 'recent'
                    })

            self.log(f"  Found {len(articles)} recent articles")
            return articles

        except Exception as e:
            self.log(f"Error fetching recent articles: {e}")
            return []

    def get_high_traffic_articles(self, count=10):
        """Get high-traffic articles from Featured/Good articles"""
        self.log(f"Fetching {count} high-traffic articles...")

        articles = []

        try:
            # Get Featured Articles
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'categorymembers',
                'cmtitle': 'Category:Featured articles',
                'cmlimit': 100,
                'cmnamespace': 0
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'categorymembers' in data['query']:
                for member in data['query']['categorymembers']:
                    if len(articles) >= count:
                        break

                    articles.append({
                        'title': member['title'],
                        'category': 'high-traffic'
                    })

            self.log(f"  Found {len(articles)} high-traffic articles")
            return articles

        except Exception as e:
            self.log(f"Error fetching high-traffic articles: {e}")
            return []

    def get_medium_traffic_articles(self, count=10):
        """Get medium-traffic articles from Good articles"""
        self.log(f"Fetching {count} medium-traffic articles...")

        articles = []

        try:
            # Get Good Articles
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'categorymembers',
                'cmtitle': 'Category:Good articles',
                'cmlimit': 100,
                'cmnamespace': 0
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'categorymembers' in data['query']:
                for member in data['query']['categorymembers']:
                    if len(articles) >= count:
                        break

                    articles.append({
                        'title': member['title'],
                        'category': 'medium-traffic'
                    })

            self.log(f"  Found {len(articles)} medium-traffic articles")
            return articles

        except Exception as e:
            self.log(f"Error fetching medium-traffic articles: {e}")
            return []

    def analyze_edit_history(self, article_title):
        """Analyze edit history for AI-related enforcement"""
        self.log(f"  Analyzing edit history for: {article_title}")

        ai_edits = []

        try:
            # Get revisions since start_date
            params = {
                'action': 'query',
                'format': 'json',
                'titles': article_title,
                'prop': 'revisions',
                'rvprop': 'timestamp|user|comment|ids',
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

                        # Check if edit summary contains AI keywords
                        if self.ai_pattern.search(comment):
                            # Determine if it's a revert
                            is_revert = bool(re.search(r'revert|undid|undo|rv\b', comment, re.IGNORECASE))

                            # Extract policy mentions
                            policies = self.extract_policy_mentions(comment)

                            ai_edits.append({
                                'article': article_title,
                                'timestamp': rev['timestamp'],
                                'user': rev['user'],
                                'revid': rev['revid'],
                                'edit_summary': comment,
                                'is_revert': is_revert,
                                'policies_cited': ', '.join(policies) if policies else 'None'
                            })

            self.log(f"    Found {len(ai_edits)} AI-related edits")
            return ai_edits

        except Exception as e:
            self.log(f"    Error analyzing edit history: {e}")
            return []

    def analyze_talk_page(self, article_title):
        """Analyze talk page for AI-related discussions"""
        talk_title = f"Talk:{article_title}"
        self.log(f"  Analyzing talk page: {talk_title}")

        ai_discussions = []

        try:
            # Get talk page content
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
                        if self.ai_pattern.search(section['content']):
                            # Count AI keyword occurrences
                            ai_count = len(self.ai_pattern.findall(section['content']))

                            # Extract policy mentions
                            policies = self.extract_policy_mentions(section['content'])

                            # Get excerpt (first 200 chars)
                            excerpt = section['content'][:200].replace('\n', ' ').strip()

                            ai_discussions.append({
                                'article': article_title,
                                'section_title': section['title'],
                                'ai_keyword_count': ai_count,
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

        # Split by headers (== Header ==)
        header_pattern = r'^(={2,})\s*([^=]+?)\s*\1\s*$'
        lines = content.split('\n')

        current_section = {'title': 'Introduction', 'content': ''}

        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Save previous section
                if current_section['content']:
                    sections.append(current_section)

                # Start new section
                current_section = {
                    'title': match.group(2).strip(),
                    'content': ''
                }
            else:
                current_section['content'] += line + '\n'

        # Add last section
        if current_section['content']:
            sections.append(current_section)

        return sections

    def extract_policy_mentions(self, text):
        """Extract Wikipedia policy mentions from text"""
        policies = []

        policy_patterns = {
            'WP:BOT': r'\bWP:BOT\b|bot policy',
            'WP:V': r'\bWP:V\b|verifiability',
            'WP:RS': r'\bWP:RS\b|reliable source',
            'WP:NOR': r'\bWP:NOR\b|no original research',
            'WP:NOTAI': r'\bWP:NOTAI\b',
            'WP:AI': r'\bWP:AI\b|artificial intelligence',
            'WP:COPIED': r'\bWP:COPIED\b|copyright',
            'WP:SPAM': r'\bWP:SPAM\b'
        }

        for policy, pattern in policy_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                policies.append(policy)

        return policies

    def collect_sample(self):
        """Collect sample of 30 articles"""
        self.log("Collecting sample of 30 articles...")
        self.log("=" * 70)

        # Get 10 of each type
        recent = self.get_recent_articles(10)
        time.sleep(self.request_delay)

        high_traffic = self.get_high_traffic_articles(10)
        time.sleep(self.request_delay)

        medium_traffic = self.get_medium_traffic_articles(10)

        self.article_list = recent + high_traffic + medium_traffic

        self.log(f"\nTotal articles collected: {len(self.article_list)}")
        self.log("  Recent: " + str(len(recent)))
        self.log("  High-traffic: " + str(len(high_traffic)))
        self.log("  Medium-traffic: " + str(len(medium_traffic)))

    def analyze_all_articles(self):
        """Analyze all articles in sample"""
        self.log("\n" + "=" * 70)
        self.log("Analyzing articles for AI enforcement...")
        self.log("=" * 70)

        for i, article in enumerate(self.article_list, 1):
            title = article['title']
            category = article['category']

            self.log(f"\n[{i}/{len(self.article_list)}] {title} ({category})")

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
        self.log("ANALYSIS SUMMARY")
        self.log("=" * 70)

        # Edit statistics
        total_edits = len(self.edit_data)
        reverts = sum(1 for e in self.edit_data if e['is_revert'])
        articles_with_edits = len(set(e['article'] for e in self.edit_data))

        self.log(f"\nEDIT HISTORY ANALYSIS:")
        self.log(f"  Total AI-related edits: {total_edits}")
        self.log(f"  Articles with AI edits: {articles_with_edits}/{len(self.article_list)}")
        self.log(f"  Reverts: {reverts} ({reverts/total_edits*100:.1f}%)" if total_edits > 0 else "  Reverts: 0")

        # Policy citations in edits
        if self.edit_data:
            policy_counts = defaultdict(int)
            for edit in self.edit_data:
                if edit['policies_cited'] != 'None':
                    for policy in edit['policies_cited'].split(', '):
                        policy_counts[policy] += 1

            if policy_counts:
                self.log(f"\n  Most cited policies in edits:")
                for policy, count in sorted(policy_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    self.log(f"    {policy}: {count}")

        # Talk page statistics
        total_discussions = len(self.talk_data)
        articles_with_discussions = len(set(d['article'] for d in self.talk_data))

        self.log(f"\nTALK PAGE ANALYSIS:")
        self.log(f"  Total AI-related discussions: {total_discussions}")
        self.log(f"  Articles with AI discussions: {articles_with_discussions}/{len(self.article_list)}")

        # Policy citations in discussions
        if self.talk_data:
            policy_counts = defaultdict(int)
            for discussion in self.talk_data:
                if discussion['policies_cited'] != 'None':
                    for policy in discussion['policies_cited'].split(', '):
                        policy_counts[policy] += 1

            if policy_counts:
                self.log(f"\n  Most cited policies in discussions:")
                for policy, count in sorted(policy_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    self.log(f"    {policy}: {count}")

        # Category breakdown
        self.log(f"\nBREAKDOWN BY ARTICLE CATEGORY:")
        for category in ['recent', 'high-traffic', 'medium-traffic']:
            cat_articles = [a for a in self.article_list if a['category'] == category]
            cat_edits = [e for e in self.edit_data if any(a['title'] == e['article'] for a in cat_articles)]
            cat_discussions = [d for d in self.talk_data if any(a['title'] == d['article'] for a in cat_articles)]

            self.log(f"  {category.capitalize()}:")
            self.log(f"    AI edits: {len(cat_edits)}")
            self.log(f"    AI discussions: {len(cat_discussions)}")

    def save_results(self):
        """Save results to CSV files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save edit data
        if self.edit_data:
            edit_filename = f'ai_edit_enforcement_{timestamp}.csv'
            with open(edit_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.edit_data[0].keys())
                writer.writeheader()
                writer.writerows(self.edit_data)
            self.log(f"\nEdit data saved to: {edit_filename}")
        else:
            self.log(f"\nNo edit data to save")

        # Save talk data
        if self.talk_data:
            talk_filename = f'ai_talk_discussions_{timestamp}.csv'
            with open(talk_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.talk_data[0].keys())
                writer.writeheader()
                writer.writerows(self.talk_data)
            self.log(f"Talk data saved to: {talk_filename}")
        else:
            self.log(f"No talk data to save")

        # Save article list
        article_filename = f'ai_enforcement_articles_{timestamp}.csv'
        with open(article_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'category', 'created'])
            writer.writeheader()
            for article in self.article_list:
                writer.writerow({
                    'title': article['title'],
                    'category': article['category'],
                    'created': article.get('created', 'N/A')
                })
        self.log(f"Article list saved to: {article_filename}")

def main():
    """Main execution function"""
    analyzer = AIEnforcementAnalyzer()

    # Collect sample
    analyzer.collect_sample()

    # Analyze articles
    analyzer.analyze_all_articles()

    # Generate statistics
    analyzer.generate_statistics()

    # Save results
    analyzer.save_results()

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
