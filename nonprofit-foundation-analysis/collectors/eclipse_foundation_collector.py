#!/usr/bin/env python3
"""
Eclipse Foundation Project Data Collector

This script collects comprehensive information about Eclipse Foundation projects,
focusing on repository locations and communication channels.

Usage:
    python3 eclipse_foundation_collector.py

Output:
    - eclipse_foundation_results.json: Complete project data
    - eclipse_foundation_summary.csv: Tabular summary
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from collections import defaultdict, Counter
import os

class EclipseFoundationCollector:
    """Collector for Eclipse Foundation project data"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Eclipse Foundation Research Tool'
        })

        self.base_url = "https://projects.eclipse.org"
        self.api_base = "https://projects.eclipse.org/api"
        self.projects = []
        self.stats = defaultdict(int)

        # Rate limiting
        self.request_delay = 0.5

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_all_projects(self):
        """Get list of all Eclipse projects"""
        self.log("Fetching Eclipse project list...")

        try:
            response = self.session.get(f"{self.api_base}/projects", timeout=30)
            response.raise_for_status()

            projects_data = response.json()
            self.log(f"Found {len(projects_data)} projects")

            return projects_data

        except Exception as e:
            self.log(f"Error fetching project list: {e}")
            return []

    def analyze_project_details(self, project_data):
        """Analyze individual project details"""
        project_id = project_data.get('id', '')
        project_name = project_data.get('name', '')

        try:
            time.sleep(self.request_delay)

            # Get detailed project information
            detail_url = f"{self.api_base}/projects/{project_id}"
            response = self.session.get(detail_url, timeout=20)

            if response.status_code != 200:
                return None

            details = response.json()

            # Extract repository information
            repositories = []
            github_org = ""

            # Look for GitHub repositories in various fields
            github_url = details.get('github_url', '')
            if github_url:
                repositories.append(github_url)
                if 'github.com' in github_url:
                    parts = github_url.split('/')
                    if len(parts) >= 4:
                        github_org = parts[3]

            # Extract mailing lists
            mailing_lists = []
            dev_list = details.get('dev_list', {})
            if dev_list and dev_list.get('url'):
                mailing_lists.append(dev_list['url'])

            # Extract communication channels
            communication = {
                'mailing_lists': mailing_lists,
                'github_issues': bool(github_url and 'github.com' in github_url),
                'forums': details.get('forums', []),
                'irc': details.get('irc', ''),
                'chat': details.get('chat', '')
            }

            project_info = {
                'name': project_name,
                'project_id': project_id,
                'description': details.get('description', ''),
                'state': details.get('state', ''),
                'category': details.get('categories', []),
                'website': details.get('website', {}).get('url', ''),
                'repositories': repositories,
                'repository_platform': 'GitHub' if github_url else 'Unknown',
                'github_organization': github_org,
                'communication_channels': communication,
                'license': details.get('licenses', []),
                'technology_types': details.get('technology_types', []),
                'industry_collaborations': details.get('industry_collaborations', [])
            }

            return project_info

        except Exception as e:
            self.log(f"Error analyzing project {project_id}: {e}")
            return None

    def analyze_all_projects(self):
        """Analyze all Eclipse projects"""
        projects_data = self.get_all_projects()

        if not projects_data:
            self.log("No projects found")
            return

        self.log(f"Analyzing {len(projects_data)} projects...")

        # Process projects with threading for efficiency
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_project = {
                executor.submit(self.analyze_project_details, project): project
                for project in projects_data
            }

            for future in as_completed(future_to_project):
                project_info = future.result()
                if project_info:
                    self.projects.append(project_info)

                    # Update statistics
                    self.stats['total_projects'] += 1
                    if project_info['repository_platform'] == 'GitHub':
                        self.stats['github_projects'] += 1
                    if project_info['communication_channels']['github_issues']:
                        self.stats['github_issues_projects'] += 1
                    if project_info['communication_channels']['mailing_lists']:
                        self.stats['mailing_list_projects'] += 1

        self.log(f"Analysis complete: {len(self.projects)} projects processed")

    def generate_statistics(self):
        """Generate analysis statistics"""
        if not self.projects:
            return {}

        total = len(self.projects)

        # Repository platform analysis
        platform_counts = Counter(p['repository_platform'] for p in self.projects)

        # Communication analysis
        github_issues = sum(1 for p in self.projects if p['communication_channels']['github_issues'])
        mailing_lists = sum(1 for p in self.projects if p['communication_channels']['mailing_lists'])

        # State analysis
        state_counts = Counter(p['state'] for p in self.projects)

        # Category analysis
        all_categories = []
        for project in self.projects:
            if isinstance(project['category'], list):
                all_categories.extend(project['category'])
            elif project['category']:
                all_categories.append(project['category'])

        category_counts = Counter(all_categories)

        statistics = {
            'collection_metadata': {
                'total_projects': total,
                'analysis_date': datetime.now().isoformat(),
                'foundation': 'Eclipse Foundation'
            },
            'repository_platforms': {
                'platform_distribution': dict(platform_counts),
                'github_adoption_rate': round((platform_counts.get('GitHub', 0) / total) * 100, 1)
            },
            'communication_channels': {
                'github_issues_adoption': round((github_issues / total) * 100, 1),
                'mailing_list_usage': round((mailing_lists / total) * 100, 1),
                'projects_with_github_issues': github_issues,
                'projects_with_mailing_lists': mailing_lists
            },
            'project_states': dict(state_counts),
            'project_categories': dict(category_counts.most_common(10)),
            'top_github_organizations': self._get_top_github_orgs()
        }

        return statistics

    def _get_top_github_orgs(self):
        """Get top GitHub organizations by project count"""
        org_counts = Counter(p['github_organization'] for p in self.projects if p['github_organization'])
        return dict(org_counts.most_common(10))

    def save_results(self):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate statistics
        statistics = self.generate_statistics()

        # Prepare complete results
        results = {
            'metadata': statistics['collection_metadata'],
            'statistics': statistics,
            'projects': self.projects
        }

        # Save JSON results
        json_filename = f"../results/eclipse_foundation_results.json"
        os.makedirs(os.path.dirname(json_filename), exist_ok=True)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        self.log(f"Saved detailed results to {json_filename}")

        # Save CSV summary
        csv_filename = f"../results/eclipse_foundation_summary.csv"

        # Prepare CSV data
        csv_data = []
        for project in self.projects:
            csv_data.append({
                'name': project['name'],
                'project_id': project['project_id'],
                'state': project['state'],
                'repository_platform': project['repository_platform'],
                'github_organization': project['github_organization'],
                'has_github_issues': project['communication_channels']['github_issues'],
                'has_mailing_lists': bool(project['communication_channels']['mailing_lists']),
                'website': project['website'],
                'description': project['description'][:100] + '...' if len(project['description']) > 100 else project['description']
            })

        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False)
        self.log(f"Saved CSV summary to {csv_filename}")

        return json_filename, csv_filename

    def print_summary(self):
        """Print analysis summary"""
        if not self.projects:
            print("No projects analyzed")
            return

        stats = self.generate_statistics()

        print("\n" + "="*60)
        print("ECLIPSE FOUNDATION ANALYSIS SUMMARY")
        print("="*60)

        print(f"📊 TOTAL PROJECTS: {stats['collection_metadata']['total_projects']}")

        print(f"\n🔧 REPOSITORY PLATFORMS:")
        for platform, count in stats['repository_platforms']['platform_distribution'].items():
            percentage = (count / stats['collection_metadata']['total_projects']) * 100
            print(f"• {platform}: {count} projects ({percentage:.1f}%)")

        print(f"\n💬 COMMUNICATION CHANNELS:")
        print(f"• GitHub Issues adoption: {stats['communication_channels']['github_issues_adoption']}%")
        print(f"• Mailing list usage: {stats['communication_channels']['mailing_list_usage']}%")

        print(f"\n📈 PROJECT STATES:")
        for state, count in stats['project_states'].items():
            print(f"• {state}: {count} projects")

        print(f"\n🏆 TOP CATEGORIES:")
        for category, count in list(stats['project_categories'].items())[:5]:
            print(f"• {category}: {count} projects")

        print(f"\n🔗 TOP GITHUB ORGANIZATIONS:")
        for org, count in list(stats['top_github_organizations'].items())[:5]:
            print(f"• {org}: {count} projects")

        print("\n" + "="*60)

def main():
    """Main execution function"""
    collector = EclipseFoundationCollector()

    try:
        collector.analyze_all_projects()
        json_file, csv_file = collector.save_results()
        collector.print_summary()

        print(f"\n✅ Eclipse Foundation analysis completed!")
        print(f"📄 Detailed results: {json_file}")
        print(f"📊 CSV summary: {csv_file}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()