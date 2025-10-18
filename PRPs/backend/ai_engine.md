# Product Requirements Document: AI Strategy Analysis Engine

**Version:** 1.0.0  
**Date:** October 18, 2025  
**Hackathon Timeline:** 12 hours  
**Dependencies:** PRD 1 (Retrieval Pipeline)

---

## Executive Summary

Extract actionable AI strategy intelligence from 10-K filings using LLM-powered semantic analysis. Transform dense legal documents into structured insights about AI investments, products, risks, and timelines.

---

## Objectives

### Primary Goals
1. Parse extracted 10-K text and identify AI-relevant sections
2. Use LLMs to extract semantic meaning (not just keyword matching)
3. Generate structured AI intelligence profiles for each company
4. Calculate AI maturity scores for competitive benchmarking
5. Create SDR-ready talking points and discovery questions

### Success Metrics
- **Accuracy:** 90%+ precision on AI investment extraction (validated manually)
- **Coverage:** Extract from Business, Risk, and MD&A sections minimum
- **Speed:** Process all 10 companies in < 4 minutes
- **Actionability:** Generate 5+ specific talking points per company

---

## Technical Architecture

### Component 1: Document Section Identifier
```python
# File: src/section_identifier.py

class TenKSectionIdentifier:
    """
    Identifies and extracts key sections from 10-K HTML
    """
    
    CRITICAL_SECTIONS = [
        "Item 1. Business",
        "Item 1A. Risk Factors", 
        "Item 7. Management's Discussion and Analysis",
        "Item 8. Financial Statements"
    ]
    
    def identify_sections(self, html_content: str) -> dict:
        """
        Parse HTML and extract section boundaries
        
        Returns:
        {
            'business': {'start_idx': 0, 'end_idx': 5000, 'text': '...'},
            'risk_factors': {...},
            'mda': {...}
        }
        """
        pass
    
    def extract_section_text(self, html_content: str, section_name: str) -> str:
        """
        Extract clean text from specific section
        
        Handles:
        - HTML tags removal
        - Table extraction
        - Footnote handling
        - Page break artifacts
        """
        pass
```

**Requirements:**
- Use BeautifulSoup4 or similar for HTML parsing
- Identify sections by Item headers (Item 1, Item 1A, etc.)
- Extract tables separately (they often contain financial AI investments)
- Clean formatting artifacts (page numbers, headers, footers)
- Preserve paragraph structure for context

---

### Component 2: AI Content Detector
```python
# File: src/ai_content_detector.py

class AIContentDetector:
    """
    Identifies paragraphs containing AI-related content
    """
    
    AI_KEYWORDS = [
        # Direct terms
        "artificial intelligence", "AI", "machine learning", "ML",
        "deep learning", "neural network", "generative AI", "GenAI",
        
        # Product terms
        "copilot", "assistant", "automation", "intelligent",
        
        # Technology terms
        "natural language processing", "NLP", "computer vision",
        "large language model", "LLM", "foundation model",
        
        # Investment terms
        "AI investment", "AI research", "AI development"
    ]
    
    def score_paragraph_relevance(self, paragraph: str) -> float:
        """
        Score 0-1 on AI relevance
        
        Factors:
        - Keyword presence (weighted)
        - Proximity of keywords
        - Context (financial terms nearby = investment)
        - Specificity (product names, dollar amounts)
        """
        pass
    
    def filter_relevant_paragraphs(self, section_text: str, threshold=0.3) -> list:
        """
        Return paragraphs above relevance threshold
        """
        pass
```

**Requirements:**
- Case-insensitive keyword matching
- Context-aware scoring (paragraph-level, not sentence)
- Handle acronyms and variations
- Filter out boilerplate legal language
- Preserve context (include surrounding paragraphs)

---

