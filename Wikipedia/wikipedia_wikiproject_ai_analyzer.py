#!/usr/bin/env python3
"""
Wikipedia WikiProject AI Policy Analyzer

This script identifies the most popular WikiProjects and analyzes their
specific policies, guidelines, and discussions regarding AI usage.

It checks if WikiProjects have their own AI-specific rules separate from
Wikipedia's general governance.
"""

import requests
import json
import time
from datetime import datetime
import re
import os
from collections import defaultdict

class WikiProjectAIAnalyzer:
    """Analyzer for WikiProject-specific AI policies"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia WikiProject AI Research Tool (Educational Research)'
        })

        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.request_delay = 1

        # AI-related keywords to search for
        self.ai_keywords = [
            'artificial intelligence', 'AI', 'machine learning', 'ML',
            'bot', 'automated', 'automation', 'algorithm',
            'neural network', 'deep learning', 'chatbot', 'language model',
            'GPT', 'ChatGPT', 'generative', 'AI-generated', 'AI-assisted',
            'LLM', 'large language model', 'computer-generated'
        ]

        self.wikiproject_data = []

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_popular_wikiprojects(self, limit=50):
        """
        Get most popular WikiProjects by number of members and articles

        Strategy:
        1. Search for all pages starting with "Wikipedia:WikiProject "
        2. For each project, get statistics (watchers, pageviews)
        3. Sort by popularity metrics
        """
        self.log(f"Fetching popular WikiProjects (limit: {limit})...")

        wikiprojects = []

        try:
            # Use allpages to find ALL WikiProject pages
            continue_token = None
            batch_count = 0
            previous_count = 0

            while True:
                batch_count += 1
                self.log(f"  Fetching batch {batch_count}...")

                params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'allpages',
                    'apprefix': 'WikiProject ',
                    'apnamespace': 4,  # Wikipedia namespace
                    'aplimit': 500,
                    'apfilterredir': 'nonredirects'  # Exclude redirects
                }

                if continue_token:
                    params['apcontinue'] = continue_token

                response = self.session.get(self.api_base, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                previous_count = len(wikiprojects)
                batch_size = 0
                total_pages_in_batch = 0
                if 'query' in data and 'allpages' in data['query']:
                    total_pages_in_batch = len(data['query']['allpages'])
                    for page in data['query']['allpages']:
                        title = page['title']
                        # Only include main WikiProject pages, not subpages
                        if title.count('/') == 0:
                            wikiprojects.append({
                                'title': title,
                                'pageid': page['pageid']
                            })
                            batch_size += 1

                self.log(f"  Found {batch_size} main WikiProjects (out of {total_pages_in_batch} pages) - total: {len(wikiprojects)}")

                # Check for continuation
                if 'continue' in data and 'apcontinue' in data['continue']:
                    continue_token = data['continue']['apcontinue']
                    time.sleep(self.request_delay)
                else:
                    self.log(f"  No more WikiProjects available from API")
                    break

            self.log(f"Found {len(wikiprojects)} total WikiProjects")

            # Get popularity data for all fetched projects
            self.log(f"Getting popularity data for {len(wikiprojects)} WikiProjects...")

            subset = wikiprojects

            for i in range(0, len(subset), 50):  # API limit is 50 titles per request
                batch = subset[i:i+50]
                self.log(f"  Processing batch {i//50 + 1}/{(len(subset)-1)//50 + 1}...")
                titles = '|'.join([wp['title'] for wp in batch])

                params = {
                    'action': 'query',
                    'format': 'json',
                    'titles': titles,
                    'prop': 'info|pageviews',
                    'inprop': 'watchers',
                    'pvipdays': 30  # Last 30 days of pageviews
                }

                response = self.session.get(self.api_base, params=params, timeout=30)
                data = response.json()

                if 'query' in data and 'pages' in data['query']:
                    for page_id, page_data in data['query']['pages'].items():
                        # Find matching WikiProject and update it
                        for wp in batch:
                            if str(wp['pageid']) == page_id:
                                wp['watchers'] = page_data.get('watchers', 0)
                                # Sum pageviews
                                pageviews = page_data.get('pageviews', {})
                                wp['monthly_views'] = sum(v for v in pageviews.values() if v is not None)
                                break

                time.sleep(self.request_delay)

            # Sort by watchers (proxy for active participation)
            subset.sort(key=lambda x: x.get('watchers', 0), reverse=True)

            # Take top projects from the subset
            top_projects = subset[:limit]

            self.log(f"Selected top {len(top_projects)} WikiProjects by popularity")

            return top_projects

        except Exception as e:
            self.log(f"Error fetching WikiProjects: {e}")
            return []

    def get_wikiproject_subpages(self, wikiproject_title):
        """Get all subpages of a WikiProject (guidelines, policies, etc.)"""
        try:
            subpages = []

            params = {
                'action': 'query',
                'format': 'json',
                'list': 'allpages',
                'apprefix': wikiproject_title.replace('Wikipedia:', '') + '/',
                'apnamespace': 4,  # Wikipedia namespace
                'aplimit': 500
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'allpages' in data['query']:
                subpages = [page['title'] for page in data['query']['allpages']]

            return subpages

        except Exception as e:
            self.log(f"Error getting subpages for {wikiproject_title}: {e}")
            return []

    def get_page_content(self, page_title):
        """Get full content and metadata for a page"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_title,
                'prop': 'revisions|info|categories',
                'rvprop': 'content|timestamp|user|size',
                'rvlimit': 1,
                'inprop': 'url'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page_data = list(data['query']['pages'].values())[0]

                if 'revisions' in page_data and page_data['revisions']:
                    revision = page_data['revisions'][0]
                    page_data['wikitext'] = revision.get('*', '')
                    page_data['last_modified'] = revision.get('timestamp', '')
                    page_data['last_editor'] = revision.get('user', '')
                    page_data['size'] = revision.get('size', 0)

                return page_data

            return None

        except Exception as e:
            self.log(f"Error getting content for {page_title}: {e}")
            return None

    def count_ai_references(self, text):
        """Count AI-related keyword mentions in text"""
        if not text:
            return 0

        text_lower = text.lower()
        count = 0

        for keyword in self.ai_keywords:
            # Use word boundaries for more accurate matching
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = re.findall(pattern, text_lower)
            count += len(matches)

        return count

    def extract_ai_policy_sections(self, wikitext, page_title):
        """Extract sections that might contain AI policies"""
        if not wikitext:
            return []

        sections = []

        # Split by headers (== Header ==)
        header_pattern = r'^(={2,})\s*([^=]+?)\s*\1\s*$'
        lines = wikitext.split('\n')

        current_section = {'title': 'Introduction', 'content': '', 'level': 0}

        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Check if current section has AI content
                if current_section['content']:
                    ai_count = self.count_ai_references(current_section['content'])
                    if ai_count > 0:
                        current_section['ai_references'] = ai_count
                        sections.append(current_section)

                # Start new section
                level = len(match.group(1))
                title = match.group(2).strip()
                current_section = {
                    'title': title,
                    'content': '',
                    'level': level
                }
            else:
                current_section['content'] += line + '\n'

        # Check last section
        if current_section['content']:
            ai_count = self.count_ai_references(current_section['content'])
            if ai_count > 0:
                current_section['ai_references'] = ai_count
                sections.append(current_section)

        return sections

    def analyze_wikiproject(self, wikiproject):
        """Analyze a single WikiProject for AI policies"""
        title = wikiproject['title']
        self.log(f"Analyzing {title}...")

        analysis = {
            'title': title,
            'watchers': wikiproject.get('watchers', 0),
            'monthly_views': wikiproject.get('monthly_views', 0),
            'main_page_ai_content': False,
            'main_page_ai_count': 0,
            'subpages': [],
            'ai_policy_pages': [],
            'total_ai_references': 0,
            'has_specific_ai_policy': False
        }

        # Analyze main page
        main_page = self.get_page_content(title)
        if main_page and 'wikitext' in main_page:
            ai_count = self.count_ai_references(main_page['wikitext'])
            analysis['main_page_ai_count'] = ai_count
            analysis['main_page_ai_content'] = ai_count > 0
            analysis['total_ai_references'] += ai_count

            if ai_count > 0:
                ai_sections = self.extract_ai_policy_sections(main_page['wikitext'], title)
                analysis['main_page_ai_sections'] = ai_sections

        time.sleep(self.request_delay)

        # Get and analyze subpages
        subpages = self.get_wikiproject_subpages(title)
        analysis['subpages'] = subpages

        self.log(f"  Found {len(subpages)} subpages")

        # Check subpages for AI-related content
        ai_related_subpages = []
        for subpage in subpages:
            # Look for guideline/policy-related subpages
            subpage_lower = subpage.lower()
            if any(keyword in subpage_lower for keyword in ['guideline', 'policy', 'rule', 'standard', 'criteria', 'assessment']):
                page_content = self.get_page_content(subpage)
                if page_content and 'wikitext' in page_content:
                    ai_count = self.count_ai_references(page_content['wikitext'])
                    if ai_count > 0:
                        ai_sections = self.extract_ai_policy_sections(page_content['wikitext'], subpage)
                        ai_related_subpages.append({
                            'title': subpage,
                            'ai_count': ai_count,
                            'size': page_content.get('size', 0),
                            'ai_sections': ai_sections,
                            'last_modified': page_content.get('last_modified', ''),
                            'url': page_content.get('fullurl', '')
                        })
                        analysis['total_ai_references'] += ai_count

                        # Check if this is a dedicated AI policy
                        if any(keyword in subpage_lower for keyword in ['ai', 'artificial intelligence', 'bot', 'automated']):
                            analysis['has_specific_ai_policy'] = True

                time.sleep(self.request_delay)

        analysis['ai_policy_pages'] = ai_related_subpages

        self.log(f"  Total AI references: {analysis['total_ai_references']}")
        self.log(f"  AI policy pages: {len(ai_related_subpages)}")

        return analysis

    def analyze_all_wikiprojects(self, limit=50):
        """Analyze top WikiProjects for AI policies"""
        self.log("Starting WikiProject AI Policy Analysis")
        self.log("=" * 70)

        # Get popular WikiProjects
        wikiprojects = self.get_popular_wikiprojects(limit)

        if not wikiprojects:
            self.log("No WikiProjects found!")
            return

        self.log(f"\nAnalyzing {len(wikiprojects)} WikiProjects for AI policies...")
        self.log("-" * 70)

        # Analyze each WikiProject
        for i, wikiproject in enumerate(wikiprojects, 1):
            self.log(f"\n[{i}/{len(wikiprojects)}] {wikiproject['title']}")

            analysis = self.analyze_wikiproject(wikiproject)
            self.wikiproject_data.append(analysis)

        self.log("\n" + "=" * 70)
        self.log("Analysis complete!")

    def generate_report(self):
        """Generate summary report"""
        self.log("\n" + "=" * 70)
        self.log("SUMMARY REPORT")
        self.log("=" * 70)

        total_projects = len(self.wikiproject_data)
        projects_with_ai = sum(1 for p in self.wikiproject_data if p['total_ai_references'] > 0)
        projects_with_specific_policy = sum(1 for p in self.wikiproject_data if p['has_specific_ai_policy'])

        self.log(f"\nTotal WikiProjects analyzed: {total_projects}")
        self.log(f"WikiProjects with AI content: {projects_with_ai} ({projects_with_ai/total_projects*100:.1f}%)")
        self.log(f"WikiProjects with specific AI policies: {projects_with_specific_policy}")

        # Top WikiProjects by AI content
        self.log("\n" + "-" * 70)
        self.log("TOP WIKIPROJECTS BY AI CONTENT")
        self.log("-" * 70)

        sorted_by_ai = sorted(self.wikiproject_data, key=lambda x: x['total_ai_references'], reverse=True)

        for i, project in enumerate(sorted_by_ai[:20], 1):
            if project['total_ai_references'] > 0:
                self.log(f"{i}. {project['title']}")
                self.log(f"   AI References: {project['total_ai_references']}")
                self.log(f"   Watchers: {project['watchers']}")
                self.log(f"   Specific AI Policy: {'Yes' if project['has_specific_ai_policy'] else 'No'}")
                if project['ai_policy_pages']:
                    self.log(f"   AI Policy Pages: {len(project['ai_policy_pages'])}")
                    for page in project['ai_policy_pages']:
                        self.log(f"     - {page['title']} ({page['ai_count']} refs)")

        # WikiProjects with dedicated AI policies
        self.log("\n" + "-" * 70)
        self.log("WIKIPROJECTS WITH DEDICATED AI POLICIES")
        self.log("-" * 70)

        projects_with_policies = [p for p in self.wikiproject_data if p['has_specific_ai_policy']]

        if projects_with_policies:
            for project in projects_with_policies:
                self.log(f"\n{project['title']}")
                for page in project['ai_policy_pages']:
                    if any(keyword in page['title'].lower() for keyword in ['ai', 'artificial intelligence', 'bot', 'automated']):
                        self.log(f"  Policy: {page['title']}")
                        self.log(f"  AI References: {page['ai_count']}")
                        self.log(f"  Last Modified: {page['last_modified']}")
                        self.log(f"  URL: {page['url']}")
                        if page.get('ai_sections'):
                            self.log(f"  Sections with AI content:")
                            for section in page['ai_sections'][:5]:  # Show first 5 sections
                                self.log(f"    - {section['title']} ({section['ai_references']} refs)")
        else:
            self.log("No WikiProjects with dedicated AI policies found.")

    def save_results(self):
        """Save results to JSON and CSV files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save detailed JSON
        json_filename = f'wikipedia_wikiproject_ai_analysis_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.wikiproject_data, f, indent=2, ensure_ascii=False)
        self.log(f"\nDetailed results saved to: {json_filename}")

        # Save summary CSV
        import csv
        csv_filename = f'wikipedia_wikiproject_ai_summary_{timestamp}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'WikiProject', 'Watchers', 'Monthly Views',
                'Total AI References', 'Main Page AI Count',
                'AI Policy Pages', 'Has Specific AI Policy',
                'Subpages Count'
            ])

            for project in sorted(self.wikiproject_data, key=lambda x: x['total_ai_references'], reverse=True):
                writer.writerow([
                    project['title'],
                    project['watchers'],
                    project['monthly_views'],
                    project['total_ai_references'],
                    project['main_page_ai_count'],
                    len(project['ai_policy_pages']),
                    'Yes' if project['has_specific_ai_policy'] else 'No',
                    len(project['subpages'])
                ])

        self.log(f"Summary CSV saved to: {csv_filename}")

def main():
    """Main execution function"""
    analyzer = WikiProjectAIAnalyzer()

    # Analyze top 50 WikiProjects by default
    # Set to higher number to analyze more projects
    analyzer.analyze_all_wikiprojects(limit=50)

    # Generate report
    analyzer.generate_report()

    # Save results
    analyzer.save_results()

if __name__ == '__main__':
    main()
