# Wikipedia AI Governance Analysis

**Research Period**: October 30 - November 4, 2025
**Research Question**: How does Wikipedia govern AI-generated content without formal AI-specific policies?

This repository contains a comprehensive, multi-method analysis of Wikipedia's AI governance, examining policies, WikiProjects, enforcement practices, deletion discussions, and community norms.

---

## Executive Summary

**Start here**: [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) - Complete overview of all findings

### Key Discovery: "Invisible Policy" Paradox

Wikipedia has **NO formal AI policy** yet maintains **active AI governance**:

- No adopted AI policy (Wikipedia:AI-generated content is still a draft)
- No policy shortcuts (WP:NOTAI doesn't exist)
- **0 AI policy citations** in 10,000 recent edits (0.000%)
- **100+ active deletion discussions** about AI content
- **59% deletion rate** for AI-generated articles
- **Bottom-up governance** through community practice

**Finding**: AI governance emerges through **community norms** and **deletion discussions**, not formal policy.

---

## Key Statistics

### Policy Citation Analysis (10,000 edits, 2025)
```
Total policy citations: 1,820
 AI-specific policies: 0 (0.000%)
 Bot/automation policies: 311 (17.1%)
 Other policies: 1,509 (82.9%)

AI shortcuts: WP:AI → Info page (not policy)
 WP:NOTAI → Does NOT exist
```

### AfD Analysis (100+ discussions found, 30 analyzed)
```
Deletion rate: 59%
Keep rate: 11%
Detection tool usage: 20% (GPTZero)
Average voters: 2.8 per discussion
Policy citations: 51 total (NO AI-specific)
```

### WikiProject Analysis (1,096+ projects examined)
```
WikiProjects with AI policies: 0
Top project: AI Cleanup
 Watchers: 207
 AI references: 109
 Governance model: Centralized (no autonomy)
```

---

## Repository Structure

### Main Reports (Read in Order)

1. **[`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md)** START HERE
 - Complete overview of all findings
 - Key statistics and implications
 - Comparative framework for software projects

2. **[`Complete_Wikipedia_AI_Governance_Analysis.md`](Complete_Wikipedia_AI_Governance_Analysis.md)**
 - Initial comprehensive policy analysis
 - 42 governance pages, 581 AI references
 - Foundation of the research

3. **[`Wikipedia_WikiProject_AI_Policy_Analysis.md`](Wikipedia_WikiProject_AI_Policy_Analysis.md)**
 - Analysis of 1,096+ WikiProjects
 - **Finding**: 0 WikiProjects have separate AI policies
 - Centralized governance model documented

4. **[`AI_Enforcement_Preliminary_Analysis.md`](AI_Enforcement_Preliminary_Analysis.md)**
 - Random sampling approach (30 articles)
 - **Result**: 0% hit rate (methodology lesson)
 - Led to targeted approach development

5. **[`AI_Enforcement_Targeted_Analysis.md`](AI_Enforcement_Targeted_Analysis.md)**
 - Targeted sampling (13 articles from WikiProject AI Cleanup)
 - **Success**: 116 AI-related edits found (46% hit rate)
 - Distinction between article maintenance vs. enforcement

6. **[`Wikipedia_AI_Policy_Citation_Analysis_2025.md`](Wikipedia_AI_Policy_Citation_Analysis_2025.md)**
 - Quantitative analysis of policy usage
 - 10,000 edits analyzed
 - **Finding**: 0 AI policy citations vs. 311 bot policy citations

7. **[`Wikipedia_AfD_AI_Detection_Analysis.md`](Wikipedia_AfD_AI_Detection_Analysis.md)** KEY INSIGHTS
 - Deep dive into 30 deletion discussions
 - How editors detect AI content
 - Community language and arguments
 - **Finding**: 59% deletion rate, GPTZero used in 20% of cases

---

### Analysis Scripts

All scripts use Wikipedia Action API with proper rate limiting:

#### Core Analysis Tools
- **`wikipedia_ai_governance_analyzer.py`** - General governance page analysis
- **`wikipedia_specific_governance_analyzer.py`** - Targeted 42-page analysis
- **`wikipedia_wikiproject_ai_analyzer.py`** - WikiProject enumeration (1,096+ projects)

#### Enforcement Analysis Tools
- **`wikipedia_ai_enforcement_analyzer.py`** - Random sampling (failed approach)
- **`wikipedia_ai_enforcement_targeted_analyzer.py`** - Targeted sampling (successful)
- **`wikipedia_policy_citation_analyzer.py`** - Policy citation frequency analysis

#### Discussion Analysis Tools
- **`wikipedia_ai_discussions_analyzer.py`** - Current discussions tracker
- **`wikipedia_ai_talk_discussion_analyzer.py`** - Talk page search
- **`wikipedia_afd_ai_pattern_analyzer.py`** - AfD deep analysis (detection patterns)

---

### Data Files

#### Analysis Results (JSON)
- `wikipedia_specific_governance_ai_analysis_20251030_183154.json` - 42 governance pages
- `wikipedia_wikiproject_ai_analysis_20251104_153844.json` - 1,096+ WikiProjects
- `wikipedia_policy_citations_2025_20251104_175208.json` - 1,820 policy citations
- `wikipedia_ai_talk_discussions_20251104_180104.json` - 118 discussion spaces
- `wikipedia_afd_ai_patterns_20251104_180544.json` - 30 AfD discussions (detailed)

#### Summary Data (CSV)
- `wikipedia_ai_governance_pages_20251030_183154.csv` - Governance page summary
- `wikipedia_wikiproject_ai_summary_20251104_153844.csv` - WikiProject summary
- `ai_enforcement_targeted_edits_20251104_174005.csv` - 116 AI edits
- `ai_enforcement_targeted_discussions_20251104_174005.csv` - Talk discussions
- `ai_enforcement_targeted_articles_20251104_174005.csv` - Article list

---

## Major Findings

### 1. **No Formal AI Policy, But Active Governance**

**Policy Status**:
- `Wikipedia:AI-generated content` exists but is **draft proposal** (not adopted)
- No shortcuts: `WP:NOTAI` doesn't exist
- No AI-specific policy citations in 10,000 edits

**But Governance Exists**:
- 100+ Articles for Deletion discussions
- 59% deletion rate for AI content
- GPTZero used in 20% of cases
- Community norms emerging through practice

### 2. **Centralized Governance Model**

**WikiProject Analysis**:
- 1,096+ WikiProjects examined
- **0 have separate AI policies**
- All defer to centralized Wikipedia policies
- WikiProject AI Cleanup coordinates enforcement, doesn't create policy

### 3. **Detection Methods**

**How editors identify AI content**:
- 80% rely on **human judgment** ("reads like AI", style-based)
- 20% use **GPTZero** detection tool
- Focus on **secondary indicators**: no sources, generic text, hallucinated refs

**Top indicators** (from 30 AfD discussions):
- GPT: 170 mentions
- ChatGPT: 155 mentions
- AI-generated: 67 mentions
- Hallucination: 3 mentions

### 4. **Community Language**

**Pejorative terms**:
- "AI slop" - Low-quality content
- "AI garbage/mess" - Worthless content
- "Word salad" - Incoherent text

**Technical terms**:
- "Hallucination" - Fabricated information
- "Hallucinated references" - Fake citations

**Attitude**: Generally negative toward AI-generated content, emphasis on **deception** and **wasted cleanup effort**.

### 5. **Deletion Arguments**

**Most common reasons for deletion**:
1. **Hallucinated references** (fabricated citations)
2. **Lack of sources** (unverifiable)
3. **Wasted cleanup effort** ("not worth volunteer time")
4. **Undisclosed AI use** (deception)
5. **Mass creation** (systematic abuse)

**Key quote**:
> "It is better to remove AI generated content... due to their tendency to hallucinate information and references, rather than waste volunteer time trying to clean them up."

### 6. **When AI Content Survives (11% "Keep" rate)**

**Criteria**:
- Notable subject (e.g., historical figure)
- Cleanup feasible
- Sources added
- Content valuable

**Principle**: **Notability trumps method** - generation method matters less than quality.

### 7. **Policy Application**

**Most cited policies in AI AfD** (NO AI-specific policies):
- WP:TNT (Total Nuke & Rewrite): 8 citations
- WP:SIGCOV (Significant Coverage): 4 citations
- WP:V (Verifiability): 3 citations
- WP:OR (No Original Research): 2 citations

**Insight**: Existing content quality policies applied to AI cases.

### 8. **Temporal Trends**

**AI activity increasing**:
- 2023: 44 AI-related edits
- 2024: 9 AI-related edits
- 2025: 63 AI-related edits (to Nov 4)

**Editor quote**:
> "I've seen 5 AI-generated article AFDs in the past month alone... Honestly kind of scary."

---

## Research Implications

### For Understanding Wikipedia

1. **Bottom-up governance works** (but has limits)
 - Effective without formal policy
 - Inconsistent standards
 - Eventually needs formalization

2. **Existing frameworks adapt**
 - WP:V, WP:RS, WP:OR applied to AI cases
 - New technology doesn't always need new rules

3. **Detection is the bottleneck**
 - Subjective human judgment
 - Tool usage low (20%)
 - False positive risk

4. **Community trust matters**
 - Undisclosed AI use = deception
 - Hallucinated refs = false information
 - Trust breach > technical quality issues

5. **Pragmatism wins**
 - Notable subjects kept despite AI generation
 - Results matter more than provenance
 - Quality standards can be met

### For Comparing with Software Projects

**Questions for Apache/FSF analysis**:

1. **Detection**: Is AI code easier/harder to detect than text?
2. **Policy**: Do they have formal AI policies?
3. **Philosophy**: Open-source (pragmatic) vs. free-software (ideological)?
4. **Enforcement**: What happens to AI-generated PRs?
5. **Language**: Similar vocabulary? Attitudes?

---

## Methodology

### Data Collection Methods

1. **Policy Analysis** (Wikipedia Action API)
 - 42 governance pages analyzed
 - 581 AI references found

2. **WikiProject Analysis** (API enumeration)
 - 1,096+ projects fetched
 - Top 50 analyzed in depth

3. **Edit History Analysis** (revisions API)
 - Random sample: 30 articles (0% hit rate)
 - Targeted sample: 13 articles (46% hit rate, 116 AI edits)

4. **Policy Citation Analysis** (recent changes API)
 - 10,000 recent edits analyzed
 - 1,820 policy citations extracted

5. **Discussion Analysis** (search + parse APIs)
 - 118 discussion spaces searched
 - 100+ AfD discussions found
 - 30 analyzed in depth

### API Usage

**Endpoints used**:
- `query` - General queries
- `parse` - Page parsing
- `search` - Full-text search
- `recentchanges` - Recent edits
- `revisions` - Edit history
- `categorymembers` - Category listings
- `allpages` - Page enumeration

**Rate limiting**: 0.5-1 second delays between requests

---

## Additional Context

### Wikipedia Infrastructure Note

**GitBox and GitHub**:

Wikipedia content is NOT on GitHub. The research in this repository analyzes Wikipedia governance through the Wikimedia API.

**Apache Foundation Projects** (main repository focus) use dual infrastructure:
- **GitBox**: Apache's Git service (canonical repositories)
- **GitHub**: Public mirrors with issues/PRs enabled (when communities choose)

This Wikipedia analysis provides a **comparison baseline** for understanding how different open communities govern AI-generated contributions.

## Running the Analysis

### Prerequisites

```bash
pip install requests
```

### Running Individual Scripts

Each script is self-contained and can be run independently:

```bash
# Policy analysis
python3 wikipedia_ai_governance_analyzer.py
python3 wikipedia_specific_governance_analyzer.py

# WikiProject analysis
python3 wikipedia_wikiproject_ai_analyzer.py

# Enforcement analysis
python3 wikipedia_ai_enforcement_targeted_analyzer.py
python3 wikipedia_policy_citation_analyzer.py

# Discussion analysis
python3 wikipedia_ai_talk_discussion_analyzer.py
python3 wikipedia_afd_ai_pattern_analyzer.py
```

**Note**: Scripts use Wikipedia API with rate limiting (0.5-1s delays). Each run takes 3-10 minutes depending on sample size.

---

## Citation

If you use this research, please cite:

```
Wikipedia AI Governance Analysis
Research Period: October 30 - November 4, 2025
Repository: Apache-Foundation-Projects/Wikipedia
Data Source: Wikipedia/Wikimedia Foundation (via Action API)
Methodology: Mixed methods (quantitative API analysis + qualitative discussion analysis)
```

---

## Related Projects

This analysis is part of a larger comparative study:

- **Wikipedia** (this repository) - Community-driven content governance
- **Apache Foundation** - Open-source software governance
- **FSF/GNU** - Free-software governance

**Research Goal**: Compare AI governance models across community-driven projects to understand:
- Centralized vs. decentralized approaches
- Formal policy vs. emergent norms
- Content vs. code governance differences
- Pragmatic vs. ideological philosophies

---

## Contact & Contributions

This is academic research. For questions or collaboration:
- Open an issue in this repository
- Contributions welcome (additional analysis, corrections, extensions)

---

## License & Acknowledgments

**Data Source**: Wikipedia/Wikimedia Foundation
**API**: Wikimedia Action API (public, with proper attribution)
**Tools**: Python 3, requests library

Wikipedia content is licensed under Creative Commons Attribution-ShareAlike 3.0.
This analysis and code are provided for educational and research purposes.

---

## Useful Links

**Wikipedia Resources**:
- [Wikipedia:AI-generated content](https://en.wikipedia.org/wiki/Wikipedia:AI-generated_content) (draft policy)
- [Wikipedia:WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- [Wikipedia:Village pump (policy)](https://en.wikipedia.org/wiki/Wikipedia:Village_pump_(policy))
- [Wikipedia:Articles for deletion](https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion)

**API Documentation**:
- [Wikimedia Action API](https://www.mediawiki.org/wiki/API:Main_page)
- [API Tutorial](https://www.mediawiki.org/wiki/API:Tutorial)

---

**Last Updated**: November 4, 2025
**Status**: Analysis Complete - Ready for publication and comparison with software projects

### Prerequisites
```bash
# Install required packages
pip install requests pandas beautifulsoup4
```

### Run Individual Analyzers
```bash
# Analyze specific governance pages
python wikipedia_specific_governance_analyzer.py

# Search for current AI discussions
python wikipedia_ai_discussions_analyzer.py

# Run comprehensive analysis
python wikipedia_ai_governance_analyzer.py
```

## Analysis Methodology

**Approach**: Multi-dimensional analysis covering:
1. **Static governance documents** - Policies, guidelines, essays
2. **Active community discussions** - Village pump, noticeboards, talk pages
3. **Operational frameworks** - Bot policies, administrative procedures

**Data Sources**:
- Wikipedia API (Action API)
- MediaWiki REST API
- Wikipedia namespaces (0, 4, 5 primarily)

**Search Terms**: 15+ AI-related keywords including 'artificial intelligence', 'bot', 'automated', 'AI-generated', 'ChatGPT', 'machine learning'

## Use Cases

This analysis can be used for:
- **Policy research** on platform AI governance
- **Comparative studies** of AI regulation approaches
- **Academic research** on community-driven governance
- **Policy development** guidance for other platforms
- **Tracking evolution** of AI governance over time

## Analysis Date

**Conducted**: October 30, 2025
**Coverage Period**: Current governance state + 90 days of discussion history
**Data Freshness**: Real-time API queries

## Updating the Analysis

To refresh the analysis with current data:

```bash
# Update governance page analysis
python wikipedia_specific_governance_analyzer.py

# Check for new discussions
python wikipedia_ai_discussions_analyzer.py
```

The tools automatically generate timestamped output files, so you can track changes over time.

---

*This analysis provides a comprehensive baseline for understanding Wikipedia's AI governance as of late 2025, capturing both established frameworks and emerging policy discussions.*