### Component 3: LLM Extraction Engine
```python
# File: src/llm_extractor.py

class AIInsightExtractor:
    """
    Use LLMs to extract structured insights from relevant text
    """
    
    def __init__(self, model="claude-sonnet-4-5-20250929"):
        self.model = model
    
    async def extract_ai_investments(self, text_chunks: list) -> dict:
        """
        Extract specific AI investment amounts and initiatives
        
        Prompt:
        '''
        Analyze this 10-K section for AI investments. Extract:
        
        1. SPECIFIC DOLLAR AMOUNTS mentioned for AI initiatives
           - Include: "invested $X in AI", "allocated $Y for machine learning"
           - Exclude: vague mentions, competitor comparisons
        
        2. INVESTMENT AREAS
           - What specifically is the money going toward?
           - Infrastructure, research, acquisitions, talent?
        
        3. TIMEFRAME
           - When was this investment made or planned?
           - Is it past, present, or future?
        
        Return JSON:
        {
            "investments": [
                {
                    "amount": "$50M",
                    "amount_numeric": 50000000,
                    "purpose": "AI research and development",
                    "timeframe": "fiscal year 2024",
                    "quote": "direct quote from 10-K",
                    "confidence": "high|medium|low"
                }
            ]
        }
        '''
        
        Returns: Structured investment data
        """
        pass
    
    async def extract_ai_products(self, text_chunks: list) -> list:
        """
        Extract AI products, features, or services mentioned
        
        Prompt focus:
        - Product names (e.g., "Microsoft Copilot", "Adobe Firefly")
        - AI features in existing products
        - New AI service offerings
        - Customer-facing vs internal AI tools
        
        Returns:
        [
            {
                "product_name": "Copilot",
                "description": "AI assistant integrated into Office",
                "launch_status": "available|beta|planned",
                "target_market": "enterprise|consumer|developer",
                "quote": "..."
            }
        ]
        """
        pass
    
    async def extract_ai_risks(self, text_chunks: list) -> list:
        """
        Extract AI-related risks from Risk Factors section
        
        Prompt focus:
        - Competitive risks (others' AI threatening business)
        - Implementation risks (AI projects failing)
        - Regulatory risks (AI regulation)
        - Ethical risks (bias, safety concerns)
        
        Returns risk categories with severity
        """
        pass
    
    async def extract_ai_timeline(self, text_chunks: list) -> dict:
        """
        Extract temporal information about AI initiatives
        
        Returns:
        {
            "current_year_initiatives": [...],
            "next_year_plans": [...],
            "long_term_vision": "...",
            "milestones": [
                {"date": "Q4 2024", "event": "Launch Copilot Pro"}
            ]
        }
        """
        pass
    
    async def extract_competitive_positioning(self, text_chunks: list) -> dict:
        """
        How does company position itself vs competitors on AI?
        
        Returns:
        {
            "strengths_claimed": [...],
            "competitors_mentioned": [...],
            "differentiation": "...",
            "concerns_about_competition": [...]
        }
        """
        pass
```

**Requirements:**
- Use Claude Sonnet 4.5 for accuracy
- Implement prompt caching for cost efficiency
- Handle rate limiting (max 1000 requests/min)
- Chunk text to fit context windows (180K tokens)
- Include few-shot examples in prompts for consistency
- Validate JSON outputs with Pydantic models
- Log all LLM calls for debugging

---

### Component 4: AI Maturity Scorer
```python
# File: src/ai_maturity_scorer.py

class AIMaturityScorer:
    """
    Calculate AI maturity score (0-100) based on extracted insights
    """
    
    def calculate_maturity_score(self, insights: dict) -> dict:
        """
        Score breakdown:
        
        1. Investment Score (25 points)
           - Dollar amount invested
           - % of revenue allocated to AI
           - Consistency over years
        
        2. Product Score (25 points)
           - Number of AI products
           - Market availability (beta vs GA)
           - Customer adoption metrics mentioned
        
        3. Strategic Importance (25 points)
           - Frequency of AI mentions in Business section
           - Executive quotes about AI
           - AI in company strategy vs tactical mention
        
        4. Organizational Readiness (25 points)
           - AI talent hiring (from job postings - PRD 3)
           - AI infrastructure mentioned
           - Partnerships with AI vendors
        
        Returns:
        {
            "total_score": 78,
            "breakdown": {
                "investment": 22,
                "product": 19,
                "strategic_importance": 20,
                "organizational_readiness": 17
            },
            "percentile": 85,  # vs other 9 companies
            "maturity_label": "Leader|Fast Follower|Emerging|Laggard"
        }
        """
        pass
```

**Requirements:**
- Normalize scores across different company sizes
- Handle missing data gracefully (score = 0 for that component)
- Calculate relative percentiles within the 10-company cohort
- Provide explanation for each score component

---

### Component 5: SDR Playbook Generator
```python
# File: src/sdr_playbook_generator.py

class SDRPlaybookGenerator:
    """
    Generate sales-ready intelligence from AI insights
    """
    
    def generate_discovery_questions(self, company_insights: dict) -> list:
        """
        Create specific questions based on 10-K findings
        
        Template examples:
        - "I saw in your 10-K that you invested {amount} in {area} - 
           how is that progressing?"
        - "Your Risk Factors mention {risk} - what's your mitigation strategy?"
        - "You launched {product} - what adoption are you seeing?"
        
        Returns: 5-7 contextual questions
        """
        pass
    
    def generate_value_propositions(self, company_insights: dict) -> list:
        """
        Align our value props to their AI strategy
        
        Consider:
        - Their tech stack (from job postings in PRD 3)
        - Their stated challenges
        - Their timeline urgency
        - Their competitive positioning
        
        Returns: 3-5 tailored value props
        """
        pass
    
    def generate_objection_handlers(self, company_insights: dict) -> dict:
        """
        Anticipate objections based on 10-K
        
        Common patterns:
        - "We're building in-house" → Counter with speed/expertise
        - "We use Competitor X" → Counter with differentiation
        - "AI is too risky" → Address their specific risk concerns
        
        Returns: {objection: handler} mapping
        """
        pass
    
    def generate_executive_summary(self, company_insights: dict) -> str:
        """
        One-page AI intelligence brief for SDRs
        
        Format:
        - Company AI Strategy (3 bullets)
        - Current State (what they're doing now)
        - Opportunities (where we can help)
        - Key Talking Points (top 3)
        - Red Flags (what to avoid)
        """
        pass
```

