# Community AI Governance Research - For Potential Collaborators

**Quick Start Guide for Reviewers**

---

## What You're Looking At

This is a **comparative research project** studying how different open communities govern AI-generated contributions. Think of it as investigating:

> "When there are no universal rules about AI, how do Wikipedia, Apache, and other open communities figure out what to do?"

---

## The Big Question

**How do community-driven projects develop governance around AI/LLMs when:**
- No universal standards exist
- Technology evolves faster than policy
- Detection is difficult
- Communities have different values

---

## What's Complete vs. What's Coming

### **COMPLETE: Wikipedia Deep Dive**

**Dates**: October 30 - November 4, 2025
**Status**: Fully analyzed, documented, ready for review

**The Surprising Finding**:
- Wikipedia has NO formal AI policy
- Yet successfully deletes 59% of AI-generated content
- Through bottom-up community norms, not top-down rules
- We call this the **"Invisible Policy Paradox"**

### **IN PROGRESS: Foundation Analysis**

**Status**: Framework and tools ready, execution pending

**Organizations to Study**:
- Apache Software Foundation
- Linux Foundation
- Eclipse Foundation
- Mozilla Foundation
- Free Software Foundation (FSF/GNU)
- Open Source Initiative (OSI)

---

## Repository Guide

### Start Here (15 minutes)

1. **[This README](README.md)** - Repository overview
2. **[Wikipedia/EXECUTIVE_SUMMARY.md](Wikipedia/EXECUTIVE_SUMMARY.md)** - Complete Wikipedia findings 

### For Deep Understanding (2-3 hours)

3. **[Wikipedia/README.md](Wikipedia/README.md)** - Wikipedia analysis overview
4. **[Wikipedia_AfD_AI_Detection_Analysis.md](Wikipedia/Wikipedia_AfD_AI_Detection_Analysis.md)** - Real enforcement examples (19 KB)
5. **[Wikipedia_WikiProject_AI_Policy_Analysis.md](Wikipedia/Wikipedia_WikiProject_AI_Policy_Analysis.md)** - Governance structure (18 KB)

### Quick Reference (5 minutes)

6. **[Wikipedia/QUICK_REFERENCE.md](Wikipedia/QUICK_REFERENCE.md)** - Key statistics at a glance

---

## Wikipedia Findings - The Highlights

### The Numbers

```
10,000 edits analyzed → 0 AI policy citations (0.000%)
100+ deletion discussions → 59% deletion rate
1,096+ WikiProjects → 0 have separate AI policies
GPTZero detection tool → Used in only 20% of cases
```

### What This Means

