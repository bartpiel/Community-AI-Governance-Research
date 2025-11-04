# Nonprofit Foundation Analysis: Repository Platforms & Communication Channels

A comprehensive analysis of where major nonprofit open source foundations store their code and how their communities communicate.

## 📊 Analysis Overview

This project analyzes **6 major nonprofit open source foundations** to understand:
- **Where projects store their code** (GitHub, self-hosted, mixed platforms)
- **How communities communicate** (mailing lists, GitHub Issues, IRC, chat platforms)
- **Infrastructure strategies** and organizational philosophies

## 🏛️ Foundations Analyzed

| Foundation | Projects | Primary Repository | Primary Communication | Analysis Status |
|------------|----------|-------------------|---------------------|-----------------|
| **Apache Software Foundation** | ~400 | GitBox + GitHub (~95%)* | Mailing lists + GitHub Issues | ✅ Complete |
| **Eclipse Foundation** | ~415 | GitHub (100%) | GitHub Issues (100%) | ✅ Complete |
| **Linux Foundation** | ~220 | Mixed (~70% GitHub) | Mixed approaches | ✅ Complete |
| **Mozilla Foundation** | 1,048 | GitHub (100%) | GitHub Issues (87%) | ✅ Complete |
| **Open Source Initiative** | 70+ affiliates | N/A (standards body) | Mailing lists | ✅ Complete |
| **Free Software Foundation** | 405+ GNU | Savannah (self-hosted) | Mailing lists + IRC | ✅ Complete |

### *Apache GitBox-GitHub Infrastructure Note

**Apache's Unique Dual Repository Model**: Apache Software Foundation uses GitBox as their primary Git infrastructure, which automatically mirrors to GitHub. This means:

- **Primary Storage**: GitBox (`gitbox.apache.org`) - Apache-controlled canonical repositories
- **Community Interface**: GitHub (`github.com/apache/`) - Synchronized mirrors for community interaction
- **Practical Access**: Contributors interact with GitHub (PRs, Issues, cloning) while Apache maintains sovereignty through GitBox
- **Data Completeness**: GitHub repositories contain complete project data (code + community activity) due to real-time synchronization

**Analysis Impact**: When analyzing Apache projects through GitHub extraction, you're accessing the complete project ecosystem while Apache retains infrastructure independence through their GitBox system.

## 🔧 Quick Start

## 🔧 Quick Start

### Prerequisites
```bash
# Install system packages
sudo apt update
sudo apt install python3-full python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Complete Analysis
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run full analysis
python3 run_full_analysis.py
```

### Run Individual Foundation Analysis
```bash
# Apache Software Foundation
python3 collectors/apache_foundation_collector.py

# Eclipse Foundation
python3 collectors/eclipse_foundation_collector.py

# Linux Foundation
python3 collectors/linux_foundation_collector.py

# Mozilla Foundation
python3 collectors/mozilla_foundation_collector.py

# Open Source Initiative
python3 collectors/osi_ecosystem_collector.py

# Free Software Foundation
python3 collectors/fsf_ecosystem_collector.py
```

### Generate Comprehensive Comparison
```bash
python3 generate_foundation_comparison.py
```

## 📁 Project Structure

```
nonprofit-foundation-analysis/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── collectors/                        # Foundation-specific collectors
│   ├── apache_foundation_collector.py
│   ├── eclipse_foundation_collector.py
│   ├── linux_foundation_collector.py
│   ├── mozilla_foundation_collector.py
│   ├── osi_ecosystem_collector.py
│   └── fsf_ecosystem_collector.py
├── generate_foundation_comparison.py  # Comprehensive analysis
├── results/                           # Generated analysis results
│   ├── apache_foundation_results.json
│   ├── eclipse_foundation_results.json
│   ├── linux_foundation_results.json
│   ├── mozilla_foundation_results.json
│   ├── osi_ecosystem_results.json
│   ├── fsf_ecosystem_results.json
│   └── comprehensive_comparison.json
└── docs/                             # Documentation and insights
    ├── METHODOLOGY.md
    ├── KEY_FINDINGS.md
    └── FOUNDATION_PROFILES.md
```

## 📊 Key Findings Summary

### Repository Platform Adoption
- **100% GitHub:** Eclipse, Mozilla
- **~95% GitBox+GitHub:** Apache Software Foundation (dual infrastructure)
- **~70% GitHub:** Linux Foundation
- **~5% GitHub:** Free Software Foundation
- **N/A:** Open Source Initiative (standards body)

### Communication Patterns
- **GitHub Issues Primary:** Eclipse (100%), Mozilla (87%)
- **Mailing Lists Primary:** Apache, FSF, OSI
- **Mixed Approaches:** Linux Foundation
- **Traditional Methods:** FSF (mailing lists + IRC only)

### Infrastructure Strategies
- **Full External Platform:** Eclipse, Mozilla (GitHub)
- **Hybrid Mirror Approach:** Apache (GitBox primary + GitHub community interface)
- **Mixed Platform Strategy:** Linux Foundation (various platforms)
- **Complete Self-Hosting:** FSF (Savannah platform)
- **Federated Model:** OSI (no central hosting)

## 🎯 Research Questions Answered

1. **Where do nonprofit foundations store their code?**
   - GitHub dominates modern foundations (80%+)
   - Self-hosting rare but ideologically important (FSF)
   - Hybrid approaches balance control and convenience

2. **How do foundation communities communicate?**
   - GitHub Issues replacing traditional bug trackers
   - Mailing lists persist for governance
   - Real-time chat emerging for development
   - Philosophical consistency in some foundations (FSF)

3. **What drives platform choices?**
   - Organizational mission influences technical decisions
   - Corporate foundations embrace modern tools
   - Ideological foundations maintain independence
   - Standards bodies operate differently than project hosts

## 📈 Analysis Methodology

Each foundation collector:
1. **Discovers projects** through APIs, web scraping, and official listings
2. **Analyzes repository platforms** (GitHub, GitLab, self-hosted, etc.)
3. **Maps communication channels** (Issues, mailing lists, chat, forums)
4. **Extracts statistics** (project counts, adoption rates, platform distribution)
5. **Documents infrastructure** (technology stacks, hosting models)

## 🛠️ Technical Details

### Data Collection Methods
- **APIs:** GitHub API, GitLab API where available
- **Web Scraping:** Foundation websites, project listings
- **Manual Curation:** Official documentation review
- **Rate Limiting:** Respectful API usage with delays

### Output Formats
- **JSON:** Structured data for programmatic analysis
- **CSV:** Tabular data for spreadsheet analysis
- **Markdown:** Human-readable reports and summaries

## 📄 License

This analysis project is released under the MIT License. See individual foundation data for their respective licenses and terms.

---

**Analysis Date:** October 2025
**Foundations Analyzed:** 6 major nonprofit organizations
**Total Projects Studied:** 2,500+ open source projects
**Focus:** Repository platforms and communication channels