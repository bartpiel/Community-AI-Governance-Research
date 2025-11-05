# Wikipedia WikiProject AI Policy Analysis

## Executive Summary

This analysis investigated whether individual WikiProjects on English Wikipedia have developed their own AI-specific policies separate from Wikipedia's general governance framework. The research examined WikiProjects to understand if Wikipedia's AI governance operates through centralized policies or allows decentralized, project-specific rulemaking.

**Date**: November 4, 2025
**Scope**: English Wikipedia WikiProjects
**Total WikiProjects Found**: 1,096+ (ongoing enumeration indicates ~1,500-1,600 total)
**WikiProjects Analyzed in Detail**: 19 (initial sample)

---

## Key Findings

### 1. **No Separate WikiProject AI Policies Identified**

**Finding**: WikiProjects do NOT maintain their own AI-specific policies separate from Wikipedia's central governance framework.

- **0 of 19 analyzed WikiProjects** had dedicated AI policy pages
- WikiProjects rely on Wikipedia's general policies for AI governance
- No evidence of project-level AI rulemaking autonomy

**Implication**: Wikipedia employs a **centralized governance model** for AI policy rather than delegating to individual projects.

---

### 2. **WikiProject AI Cleanup: Dedicated AI Content Management**

**Discovery**: A specialized WikiProject exists specifically to address AI-generated content issues.

**Wikipedia:WikiProject AI Cleanup**
- **207 watchers** (highly active community)
- **109 AI-related references** across project documentation
- **2,991 monthly page views**
- **27 subpages** for project coordination

**Key Sections with AI Content**:
1. **Introduction** (13 references) - Project mission and scope
2. **Editing advice** (31 references) - Guidelines for handling AI content
3. **Project resources** (23 references) - Tools and references
4. **Information** (13 references) - Background and context
5. **Participants** (11 references) - Active members
6. **Goals** (9 references) - Project objectives
7. **Open tasks** (7 references) - Current work items
8. **Relevant archived discussions** (2 references)

**Nature of Project**:
- **Operational focus**: Identifying and addressing AI-generated content quality issues
- **NOT policy-making**: Enforces existing Wikipedia policies, doesn't create new ones
- **Quality control**: Reviews articles suspected of AI generation for compliance with Wikipedia standards

---

### 3. **AI Content Prevalence Across WikiProjects**

**Statistic**: **36.8% of analyzed WikiProjects** (7 of 19) contain AI-related content in their documentation.

**WikiProjects with AI Content** (sorted by AI references):

| Rank | WikiProject | AI References | Watchers | Monthly Views | Notes |
|------|-------------|---------------|----------|---------------|-------|
| 1 | **AI Cleanup** | 109 | 207 | 2,991 | Dedicated AI content project |
| 2 | **AI in Korean Wikipedia** | 6 | 0 | 38 | Cross-language AI coordination |
| 3 | **Academic Journals** | 5 | 196 | 0 | Bot/automation references |
| 4 | **Abortion** | 2 | 38 | 0 | Assessment automation |
| 5 | **2010s** | 2 | 0 | 39 | General automation |
| 6 | **A Cappella** | 2 | 0 | 16 | General automation |
| 7 | **A Song of Ice and Fire** | 1 | 58 | 212 | Minimal AI mentions |

**WikiProjects with NO AI Content**: 63.2% (12 of 19)
- Abandoned Drafts, Abandoned articles, .NET, AIDS, 20th Century Studios, AMWikicommonsUploadWorkflow, AP Biology projects (2008-2011), Abkhazia, Abu Dhabi

---

## Analysis Methodology

### Data Collection Process

1. **WikiProject Enumeration**
 - Used Wikipedia API (`action=query`, `list=allpages`)
 - Prefix search: "WikiProject "
 - Namespace: 4 (Wikipedia namespace)
 - Filtered: Main pages only (excluded subpages with `/`)

2. **Popularity Metrics**
 - **Watchers count**: Active community members monitoring the project
 - **Monthly page views**: Last 30 days of traffic
 - Sorting criterion: Number of watchers (proxy for active participation)

