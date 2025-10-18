import { useState } from "react";
import { CompanyCard } from "@/components/CompanyCard";
import { CompanyDetail } from "@/components/CompanyDetail";
import { DebugPanel } from "@/components/DebugPanel";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Play, Download, GitCompare } from "lucide-react";
import { CompanyProfile, WorkflowStep } from "@/types/api";
import { mockMicrosoftProfile, mockNvidiaProfile, mockAppleProfile } from "@/mocks/mockData";

// Mock companies with workflow status
const mockCompanies: CompanyProfile[] = [
  mockMicrosoftProfile,
  mockNvidiaProfile,
  mockAppleProfile,
];

// OLD inline mock data (kept for reference but not used)
const oldMockCompanies: CompanyProfile[] = [
  {
    ticker: "MSFT",
    company_name: "Microsoft",
    filing_date: "2024-07-30",
    analyzed_at: "2025-10-18T10:30:00Z",
    ai_maturity: {
      total_score: 85,
      label: "Leader",
      breakdown: { investment: 23, product: 22, strategic: 21, organizational: 19 }
    },
    investments: [
      { category: "R&D", amount: 30_000_000, description: "AI Research" },
      { category: "Infrastructure", amount: 20_000_000, description: "Azure AI" }
    ],
    products: ["GitHub Copilot", "Azure OpenAI", "Microsoft 365 Copilot", "Bing Chat", "Security Copilot"],
    risk_factors: ["Competition from Google AI", "Regulatory scrutiny", "Talent acquisition challenges"],
    enrichment: {
      jobs: [
        {
          title: "Senior ML Engineer",
          location: "Seattle, WA (Remote)",
          posted_date: "2025-10-13",
          tech_stack: ["Python", "TensorFlow", "Azure ML"],
          url: "#"
        },
        {
          title: "AI Research Scientist",
          location: "Redmond, WA",
          posted_date: "2025-10-11",
          tech_stack: ["PyTorch", "CUDA", "Distributed Training"],
          url: "#"
        }
      ],
      news: [
        {
          title: "Microsoft announces Copilot Pro",
          date: "2025-10-15",
          source: "TechCrunch",
          category: "Product Launch",
          url: "#"
        }
      ],
      signals: { hiring_velocity: "HIGH", recent_launches: 3 }
    },
    sdr_playbook: {
      discovery_questions: [
        "I noticed you invested $50M in AI infrastructure - what's been the ROI?",
        "Your 10-K mentions competitive pressure from Google AI - how are you differentiating?"
      ],
      value_propositions: ["Enterprise-grade AI at scale", "Deep Microsoft ecosystem integration"],
      competitive_angles: ["More enterprise-focused than Google", "Better security than OpenAI"],
      executive_summary: "Microsoft is an AI Leader with strategic investments across product portfolio..."
    }
  },
  {
    ticker: "NVDA",
    company_name: "NVIDIA",
    filing_date: "2024-08-15",
    analyzed_at: "2025-10-18T10:32:00Z",
    ai_maturity: {
      total_score: 92,
      label: "Leader",
      breakdown: { investment: 24, product: 24, strategic: 23, organizational: 21 }
    },
    investments: [
      { category: "Chip Development", amount: 45_000_000, description: "Next-gen AI chips" },
      { category: "Software", amount: 30_000_000, description: "CUDA ecosystem" }
    ],
    products: ["H100 GPUs", "DGX Systems", "CUDA", "Omniverse", "AI Enterprise"],
    risk_factors: ["Supply chain dependencies", "Competition from AMD", "Export restrictions"],
    enrichment: {
      jobs: Array(47).fill(null).map((_, i) => ({
        title: `AI Engineer ${i + 1}`,
        location: "Santa Clara, CA",
        posted_date: "2025-10-10",
        tech_stack: ["CUDA", "C++", "Python"],
        url: "#"
      })),
      news: [
        {
          title: "NVIDIA announces new AI chip architecture",
          date: "2025-10-12",
          source: "Bloomberg",
          category: "Product Launch",
          url: "#"
        }
      ],
      signals: { hiring_velocity: "HIGH", recent_launches: 2 }
    },
    sdr_playbook: {
      discovery_questions: ["How are you scaling your AI infrastructure?"],
      value_propositions: ["Industry-leading GPU performance"],
      competitive_angles: ["Superior to AMD in AI workloads"],
      executive_summary: "NVIDIA leads AI hardware with dominant market position..."
    }
  },
  {
    ticker: "AAPL",
    company_name: "Apple",
    filing_date: "2024-09-01",
    analyzed_at: "2025-10-18T10:33:00Z",
    ai_maturity: {
      total_score: 78,
      label: "Fast Follower",
      breakdown: { investment: 20, product: 19, strategic: 20, organizational: 19 }
    },
    investments: [
      { category: "AI Research", amount: 25_000_000, description: "On-device AI" },
      { category: "Acquisitions", amount: 10_000_000, description: "AI startups" }
    ],
    products: ["Apple Intelligence", "Siri", "Neural Engine", "Core ML"],
    risk_factors: ["Late to generative AI", "Privacy constraints limit data collection"],
    enrichment: {
      jobs: Array(15).fill(null).map((_, i) => ({
        title: `ML Scientist ${i + 1}`,
        location: "Cupertino, CA",
        posted_date: "2025-10-08",
        tech_stack: ["Swift", "Metal", "Core ML"],
        url: "#"
      })),
      news: [],
      signals: { hiring_velocity: "MEDIUM", recent_launches: 1 }
    },
    sdr_playbook: {
      discovery_questions: ["How is Apple Intelligence performing for your users?"],
      value_propositions: ["Privacy-first AI approach"],
      competitive_angles: ["More privacy-focused than competitors"],
      executive_summary: "Apple is catching up in AI with on-device focus..."
    }
  }
];

