# Wikipedia AI Governance - File Organization

## 📁 Directory Structure

```
Wikipedia/
├── README.md                                          # Main entry point
├── EXECUTIVE_SUMMARY.md                              # Complete findings overview ⭐
│
├── 📖 Analysis Reports/
│   ├── Complete_Wikipedia_AI_Governance_Analysis.md   # Initial comprehensive analysis
│   ├── Wikipedia_AI_Governance_Analysis_Report.md     # Executive report (early version)
│   ├── Wikipedia_WikiProject_AI_Policy_Analysis.md    # WikiProject governance (1,096+)
│   ├── AI_Enforcement_Preliminary_Analysis.md         # Random sampling (failed)
│   ├── AI_Enforcement_Targeted_Analysis.md            # Targeted sampling (success)
│   ├── Wikipedia_AI_Policy_Citation_Analysis_2025.md  # Policy citation frequency
│   └── Wikipedia_AfD_AI_Detection_Analysis.md         # AfD deep dive ⭐
│
├── 🔧 Python Scripts/
│   ├── wikipedia_ai_governance_analyzer.py            # General governance analysis
│   ├── wikipedia_specific_governance_analyzer.py      # 42 governance pages
│   ├── wikipedia_wikiproject_ai_analyzer.py           # WikiProject enumeration
│   ├── wikipedia_ai_enforcement_analyzer.py           # Random sampling
│   ├── wikipedia_ai_enforcement_targeted_analyzer.py  # Targeted sampling
│   ├── wikipedia_policy_citation_analyzer.py          # Policy citations
│   ├── wikipedia_ai_discussions_analyzer.py           # Current discussions
│   ├── wikipedia_ai_talk_discussion_analyzer.py       # Talk page search
│   └── wikipedia_afd_ai_pattern_analyzer.py           # AfD pattern analysis
│
└── 📊 Data Files/
    ├── JSON (detailed results)/
    │   ├── wikipedia_specific_governance_ai_analysis_20251030_183154.json
    │   ├── wikipedia_wikiproject_ai_analysis_20251104_153844.json
    │   ├── wikipedia_policy_citations_2025_20251104_175208.json
    │   ├── wikipedia_ai_talk_discussions_20251104_180104.json
    │   ├── wikipedia_afd_ai_patterns_20251104_180544.json
    │   └── wikipedia_ai_discussions_analysis_20251030_183552.json
    │
    └── CSV (summary data)/
        ├── wikipedia_ai_governance_pages_20251030_183154.csv
        ├── wikipedia_wikiproject_ai_summary_20251104_153844.csv
        ├── ai_enforcement_targeted_articles_20251104_174005.csv
        ├── ai_enforcement_targeted_edits_20251104_174005.csv
        ├── ai_enforcement_targeted_discussions_20251104_174005.csv
        ├── ai_enforcement_articles_20251104_173519.csv
        ├── ai_edit_enforcement_20251104_173519.csv
        └── ai_talk_discussions_20251104_173519.csv
```

---

## 📖 Reading Guide

### For Quick Overview (15 minutes)
1. Read `EXECUTIVE_SUMMARY.md` (sections 1-5)
2. Skim key statistics

### For Deep Understanding (2-3 hours)
1. Start with `EXECUTIVE_SUMMARY.md`
2. Read `Wikipedia_AfD_AI_Detection_Analysis.md` (real-world enforcement)
3. Read `Wikipedia_WikiProject_AI_Policy_Analysis.md` (governance structure)
4. Read `Wikipedia_AI_Policy_Citation_Analysis_2025.md` (quantitative data)

