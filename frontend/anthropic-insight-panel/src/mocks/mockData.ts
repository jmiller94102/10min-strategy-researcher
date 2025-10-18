// Enhanced Mock Data for Development
// Matches API Contract v2.0 exactly

import type {
  CompanyProfile,
  Company,
  AIInsights,
  EnrichmentData,
  AIMaturityScore,
  SDRPlaybook,
  ProfileMetadata,
} from '@/types/api';

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

const generateMockDate = (daysAgo: number = 0): string => {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date.toISOString();
};

// ============================================================================
// MOCK COMPANIES
// ============================================================================

export const mockCompanies: Company[] = [
  { name: 'Microsoft Corporation', ticker: 'MSFT', cik: '0000789019', domain: 'microsoft.com' },
  { name: 'Apple Inc.', ticker: 'AAPL', cik: '0000320193', domain: 'apple.com' },
  { name: 'NVIDIA Corporation', ticker: 'NVDA', cik: '0001045810', domain: 'nvidia.com' },
  { name: 'Alphabet Inc.', ticker: 'GOOGL', cik: '0001652044', domain: 'google.com' },
  { name: 'Amazon.com Inc.', ticker: 'AMZN', cik: '0001018724', domain: 'amazon.com' },
  { name: 'Meta Platforms Inc.', ticker: 'META', cik: '0001326801', domain: 'meta.com' },
  { name: 'Tesla Inc.', ticker: 'TSLA', cik: '0001318605', domain: 'tesla.com' },
  { name: 'Salesforce Inc.', ticker: 'CRM', cik: '0001108524', domain: 'salesforce.com' },
  { name: 'Adobe Inc.', ticker: 'ADBE', cik: '0000796343', domain: 'adobe.com' },
  { name: 'Netflix Inc.', ticker: 'NFLX', cik: '0001065280', domain: 'netflix.com' },
];

// ============================================================================
// DETAILED MOCK PROFILES
// ============================================================================