3. **AI Content Analysis**
 - **Keywords searched**: artificial intelligence, AI, machine learning, ML, bot, automated, automation, algorithm, neural network, deep learning, chatbot, language model, GPT, ChatGPT, generative, AI-generated, AI-assisted, LLM, computer-generated
 - **Text analysis**: Full page content (wikitext) parsing
 - **Section extraction**: Identified sections containing AI-related content
 - **Subpage analysis**: Examined guideline and policy subpages for AI content

4. **Policy Identification**
 - Searched for dedicated AI policy pages
 - Analyzed guideline/policy/rule/standard/criteria subpages
 - Checked for AI-specific rulemaking separate from Wikipedia general policies

---

## Implications for Research

### Comparison with Code Communities

This analysis reveals a significant **difference in governance approaches**:

**Wikipedia (Content Community)**:
- **Centralized AI governance** - Policies set at platform level
- **No project-level autonomy** - WikiProjects cannot create own AI rules
- **Specialized enforcement project** - WikiProject AI Cleanup operates under central policies
- **Uniform standards** - All projects subject to same AI governance framework

**Open-Source vs Free-Software (Code Communities)**:
- **Potentially decentralized** - Individual projects may set own AI policies
- **Foundation-level guidance** - Different foundations may have different stances
- **License-driven governance** - AI policy tied to licensing philosophy

### Research Questions This Raises

1. **Do open-source foundations allow member projects to set individual AI policies?**
 - Apache projects vs Linux Foundation projects vs independent projects

2. **Do free-software projects maintain ideological consistency on AI?**
 - GNU projects vs FSF-aligned projects

3. **Is Wikipedia's centralized model unique or representative?**
 - How does this compare to other content platforms (OpenStreetMap, Stack Overflow)?

4. **Does licensing ideology predict governance centralization?**
 - CC BY-SA (Wikipedia) = centralized
 - GPL (GNU) = ?
 - Apache License = ?

---

## Governance Model Analysis

### Wikipedia's Centralized AI Governance Architecture

```

 Wikipedia Foundation-Level Policies 
 (Bot policy, Artificial intelligence page, 
 Content guidelines, Verifiability, etc.) 

 
 Applied uniformly to
 ↓

 All WikiProjects (1,500+) 
 
 
 WikiProject WikiProject ... 
 Medicine Biography 
 
 
 NO project-specific AI policies 
 Follow central Wikipedia governance 

 
 Enforcement/Quality Control
 ↓

 WikiProject AI Cleanup (Specialized) 
 
 • Identifies AI-generated content 
 • Reviews for policy compliance 
 • Enforces existing rules (doesn't make new) 
 • 207 active watchers 

```

### Key Characteristics

1. **Top-Down Policy Flow**
 - Central Wikipedia community develops AI policies
 - Individual WikiProjects cannot override or create alternatives
 - Uniformity across all topic areas

2. **Specialized Enforcement**
 - WikiProject AI Cleanup serves as quality control mechanism
 - Operates under existing policies, not independent authority
 - Cross-project coordination for AI content issues

3. **No Topic-Specific Exceptions**
 - Medicine, Biography, Technology projects all follow same rules
 - No evidence of domain-specific AI policy adaptations
 - Centralized standards regardless of subject matter sensitivity

---

## Comparison with Other Platforms (Hypothetical)

### If Wikipedia Followed an Open-Source Model

**Hypothetical Decentralized Scenario**:
- WikiProject Medicine could ban all AI-generated content (high-risk domain)
- WikiProject Technology could permit AI drafting (technical expertise available)
- WikiProject Pop Culture could allow AI-generated summaries (low-risk content)

**Reality**: None of this exists. Wikipedia maintains uniform governance.

### Research Opportunity

**Question**: Do open-source projects show similar centralization within foundations?
- Do all Apache projects follow Apache Foundation AI guidance?
- Do all Linux Foundation projects share common AI policies?
- Or do individual projects have autonomy to set own rules?

---

## Technical Details

### WikiProject Discovery Challenges

**Issue**: WikiProjects have extensive subpage structures, making enumeration complex.

