"""Mock data for frontend development"""
from datetime import datetime, timedelta
from src.models.company import (
    Company, CompanyProfile, AIInsights, AIInvestment, AIProduct, AIRisk,
    AITimeline, Milestone, CompetitivePositioning, EnrichmentData, HiringData,
    JobPosting, NewsItem, AIMaturityScore, SDRPlaybook, ProfileMetadata
)


def get_mock_company_profile(ticker: str) -> CompanyProfile:
    """Generate realistic mock company profile"""

    # Company info
    companies_data = {
        "MSFT": {
            "name": "Microsoft",
            "cik": "0000789019",
            "domain": "microsoft.com",
            "filing_date": "2024-07-30"
        },
        "AAPL": {
            "name": "Apple",
            "cik": "0000320193",
            "domain": "apple.com",
            "filing_date": "2024-11-01"
        },
        "NVDA": {
            "name": "NVIDIA",
            "cik": "0001045810",
            "domain": "nvidia.com",
            "filing_date": "2024-03-15"
        }
    }

    company_info = companies_data.get(ticker, companies_data["MSFT"])

    company = Company(
        name=company_info["name"],
        ticker=ticker,
        cik=company_info["cik"],
        domain=company_info["domain"]
    )

    # AI Insights
    ai_insights = AIInsights(
        investments=[
            AIInvestment(
                amount="$10B+",
                amount_numeric=10000000000,
                purpose="AI infrastructure including data centers and specialized AI chips",
                timeframe="FY2024",
                quote="We invested significantly in AI infrastructure, including data centers and specialized hardware to support our growing AI capabilities.",
                confidence="high",
                source_section="mda"
            ),
            AIInvestment(
                amount="$5B",
                amount_numeric=5000000000,
                purpose="AI research and development initiatives",
                timeframe="FY2023-2024",
                quote="Our R&D investments in AI technologies continue to grow, with focus on generative AI and machine learning capabilities.",
                confidence="high",
                source_section="business"
            )
        ],
        products=[
            AIProduct(
                product_name="Azure OpenAI Service",
                description="Enterprise-grade AI service providing access to advanced language models",
                launch_status="available",
                target_market="enterprise",
                quote="Azure OpenAI Service enables customers to build innovative AI applications using state-of-the-art models.",
                revenue_impact="mentioned"
            ),
            AIProduct(
                product_name="GitHub Copilot",
                description="AI-powered code completion and programming assistant",
                launch_status="available",
                target_market="developer",
                quote="GitHub Copilot has been adopted by millions of developers, significantly enhancing productivity.",
                revenue_impact="mentioned"
            ),
            AIProduct(
                product_name="Microsoft 365 Copilot",
                description="AI assistant integrated across Microsoft 365 applications",
                launch_status="available",
                target_market="enterprise",
                quote="Microsoft 365 Copilot transforms how customers work with AI-powered assistance across Word, Excel, PowerPoint, and Teams.",
                revenue_impact="mentioned"
            )
        ],
        risks=[
            AIRisk(
                category="competitive",
                risk="Intense competition from Google, Amazon, and other cloud providers in AI services",
                severity="high",
                quote="The AI services market is highly competitive, with major technology companies investing heavily in similar capabilities."
            ),
            AIRisk(
                category="regulatory",
                risk="Evolving AI regulations could impact product development and deployment",
                severity="medium",
                quote="We face increasing regulatory scrutiny regarding AI ethics, privacy, and safety across multiple jurisdictions."
            ),
            AIRisk(
                category="implementation",
                risk="Challenges in scaling AI infrastructure to meet growing demand",
                severity="medium",
                quote="Rapid adoption of our AI services requires significant infrastructure investments and may strain capacity."
            )
        ],
        timeline=AITimeline(
            current_initiatives=[
                "Expanding Azure OpenAI Service capabilities",
                "Integrating AI across Microsoft 365 suite",
                "Enhancing GitHub Copilot features",
                "Building custom AI chips for infrastructure"
            ],
            near_term_plans=[
                "Launch new AI-powered features in Windows",
                "Expand Copilot to additional enterprise applications",
                "Enhance AI safety and alignment research"
            ],
            long_term_vision="Position Microsoft as the leading platform for enterprise AI, democratizing access to AI capabilities while ensuring responsible development and deployment.",
            milestones=[
                Milestone(date="2023-02", event="ChatGPT integration with Bing announced"),
                Milestone(date="2023-03", event="Microsoft 365 Copilot unveiled"),
                Milestone(date="2023-11", event="GitHub Copilot Chat launched"),
                Milestone(date="2024-01", event="Copilot Pro subscription tier introduced")
            ]
        ),
        competitive_positioning=CompetitivePositioning(
            strengths=[
                "Enterprise-grade AI at scale",
                "Deep Microsoft ecosystem integration",
                "Strong partnership with OpenAI",
                "Comprehensive cloud infrastructure"
            ],
            competitors_mentioned=["Google", "Amazon", "Salesforce", "Oracle"],
            differentiation="Unlike competitors focused primarily on consumer AI, Microsoft's strategy centers on enterprise integration, combining OpenAI's technology with Azure's scale and the Office ecosystem's reach.",
            concerns_about_competition=[
                "Google's competitive AI offerings and cloud infrastructure",
                "Amazon's broad customer base and AWS market position",
                "Emerging AI-native startups with innovative approaches"
            ]
        )
    )

    # Enrichment Data
    enrichment = EnrichmentData(
        hiring=HiringData(
            total_jobs=142,
            ai_jobs=38,
            ai_job_details=[
                JobPosting(
                    title="Senior AI Research Scientist",
                    location="Redmond, WA",
                    job_url="https://careers.microsoft.com/ai-research-scientist",
                    tech_stack=["PyTorch", "TensorFlow", "CUDA", "Azure"],
                    posted_date="2024-10-15",
                    seniority="senior",
                    remote=False
                ),
                JobPosting(
                    title="Machine Learning Engineer - Azure AI",
                    location="San Francisco, CA",
                    job_url="https://careers.microsoft.com/ml-engineer-azure",
                    tech_stack=["Python", "Kubernetes", "Azure", "MLOps"],
                    posted_date="2024-10-12",
                    seniority="mid",
                    remote=True
                ),
                JobPosting(
                    title="Principal AI Platform Architect",
                    location="Redmond, WA",
                    job_url="https://careers.microsoft.com/ai-platform-architect",
                    tech_stack=["Azure", "Distributed Systems", "LLMs", "Microservices"],
                    posted_date="2024-10-10",
                    seniority="principal",
                    remote=False
                )
            ],
            hiring_urgency="HIGH",
            tech_stack=["PyTorch", "TensorFlow", "Azure", "Python", "CUDA", "Kubernetes", "MLOps"],
            scraped_at=datetime.now().isoformat()
        ),
        recent_news=[
            NewsItem(
                headline="Microsoft announces new AI chip for data centers",
                source="TechCrunch",
                date="2024-10-16",
                url="https://techcrunch.com/microsoft-ai-chip",
                summary="Microsoft unveiled a new custom AI chip designed to accelerate Azure AI workloads.",
                category="product_launch"
            ),
            NewsItem(
                headline="GitHub Copilot reaches 1 million paid subscribers",
                source="The Verge",
                date="2024-10-14",
                url="https://theverge.com/github-copilot-milestone",
                summary="GitHub's AI coding assistant crosses major subscription milestone.",
                category="general"
            )
        ],
        enriched_at=datetime.now().isoformat()
    )

    # AI Maturity Score
    ai_maturity = AIMaturityScore(
        total_score=85,
        breakdown={
            "investment": 23,
            "product": 24,
            "strategic_importance": 22,
            "organizational_readiness": 16
        },
        percentile=92,
        label="Leader"
    )

    # SDR Playbook (matching the UI screenshot)
    sdr_playbook = SDRPlaybook(
        discovery_questions=[
            "I noticed you invested $50M in AI infrastructure - what's been the ROI?",
            "Your 10-K mentions competitive pressure from Google AI - how are you differentiating?",
            "With 38 AI job openings, what are your biggest hiring challenges?",
            "How are you handling the increased demand for Azure OpenAI Service?",
            "What's your strategy for AI safety and responsible development?"
        ],
        value_propositions=[
            "✓ Enterprise-grade AI at scale",
            "✓ Deep Microsoft ecosystem integration",
            "✓ Strong partnership with OpenAI",
            "✓ Comprehensive cloud infrastructure"
        ],
        objection_handlers={
            "Too expensive": "Our enterprise customers typically see 3x ROI within 6 months through productivity gains. Let's discuss a pilot program tailored to your use case.",
            "Already using Google AI": "Unlike Google's consumer-focused approach, our Azure AI platform is built for enterprise security, compliance, and integration with your existing Microsoft investments.",
            "Not ready for AI": "We offer comprehensive change management support and training. Many customers start with GitHub Copilot as a low-risk entry point."
        },
        executive_summary="Microsoft is a clear AI leader with $15B+ invested in AI infrastructure and R&D. Their enterprise-focused strategy, OpenAI partnership, and deep ecosystem integration create significant competitive advantages. Key opportunities: Azure AI expansion, Microsoft 365 Copilot adoption, and developer tools.",
        talking_points=[
            "→ More enterprise-focused than Google",
            "→ Deeper ecosystem integration than AWS",
            "→ Proven track record with Fortune 500",
            "→ Comprehensive AI safety and compliance program",
            "→ High hiring urgency signals growth acceleration"
        ]
    )

    # Metadata
    metadata = ProfileMetadata(
        analyzed_at=datetime.now().isoformat(),
        analysis_time_seconds=45.2,
        retrieval_time_seconds=12.8,
        enrichment_time_seconds=8.5,
        enrichment_completeness=0.95,
        status="complete"
    )

    return CompanyProfile(
        company=company,
        filing_date=company_info["filing_date"],
        fiscal_year=2024,
        ai_insights=ai_insights,
        enrichment=enrichment,
        ai_maturity=ai_maturity,
        sdr_playbook=sdr_playbook,
        metadata=metadata
    )
