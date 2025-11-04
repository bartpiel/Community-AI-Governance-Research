#!/usr/bin/env python3
"""
Wikipedia Specific AI Governance Page Analyzer

This script directly analyzes known Wikipedia governance pages that are likely
to contain AI-related policies and guidelines.

It focuses on key governance pages like:
- Wikipedia:Policies and guidelines
- Wikipedia:Bot policy
- Wikipedia:Copyright
- Wikipedia:Reliable sources
- Wikipedia:Verifiability
- Wikipedia:Content assessment
- Wikipedia:Manual of Style
"""

import requests
import json
import time
from datetime import datetime
import re
import os

class WikipediaSpecificGovernanceAnalyzer:
    """Analyzer for specific Wikipedia governance pages"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia AI Governance Research Tool (Educational Research)'
        })

        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.request_delay = 1

        # Key governance pages likely to contain AI-related content
        self.key_governance_pages = [
            # Core policies
            "Wikipedia:Five pillars",
            "Wikipedia:What Wikipedia is not",
            "Wikipedia:Neutral point of view",
            "Wikipedia:Verifiability",
            "Wikipedia:No original research",
            "Wikipedia:Biographies of living persons",
            "Wikipedia:Copyright",

            # Content guidelines
            "Wikipedia:Reliable sources",
            "Wikipedia:Citing sources",
            "Wikipedia:Manual of Style",
            "Wikipedia:Article titles",
            "Wikipedia:Notability",

            # Behavioral guidelines
            "Wikipedia:Civility",
            "Wikipedia:Consensus",
            "Wikipedia:Edit warring",
            "Wikipedia:Sock puppetry",

            # Bot and automation policies
            "Wikipedia:Bot policy",
            "Wikipedia:Bots",
            "Wikipedia:Bot requests",
            "Wikipedia:AutoWikiBrowser",
            "Wikipedia:Automated editing",

            # Content creation and assessment
            "Wikipedia:Content assessment",
            "Wikipedia:WikiProject",
            "Wikipedia:Good article criteria",
            "Wikipedia:Featured article criteria",

            # Administrative and process pages
            "Wikipedia:Administrators",
            "Wikipedia:Bureaucrats",
            "Wikipedia:Checkuser",
            "Wikipedia:Oversight",
            "Wikipedia:Arbitration",

            # Help and information pages
            "Wikipedia:Help desk",
            "Wikipedia:Village pump",
            "Wikipedia:Reference desk",
            "Wikipedia:Teahouse",

            # AI-specific or technology-related pages
            "Wikipedia:Artificial intelligence",
            "Wikipedia:Machine learning",
            "Wikipedia:Technology",
            "Wikipedia:Computer science",

            # Essay pages (opinions but influential)
            "Wikipedia:Essays",
            "Wikipedia:Ignore all rules",
            "Wikipedia:Be bold",
            "Wikipedia:Assume good faith"
        ]

        self.ai_related_keywords = [
            'artificial intelligence', 'AI', 'machine learning', 'ML',
            'bot', 'automated', 'automation', 'algorithm', 'algorithmic',
            'neural network', 'deep learning', 'chatbot', 'language model',
            'GPT', 'ChatGPT', 'generative', 'AI-generated', 'AI-assisted',
            'computer-generated', 'synthetic', 'auto-generated'
        ]

        self.governance_pages_data = []

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_page_full_content(self, page_title):
        """Get the full wikitext content of a page"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_title,
                'prop': 'revisions|info|categories',
                'rvprop': 'content|timestamp|user|comment',
                'rvlimit': 1,
                'inprop': 'url'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page_data = list(data['query']['pages'].values())[0]

                if 'revisions' in page_data and page_data['revisions']:
                    revision = page_data['revisions'][0]
                    page_data['wikitext'] = revision.get('*', '')
                    page_data['last_modified'] = revision.get('timestamp', '')
                    page_data['last_editor'] = revision.get('user', '')
                    page_data['edit_comment'] = revision.get('comment', '')

                return page_data

            return None

        except Exception as e:
            self.log(f"Error getting content for '{page_title}': {e}")
            return None

    def extract_ai_references(self, page_content, page_title):
        """Extract all AI-related references from a page"""

        wikitext = page_content.get('wikitext', '')

        if not wikitext:
            return {
                'ai_found': False,
                'ai_sections': [],
                'ai_mentions': [],
                'total_ai_references': 0
            }

        # Find AI-related content
        ai_mentions = []
        ai_sections = []

        # Split into sections
        sections = re.split(r'\n==+\s*([^=]+)\s*==+', wikitext)

        current_section = "Introduction"
        section_content = ""

        for i, part in enumerate(sections):
            if i % 2 == 0:  # Content
                section_content = part

                # Look for AI keywords in this section
                for keyword in self.ai_related_keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    matches = re.finditer(pattern, section_content, re.IGNORECASE)

                    for match in matches:
                        # Get context around the match
                        start = max(0, match.start() - 100)
                        end = min(len(section_content), match.end() + 100)
                        context = section_content[start:end].strip()

                        ai_mentions.append({
                            'keyword': keyword,
                            'section': current_section,
                            'context': context,
                            'position': match.start()
                        })

                # If section contains AI content, save the section
                if any(keyword.lower() in section_content.lower()
                      for keyword in self.ai_related_keywords):
                    ai_sections.append({
                        'section_title': current_section,
                        'content': section_content[:1000],  # First 1000 chars
                        'ai_keywords_found': [kw for kw in self.ai_related_keywords
                                            if kw.lower() in section_content.lower()]
                    })

            else:  # Section header
                current_section = part.strip()

        return {
            'ai_found': len(ai_mentions) > 0,
            'ai_sections': ai_sections,
            'ai_mentions': ai_mentions,
            'total_ai_references': len(ai_mentions),
            'unique_ai_terms': list(set(mention['keyword'] for mention in ai_mentions))
        }

    def analyze_governance_pages(self):
        """Analyze all key governance pages for AI content"""
        self.log("Starting analysis of specific Wikipedia governance pages...")

        for page_title in self.key_governance_pages:
            self.log(f"Analyzing: {page_title}")

            # Get page content
            page_content = self.get_page_full_content(page_title)

            if page_content:
                # Extract AI references
                ai_analysis = self.extract_ai_references(page_content, page_title)

                # Determine page type
                page_type = self.categorize_governance_page(page_title)

                # Compile page analysis
                page_analysis = {
                    'title': page_title,
                    'url': page_content.get('fullurl', ''),
                    'page_type': page_type,
                    'last_modified': page_content.get('last_modified', ''),
                    'last_editor': page_content.get('last_editor', ''),
                    'edit_comment': page_content.get('edit_comment', ''),
                    'categories': [cat.get('title', '') for cat in page_content.get('categories', [])],
                    'ai_analysis': ai_analysis,
                    'page_size': len(page_content.get('wikitext', '')),
                    'has_ai_content': ai_analysis['ai_found']
                }

                self.governance_pages_data.append(page_analysis)

                if ai_analysis['ai_found']:
                    self.log(f"  ✅ AI content found: {ai_analysis['total_ai_references']} references")
                else:
                    self.log(f"  ❌ No AI content found")
            else:
                self.log(f"  ⚠️ Could not retrieve page content")

            time.sleep(self.request_delay)

        self.log(f"Analysis complete: {len(self.governance_pages_data)} pages analyzed")

        # Count pages with AI content
        ai_pages = [page for page in self.governance_pages_data if page['has_ai_content']]
        self.log(f"AI content found in {len(ai_pages)} governance pages")

        return self.governance_pages_data

    def categorize_governance_page(self, page_title):
        """Categorize the type of governance page"""
        title_lower = page_title.lower()

        if 'policy' in title_lower or page_title in ['Wikipedia:Five pillars', 'Wikipedia:What Wikipedia is not']:
            return 'Policy'
        elif 'guideline' in title_lower or any(term in title_lower for term in ['manual of style', 'reliable sources', 'notability']):
            return 'Guideline'
        elif 'bot' in title_lower or 'automated' in title_lower:
            return 'Bot/Automation Policy'
        elif 'essay' in title_lower or page_title in ['Wikipedia:Ignore all rules', 'Wikipedia:Be bold']:
            return 'Essay'
        elif any(term in title_lower for term in ['help', 'village pump', 'teahouse']):
            return 'Help/Community Page'
        elif 'arbitration' in title_lower or 'administrator' in title_lower:
            return 'Administrative Page'
        elif 'wikiproject' in title_lower or 'assessment' in title_lower:
            return 'Project/Assessment Page'
        else:
            return 'Information Page'

    def generate_ai_governance_report(self):
        """Generate comprehensive report on AI governance"""

        if not self.governance_pages_data:
            return {}

        # Pages with AI content
        ai_pages = [page for page in self.governance_pages_data if page['has_ai_content']]

        # Statistics by page type
        page_type_stats = {}
        ai_by_type = {}

        for page in self.governance_pages_data:
            page_type = page['page_type']
            page_type_stats[page_type] = page_type_stats.get(page_type, 0) + 1

            if page['has_ai_content']:
                ai_by_type[page_type] = ai_by_type.get(page_type, 0) + 1

        # Most AI-heavy pages
        ai_heavy_pages = sorted(ai_pages,
                              key=lambda x: x['ai_analysis']['total_ai_references'],
                              reverse=True)

        # AI terms frequency
        all_ai_terms = []
        for page in ai_pages:
            all_ai_terms.extend(page['ai_analysis']['unique_ai_terms'])

        from collections import Counter
        ai_term_frequency = Counter(all_ai_terms)

        # Recent AI-related edits
        recent_ai_pages = [page for page in ai_pages if page['last_modified']]
        recent_ai_pages.sort(key=lambda x: x['last_modified'], reverse=True)

        report = {
            'summary': {
                'total_pages_analyzed': len(self.governance_pages_data),
                'pages_with_ai_content': len(ai_pages),
                'ai_coverage_percentage': round((len(ai_pages) / len(self.governance_pages_data)) * 100, 1),
                'total_ai_references': sum(page['ai_analysis']['total_ai_references'] for page in ai_pages)
            },
            'by_page_type': {
                'total_distribution': page_type_stats,
                'ai_content_distribution': ai_by_type,
                'ai_coverage_by_type': {
                    page_type: round((ai_by_type.get(page_type, 0) / total) * 100, 1)
                    for page_type, total in page_type_stats.items()
                }
            },
            'most_ai_relevant_pages': [
                {
                    'title': page['title'],
                    'page_type': page['page_type'],
                    'ai_references': page['ai_analysis']['total_ai_references'],
                    'unique_ai_terms': len(page['ai_analysis']['unique_ai_terms']),
                    'last_modified': page['last_modified']
                }
                for page in ai_heavy_pages[:10]
            ],
            'ai_term_analysis': {
                'most_frequent_terms': dict(ai_term_frequency.most_common(15)),
                'total_unique_terms': len(ai_term_frequency)
            },
            'recent_activity': [
                {
                    'title': page['title'],
                    'last_modified': page['last_modified'],
                    'last_editor': page['last_editor'],
                    'edit_comment': page['edit_comment'][:100] + '...' if len(page['edit_comment']) > 100 else page['edit_comment']
                }
                for page in recent_ai_pages[:10]
            ]
        }

        return report

    def save_results(self):
        """Save analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate report
        report = self.generate_ai_governance_report()

        # Complete results
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'analysis_type': 'Wikipedia Specific Governance Pages AI Analysis',
                'pages_analyzed': len(self.governance_pages_data)
            },
            'report': report,
            'detailed_pages': self.governance_pages_data
        }

        # Save JSON
        json_filename = f"wikipedia_specific_governance_ai_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        self.log(f"Saved results to {json_filename}")

        # Save CSV of AI pages
        csv_filename = f"wikipedia_ai_governance_pages_{timestamp}.csv"

        ai_pages = [page for page in self.governance_pages_data if page['has_ai_content']]

        csv_data = []
        for page in ai_pages:
            csv_data.append({
                'title': page['title'],
                'page_type': page['page_type'],
                'ai_references': page['ai_analysis']['total_ai_references'],
                'unique_ai_terms': len(page['ai_analysis']['unique_ai_terms']),
                'ai_terms_found': ', '.join(page['ai_analysis']['unique_ai_terms']),
                'last_modified': page['last_modified'],
                'url': page['url']
            })

        import pandas as pd
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False)
        self.log(f"Saved CSV to {csv_filename}")

        return json_filename, csv_filename

    def print_summary(self):
        """Print analysis summary"""
        report = self.generate_ai_governance_report()

        print("\n" + "="*70)
        print("WIKIPEDIA SPECIFIC GOVERNANCE PAGES AI ANALYSIS")
        print("="*70)

        print(f"📊 ANALYSIS OVERVIEW:")
        print(f"• Total pages analyzed: {report['summary']['total_pages_analyzed']}")
        print(f"• Pages with AI content: {report['summary']['pages_with_ai_content']}")
        print(f"• AI coverage: {report['summary']['ai_coverage_percentage']}%")
        print(f"• Total AI references: {report['summary']['total_ai_references']}")

        print(f"\n📋 AI CONTENT BY PAGE TYPE:")
        for page_type, coverage in report['by_page_type']['ai_coverage_by_type'].items():
            total = report['by_page_type']['total_distribution'][page_type]
            ai_count = report['by_page_type']['ai_content_distribution'].get(page_type, 0)
            print(f"• {page_type}: {ai_count}/{total} pages ({coverage}%)")

        print(f"\n🔝 MOST AI-RELEVANT GOVERNANCE PAGES:")
        for i, page in enumerate(report['most_ai_relevant_pages'][:5], 1):
            print(f"{i}. {page['title']} ({page['page_type']})")
            print(f"   AI references: {page['ai_references']}, Unique terms: {page['unique_ai_terms']}")

        print(f"\n📈 MOST FREQUENT AI TERMS:")
        for term, count in list(report['ai_term_analysis']['most_frequent_terms'].items())[:10]:
            print(f"• {term}: {count} occurrences")

        print(f"\n⏰ RECENT AI-RELATED ACTIVITY:")
        for activity in report['recent_activity'][:3]:
            print(f"• {activity['title']}")
            print(f"  Modified: {activity['last_modified'][:10]} by {activity['last_editor']}")

        print("\n" + "="*70)

def main():
    """Main execution"""
    analyzer = WikipediaSpecificGovernanceAnalyzer()

    try:
        analyzer.analyze_governance_pages()
        json_file, csv_file = analyzer.save_results()
        analyzer.print_summary()

        print(f"\n✅ Specific governance page analysis completed!")
        print(f"📄 Detailed results: {json_file}")
        print(f"📊 CSV summary: {csv_file}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()