export const mockMicrosoftProfile: CompanyProfile = {
  company: mockCompanies[0],
  filing_date: '2024-07-30',
  fiscal_year: 2024,
  ai_insights: {
    investments: [
      {
        amount: '$50M',
        amount_numeric: 50000000,
        purpose: 'AI infrastructure and OpenAI partnership expansion',
        timeframe: 'FY2024',
        quote: 'We continue to invest heavily in AI capabilities, including our strategic partnership with OpenAI and expansion of Azure AI services.',
        confidence: 'high',
        source_section: 'mda',
      },
      {
        amount: '$30M',
        amount_numeric: 30000000,
        purpose: 'AI research and development',
        timeframe: 'FY2024',
        quote: 'Significant investment in AI research to maintain competitive advantage.',
        confidence: 'high',
        source_section: 'business',
      },
    ],
    products: [
      {
        product_name: 'GitHub Copilot',
        description: 'AI-powered code completion and generation tool',
        launch_status: 'available',
        target_market: 'developer',
        quote: 'GitHub Copilot has been adopted by millions of developers worldwide.',
        revenue_impact: 'mentioned',
      },
      {
        product_name: 'Microsoft 365 Copilot',
        description: 'AI assistant integrated into Microsoft 365 applications',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'Copilot for Microsoft 365 represents a significant new revenue stream.',
        revenue_impact: 'mentioned',
      },
      {
        product_name: 'Azure OpenAI Service',
        description: 'Enterprise access to OpenAI models via Azure',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'Azure OpenAI Service is experiencing strong enterprise adoption.',
      },
      {
        product_name: 'Bing Chat',
        description: 'AI-powered search and conversational interface',
        launch_status: 'available',
        target_market: 'consumer',
        quote: 'Bing Chat integration has increased user engagement significantly.',
      },
      {
        product_name: 'Security Copilot',
        description: 'AI-powered cybersecurity assistant',
        launch_status: 'beta',
        target_market: 'enterprise',
        quote: 'Security Copilot is in preview with select enterprise customers.',
      },
    ],
    risks: [
      {
        category: 'competitive',
        risk: 'Intense competition from Google, Amazon, and other tech giants in AI',
        severity: 'high',
        quote: 'We face intense competition in the AI and cloud markets from well-established companies with significant resources.',
      },
      {
        category: 'regulatory',
        risk: 'Increasing AI regulation and compliance requirements',
        severity: 'medium',
        quote: 'Regulatory developments related to AI could impact our ability to deploy AI solutions.',
      },
      {
        category: 'ethical',
        risk: 'Responsible AI development and bias mitigation',
        severity: 'medium',
        quote: 'We must ensure our AI systems are developed and deployed responsibly to maintain customer trust.',
      },
    ],
    timeline: {
      current_initiatives: [
        'Azure OpenAI Service expansion',
        'Microsoft 365 Copilot rollout',
        'GitHub Copilot enterprise features',
      ],
      near_term_plans: [
        'AI model optimization for edge deployment',
        'Copilot integration across product suite',
        'Enhanced AI security features',
      ],
      long_term_vision: 'Democratize AI access through Azure platform and empower every person and organization to achieve more with AI assistance.',
      milestones: [
        { date: '2024-Q1', event: 'Launch of GPT-4 integration in Azure OpenAI Service' },
        { date: '2024-Q2', event: 'Microsoft 365 Copilot general availability' },
        { date: '2024-Q3', event: 'Security Copilot enterprise preview' },
      ],
    },
    competitive_positioning: {
      strengths: [
        'Azure cloud infrastructure and global reach',
        'Strategic partnership with OpenAI',
        'Enterprise customer base and trust',
        'Integration across product portfolio',
      ],
      competitors_mentioned: ['Google', 'Amazon', 'Meta', 'IBM'],
      differentiation: 'Enterprise-focused AI with strong security, compliance, and integration with existing Microsoft ecosystem.',
      concerns_about_competition: [
        "Google's AI research capabilities and resources",
        "Amazon's cloud infrastructure and AI services",
        'Open-source AI model development',
      ],
    },
  },
  enrichment: {
    hiring: {
      total_jobs: 150,
      ai_jobs: 23,
      ai_job_details: [
        {
          title: 'Senior ML Engineer',
          location: 'Seattle, WA (Remote)',
          job_url: 'https://careers.microsoft.com/job/123',
          tech_stack: ['Python', 'TensorFlow', 'Azure ML', 'PyTorch'],
          posted_date: generateMockDate(5),
          seniority: 'senior',
          remote: true,
        },
        {
          title: 'AI Research Scientist',
          location: 'Redmond, WA',
          job_url: 'https://careers.microsoft.com/job/124',
          tech_stack: ['PyTorch', 'CUDA', 'Distributed Training', 'Python'],
          posted_date: generateMockDate(7),
          seniority: 'senior',
          remote: false,
        },
        {
          title: 'Principal AI Architect',
          location: 'San Francisco, CA (Hybrid)',
          job_url: 'https://careers.microsoft.com/job/125',
          tech_stack: ['Azure', 'MLOps', 'Kubernetes', 'Python'],
          posted_date: generateMockDate(3),
          seniority: 'principal',
          remote: true,
        },
        {
          title: 'ML Platform Engineer',
          location: 'Seattle, WA (Remote)',
          job_url: 'https://careers.microsoft.com/job/126',
          tech_stack: ['Python', 'Azure ML', 'Docker', 'Terraform'],
          posted_date: generateMockDate(10),
          seniority: 'senior',
          remote: true,
        },
        {
          title: 'AI Product Manager',
          location: 'Redmond, WA (Hybrid)',
          job_url: 'https://careers.microsoft.com/job/127',
          tech_stack: ['Product Strategy', 'AI/ML', 'Azure'],
          posted_date: generateMockDate(2),
          seniority: 'senior',
          remote: true,
        },
      ],
      hiring_urgency: 'HIGH',
      tech_stack: ['Python', 'PyTorch', 'TensorFlow', 'Azure ML', 'CUDA', 'Kubernetes', 'MLOps'],
      scraped_at: generateMockDate(0),
    },
    recent_news: [
      {
        headline: 'Microsoft announces new AI features in Office 365',
        source: 'TechCrunch',
        date: generateMockDate(2),
        url: 'https://techcrunch.com/microsoft-ai',
        summary: 'Microsoft unveils Copilot Pro with advanced AI capabilities for enterprise customers.',
        category: 'product_launch',
      },
      {
        headline: 'Microsoft invests additional $1.5B in AI infrastructure',
        source: 'Bloomberg',
        date: generateMockDate(5),
        url: 'https://bloomberg.com/microsoft-investment',
        summary: 'Expansion of Azure AI capabilities with new data centers.',
        category: 'investment',
      },
      {
        headline: 'GitHub Copilot reaches 1 million paid subscribers',
        source: 'The Verge',
        date: generateMockDate(8),
        url: 'https://theverge.com/github-copilot',
        summary: 'Developer tool continues strong adoption trajectory.',
        category: 'product_launch',
      },
    ],
    enriched_at: generateMockDate(0),
  },
  ai_maturity: {
    total_score: 85,
    breakdown: {
      investment: 23,
      product: 22,
      strategic_importance: 21,
      organizational_readiness: 19,
    },
    percentile: 92,
    label: 'Leader',
  },
  sdr_playbook: {
    discovery_questions: [
      "I noticed you invested $50M in AI infrastructure last year - what's been the ROI on that investment?",
      "Your 10-K mentions competitive pressure from Google AI - how are you differentiating in the market?",
      "You have 23 open AI roles right now - what capabilities are you building that you don't have today?",
      'How is the Microsoft 365 Copilot rollout going with your enterprise customers?',
      'What challenges are you facing with AI model deployment at scale?',
    ],
    value_propositions: [
      'Help Microsoft-scale organizations leverage similar AI infrastructure',
      'Proven expertise in enterprise AI deployment (23 active AI hiring roles)',
      'Understanding of regulatory and ethical concerns around AI implementation',
      'Experience with Azure-integrated AI solutions',
    ],
    objection_handlers: {
      'too_expensive': "Microsoft invested $50M in AI last year - this represents a fraction of that scale and can help optimize similar investments.",
      'already_have_solution': "With 23 open AI roles, you're clearly scaling - we can accelerate that growth based on your documented needs.",
      'not_a_priority': "Your 10-K mentions AI 47 times and lists it as a competitive differentiator - let's discuss the timeline.",
    },
    executive_summary: 'Microsoft is an AI Leader (85/100) with significant investment ($50M in FY2024) across infrastructure, R&D, and strategic partnerships like OpenAI. They\'re actively hiring 23 AI roles (HIGH urgency) focusing on PyTorch/TensorFlow/Azure ML stack. Recent product launches (Copilot Pro, Security Copilot) show strong execution capability. Primary competitive concern: Google\'s AI research capabilities. Key conversation angles: enterprise AI security, Azure integration, developer productivity tools.',
    talking_points: [
      'Recent $50M AI investment signals aggressive expansion',
      '23 active AI hiring roles indicate rapid scaling phase',
      'OpenAI partnership creates unique market positioning',
      'Competitive pressure from Google mentioned 3x in 10-K',
      'Strong enterprise customer base provides AI deployment advantages',
    ],
  },
  metadata: {
    analyzed_at: generateMockDate(0),
    analysis_time_seconds: 15.3,
    retrieval_time_seconds: 2.1,
    enrichment_time_seconds: 3.2,
    enrichment_completeness: 0.95,
    status: 'complete',
  },

  // Workflow status (for demo UI)
  workflow_status: 'Complete',
  workflow_progress: 100,
  workflow_message: 'Analysis complete',
};

