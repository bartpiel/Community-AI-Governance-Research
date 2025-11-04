#!/usr/bin/env python3
"""
Wikipedia AI Policy Discussions Analyzer

This script searches for recent AI-related policy discussions and proposals
on Wikipedia by analyzing community discussion pages and policy proposal areas.
"""

import requests
import json
import time
from datetime import datetime, timedelta
import re

class WikipediaAIPolicyDiscussionAnalyzer:
    """Analyzer for AI-related policy discussions on Wikipedia"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia AI Policy Research Tool (Educational Research)'
        })

        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.request_delay = 1

        # Key discussion and policy proposal pages
        self.discussion_pages = [
            # Main policy discussion areas
            "Wikipedia:Village pump (policy)",
            "Wikipedia:Village pump (proposals)",
            "Wikipedia:Village pump (technical)",
            "Wikipedia:Village pump (miscellaneous)",

            # Policy development areas
            "Wikipedia:Requests for comment",
            "Wikipedia:Policy proposals",
            "Wikipedia:Guideline proposals",

            # AI-specific discussion areas
            "Wikipedia talk:Artificial intelligence",
            "Wikipedia talk:Bot policy",
            "Wikipedia talk:Reliable sources",

            # Administrative areas
            "Wikipedia:Administrators' noticeboard",
            "Wikipedia:Administrators' noticeboard/Incidents",
            "Wikipedia:Bureaucrats' noticeboard",

            # Community discussion
            "Wikipedia:Help desk",
            "Wikipedia:Teahouse",
            "Wikipedia:Reference desk/Computing",

            # Bot-related discussions
            "Wikipedia:Bot requests",
            "Wikipedia talk:Bots",

            # Arbitration and conflicts
            "Wikipedia:Arbitration/Requests",
            "Wikipedia:Dispute resolution noticeboard"
        ]

        self.ai_discussion_keywords = [
            'AI policy', 'AI guidelines', 'AI-generated content', 'ChatGPT',
            'artificial intelligence policy', 'machine learning policy',
            'generative AI', 'language model', 'AI bot', 'AI tool',
            'AI detection', 'AI verification', 'synthetic content',
            'automated content generation', 'AI assistance', 'AI ethics'
        ]

        self.discussion_data = []

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def search_page_for_ai_discussions(self, page_title):
        """Search a page for AI-related discussions"""
        try:
            # Get recent revisions to find active discussions
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_title,
                'prop': 'revisions',
                'rvprop': 'content|timestamp|user|comment',
                'rvlimit': 50,  # Last 50 revisions
                'rvstart': (datetime.now() - timedelta(days=90)).isoformat()  # Last 90 days
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page_data = list(data['query']['pages'].values())[0]

                if 'revisions' in page_data:
                    # Get current content
                    current_content = page_data['revisions'][0].get('*', '') if page_data['revisions'] else ''

                    # Search for AI discussions in current content
                    ai_discussions = self.extract_ai_discussions(current_content, page_title)

                    # Check recent edit comments for AI activity
                    recent_ai_activity = []
                    for revision in page_data['revisions']:
                        comment = revision.get('comment', '').lower()
                        if any(keyword.lower() in comment for keyword in self.ai_discussion_keywords):
                            recent_ai_activity.append({
                                'timestamp': revision.get('timestamp'),
                                'user': revision.get('user'),
                                'comment': revision.get('comment'),
                                'ai_related': True
                            })

                    return {
                        'page_title': page_title,
                        'current_ai_discussions': ai_discussions,
                        'recent_ai_activity': recent_ai_activity,
                        'last_checked': datetime.now().isoformat()
                    }

            return None

        except Exception as e:
            self.log(f"Error searching '{page_title}': {e}")
            return None

    def extract_ai_discussions(self, content, page_title):
        """Extract AI-related discussion sections from page content"""

        if not content:
            return []

        discussions = []

        # Split content into sections
        sections = re.split(r'\n=+\s*([^=]+)\s*=+', content)

        current_section = "Introduction"

        for i, part in enumerate(sections):
            if i % 2 == 0:  # Content
                section_content = part

                # Check if section contains AI discussion
                ai_found = False
                for keyword in self.ai_discussion_keywords:
                    if keyword.lower() in section_content.lower():
                        ai_found = True
                        break

                if ai_found:
                    # Extract discussion threads
                    discussion_threads = self.extract_discussion_threads(section_content, current_section)
                    discussions.extend(discussion_threads)

            else:  # Section header
                current_section = part.strip()

        return discussions

    def extract_discussion_threads(self, section_content, section_title):
        """Extract individual discussion threads from section content"""

        threads = []

        # Look for discussion patterns (signatures, timestamps, etc.)
        # Wikipedia discussions often have user signatures and timestamps
        signature_pattern = r'\[\[User[^]]*\]\].*?(\d{2}:\d{2}.*?\d{4}|\d{4}-\d{2}-\d{2})'

        # Split by signatures to identify individual comments
        comments = re.split(signature_pattern, section_content)

        for i in range(0, len(comments)-2, 3):  # Process in groups of 3 (comment, user, timestamp)
            comment_text = comments[i].strip()

            if len(comment_text) > 50:  # Filter out very short comments
                # Check if this comment discusses AI
                ai_keywords_found = []
                for keyword in self.ai_discussion_keywords:
                    if keyword.lower() in comment_text.lower():
                        ai_keywords_found.append(keyword)

                if ai_keywords_found:
                    threads.append({
                        'section': section_title,
                        'comment_preview': comment_text[:300] + '...' if len(comment_text) > 300 else comment_text,
                        'ai_keywords': ai_keywords_found,
                        'estimated_length': len(comment_text)
                    })

        return threads

    def search_recent_ai_proposals(self):
        """Search for recent AI-related policy proposals"""
        try:
            # Search for pages with AI-related titles
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': 'AI policy OR "artificial intelligence" OR "AI-generated" OR "ChatGPT policy"',
                'srnamespace': '4|5',  # Wikipedia and Wikipedia talk namespaces
                'srlimit': 50,
                'srinfo': 'totalhits'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            proposals = []
            if 'query' in data and 'search' in data['query']:
                for result in data['query']['search']:
                    proposals.append({
                        'title': result['title'],
                        'snippet': result['snippet'],
                        'timestamp': result.get('timestamp'),
                        'size': result.get('size', 0)
                    })

            return proposals

        except Exception as e:
            self.log(f"Error searching for AI proposals: {e}")
            return []

    def analyze_ai_discussions(self):
        """Analyze all discussion pages for AI-related content"""
        self.log("Starting analysis of AI policy discussions...")

        for page_title in self.discussion_pages:
            self.log(f"Searching: {page_title}")

            discussion_analysis = self.search_page_for_ai_discussions(page_title)

            if discussion_analysis:
                ai_discussion_count = len(discussion_analysis['current_ai_discussions'])
                ai_activity_count = len(discussion_analysis['recent_ai_activity'])

                if ai_discussion_count > 0 or ai_activity_count > 0:
                    self.log(f"  ✅ Found {ai_discussion_count} AI discussions, {ai_activity_count} recent AI activities")
                    self.discussion_data.append(discussion_analysis)
                else:
                    self.log(f"  ❌ No AI discussions found")
            else:
                self.log(f"  ⚠️ Could not analyze page")

            time.sleep(self.request_delay)

        # Search for recent AI proposals
        self.log("Searching for recent AI policy proposals...")
        ai_proposals = self.search_recent_ai_proposals()

        self.log(f"Analysis complete: {len(self.discussion_data)} pages with AI discussions")
        self.log(f"Found {len(ai_proposals)} AI-related proposals")

        return self.discussion_data, ai_proposals

    def generate_discussion_report(self, ai_proposals):
        """Generate report on AI discussions and proposals"""

        if not self.discussion_data and not ai_proposals:
            return {}

        # Count discussions by page type
        page_type_discussions = {}
        total_discussions = 0
        total_activities = 0

        for page_data in self.discussion_data:
            page_title = page_data['page_title']
            discussion_count = len(page_data['current_ai_discussions'])
            activity_count = len(page_data['recent_ai_activity'])

            total_discussions += discussion_count
            total_activities += activity_count

            # Categorize page type
            if 'village pump' in page_title.lower():
                page_type = 'Village Pump'
            elif 'talk:' in page_title.lower():
                page_type = 'Talk Page'
            elif 'noticeboard' in page_title.lower():
                page_type = 'Noticeboard'
            elif 'help' in page_title.lower() or 'teahouse' in page_title.lower():
                page_type = 'Help/Community'
            else:
                page_type = 'Other'

            if page_type not in page_type_discussions:
                page_type_discussions[page_type] = []

            page_type_discussions[page_type].append({
                'page': page_title,
                'discussions': discussion_count,
                'activities': activity_count
            })

        # Most active discussion areas
        most_active = sorted(self.discussion_data,
                           key=lambda x: len(x['current_ai_discussions']) + len(x['recent_ai_activity']),
                           reverse=True)

        report = {
            'summary': {
                'pages_with_ai_discussions': len(self.discussion_data),
                'total_ai_discussions': total_discussions,
                'total_recent_activities': total_activities,
                'ai_proposals_found': len(ai_proposals)
            },
            'by_page_type': page_type_discussions,
            'most_active_pages': [
                {
                    'page': page['page_title'],
                    'total_ai_discussions': len(page['current_ai_discussions']),
                    'recent_ai_activities': len(page['recent_ai_activity'])
                }
                for page in most_active[:10]
            ],
            'recent_proposals': ai_proposals[:10],
            'analysis_date': datetime.now().isoformat()
        }

        return report

    def save_discussion_results(self, ai_proposals):
        """Save discussion analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate report
        report = self.generate_discussion_report(ai_proposals)

        # Complete results
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'analysis_type': 'Wikipedia AI Policy Discussions Analysis',
                'pages_analyzed': len(self.discussion_pages),
                'ai_discussion_pages': len(self.discussion_data)
            },
            'report': report,
            'detailed_discussions': self.discussion_data,
            'ai_proposals': ai_proposals
        }

        # Save JSON
        json_filename = f"wikipedia_ai_discussions_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        self.log(f"Saved discussion results to {json_filename}")

        return json_filename

    def print_discussion_summary(self, ai_proposals):
        """Print discussion analysis summary"""
        report = self.generate_discussion_report(ai_proposals)

        print("\n" + "="*70)
        print("WIKIPEDIA AI POLICY DISCUSSIONS ANALYSIS")
        print("="*70)

        print(f"📊 DISCUSSION OVERVIEW:")
        print(f"• Pages with AI discussions: {report['summary']['pages_with_ai_discussions']}")
        print(f"• Total AI discussions found: {report['summary']['total_ai_discussions']}")
        print(f"• Recent AI activities: {report['summary']['total_recent_activities']}")
        print(f"• AI proposals found: {report['summary']['ai_proposals_found']}")

        if report['by_page_type']:
            print(f"\n📋 DISCUSSIONS BY PAGE TYPE:")
            for page_type, pages in report['by_page_type'].items():
                total_discussions = sum(p['discussions'] for p in pages)
                total_activities = sum(p['activities'] for p in pages)
                print(f"• {page_type}: {len(pages)} pages, {total_discussions} discussions, {total_activities} activities")

        if report['most_active_pages']:
            print(f"\n🔝 MOST ACTIVE AI DISCUSSION PAGES:")
            for i, page in enumerate(report['most_active_pages'][:5], 1):
                if page['total_ai_discussions'] > 0 or page['recent_ai_activities'] > 0:
                    print(f"{i}. {page['page']}")
                    print(f"   Discussions: {page['total_ai_discussions']}, Activities: {page['recent_ai_activities']}")

        if report['recent_proposals']:
            print(f"\n📝 RECENT AI-RELATED PROPOSALS:")
            for i, proposal in enumerate(report['recent_proposals'][:3], 1):
                print(f"{i}. {proposal['title']}")
                snippet = proposal['snippet'].replace('<span class="searchmatch">', '').replace('</span>', '')
                print(f"   {snippet[:100]}...")

        print("\n" + "="*70)

def main():
    """Main execution"""
    analyzer = WikipediaAIPolicyDiscussionAnalyzer()

    try:
        discussion_data, ai_proposals = analyzer.analyze_ai_discussions()
        json_file = analyzer.save_discussion_results(ai_proposals)
        analyzer.print_discussion_summary(ai_proposals)

        print(f"\n✅ AI policy discussions analysis completed!")
        print(f"📄 Detailed results: {json_file}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()