### For Methodology (1 hour)
1. `AI_Enforcement_Preliminary_Analysis.md` (what didn't work)
2. `AI_Enforcement_Targeted_Analysis.md` (what worked)
3. Review Python scripts for implementation details

### For Replication
1. All Python scripts are self-contained
2. Use Wikipedia Action API (free, no authentication)
3. Respect rate limits (0.5-1s delays between requests)
4. Expected runtime: 3-10 minutes per script

---

## 📊 Data File Guide

### Key Data Files

**Most Important**:
- `wikipedia_afd_ai_patterns_20251104_180544.json` - 30 AfD discussions analyzed
- `wikipedia_policy_citations_2025_20251104_175208.json` - 1,820 policy citations
- `wikipedia_wikiproject_ai_analysis_20251104_153844.json` - 1,096+ WikiProjects

**Enforcement Data**:
- `ai_enforcement_targeted_edits_20251104_174005.csv` - 116 AI-related edits
- `ai_enforcement_targeted_discussions_20251104_174005.csv` - 20 talk discussions
- `ai_enforcement_targeted_articles_20251104_174005.csv` - 13 articles analyzed

**Summary Data**:
- `wikipedia_ai_governance_pages_20251030_183154.csv` - 42 governance pages
- `wikipedia_wikiproject_ai_summary_20251104_153844.csv` - WikiProject summary

### Older/Superseded Files

These files are from preliminary analysis (kept for reproducibility):
- `ai_edit_enforcement_20251104_173519.csv` - Random sampling (0 hits)
- `ai_talk_discussions_20251104_173519.csv` - Random sampling (false positives)
- `ai_enforcement_articles_20251104_173519.csv` - Random sample articles

**Note**: Random sampling failed; targeted approach succeeded.

---

## 🔄 Analysis Timeline

### Phase 1: Policy Analysis (Oct 30)
- Analyzed 42 governance pages
- Found 581 AI references
- Output: `Complete_Wikipedia_AI_Governance_Analysis.md`

### Phase 2: WikiProject Analysis (Nov 4, morning)
- Enumerated 1,096+ WikiProjects
- Analyzed top 50 for AI policies
- **Finding**: 0 WikiProjects have separate AI policies
- Output: `Wikipedia_WikiProject_AI_Policy_Analysis.md`

### Phase 3: Enforcement Analysis (Nov 4, afternoon)
- **Attempt 1**: Random sampling of 30 articles → 0% hit rate
- **Attempt 2**: Targeted sampling from WikiProject AI Cleanup → 46% hit rate
- Found 116 AI-related edits
- Output: `AI_Enforcement_Targeted_Analysis.md`

### Phase 4: Policy Citation Analysis (Nov 4, afternoon)
- Analyzed 10,000 recent edits
- Found 1,820 policy citations
- **Finding**: 0 AI policy citations (0.000%)
- Output: `Wikipedia_AI_Policy_Citation_Analysis_2025.md`

### Phase 5: Discussion Analysis (Nov 4, evening)
- Searched 118 discussion spaces
- Found 100+ AfD discussions
- Analyzed 30 in depth
- **Finding**: 59% deletion rate, GPTZero used in 20%
- Output: `Wikipedia_AfD_AI_Detection_Analysis.md`

### Phase 6: Synthesis (Nov 4, evening)
- Created `EXECUTIVE_SUMMARY.md`
- Organized repository
- Ready for publication

---

## 🎯 Key Findings Summary

### Quantitative Results

```
Policy Analysis:
├─ Governance pages analyzed:     42
├─ Pages with AI content:         16 (38%)
└─ Total AI references:          581

WikiProject Analysis:
├─ Projects enumerated:        1,096+
├─ Projects analyzed:             50
└─ Projects with AI policies:      0 (0%)

Enforcement Analysis:
├─ Random sample hit rate:        0%
├─ Targeted sample hit rate:     46%
└─ AI-related edits found:       116

Policy Citations (10,000 edits):
├─ Total citations:            1,820
├─ AI-specific:                    0 (0.000%)
└─ Bot/automation:               311 (17.1%)

AfD Analysis (30 discussions):
├─ Total discussions found:      100+
├─ Deletion rate:                59%
├─ Keep rate:                    11%
└─ GPTZero usage:                20%
```

### Qualitative Findings

**Detection Methods**:
- 80% human judgment ("reads like AI")
- 20% detection tools (GPTZero)
- Focus on secondary indicators (no sources, hallucinated refs)

**Community Language**:
- Pejorative: "AI slop", "AI garbage"
- Technical: "hallucination", "fabricated references"
- Generally negative attitude

**Deletion Arguments**:
1. Hallucinated references
2. Lack of sources
3. Wasted cleanup effort
4. Undisclosed AI use
5. Mass creation

**Governance Model**:
- Bottom-up (emergent norms)
- Distributed enforcement (AfD discussions)
- Centralized policy (no WikiProject autonomy)
- Pragmatic (notability trumps method)

---

## 🔬 Methodology Notes

### What Worked

✅ **Targeted sampling** (from WikiProject AI Cleanup)
✅ **Policy citation analysis** (quantitative measure)
✅ **AfD discussion analysis** (real-world enforcement)
✅ **API-based data collection** (reproducible)
✅ **Mixed methods** (quant + qual)

### What Didn't Work

❌ **Random sampling** (0% hit rate for rare events)
❌ **Simple keyword search** ("AI" too generic, many false positives)

### Lessons Learned

1. **Rare events need targeted sampling**, not random
2. **Context matters**: "AI" in "AI Cleanup" vs. "AI-generated content"
3. **Follow the enforcement trail**: AfD discussions more informative than edit summaries
4. **Policy lag**: Practice precedes formal policy by 2+ years
5. **Bottom-up governance**: Effective without top-down rules (but has limits)

---

## 🚀 Future Directions

### For Wikipedia Research

- [ ] Monitor draft policy adoption process
- [ ] Track detection tool usage over time
- [ ] Analyze false positive/negative rates
- [ ] Study successful cleanup cases
- [ ] Long-term trend analysis (2026+)

### For Comparative Study

- [ ] Apache Foundation AI governance
- [ ] FSF/GNU philosophical stance
- [ ] Compare software vs. content governance
- [ ] Open-source vs. free-software approaches
- [ ] Cross-domain governance patterns

---

## 📝 Publication Checklist

Before sharing on GitHub:

- [x] Executive summary complete
- [x] All analysis reports present
- [x] README updated
- [x] File organization document
- [x] Data files included
- [x] Scripts documented
- [x] Methodology explained
- [x] Key findings highlighted
- [x] Citation info provided
- [x] License/attribution clear

**Status**: ✅ Ready for publication

---

**Last Updated**: November 4, 2025
