#!/usr/bin/env python3
"""
Mozilla Foundation Project Data Collector

This script collects comprehensive information about Mozilla Foundation projects,
focusing on repository locations and communication channels.

Usage:
    python3 mozilla_foundation_collector.py

Output:
    - mozilla_foundation_results.json: Complete project data
    - mozilla_foundation_summary.csv: Tabular summary
"""

import requests
import json
import csv
import time
from datetime import datetime
from collections import defaultdict, Counter
import os

class MozillaFoundationCollector:
    """Collector for Mozilla Foundation project data"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla Foundation Research Tool'
        })

        # Mozilla GitHub organizations to analyze
        self.mozilla_orgs = [
            'mozilla', 'mozilla-mobile', 'mozilla-services', 'mozilla-iot',
            'mozilla-extensions', 'mozilla-platform-ops', 'mozilla-releng',
            'mozilla-conduit', 'mozilla-frontend-infra', 'mozilla-lockwise',
            'mozilla-spidermonkey', 'mozmeao', 'mozillareality', 'firefoxux'
        ]

        self.projects = []
        self.stats = defaultdict(int)
        self.rate_limit_delay = 1

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_github_org_repos(self, org_name):
        """Get repositories for a GitHub organization"""
        self.log(f"Fetching repositories for {org_name}...")

        repos = []
        page = 1

        while True:
            try:
                url = f"https://api.github.com/orgs/{org_name}/repos"
                params = {'page': page, 'per_page': 100, 'type': 'all'}

                response = self.session.get(url, params=params, timeout=30)

                if response.status_code == 404:
                    self.log(f"Organization {org_name} not found")
                    break
                elif response.status_code != 200:
                    self.log(f"Error fetching {org_name} repos: {response.status_code}")
                    break

                page_repos = response.json()
                if not page_repos:
                    break

                repos.extend(page_repos)
                page += 1

                time.sleep(self.rate_limit_delay)

            except Exception as e:
                self.log(f"Error fetching repos for {org_name}: {e}")
                break

        return repos

    def analyze_repository(self, repo_data, org_name):
        """Analyze individual repository"""
        try:
            # Skip forks unless they're active
            if repo_data.get('fork', False) and repo_data.get('stargazers_count', 0) < 5:
                return None

            # Skip archived repositories
            if repo_data.get('archived', False):
                return None

            # Determine communication channels
            has_issues = repo_data.get('has_issues', False)
            has_wiki = repo_data.get('has_wiki', False)
            has_pages = repo_data.get('has_pages', False)

            # Extract topics/tags
            topics = repo_data.get('topics', [])

            # Determine project activity level
            activity_level = 'unknown'
            updated = repo_data.get('updated_at', '')
            if updated:
                try:
                    from datetime import datetime
                    last_update = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                    days_since_update = (datetime.now().astimezone() - last_update).days

                    if days_since_update < 30:
                        activity_level = 'active'
                    elif days_since_update < 365:
                        activity_level = 'maintained'
                    else:
                        activity_level = 'stale'
                except:
                    pass

            project_info = {
                'name': repo_data['name'],
                'full_name': repo_data['full_name'],
                'organization': org_name,
                'description': repo_data.get('description', ''),
                'url': repo_data['html_url'],
                'clone_url': repo_data['clone_url'],
                'repository_platform': 'GitHub',
                'primary_language': repo_data.get('language', ''),
                'stars': repo_data.get('stargazers_count', 0),
                'forks': repo_data.get('forks_count', 0),
                'watchers': repo_data.get('watchers_count', 0),
                'open_issues': repo_data.get('open_issues_count', 0),
                'size_kb': repo_data.get('size', 0),
                'created_at': repo_data.get('created_at', ''),
                'updated_at': repo_data.get('updated_at', ''),
                'activity_level': activity_level,
                'topics': topics,
                'license': repo_data.get('license', {}).get('name', '') if repo_data.get('license') else '',
                'communication_channels': {
                    'github_issues': has_issues,
                    'github_wiki': has_wiki,
                    'github_pages': has_pages,
                    'primary_platform': 'GitHub Issues' if has_issues else 'None'
                },
                'default_branch': repo_data.get('default_branch', 'main'),
                'is_fork': repo_data.get('fork', False),
                'visibility': 'public'  # All analyzed repos are public
            }

            return project_info

        except Exception as e:
            self.log(f"Error analyzing repository {repo_data.get('name', 'unknown')}: {e}")
            return None

    def collect_all_mozilla_projects(self):
        """Collect projects from all Mozilla organizations"""
        self.log("Starting Mozilla Foundation project collection...")

        for org_name in self.mozilla_orgs:
            self.log(f"Processing organization: {org_name}")

            repos = self.get_github_org_repos(org_name)

            for repo in repos:
                project_info = self.analyze_repository(repo, org_name)
                if project_info:
                    self.projects.append(project_info)

                    # Update statistics
                    self.stats['total_projects'] += 1
                    if project_info['communication_channels']['github_issues']:
                        self.stats['github_issues_projects'] += 1
                    if project_info['activity_level'] == 'active':
                        self.stats['active_projects'] += 1

            self.log(f"Processed {len(repos)} repositories from {org_name}")

        self.log(f"Collection complete: {len(self.projects)} total projects")

    def generate_statistics(self):
        """Generate comprehensive statistics"""
        if not self.projects:
            return {}

        total = len(self.projects)

        # Organization distribution
        org_counts = Counter(p['organization'] for p in self.projects)

        # Language analysis
        language_counts = Counter(p['primary_language'] for p in self.projects if p['primary_language'])

        # Activity analysis
        activity_counts = Counter(p['activity_level'] for p in self.projects)

        # Communication analysis
        issues_enabled = sum(1 for p in self.projects if p['communication_channels']['github_issues'])

        # License analysis
        license_counts = Counter(p['license'] for p in self.projects if p['license'])

        # Project size analysis (stars as popularity metric)
        star_counts = [p['stars'] for p in self.projects]
        avg_stars = sum(star_counts) / len(star_counts) if star_counts else 0

        statistics = {
            'collection_metadata': {
                'total_projects': total,
                'organizations_analyzed': len(self.mozilla_orgs),
                'analysis_date': datetime.now().isoformat(),
                'foundation': 'Mozilla Foundation'
            },
            'repository_platforms': {
                'github_adoption_rate': 100.0,  # All Mozilla projects on GitHub
                'total_github_projects': total
            },
            'communication_channels': {
                'github_issues_adoption': round((issues_enabled / total) * 100, 1),
                'projects_with_issues': issues_enabled,
                'primary_communication': 'GitHub Issues'
            },
            'organization_distribution': dict(org_counts.most_common()),
            'programming_languages': dict(language_counts.most_common(10)),
            'project_activity': dict(activity_counts),
            'licenses': dict(license_counts.most_common(10)),
            'project_metrics': {
                'average_stars': round(avg_stars, 1),
                'total_stars': sum(star_counts),
                'most_starred': max(star_counts) if star_counts else 0
            }
        }

        return statistics

    def save_results(self):
        """Save analysis results to files"""
        # Generate statistics
        statistics = self.generate_statistics()

        # Prepare complete results
        results = {
            'metadata': statistics['collection_metadata'],
            'statistics': statistics,
            'projects': self.projects
        }

        # Save JSON results
        json_filename = "../results/mozilla_foundation_results.json"
        os.makedirs(os.path.dirname(json_filename), exist_ok=True)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        self.log(f"Saved detailed results to {json_filename}")

        # Save CSV summary
        csv_filename = "../results/mozilla_foundation_summary.csv"

        # Prepare CSV data
        csv_data = []
        for project in self.projects:
            csv_data.append({
                'name': project['name'],
                'organization': project['organization'],
                'primary_language': project['primary_language'],
                'stars': project['stars'],
                'activity_level': project['activity_level'],
                'has_issues': project['communication_channels']['github_issues'],
                'license': project['license'],
                'url': project['url'],
                'description': project['description'][:100] + '...' if len(project['description']) > 100 else project['description']
            })

        import pandas as pd
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
        print("MOZILLA FOUNDATION ANALYSIS SUMMARY")
        print("="*60)

        print(f"📊 TOTAL PROJECTS: {stats['collection_metadata']['total_projects']}")
        print(f"🏢 ORGANIZATIONS: {stats['collection_metadata']['organizations_analyzed']}")

        print(f"\n🔧 REPOSITORY PLATFORMS:")
        print(f"• GitHub: {stats['repository_platforms']['total_github_projects']} projects (100%)")

        print(f"\n💬 COMMUNICATION CHANNELS:")
        print(f"• GitHub Issues adoption: {stats['communication_channels']['github_issues_adoption']}%")
        print(f"• Projects with Issues enabled: {stats['communication_channels']['projects_with_issues']}")

        print(f"\n🏢 TOP ORGANIZATIONS:")
        for org, count in list(stats['organization_distribution'].items())[:5]:
            print(f"• {org}: {count} projects")

        print(f"\n💻 TOP PROGRAMMING LANGUAGES:")
        for lang, count in list(stats['programming_languages'].items())[:5]:
            print(f"• {lang}: {count} projects")

        print(f"\n📈 PROJECT ACTIVITY:")
        for activity, count in stats['project_activity'].items():
            print(f"• {activity}: {count} projects")

        print(f"\n⚖️ TOP LICENSES:")
        for license_name, count in list(stats['licenses'].items())[:5]:
            print(f"• {license_name}: {count} projects")

        print(f"\n⭐ PROJECT METRICS:")
        print(f"• Average stars: {stats['project_metrics']['average_stars']}")
        print(f"• Total stars: {stats['project_metrics']['total_stars']:,}")
        print(f"• Most starred project: {stats['project_metrics']['most_starred']:,} stars")

        print("\n" + "="*60)

def main():
    """Main execution function"""
    collector = MozillaFoundationCollector()

    try:
        collector.collect_all_mozilla_projects()
        json_file, csv_file = collector.save_results()
        collector.print_summary()

        print(f"\n✅ Mozilla Foundation analysis completed!")
        print(f"📄 Detailed results: {json_file}")
        print(f"📊 CSV summary: {csv_file}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()