export const mockNvidiaProfile: CompanyProfile = {
  company: mockCompanies[2],
  filing_date: '2024-07-28',
  fiscal_year: 2024,
  ai_insights: {
    investments: [
      {
        amount: '$75M',
        amount_numeric: 75000000,
        purpose: 'AI chip research and next-generation GPU development',
        timeframe: 'FY2024',
        quote: 'Continued investment in AI and accelerated computing research.',
        confidence: 'high',
        source_section: 'mda',
      },
    ],
    products: [
      {
        product_name: 'H100 GPU',
        description: 'High-performance GPU for AI training',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'H100 Tensor Core GPU is driving significant revenue growth.',
        revenue_impact: 'mentioned',
      },
      {
        product_name: 'DGX Cloud',
        description: 'Cloud-based AI infrastructure',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'DGX Cloud provides instant access to AI supercomputing.',
      },
      {
        product_name: 'AI Enterprise',
        description: 'AI software suite for enterprises',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'NVIDIA AI Enterprise simplifies AI deployment.',
      },
      {
        product_name: 'Omniverse',
        description: 'Platform for 3D simulation and collaboration',
        launch_status: 'available',
        target_market: 'enterprise',
        quote: 'Omniverse enables industrial metaverse applications.',
      },
    ],
    risks: [
      {
        category: 'competitive',
        risk: 'Competition from AMD, Intel, and custom AI chips',
        severity: 'high',
        quote: 'We face increasing competition in the AI accelerator market.',
      },
      {
        category: 'implementation',
        risk: 'Supply chain constraints for advanced chip manufacturing',
        severity: 'medium',
        quote: 'Manufacturing capacity constraints could impact growth.',
      },
    ],
    timeline: {
      current_initiatives: ['H100 production ramp', 'DGX Cloud expansion'],
      near_term_plans: ['Next-gen GPU architecture', 'Software ecosystem growth'],
      long_term_vision: 'Enable AI computing at every scale, from edge to cloud.',
      milestones: [
        { date: '2024-Q2', event: 'H100 GPU mass production' },
        { date: '2024-Q4', event: 'Next-gen architecture announcement' },
      ],
    },
    competitive_positioning: {
      strengths: ['Dominant GPU market share', 'CUDA ecosystem', 'AI software stack'],
      competitors_mentioned: ['AMD', 'Intel', 'Google TPU'],
      differentiation: 'Complete AI computing platform with hardware and software integration.',
      concerns_about_competition: ['Custom AI chips from cloud providers', 'AMD GPU competition'],
    },
  },
  enrichment: {
    hiring: {
      total_jobs: 200,
      ai_jobs: 47,
      ai_job_details: [
        {
          title: 'Deep Learning Architect',
          location: 'Santa Clara, CA',
          job_url: 'https://nvidia.com/careers/001',
          tech_stack: ['CUDA', 'PyTorch', 'TensorRT', 'C++'],
          posted_date: generateMockDate(3),
          seniority: 'principal',
          remote: false,
        },
        {
          title: 'AI Infrastructure Engineer',
          location: 'Austin, TX (Remote)',
          job_url: 'https://nvidia.com/careers/002',
          tech_stack: ['Kubernetes', 'CUDA', 'Python', 'Linux'],
          posted_date: generateMockDate(1),
          seniority: 'senior',
          remote: true,
        },
      ],
      hiring_urgency: 'HIGH',
      tech_stack: ['CUDA', 'PyTorch', 'TensorRT', 'C++', 'Python', 'Kubernetes'],
      scraped_at: generateMockDate(0),
    },
    recent_news: [
      {
        headline: 'NVIDIA H100 GPUs in high demand, supply constrained',
        source: 'Reuters',
        date: generateMockDate(4),
        url: 'https://reuters.com/nvidia-h100',
        category: 'product_launch',
      },
    ],
    enriched_at: generateMockDate(0),
  },
  ai_maturity: {
    total_score: 92,
    breakdown: {
      investment: 25,
      product: 24,
      strategic_importance: 23,
      organizational_readiness: 20,
    },
    percentile: 98,
    label: 'Leader',
  },
  sdr_playbook: {
    discovery_questions: [
      "You're hiring 47 AI roles - what's driving this rapid expansion?",
      'How are you managing the supply constraints for H100 GPUs?',
    ],
    value_propositions: [
      'Support for NVIDIA-scale AI infrastructure deployment',
    ],
    objection_handlers: {
      'too_expensive': 'NVIDIA invested $75M in AI - we help optimize similar investments.',
    },
    executive_summary: 'NVIDIA is the top AI Leader (92/100) with massive AI infrastructure investment.',
    talking_points: ['Market leader in AI hardware', '47 active AI job openings'],
  },
  metadata: {
    analyzed_at: generateMockDate(0),
    analysis_time_seconds: 16.5,
    retrieval_time_seconds: 2.3,
    enrichment_time_seconds: 3.5,
    enrichment_completeness: 0.92,
    status: 'complete',
  },

  // Workflow status (for demo UI)
  workflow_status: 'Enriching',
  workflow_progress: 66,
  workflow_message: 'Scraping job postings',
};