**Wikipedia governance is "invisible"**:
- No formal policy exists (still a draft)
- No policy shortcuts (WP:NOTAI doesn't exist)
- Yet enforcement happens actively through deletion discussions
- Community develops norms through practice, not rules

### How They Detect AI

**80% Human Judgment**:
- "Reads like AI"
- "Sounds generic"
- Hallucinated references (fake citations)
- No sources

**20% Detection Tools**:
- GPTZero (explicit AI detector)
- Pattern recognition

### Why They Delete

Top reasons for removing AI content:
1. **Fabricated citations** - AI makes up references
2. **No sources** - Can't verify claims
3. **Wasted effort** - "Not worth cleaning up"
4. **Deception** - Undisclosed AI use
5. **Mass creation** - Systematic abuse

**Key Quote from Editors**:
> "Better to remove AI content due to their tendency to hallucinate information and references, rather than waste volunteer time trying to clean them up."

### When They Keep AI Content (11%)

**If the subject is notable enough**:
- Historical figures mentioned in ancient texts
- Can be cleaned up with proper sources
- Content is valuable despite generation method

**Principle**: **Quality matters more than how it was made**

### Community Language

Editors developed informal vocabulary:
- **"AI slop"** - Low-quality automated content
- **"Word salad"** - Incoherent text
- **"Hallucination"** - AI fabricating information

**Attitude**: Generally negative, emphasis on trust breach (deception) rather than just quality

---

## Why This Matters

### For Wikipedia Itself

Shows that **informal governance can work**:
- Bottom-up norms emerge naturally
- Community develops detection skills
- Deletion discussions build consensus
- No formal policy needed (yet)

**But has limits**:
- Inconsistent standards
- Subjective detection
- May not scale to larger AI influx

### For Software Projects (Next Phase)

**Key Questions**:
1. Will Apache/FSF show similar bottom-up patterns?
2. Is code easier or harder to detect than text?
3. Do foundations formalize faster than communities?
4. Does ideology matter? (FSF free-software vs. Apache open-source)

### For Policy Makers

**Lessons**:
1. **Practice precedes policy** - Communities develop norms first (~2 year lag before formalization)
2. **Detection is the bottleneck** - Without good tools, governance is subjective
3. **Trust > Quality** - Deception (undisclosed AI use) matters more than output quality
4. **Existing rules can adapt** - May not need AI-specific policies
5. **Scale drives formalization** - Small problems handled informally, large ones force policy

---

## What We Found: Timeline

### Wikipedia AI Governance Evolution

**2023**: 44 AI-related edits, informal detection begins
**2024**: 9 AI-related edits (drop)
**2025**: 63 AI-related edits (**spike**), increased deletion discussions

**Editor Quote**:
> "I've seen 5 AI-generated article AFDs in the past month alone. Prior to that, I had not seen one. Honestly kind of scary if you ask me."

**Interpretation**: Growing problem, may force formal policy creation

---

## Methodology Overview

### What We Did for Wikipedia

**6 Different Analysis Approaches**:

1. **Policy Document Analysis** (42 pages)
2. **WikiProject Enumeration** (1,096+ projects)
3. **Edit History Analysis** (116 AI-related edits)
4. **Policy Citation Analysis** (10,000 recent edits)
5. **Discussion Space Search** (118 spaces)
6. **Deletion Discussion Deep Dive** (30 analyzed in depth)

**Result**: 89 KB of documentation, 18 data files, 9 analysis scripts

### What We'll Do for Foundations

**Similar multi-method approach**:
- Policy documents
- Mailing list archives
- GitHub/Git discussions
- Issue trackers
- License analysis
- Philosophical texts (FSF)

**Tools Ready**: 6 data collectors prepared

---

## Interesting Discoveries

### 1. The "Hallucination Problem" Drives Policy

**What we learned**:
- AI fabricating citations is taken VERY seriously
- Worse than having no sources (creates false information)
- Primary reason for deletion
- Seen as breach of trust

**Implication**: Wikipedia's core value is **verifiability** - AI's hallucination problem directly conflicts with this

### 2. No Policy ≠ No Governance

**What we learned**:
- Wikipedia has zero AI policy citations
- But has 100+ active enforcement discussions
- Governance emerges from practice

**Implication**: Formal policy may not be necessary for effective governance (at small scale)

### 3. "Notability Trumps Method"

**What we learned**:
- 11% of AI-generated articles are kept
- If subject is notable and sources are added
- Generation method becomes irrelevant

**Implication**: Wikipedia is pragmatic - **results matter more than provenance**

### 4. Bot Policies Mature, AI Policies Emerging

**What we learned**:
- Bot/automation policies: 311 citations (17% of all policy citations)
- AI-specific policies: 0 citations (0%)
- But bot policies are decades old

**Implication**: AI governance may follow similar trajectory as bot governance (slow formalization)

---

## Comparative Framework (Coming Next)

### What We'll Compare

| Dimension | Wikipedia | Apache | FSF | Others |
|-----------|-----------|--------|-----|--------|
| **Domain** | Content (text) | Code | Code | Mixed |
| **Structure** | Community | Foundation | Movement | Various |
| **Philosophy** | Neutral | Pragmatic | Ideological | Various |
| **Governance** | Centralized policy, distributed enforcement | TBD | TBD | TBD |
| **AI Policy** | None (draft) | TBD | TBD | TBD |
| **Detection** | 80% human, 20% tools | TBD | TBD | TBD |

### Key Questions

1. **Is code detection easier than text detection?**
 - Code has patterns, style, syntax
 - But also more complex

2. **Do foundations formalize faster?**
 - Organizational resources
 - Legal concerns (licenses)

3. **Does ideology matter?**
 - FSF (freedom-focused) vs. Apache (quality-focused)
 - Will outcomes differ?

4. **Can lessons transfer?**
 - Wikipedia → Software projects
 - Or fundamentally different?

---

## File Navigation

### Essential Documents (Start Here)

1. **Main README** (this document) - Overview
2. **Wikipedia/EXECUTIVE_SUMMARY.md** - Complete findings
3. **Wikipedia/QUICK_REFERENCE.md** - Statistics cheat sheet

### Detailed Reports (For Deep Dive)

**Most Interesting**:
- **Wikipedia_AfD_AI_Detection_Analysis.md** (19 KB) - Real deletion discussions, editor language, arguments
- **Wikipedia_WikiProject_AI_Policy_Analysis.md** (18 KB) - Governance structure, centralization finding

**Quantitative**:
- **Wikipedia_AI_Policy_Citation_Analysis_2025.md** (8 KB) - 0 AI citations finding
- **AI_Enforcement_Targeted_Analysis.md** (12 KB) - 116 AI edits analyzed

**Methodology**:
- **AI_Enforcement_Preliminary_Analysis.md** (13 KB) - What didn't work (random sampling)
- **FILE_ORGANIZATION.md** (9 KB) - Repository guide

### Data Files

**All included** in Wikipedia/ directory:
- 6 JSON files (detailed results)
- 12 CSV files (summary data)
- All reproducible with included scripts

### Foundation Analysis

**Framework in** nonprofit-foundation-analysis/ directory:
- 6 data collectors (Python scripts)
- Methodology documentation
- Results directory (pending execution)

---

## Next Steps

### For You (Potential Collaborators)

**Quick Review** (30 minutes):
1. Read this document
2. Skim Wikipedia/EXECUTIVE_SUMMARY.md
3. Check Wikipedia/QUICK_REFERENCE.md
4. Provide feedback

**Detailed Review** (3-4 hours):
1. Read all Wikipedia analysis reports
2. Examine methodology
3. Review data files
4. Suggest improvements

**Collaboration** (ongoing):
1. Help with foundation analysis
2. Suggest additional research questions
3. Review comparative framework
4. Co-author papers/presentations

### For the Project

**Immediate**:
- Incorporate colleague feedback
- Refine foundation research questions
- Begin foundation data collection

**Short-term**:
- Execute foundation analysis (Apache, FSF, etc.)
- Comparative analysis across domains
- Synthesis of findings

**Long-term**:
- Academic paper
- Conference presentations
- Interactive visualizations
- Longitudinal tracking (2026+)

---

## FAQ

### "Why Wikipedia first?"

**Answer**: Easier to start with:
- Public API (no authentication)
- Rich discussion data
- Active enforcement happening now
- Provides baseline for comparison

### "How long did Wikipedia analysis take?"

**Answer**: ~6 days (Oct 30 - Nov 4)
- Multiple analytical approaches
- Failed approaches documented (random sampling)
- Successful targeted methods
- Comprehensive documentation

### "Is Wikipedia representative?"

**Answer**: No, and that's the point!
- Wikipedia = content, community-driven, neutral
- Software = code, foundation-led, various philosophies
- Comparison will show what's universal vs. context-specific

### "What about other platforms?"

**Answer**: Could expand to:
- Stack Overflow (Q&A)
- Reddit communities (various)
- OpenStreetMap (geographic data)
- Wikimedia Commons (media)
- But: scope management, need baseline first

### "Can I replicate the analysis?"

**Answer**: Yes!
- All scripts included
- Data files provided
- Methodology documented
- Wikipedia API is public and free

### "When will foundation analysis be done?"

**Answer**: TBD
- Framework ready
- Depends on data availability
- Some foundation data may require access requests
- Estimated: 2-4 weeks per foundation

---

## How to Contribute

### Provide Feedback

- Review Wikipedia findings
- Suggest additional analyses
- Point out missing perspectives
- Challenge interpretations

### Help with Foundation Analysis

- Access to foundation data
- Domain expertise (Apache, Linux, etc.)
- Legal/licensing knowledge
- Philosophical texts (FSF)

### Extend the Research

- Additional domains
- Longitudinal tracking
- Quantitative modeling
- Visualization tools

### Academic Outputs

- Co-author papers
- Conference presentations
- Workshop organization
- Dataset publication

---

## Contact

**For Questions**:
- Open an issue in this repository
- [Your contact information]

**For Collaboration**:
- All contributions welcome
- Credit appropriately attributed
- Academic standards maintained

---

## Summary for Busy Potential Collaborators

### TL;DR

**What**: Comparative study of AI governance in open communities
**Where**: Wikipedia (done), Apache/FSF/etc. (next)
**Finding**: Wikipedia governs AI without formal policy through bottom-up norms
**Why It Matters**: Shows governance can emerge from practice, not just rules
**Next**: See if software projects show similar or different patterns
**What You Can Do**: Read Wikipedia/EXECUTIVE_SUMMARY.md (15 min), provide feedback

### The One Key Finding

> **"The Invisible Policy Paradox"**: Wikipedia has NO formal AI policy, yet successfully governs AI content through community norms, deletion discussions, and consensus-building. This bottom-up model works (for now) but may not scale.

### The One Key Question for Next Phase

> **Will software foundations show similar bottom-up patterns, or do they formalize faster due to organizational structure, legal concerns, and code-specific challenges?**

---

**Repository**: Community-AI-Governance-Research
**Status**: Phase 1 (Wikipedia) Complete | Phase 2 (Foundations) Ready
**Last Updated**: November 4, 2025
**Ready For**: Colleague review and foundation analysis execution