const Dashboard = () => {
  const [companies] = useState<CompanyProfile[]>(mockCompanies);
  const [selectedCompany, setSelectedCompany] = useState<CompanyProfile | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  
  // Mock workflow steps for debug panel
  const [workflowSteps] = useState<WorkflowStep[]>([
    {
      id: "1",
      name: "Scrape SEC Filing",
      tool: "Browser Use",
      status: "complete",
      startTime: Date.now() - 120000,
      endTime: Date.now() - 105000,
      details: "Retrieved 10-K filing from SEC EDGAR"
    },
    {
      id: "2",
      name: "Parse Document",
      tool: "Agent",
      status: "complete",
      startTime: Date.now() - 105000,
      endTime: Date.now() - 90000,
      details: "Extracted sections: MD&A, Risk Factors, Notes"
    },
    {
      id: "3",
      name: "Analyze AI Investment",
      tool: "Agent",
      status: "complete",
      startTime: Date.now() - 90000,
      endTime: Date.now() - 75000,
      details: "Calculated maturity scores across dimensions"
    },
    {
      id: "4",
      name: "Scrape Job Postings",
      tool: "Browser Use",
      status: "running",
      startTime: Date.now() - 15000,
      details: "Searching careers page for AI roles..."
    },
    {
      id: "5",
      name: "Generate Playbook",
      tool: "Agent",
      status: "pending",
      details: "Waiting for enrichment data"
    }
  ]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">🤖 10-K AI Intelligence</h1>
              <p className="text-sm text-muted-foreground">Automated company intelligence from SEC filings</p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline" size="sm">
                <GitCompare className="h-4 w-4 mr-2" />
                Compare
              </Button>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export All
              </Button>
              <Button size="sm" className="bg-gradient-warm">
                <Play className="h-4 w-4 mr-2" />
                Start Pipeline
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 pr-24">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <Badge variant="outline" className="mb-2">
              {companies.length} companies analyzed
            </Badge>
            <p className="text-sm text-muted-foreground">Click any card to view detailed intelligence</p>
          </div>
        </div>

        {/* Company Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <CompanyCard
              key={company.company.ticker}
              company={company}
              onClick={() => {
                setSelectedCompany(company);
                setDetailOpen(true);
              }}
            />
          ))}
        </div>

        {/* Empty State */}
        {companies.length === 0 && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
              <Play className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-2">No companies analyzed yet</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Start the intelligence pipeline to analyze 10-K filings
            </p>
            <Button className="bg-gradient-warm">
              <Play className="h-4 w-4 mr-2" />
              Start Pipeline
            </Button>
          </div>
        )}
      </main>

      {/* Debug Panel */}
      <DebugPanel
        steps={workflowSteps}
        currentCompany={selectedCompany?.company.ticker}
      />

      {/* Company Detail Modal */}
      <CompanyDetail
        company={selectedCompany}
        open={detailOpen}
        onOpenChange={setDetailOpen}
      />
    </div>
  );
};

export default Dashboard;