export const mockAppleProfile: CompanyProfile = {
  company: mockCompanies[1],
  filing_date: '2024-07-29',
  fiscal_year: 2024,
  ai_insights: {
    investments: [
      {
        amount: '$35M',
        amount_numeric: 35000000,
        purpose: 'On-device AI and machine learning',
        timeframe: 'FY2024',
        quote: 'Investment in on-device AI capabilities for privacy and performance.',
        confidence: 'medium',
        source_section: 'mda',
      },
    ],
    products: [
      {
        product_name: 'Apple Intelligence',
        description: 'On-device AI features across Apple platforms',
        launch_status: 'beta',
        target_market: 'consumer',
        quote: 'Apple Intelligence brings advanced AI to iPhone, iPad, and Mac.',
      },
      {
        product_name: 'Siri Improvements',
        description: 'Enhanced natural language processing',
        launch_status: 'available',
        target_market: 'consumer',
        quote: 'Siri leverages advanced AI models for better understanding.',
      },
    ],
    risks: [
      {
        category: 'competitive',
        risk: 'Competition in consumer AI from Google and Samsung',
        severity: 'medium',
        quote: 'Consumer AI features are becoming key differentiators.',
      },
    ],
    timeline: {
      current_initiatives: ['Apple Intelligence rollout', 'AI chip development'],
      near_term_plans: ['Expand AI features across product line'],
      long_term_vision: 'Privacy-first AI that works seamlessly across Apple ecosystem.',
      milestones: [
        { date: '2024-Q3', event: 'Apple Intelligence public beta' },
      ],
    },
    competitive_positioning: {
      strengths: ['On-device AI processing', 'Privacy focus', 'Custom silicon'],
      competitors_mentioned: ['Google', 'Samsung'],
      differentiation: 'Privacy-preserving on-device AI with custom silicon optimization.',
      concerns_about_competition: ['Google AI capabilities', 'Android AI features'],
    },
  },
  enrichment: {
    hiring: {
      total_jobs: 120,
      ai_jobs: 15,
      ai_job_details: [
        {
          title: 'ML Engineer - Siri',
          location: 'Cupertino, CA',
          job_url: 'https://jobs.apple.com/001',
          tech_stack: ['Python', 'CoreML', 'Swift', 'NLP'],
          posted_date: generateMockDate(6),
          seniority: 'senior',
          remote: false,
        },
      ],
      hiring_urgency: 'NORMAL',
      tech_stack: ['Python', 'CoreML', 'Swift', 'TensorFlow'],
      scraped_at: generateMockDate(0),
    },
    recent_news: [
      {
        headline: 'Apple announces Apple Intelligence at WWDC',
        source: 'The Verge',
        date: generateMockDate(10),
        url: 'https://theverge.com/apple-intelligence',
        category: 'product_launch',
      },
    ],
    enriched_at: generateMockDate(0),
  },
  ai_maturity: {
    total_score: 78,
    breakdown: {
      investment: 18,
      product: 20,
      strategic_importance: 21,
      organizational_readiness: 19,
    },
    percentile: 75,
    label: 'Fast Follower',
  },
  sdr_playbook: {
    discovery_questions: [
      'How is the Apple Intelligence rollout progressing?',
    ],
    value_propositions: [
      'Support for on-device AI deployment at scale',
    ],
    objection_handlers: {
      'too_expensive': 'Apple invested $35M in AI - we help maximize that investment.',
    },
    executive_summary: 'Apple is a Fast Follower (78/100) with focus on privacy-first AI.',
    talking_points: ['Privacy-focused AI approach', 'Custom silicon advantage'],
  },
  metadata: {
    analyzed_at: generateMockDate(0),
    analysis_time_seconds: 14.8,
    retrieval_time_seconds: 2.0,
    enrichment_time_seconds: 3.0,
    enrichment_completeness: 0.88,
    status: 'complete',
  },

  // Workflow status (for demo UI)
  workflow_status: 'Analyzing',
  workflow_progress: 33,
  workflow_message: 'Parsing SEC filings',
};