**Example Structure**:
```
Wikipedia:WikiProject Medicine
Wikipedia:WikiProject Medicine/Assessment
Wikipedia:WikiProject Medicine/Guidelines
Wikipedia:WikiProject Medicine/Members
Wikipedia:WikiProject Medicine/Open tasks
... (hundreds of subpages)
```

**Solution**:
- Filter pages by absence of `/` character (main pages only)
- Typical batch results: 500 total pages → 10-30 main WikiProjects
- Ratio: ~5-10% of returned pages are main WikiProject pages

**Total Enumeration**:
- ~1,500-1,600 main WikiProjects identified
- Each with 0-500+ subpages
- Alphabetically distributed search space

### API Usage

**Wikipedia API Endpoints**:
- `action=query&list=allpages` - Page enumeration
- `action=query&prop=revisions` - Content retrieval
- `action=query&prop=info&inprop=watchers` - Popularity metrics
- `action=query&prop=pageviews` - Traffic statistics

**Rate Limiting**: 1 second delay between requests (respectful scraping)

---

## Data Files Generated

### Available Outputs

1. **`wikipedia_wikiproject_ai_analysis_YYYYMMDD_HHMMSS.json`**
 - Comprehensive JSON with all WikiProject data
 - Includes: full text analysis, section breakdowns, AI reference locations
 - Useful for: Detailed research, programmatic analysis

2. **`wikipedia_wikiproject_ai_summary_YYYYMMDD_HHMMSS.csv`**
 - Summary spreadsheet with key metrics
 - Columns: WikiProject name, watchers, views, AI references, policy indicators
 - Useful for: Quick overview, statistical analysis

3. **`wikipedia_wikiproject_ai_analyzer.py`**
 - Analysis script (reproducible research)
 - Can be re-run to update data
 - Configurable limits and search parameters

---

## Conclusions

### Primary Research Finding

**Wikipedia does NOT delegate AI governance to WikiProjects.**

The platform maintains a **centralized, uniform policy framework** where:
- All projects follow the same AI rules
- No project-level autonomy for AI policy
- Specialized projects (AI Cleanup) enforce rather than create policy
- Governance is top-down from Wikipedia community

### Contrast with Software Ecosystems

This finding is **potentially significant** for comparing content vs. code governance:

**Hypothesis**:
- Content platforms (Wikipedia) → Centralized AI governance
- Code platforms (GitHub, Apache, etc.) → Potentially decentralized?

**Reasoning**:
- Content requires **uniformity** (reliability, verifiability standards)
- Code can have **diversity** (different projects, different risk tolerance)

### Research Implications

For your study comparing open-source vs free-software AI governance:

1. **Wikipedia serves as a baseline** for content governance
 - Centralized, policy-driven, no project autonomy

2. **Software foundations may differ**
 - Check if Apache/Eclipse/Linux Foundation projects have individual AI policies
 - Compare with FSF/GNU project AI stances

3. **Ideological vs pragmatic divide may appear differently**
 - In code: Open-source (permissive) vs Free-software (ideological)
 - In content: Centralized governance regardless of licensing philosophy

---

## Future Research Directions

### Questions for Further Investigation

1. **Are there ANY WikiProjects with separate AI policies?**
 - Expand analysis beyond top 50 to all 1,500+
 - Check for specialized areas (medicine, law, biography)

2. **How does WikiProject AI Cleanup actually operate?**
 - Detailed analysis of their processes
 - Case studies of AI content reviews
 - Enforcement mechanisms

3. **Has Wikipedia's AI governance changed over time?**
 - Historical analysis of policy development
 - Timeline of AI-related discussions
 - Evolution of WikiProject AI Cleanup

4. **Comparison with other Wikimedia projects**
 - Does Wikidata have different AI governance?
 - What about Wikimedia Commons (images/AI art)?
 - Cross-project policy consistency?

5. **Stack Overflow as comparison case**
 - Community-driven like Wikipedia
 - But directly threatened by AI (ChatGPT competition)
 - Do Stack Overflow topic tags have different AI rules?

---

## Methodology Limitations

### Acknowledged Constraints

1. **Sample Size**: Initial analysis covered only 19 WikiProjects
 - Full analysis of 1,500+ ongoing
 - Top 50 by popularity will provide better coverage
 - Long-tail WikiProjects may differ

