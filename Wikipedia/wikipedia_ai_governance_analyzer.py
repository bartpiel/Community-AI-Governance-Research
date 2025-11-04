#!/usr/bin/env python3
"""
Wikipedia AI Governance Analysis

This script analyzes Wikipedia's governance documents related to AI usage,
including policies, guidelines, essays, and other governance instruments.

Wikipedia governance hierarchy:
- Policies: Binding rules and requirements
- Guidelines: Best practices and recommendations
- Essays: Individual opinions and commentary
- Process pages: How to do things on Wikipedia
- WikiProjects: Collaborative project coordination
- How-to pages: Instructions and tutorials
- Information pages: Reference and explanatory content
- Supplements: Additional supporting documentation
- Community discussions: Ongoing debates and notices

API endpoints:
- REST API: https://en.wikipedia.org/api/rest_v1/
- Action API: https://en.wikipedia.org/w/api.php
- Search API: For finding AI-related content
"""

import requests
import json
import time
import re
from datetime import datetime
from collections import defaultdict, Counter
from urllib.parse import quote
import os

class WikipediaAIGovernanceAnalyzer:
    """Analyzer for Wikipedia AI governance documents"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wikipedia AI Governance Research Tool (Educational Research)'
        })

        # Wikipedia API endpoints
        self.api_base = "https://en.wikipedia.org/w/api.php"
        self.rest_base = "https://en.wikipedia.org/api/rest_v1"

        # Rate limiting
        self.request_delay = 1  # Respectful delay between requests

        # Data collections
        self.ai_documents = []
        self.governance_categories = {
            'policies': [],
            'guidelines': [],
            'essays': [],
            'process_pages': [],
            'wiki_projects': [],
            'how_to_pages': [],
            'information_pages': [],
            'supplements': [],
            'community_discussions': []
        }

        # AI-related search terms
        self.ai_search_terms = [
            'artificial intelligence',
            'machine learning',
            'AI',
            'bot',
            'automation',
            'algorithm',
            'neural network',
            'chatbot',
            'generative AI',
            'LLM',
            'large language model',
            'ChatGPT',
            'GPT',
            'AI-generated',
            'automated editing',
            'AI tool',
            'AI assistance'
        ]

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def search_wikipedia_pages(self, search_term, namespace=0, limit=50):
        """Search Wikipedia pages using the API"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_term,
                'srnamespace': namespace,
                'srlimit': limit,
                'srprop': 'size|wordcount|timestamp|snippet'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'query' in data and 'search' in data['query']:
                return data['query']['search']

            return []

        except Exception as e:
            self.log(f"Error searching for '{search_term}': {e}")
            return []

    def get_page_content(self, page_title):
        """Get the full content of a Wikipedia page"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_title,
                'prop': 'extracts|info|categories',
                'exlimit': 1,
                'explaintext': True,
                'inprop': 'url'
            }

            response = self.session.get(self.api_base, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'query' in data and 'pages' in data['query']:
                page_data = list(data['query']['pages'].values())[0]
                return page_data

            return None

        except Exception as e:
            self.log(f"Error getting content for '{page_title}': {e}")
            return None

    def search_governance_namespaces(self):
        """Search for AI-related content in Wikipedia governance namespaces"""

        # Wikipedia namespaces for governance content
        governance_namespaces = {
            'main': 0,           # Main articles
            'wikipedia': 4,      # Wikipedia namespace (policies, guidelines)
            'help': 12,          # Help pages
            'category': 14,      # Categories
            'project': 102       # WikiProject namespace
        }

        all_results = {}

        for namespace_name, namespace_id in governance_namespaces.items():
            self.log(f"Searching {namespace_name} namespace for AI governance content...")

            namespace_results = []

            for search_term in self.ai_search_terms:
                self.log(f"  Searching for: {search_term}")

                results = self.search_wikipedia_pages(search_term, namespace_id, 20)

                for result in results:
                    # Filter for governance-related content
                    title = result['title']
                    snippet = result.get('snippet', '').lower()

                    # Look for governance keywords in title or snippet
                    governance_keywords = [
                        'policy', 'guideline', 'essay', 'process', 'procedure',
                        'rule', 'standard', 'convention', 'practice', 'protocol',
                        'governance', 'regulation', 'requirement', 'recommendation'
                    ]

                    is_governance = any(keyword in title.lower() or keyword in snippet
                                      for keyword in governance_keywords)

                    if is_governance or namespace_id in [4, 12]:  # Wikipedia/Help namespaces
                        result['search_term'] = search_term
                        result['namespace'] = namespace_name
                        namespace_results.append(result)

                time.sleep(self.request_delay)

            all_results[namespace_name] = namespace_results
            self.log(f"Found {len(namespace_results)} results in {namespace_name} namespace")

        return all_results

    def categorize_document(self, page_title, page_content):
        """Categorize a document based on Wikipedia governance hierarchy"""

        title_lower = page_title.lower()
        content_lower = page_content.get('extract', '').lower() if page_content else ''

        # Check categories
        categories = page_content.get('categories', []) if page_content else []
        category_names = [cat.get('title', '').lower() for cat in categories]

        # Categorization logic
        if any('policy' in title_lower or 'policy' in cat for cat in category_names):
            return 'policies'
        elif any('guideline' in title_lower or 'guideline' in cat for cat in category_names):
            return 'guidelines'
        elif any('essay' in title_lower or 'essay' in cat for cat in category_names):
            return 'essays'
        elif 'process' in title_lower or 'procedure' in title_lower:
            return 'process_pages'
        elif 'wikiproject' in title_lower:
            return 'wiki_projects'
        elif 'how to' in title_lower or 'howto' in title_lower:
            return 'how_to_pages'
        elif any('information' in title_lower or 'info' in title_lower or
                'about' in title_lower for term in [title_lower]):
            return 'information_pages'
        elif 'discussion' in title_lower or 'talk' in title_lower or 'rfc' in title_lower:
            return 'community_discussions'
        else:
            return 'supplements'  # Default category

    def analyze_ai_governance_content(self):
        """Main analysis function"""
        self.log("Starting Wikipedia AI governance analysis...")

        # Search across governance namespaces
        search_results = self.search_governance_namespaces()

        # Process and categorize results
        all_ai_pages = []

        for namespace, results in search_results.items():
            self.log(f"Processing {len(results)} results from {namespace} namespace...")

            for result in results:
                page_title = result['title']

                # Get detailed page content
                page_content = self.get_page_content(page_title)

                if page_content:
                    # Categorize the document
                    category = self.categorize_document(page_title, page_content)

                    # Extract AI-related content
                    ai_analysis = self.extract_ai_content(page_content)

                    document_info = {
                        'title': page_title,
                        'url': page_content.get('fullurl', ''),
                        'category': category,
                        'namespace': namespace,
                        'word_count': result.get('wordcount', 0),
                        'size': result.get('size', 0),
                        'timestamp': result.get('timestamp', ''),
                        'snippet': result.get('snippet', ''),
                        'search_term': result.get('search_term', ''),
                        'ai_content_analysis': ai_analysis,
                        'categories': [cat.get('title', '') for cat in page_content.get('categories', [])]
                    }

                    all_ai_pages.append(document_info)
                    self.governance_categories[category].append(document_info)

                time.sleep(self.request_delay)

        self.ai_documents = all_ai_pages
        self.log(f"Analysis complete: {len(all_ai_pages)} AI governance documents found")

        return all_ai_pages

    def extract_ai_content(self, page_content):
        """Extract and analyze AI-related content from a page"""

        extract = page_content.get('extract', '')

        if not extract:
            return {'ai_mentions': 0, 'key_terms': [], 'relevance_score': 0}

        # Count AI mentions
        ai_mentions = 0
        found_terms = []

        for term in self.ai_search_terms:
            count = extract.lower().count(term.lower())
            if count > 0:
                ai_mentions += count
                found_terms.append({'term': term, 'count': count})

        # Calculate relevance score (AI mentions per 1000 words)
        word_count = len(extract.split())
        relevance_score = (ai_mentions / word_count * 1000) if word_count > 0 else 0

        # Extract key sentences mentioning AI
        sentences = extract.split('.')
        ai_sentences = []

        for sentence in sentences[:50]:  # Limit to first 50 sentences
            if any(term.lower() in sentence.lower() for term in self.ai_search_terms):
                ai_sentences.append(sentence.strip())

        return {
            'ai_mentions': ai_mentions,
            'key_terms': found_terms,
            'relevance_score': round(relevance_score, 2),
            'ai_sentences': ai_sentences[:10],  # Top 10 relevant sentences
            'word_count': word_count
        }

    def generate_governance_statistics(self):
        """Generate statistics about AI governance on Wikipedia"""

        if not self.ai_documents:
            return {}

        # Overall statistics
        total_documents = len(self.ai_documents)

        # Category distribution
        category_counts = Counter(doc['category'] for doc in self.ai_documents)

        # Namespace distribution
        namespace_counts = Counter(doc['namespace'] for doc in self.ai_documents)

        # Search term effectiveness
        search_term_counts = Counter(doc['search_term'] for doc in self.ai_documents)

        # Relevance analysis
        relevance_scores = [doc['ai_content_analysis']['relevance_score'] for doc in self.ai_documents]
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

        # Most relevant documents
        most_relevant = sorted(self.ai_documents,
                             key=lambda x: x['ai_content_analysis']['relevance_score'],
                             reverse=True)[:10]

        # AI term frequency across all documents
        all_terms = []
        for doc in self.ai_documents:
            all_terms.extend([term['term'] for term in doc['ai_content_analysis']['key_terms']])

        term_frequency = Counter(all_terms)

        statistics = {
            'collection_metadata': {
                'total_documents': total_documents,
                'analysis_date': datetime.now().isoformat(),
                'search_terms_used': len(self.ai_search_terms)
            },
            'governance_distribution': {
                'by_category': dict(category_counts),
                'by_namespace': dict(namespace_counts)
            },
            'search_effectiveness': {
                'by_search_term': dict(search_term_counts.most_common()),
                'average_relevance_score': round(avg_relevance, 2)
            },
            'content_analysis': {
                'most_relevant_documents': [
                    {
                        'title': doc['title'],
                        'category': doc['category'],
                        'relevance_score': doc['ai_content_analysis']['relevance_score'],
                        'ai_mentions': doc['ai_content_analysis']['ai_mentions']
                    }
                    for doc in most_relevant
                ],
                'top_ai_terms': dict(term_frequency.most_common(15))
            }
        }

        return statistics

    def save_results(self):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate statistics
        statistics = self.generate_governance_statistics()

        # Prepare complete results
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'analysis_type': 'Wikipedia AI Governance Analysis',
                'total_documents_found': len(self.ai_documents)
            },
            'statistics': statistics,
            'governance_categories': {
                category: len(docs) for category, docs in self.governance_categories.items()
            },
            'documents': self.ai_documents
        }

        # Save detailed JSON results
        json_filename = f"wikipedia_ai_governance_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        self.log(f"Saved detailed results to {json_filename}")

        # Save CSV summary
        csv_filename = f"wikipedia_ai_governance_summary_{timestamp}.csv"

        # Prepare CSV data
        csv_data = []
        for doc in self.ai_documents:
            csv_data.append({
                'title': doc['title'],
                'category': doc['category'],
                'namespace': doc['namespace'],
                'relevance_score': doc['ai_content_analysis']['relevance_score'],
                'ai_mentions': doc['ai_content_analysis']['ai_mentions'],
                'word_count': doc['ai_content_analysis']['word_count'],
                'search_term': doc['search_term'],
                'url': doc['url']
            })

        import pandas as pd
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False)
        self.log(f"Saved CSV summary to {csv_filename}")

        return json_filename, csv_filename

    def print_analysis_summary(self):
        """Print comprehensive analysis summary"""
        if not self.ai_documents:
            print("No AI governance documents found")
            return

        stats = self.generate_governance_statistics()

        print("\n" + "="*70)
        print("WIKIPEDIA AI GOVERNANCE ANALYSIS SUMMARY")
        print("="*70)

        print(f"📊 TOTAL DOCUMENTS FOUND: {stats['collection_metadata']['total_documents']}")
        print(f"🔍 SEARCH TERMS USED: {stats['collection_metadata']['search_terms_used']}")

        print(f"\n📋 GOVERNANCE DOCUMENT DISTRIBUTION:")
        for category, count in stats['governance_distribution']['by_category'].items():
            category_name = category.replace('_', ' ').title()
            print(f"• {category_name}: {count} documents")

        print(f"\n🌐 NAMESPACE DISTRIBUTION:")
        for namespace, count in stats['governance_distribution']['by_namespace'].items():
            print(f"• {namespace.title()}: {count} documents")

        print(f"\n🎯 SEARCH EFFECTIVENESS:")
        print(f"• Average relevance score: {stats['search_effectiveness']['average_relevance_score']}")
        print(f"• Most effective search terms:")
        for term, count in list(stats['search_effectiveness']['by_search_term'].items())[:5]:
            print(f"  - '{term}': {count} documents")

        print(f"\n🔝 MOST RELEVANT DOCUMENTS:")
        for i, doc in enumerate(stats['content_analysis']['most_relevant_documents'][:5], 1):
            print(f"{i}. {doc['title']} ({doc['category']})")
            print(f"   Relevance: {doc['relevance_score']}, AI mentions: {doc['ai_mentions']}")

        print(f"\n📈 TOP AI TERMS FOUND:")
        for term, count in list(stats['content_analysis']['top_ai_terms'].items())[:10]:
            print(f"• {term}: {count} occurrences")

        print(f"\n📋 GOVERNANCE CATEGORY BREAKDOWN:")
        for category, docs in self.governance_categories.items():
            if docs:
                category_name = category.replace('_', ' ').title()
                print(f"\n{category_name} ({len(docs)} documents):")
                for doc in docs[:3]:  # Show top 3 per category
                    relevance = doc['ai_content_analysis']['relevance_score']
                    print(f"  • {doc['title']} (relevance: {relevance})")
                if len(docs) > 3:
                    print(f"  ... and {len(docs) - 3} more documents")

        print("\n" + "="*70)

def main():
    """Main execution function"""
    analyzer = WikipediaAIGovernanceAnalyzer()

    try:
        # Run the analysis
        ai_documents = analyzer.analyze_ai_governance_content()

        # Save results
        json_file, csv_file = analyzer.save_results()

        # Print summary
        analyzer.print_analysis_summary()

        print(f"\n✅ Wikipedia AI governance analysis completed!")
        print(f"📄 Detailed results: {json_file}")
        print(f"📊 CSV summary: {csv_file}")
        print(f"🔍 Found {len(ai_documents)} AI governance documents across Wikipedia")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()