// ============================================================================
// MOCK PROFILE LOOKUP
// ============================================================================

export const mockProfiles: Record<string, CompanyProfile> = {
  MSFT: mockMicrosoftProfile,
  NVDA: mockNvidiaProfile,
  AAPL: mockAppleProfile,
};

// Generate basic profiles for other companies
mockCompanies.slice(3).forEach((company) => {
  const score = 60 + Math.random() * 30;
  mockProfiles[company.ticker] = {
    company,
    filing_date: '2024-07-30',
    fiscal_year: 2024,
    ai_insights: {
      investments: [
        {
          amount: `$${(20 + Math.random() * 60).toFixed(0)}M`,
          amount_numeric: (20 + Math.random() * 60) * 1000000,
          purpose: 'AI research and development',
          timeframe: 'FY2024',
          quote: 'Investment in AI capabilities.',
          confidence: 'medium',
          source_section: 'mda',
        },
      ],
      products: [],
      risks: [],
      timeline: {
        current_initiatives: ['AI integration'],
        near_term_plans: [],
        long_term_vision: 'AI-powered products and services.',
        milestones: [],
      },
      competitive_positioning: {
        strengths: [],
        competitors_mentioned: [],
        differentiation: '',
        concerns_about_competition: [],
      },
    },
    enrichment: {
      hiring: {
        total_jobs: Math.floor(50 + Math.random() * 150),
        ai_jobs: Math.floor(5 + Math.random() * 30),
        ai_job_details: [],
        hiring_urgency: 'NORMAL',
        tech_stack: ['Python', 'TensorFlow'],
        scraped_at: generateMockDate(0),
      },
      recent_news: [],
      enriched_at: generateMockDate(0),
    },
    ai_maturity: {
      total_score: Math.floor(score),
      breakdown: {
        investment: Math.floor(score * 0.25),
        product: Math.floor(score * 0.25),
        strategic_importance: Math.floor(score * 0.25),
        organizational_readiness: Math.floor(score * 0.25),
      },
      percentile: Math.floor(score * 0.9),
      label: score >= 80 ? 'Leader' : score >= 65 ? 'Fast Follower' : score >= 50 ? 'Emerging' : 'Laggard',
    },
    sdr_playbook: {
      discovery_questions: [],
      value_propositions: [],
      objection_handlers: {},
      executive_summary: `${company.name} AI profile.`,
      talking_points: [],
    },
    metadata: {
      analyzed_at: generateMockDate(0),
      analysis_time_seconds: 15.0,
      retrieval_time_seconds: 2.0,
      enrichment_time_seconds: 3.0,
      enrichment_completeness: 0.9,
      status: 'complete',
    },
  };
});

// ============================================================================
// EXPORT HELPERS
// ============================================================================

export function getMockCompanyProfile(ticker: string): CompanyProfile | undefined {
  return mockProfiles[ticker];
}

export function getAllMockCompanies(): Company[] {
  return mockCompanies;
}

export function getAllMockProfiles(): CompanyProfile[] {
  return Object.values(mockProfiles);
}
