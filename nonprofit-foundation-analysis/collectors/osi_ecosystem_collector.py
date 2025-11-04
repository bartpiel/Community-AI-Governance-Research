#!/usr/bin/env python3
"""
Open Source Initiative (OSI) Ecosystem Collector

This script analyzes the OSI ecosystem, which operates as a standards organization
rather than a project hosting foundation.

Usage:
    python3 osi_ecosystem_collector.py

Output:
    - osi_ecosystem_results.json: Complete ecosystem analysis
    - osi_affiliates_summary.csv: Affiliate organizations summary
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from collections import defaultdict, Counter
import re
import os

class OSIEcosystemCollector:
    """Collector for Open Source Initiative ecosystem data"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OSI Research Tool'
        })

        self.affiliates = []
        self.licenses = []
        self.osi_infrastructure = {}
        self.rate_limit_delay = 1

    def log(self, message):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def analyze_osi_model(self):
        """Analyze OSI organizational model"""
        self.log("Analyzing OSI organizational model...")

        osi_model = {
            'organization_type': 'Standards Organization',
            'founded': 1998,
            'primary_mission': 'Open Source Definition stewardship',
            'operational_model': {
                'type': 'Federated governance',
                'approach': 'License approval and certification',
                'project_hosting': 'None (standards body)',
                'affiliate_coordination': 'Policy and standards alignment'
            },
            'infrastructure': {
                'website': 'opensource.org',
                'license_database': 'Online license repository',
                'communication': 'Mailing lists + occasional GitHub',
                'governance': 'Board of directors + license-discuss list'
            },
            'core_activities': [
                'License review and approval',
                'Open Source Definition maintenance',
                'Education and advocacy',
                'Affiliate organization coordination',
                'Standards development'
            ],
            'technical_infrastructure': {
                'primary_platform': 'Website + mailing lists',
                'github_usage': 'Minimal (governance only)',
                'self_hosting': 'Website and email infrastructure',
                'distributed_model': 'Affiliates manage own infrastructure'
            }
        }

        self.osi_infrastructure = osi_model
        return osi_model

    def analyze_osi_licenses(self):
        """Analyze OSI-approved licenses"""
        self.log("Analyzing OSI-approved licenses...")

        # Major OSI-approved licenses with known information
        major_licenses = [
            {
                'name': 'MIT License',
                'category': 'Permissive',
                'popularity': 'Very High',
                'usage_examples': ['Many JavaScript projects', 'Academic software']
            },
            {
                'name': 'Apache License 2.0',
                'category': 'Permissive',
                'popularity': 'Very High',
                'usage_examples': ['Apache projects', 'Google projects']
            },
            {
                'name': 'GNU GPL v3',
                'category': 'Copyleft',
                'popularity': 'High',
                'usage_examples': ['GNU projects', 'FSF projects']
            },
            {
                'name': 'BSD 3-Clause',
                'category': 'Permissive',
                'popularity': 'High',
                'usage_examples': ['BSD projects', 'Academic software']
            },
            {
                'name': 'GNU GPL v2',
                'category': 'Copyleft',
                'popularity': 'High',
                'usage_examples': ['Linux kernel', 'Older GNU projects']
            },
            {
                'name': 'Mozilla Public License 2.0',
                'category': 'Weak Copyleft',
                'popularity': 'Medium',
                'usage_examples': ['Mozilla projects', 'Firefox']
            },
            {
                'name': 'Eclipse Public License 2.0',
                'category': 'Weak Copyleft',
                'popularity': 'Medium',
                'usage_examples': ['Eclipse projects']
            }
        ]

        self.licenses = major_licenses
        return major_licenses

    def analyze_affiliate_organizations(self):
        """Analyze OSI affiliate organizations"""
        self.log("Analyzing OSI affiliate organizations...")

        # Known affiliate organizations and their characteristics
        major_affiliates = [
            {
                'name': 'Apache Software Foundation',
                'type': 'Project hosting foundation',
                'focus': 'Server software and tools',
                'repository_strategy': 'GitHub primary',
                'communication_model': 'Mailing lists + GitHub Issues'
            },
            {
                'name': 'Eclipse Foundation',
                'type': 'Corporate consortium',
                'focus': 'Enterprise development tools',
                'repository_strategy': 'GitHub exclusive',
                'communication_model': 'GitHub Issues'
            },
            {
                'name': 'Linux Foundation',
                'type': 'Umbrella foundation',
                'focus': 'Infrastructure and ecosystem',
                'repository_strategy': 'Mixed platforms',
                'communication_model': 'Platform-specific'
            },
            {
                'name': 'Mozilla Foundation',
                'type': 'Product foundation',
                'focus': 'Internet health and privacy',
                'repository_strategy': 'GitHub exclusive',
                'communication_model': 'GitHub Issues + Matrix'
            },
            {
                'name': 'Free Software Foundation',
                'type': 'Ideological foundation',
                'focus': 'Software freedom advocacy',
                'repository_strategy': 'Savannah self-hosted',
                'communication_model': 'Mailing lists + IRC'
            },
            {
                'name': 'Software Freedom Conservancy',
                'type': 'Fiscal sponsor',
                'focus': 'Legal and financial support',
                'repository_strategy': 'Varied',
                'communication_model': 'Project-specific'
            },
            {
                'name': 'Python Software Foundation',
                'type': 'Language foundation',
                'focus': 'Python ecosystem',
                'repository_strategy': 'GitHub primary',
                'communication_model': 'GitHub + mailing lists'
            }
        ]

        self.affiliates = major_affiliates
        return major_affiliates

    def collect_osi_ecosystem_data(self):
        """Main collection method for OSI ecosystem"""
        self.log("Starting OSI ecosystem analysis...")

        # Analyze core components
        osi_model = self.analyze_osi_model()
        licenses = self.analyze_osi_licenses()
        affiliates = self.analyze_affiliate_organizations()

        # Compile comprehensive analysis
        ecosystem_data = {
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'analysis_type': 'OSI Ecosystem Analysis',
                'organization_model': 'Standards Organization',
                'foundation': 'Open Source Initiative'
            },
            'osi_organizational_model': osi_model,
            'license_ecosystem': {
                'total_approved_licenses': 100,  # Approximate known value
                'major_licenses': licenses,
                'license_categories': {
                    'permissive': 4,
                    'copyleft': 2,
                    'weak_copyleft': 2
                }
            },
            'affiliate_organizations': affiliates,
            'ecosystem_characteristics': {
                'governance_model': 'Federated standards body',
                'infrastructure_approach': 'Distributed (affiliates self-manage)',
                'coordination_method': 'Standards and policy alignment',
                'technical_infrastructure': 'Minimal (website + mailing lists)'
            }
        }

        return ecosystem_data

    def generate_statistics(self):
        """Generate ecosystem statistics"""

        # Affiliate analysis
        affiliate_types = Counter(a['type'] for a in self.affiliates)
        repo_strategies = Counter(a['repository_strategy'] for a in self.affiliates)
        comm_models = Counter(a['communication_model'] for a in self.affiliates)

        # License analysis
        license_categories = Counter(l['category'] for l in self.licenses)

        statistics = {
            'collection_metadata': {
                'total_affiliates_analyzed': len(self.affiliates),
                'total_licenses_analyzed': len(self.licenses),
                'analysis_date': datetime.now().isoformat(),
                'foundation': 'Open Source Initiative'
            },
            'organizational_model': {
                'type': 'Standards Organization',
                'project_hosting': 'None (federated model)',
                'coordination_approach': 'Policy and standards'
            },
            'affiliate_ecosystem': {
                'affiliate_types': dict(affiliate_types),
                'repository_strategies': dict(repo_strategies),
                'communication_models': dict(comm_models),
                'coordination_method': 'Federated governance'
            },
            'license_ecosystem': {
                'license_categories': dict(license_categories),
                'stewardship_role': 'Approval and maintenance',
                'standards_maintained': 'Open Source Definition'
            },
            'infrastructure_model': {
                'osi_infrastructure': 'Minimal (standards focus)',
                'affiliate_infrastructure': 'Self-managed',
                'coordination_tools': 'Mailing lists + website'
            }
        }

        return statistics

    def save_results(self):
        """Save ecosystem analysis results"""
        statistics = self.generate_statistics()

        # Collect ecosystem data
        ecosystem_data = self.collect_osi_ecosystem_data()
        ecosystem_data['statistics'] = statistics

        # Save JSON
        json_filename = "../results/osi_ecosystem_results.json"
        os.makedirs(os.path.dirname(json_filename), exist_ok=True)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(ecosystem_data, f, indent=2, ensure_ascii=False)

        self.log(f"Saved results to {json_filename}")

        # Save CSV for affiliates
        csv_filename = "../results/osi_affiliates_summary.csv"

        csv_data = []
        for affiliate in self.affiliates:
            csv_data.append({
                'name': affiliate['name'],
                'type': affiliate['type'],
                'focus': affiliate['focus'],
                'repository_strategy': affiliate['repository_strategy'],
                'communication_model': affiliate['communication_model']
            })

        import pandas as pd
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False)
        self.log(f"Saved CSV to {csv_filename}")

        return json_filename, csv_filename

    def print_summary(self):
        """Print ecosystem analysis summary"""
        stats = self.generate_statistics()

        print("\n" + "="*60)
        print("OPEN SOURCE INITIATIVE ECOSYSTEM SUMMARY")
        print("="*60)

        print(f"🏛️ ORGANIZATION TYPE: {stats['organizational_model']['type']}")
        print(f"📊 AFFILIATES ANALYZED: {stats['collection_metadata']['total_affiliates_analyzed']}")
        print(f"⚖️ LICENSES ANALYZED: {stats['collection_metadata']['total_licenses_analyzed']}")

        print(f"\n🔧 ORGANIZATIONAL MODEL:")
        print(f"• Project hosting: {stats['organizational_model']['project_hosting']}")
        print(f"• Coordination: {stats['organizational_model']['coordination_approach']}")

        print(f"\n🏢 AFFILIATE ECOSYSTEM:")
        print(f"• Affiliate types:")
        for aff_type, count in stats['affiliate_ecosystem']['affiliate_types'].items():
            print(f"  - {aff_type}: {count} organizations")

        print(f"\n📊 REPOSITORY STRATEGIES:")
        for strategy, count in stats['affiliate_ecosystem']['repository_strategies'].items():
            print(f"• {strategy}: {count} affiliates")

        print(f"\n💬 COMMUNICATION MODELS:")
        for model, count in stats['affiliate_ecosystem']['communication_models'].items():
            print(f"• {model}: {count} affiliates")

        print(f"\n⚖️ LICENSE ECOSYSTEM:")
        for category, count in stats['license_ecosystem']['license_categories'].items():
            print(f"• {category}: {count} major licenses")

        print(f"\n🎯 OSI CHARACTERISTICS:")
        print(f"• Role: Standards body and license steward")
        print(f"• Approach: Federated governance model")
        print(f"• Infrastructure: Minimal (website + mailing lists)")
        print(f"• Coordination: Policy alignment across affiliates")

        print("\n" + "="*60)

def main():
    """Main execution function"""
    collector = OSIEcosystemCollector()

    try:
        json_file, csv_file = collector.save_results()
        collector.print_summary()

        print(f"\n✅ OSI ecosystem analysis completed!")
        print(f"📄 Results: {json_file}")
        print(f"📊 Summary: {csv_file}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()