**Requirements:**
- Use natural language (no jargon)
- Include direct quotes from 10-K when possible
- Flag high-confidence vs speculative insights
- Keep discovery questions open-ended
- Make objection handlers conversational

---

## Data Structures

### Input Format
```json
{
  "company": {
    "name": "Microsoft",
    "ticker": "MSFT"
  },
  "sections": {
    "business": "Item 1 text...",
    "risk_factors": "Item 1A text...",
    "mda": "Item 7 text..."
  }
}
```

### Output Format
```json
{
  "company": {
    "name": "Microsoft",
    "ticker": "MSFT"
  },
  "ai_insights": {
    "investments": [
      {
        "amount": "$50M",
        "amount_numeric": 50000000,
        "purpose": "AI infrastructure and research",
        "timeframe": "fiscal year 2024",
        "quote": "We invested approximately $50 million in...",
        "confidence": "high",
        "source_section": "business"
      }
    ],
    "products": [
      {
        "product_name": "Microsoft Copilot",
        "description": "AI assistant for Microsoft 365",
        "launch_status": "available",
        "target_market": "enterprise",
        "quote": "Microsoft Copilot, our AI assistant...",
        "revenue_impact": "mentioned|not_mentioned"
      }
    ],
    "risks": [
      {
        "category": "competitive",
        "risk": "Competitors' AI advancements may reduce our market share",
        "severity": "high|medium|low",
        "quote": "..."
      }
    ],
    "timeline": {
      "current_initiatives": ["Copilot expansion", "AI infrastructure"],
      "near_term_plans": ["Q1 2025: Copilot for Sales"],
      "long_term_vision": "Democratize AI across all products"
    },
    "competitive_positioning": {
      "strengths": ["Integrated AI across product suite"],
      "competitors_mentioned": ["Google", "Anthropic"],
      "differentiation": "Enterprise-focused, security-first AI"
    }
  },
  "ai_maturity": {
    "total_score": 85,
    "breakdown": {
      "investment": 23,
      "product": 22,
      "strategic_importance": 21,
      "organizational_readiness": 19
    },
    "percentile": 90,
    "label": "Leader"
  },
  "sdr_playbook": {
    "discovery_questions": [
      "I noticed you invested $50M in AI infrastructure last year - what's been the ROI so far?",
      "Your 10-K mentions competitive pressure from Google's AI - how are you differentiating?",
      "Copilot is available now - what adoption challenges are you seeing?"
    ],
    "value_propositions": [
      "Accelerate your AI timeline: You mentioned Q1 2025 for Copilot expansion - we can help you hit that deadline",
      "De-risk AI implementation: Your Risk Factors cite AI safety concerns - our governance framework addresses this",
      "Complement existing stack: You're using Azure ML - we integrate seamlessly"
    ],
    "objection_handlers": {
      "We're building in-house": "I saw your $50M investment - our platform can accelerate that by 6 months while you focus on differentiation",
      "We already use Microsoft AI": "Great foundation. We enhance Microsoft's capabilities specifically for [use case]"
    },
    "executive_summary": "Microsoft is an AI Leader (85/100) with $50M invested in FY24...",
    "talking_points": [
      "💰 $50M AI investment signals serious commitment",
      "🚀 Copilot launched, expanding to new products Q1 2025",
      "⚠️ Concerned about competitive threats from Google AI",
      "🎯 Focused on enterprise market, not consumer",
      "🔧 Using Azure ML, TensorFlow stack"
    ]
  },
  "metadata": {
    "analyzed_at": "2025-10-18T11:15:00Z",
    "analysis_time_seconds": 18.3,
    "sections_analyzed": ["business", "risk_factors", "mda"],
    "total_text_analyzed_chars": 125000,
    "llm_calls": 7,
    "confidence_average": 0.87
  }
}
```

---

## Implementation Phases

### Phase 1: Section Extraction (30 minutes)
- [ ] Implement TenKSectionIdentifier
- [ ] Test on Microsoft 10-K
- [ ] Validate section boundaries correct
- [ ] Extract clean text from all sections