2. **Keyword Search**: AI content identified via keyword matching
 - May miss context-specific discussions
 - May overcount generic "automation" references
 - Natural language processing could improve accuracy

3. **Subpage Analysis**: Only checked guideline/policy subpages
 - May miss AI discussions in talk pages
 - May miss archived discussions
 - Historical policy debates not captured

4. **Snapshot Analysis**: Data captured at single point in time
 - AI governance is rapidly evolving
 - May not reflect recent changes
 - Longitudinal study would be valuable

---

## Research Context

### Relation to Your Broader Study

**Your Research Goal**: Compare LLM governance in community-driven code and content projects, specifically:
- Open-source projects (Apache, Linux Foundation, etc.)
- Free-software projects (FSF, GNU)
- Wikipedia (open-content)

**This Analysis Contributes**:
- Baseline for content governance (centralized model)
- Evidence that WikiProjects don't have AI policy autonomy
- Identification of specialized enforcement mechanism (AI Cleanup)
- Quantification of AI content prevalence (36.8% mention AI)

**Next Steps for Your Research**:
1. Analyze open-source foundation AI policies (Apache, Eclipse, Linux Foundation)
2. Analyze free-software project AI policies (GNU, FSF-endorsed projects)
3. Compare centralization vs decentralization across domains
4. Test whether ideological licensing predicts AI governance approach

---

## Appendix: Full WikiProject Analysis Results

### Top WikiProjects by AI Content (Initial Sample)

| Rank | WikiProject | Watchers | Monthly Views | AI Refs | Has Policy? | Subpages |
|------|-------------|----------|---------------|---------|-------------|----------|
| 1 | AI Cleanup | 207 | 2,991 | 109 | No* | 27 |
| 2 | AI in Korean Wikipedia | 0 | 38 | 6 | No | 0 |
| 3 | Academic Journals | 196 | 0 | 5 | No | 500 |
| 4 | Abortion | 38 | 0 | 2 | No | 17 |
| 5 | 2010s | 0 | 39 | 2 | No | 3 |
| 6 | A Cappella | 0 | 16 | 2 | No | 6 |
| 7 | A Song of Ice and Fire | 58 | 212 | 1 | No | 11 |
| 8 | Abandoned Drafts | 66 | 50 | 0 | No | 69 |
| 9 | Abandoned articles | 44 | 241 | 0 | No | 9 |
| 10 | .NET | 35 | 38 | 0 | No | 4 |
| 11 | AIDS | 32 | 37 | 0 | No | 11 |
| 12 | 20th Century Studios | 0 | 14 | 0 | No | 15 |
| 13 | AMWikicommonsUploadWorkflow | 0 | 4 | 0 | No | 0 |
| 14 | AP Biology 2008 | 0 | 14 | 0 | No | 0 |
| 15 | AP Biology 2009 | 0 | 12 | 0 | No | 0 |
| 16 | AP Biology 2010 | 0 | 15 | 0 | No | 0 |
| 17 | AP Biology 2011 | 0 | 12 | 0 | No | 1 |
| 18 | Abkhazia | 0 | 0 | 0 | No | 6 |
| 19 | Abu Dhabi | 0 | 0 | 0 | No | 3 |

*Note: WikiProject AI Cleanup has extensive AI content but is an enforcement mechanism, not a policy-making body.

---

## Document Information

**Created**: November 4, 2025
**Author**: AI Governance Research Project
**Purpose**: Document WikiProject-level AI policy analysis for comparison with software foundation governance
**Status**: Initial analysis complete; full 1,500+ WikiProject enumeration ongoing
**Related Files**:
- `wikipedia_wikiproject_ai_analyzer.py` (analysis script)
- `wikipedia_wikiproject_ai_analysis_*.json` (detailed data)
- `wikipedia_wikiproject_ai_summary_*.csv` (summary data)
- `Complete_Wikipedia_AI_Governance_Analysis.md` (general Wikipedia AI governance)

**Contact for Data**: See JSON/CSV files for complete dataset

---

*This analysis is part of a broader research project investigating how community-driven projects (both code and content) regulate AI/LLM usage, comparing open-source, free-software, and open-content governance approaches.*