### Phase 2: AI Content Detection (20 minutes)
- [ ] Implement AIContentDetector
- [ ] Test keyword scoring
- [ ] Filter paragraphs above threshold
- [ ] Validate relevant content extracted

### Phase 3: LLM Extraction (90 minutes)
- [ ] Implement extract_ai_investments()
- [ ] Implement extract_ai_products()
- [ ] Implement extract_ai_risks()
- [ ] Test prompt engineering for accuracy
- [ ] Validate JSON outputs
- [ ] Implement error handling for malformed responses

### Phase 4: Scoring & Playbook (45 minutes)
- [ ] Implement AIMaturityScorer
- [ ] Calculate scores for all 10 companies
- [ ] Implement SDRPlaybookGenerator
- [ ] Generate discovery questions
- [ ] Generate value props

### Phase 5: Integration & Testing (35 minutes)
- [ ] Connect to PRD 1 retrieval output
- [ ] Run full analysis on all 10 companies
- [ ] Validate output quality manually (spot check 3 companies)
- [ ] Measure execution time

**Total Estimated Time:** 3.5 hours

---

## Prompt Engineering Examples

### Investment Extraction Prompt
```
You are analyzing a 10-K filing for AI investment information.

Extract ONLY explicit, quantified AI investments. Do not infer or estimate.

Rules:
- Must have dollar amount OR percentage of budget/revenue
- Must explicitly relate to AI/ML/artificial intelligence
- Include context about what the investment is for
- Cite the exact quote from the document

Example valid extraction:
{
  "amount": "$3.2 billion",
  "amount_numeric": 3200000000,
  "purpose": "AI research and development including foundation models",
  "timeframe": "fiscal year 2024",
  "quote": "We invested $3.2 billion in AI R&D during fiscal 2024, primarily focused on foundation models and AI infrastructure.",
  "confidence": "high"
}

Example invalid extraction (too vague):
"Significant investment in technology" ← No amount, not AI-specific

Now analyze this section:
[TEXT]
```

---

## Error Handling

### LLM Failures
- Malformed JSON → Retry with stricter prompt
- Rate limiting → Exponential backoff
- Context overflow → Chunk smaller and aggregate results

### Data Quality Issues
- No AI content found → Return empty insights, score = 0
- Ambiguous mentions → Mark confidence as "low"
- Contradictory information → Highlight for manual review

---

## Testing Strategy

### Unit Tests
```python
async def test_extract_known_investment():
    """Test extraction of Microsoft's known $10B OpenAI investment"""
    text = "We invested $10 billion in OpenAI..."
    result = await extract_ai_investments([text])
    assert result[0]['amount_numeric'] == 10000000000
```

### Integration Tests
```python
async def test_full_company_analysis():
    """Test complete analysis for MSFT"""
    sections = load_msft_sections()
    insights = await analyze_company(sections)
    assert len(insights['investments']) > 0
    assert insights['ai_maturity']['total_score'] > 0
```

### Validation Tests
- [ ] Compare extracted investments to known public data
- [ ] Validate SDR questions make sense (manual review)
- [ ] Check maturity scores follow intuition (MSFT, NVDA should be high)

---

## Dependencies

```
anthropic>=0.28.0
pydantic>=2.0.0
beautifulsoup4>=4.12.0
asyncio
json
re
```

---

## Deliverables

1. **Code**
   - All Python modules in `/src/`
   - Prompt templates in `/prompts/`

2. **Output Data**
   - `/output/ai_insights/MSFT_insights.json` (10 files)
   - `/output/ai_insights/consolidated_insights.json`

3. **Validation Report**
   - Spot-check results for 3 companies
   - Confidence metrics
   - Known discrepancies

---

## Demo Talking Points

```
"Here's where it gets interesting. We're not just searching for the word 'AI' - 
we're using Claude to actually UNDERSTAND what these companies are doing.

For Microsoft, we extracted their $10 billion OpenAI investment with full context.
For NVIDIA, we identified 5 specific AI product lines with revenue impact.
For Tesla, we found their AI risk concerns about Waymo competition.

And then we turn this into something a sales rep can actually use. 
Look at these discovery questions - they're based on exact quotes from the 10-K.
No generic 'tell me about your AI strategy' - these are specific, researched, 
and prove we did our homework."
```

---

## Success Criteria

✅ Extract AI investments with 90%+ accuracy  
✅ Generate 5+ actionable insights per company  
✅ Complete analysis of 10 companies in < 4 minutes  
✅ SDR playbook passes manual "would I use this?" test  
✅ AI maturity scores align with industry intuition  

**Sign-off Required:** Validate output quality before proceeding to PRD 3