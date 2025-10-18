import { CompanyProfile } from "@/types/api";
import { MaturityGauge } from "./MaturityGauge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Download, ExternalLink, TrendingUp, Package, AlertTriangle, Radio, FileText } from "lucide-react";

interface CompanyDetailProps {
  company: CompanyProfile | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const CompanyDetail = ({ company, open, onOpenChange }: CompanyDetailProps) => {
  if (!company) return null;

  // ✅ FIXED: Use new nested structure (company.ai_insights.investments)
  const totalInvestment = company.ai_insights.investments.reduce((sum, inv) => sum + inv.amount_numeric, 0);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] p-0">
        <DialogHeader className="px-6 pt-6 pb-4 border-b border-border">
          <div className="flex items-start justify-between">
            <div>
              <DialogTitle className="text-2xl font-bold">{company.company.name}</DialogTitle>
              <p className="text-sm text-muted-foreground mt-1">{company.company.ticker} • Filed {company.filing_date}</p>
            </div>
            <Badge className="bg-gradient-warm text-white">
              {company.ai_maturity.label}
            </Badge>
          </div>
        </DialogHeader>

        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="w-full justify-start rounded-none border-b border-border px-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="products">Products</TabsTrigger>
            <TabsTrigger value="risks">Risks</TabsTrigger>
            <TabsTrigger value="signals">Live Signals</TabsTrigger>
            <TabsTrigger value="playbook">SDR Playbook</TabsTrigger>
          </TabsList>

          <ScrollArea className="h-[60vh]">
            <div className="px-6 py-6">
              <TabsContent value="overview" className="mt-0 space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <MaturityGauge maturity={company.ai_maturity} />
                  
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                        <TrendingUp className="h-5 w-5 text-primary" />
                        AI Investments
                      </h3>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                          <span className="font-semibold">Total Investment</span>
                          <span className="text-xl font-bold text-primary">
                            ${(totalInvestment / 1_000_000).toFixed(0)}M
                          </span>
                        </div>
                        {company.ai_insights.investments.map((inv, i) => (
                          <div key={i} className="flex justify-between items-center text-sm">
                            <span className="text-muted-foreground">{inv.purpose}</span>
                            <span className="font-semibold">{inv.amount}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="p-4 bg-gradient-subtle rounded-lg border border-border">
                      <p className="text-sm leading-relaxed">{company.sdr_playbook.executive_summary}</p>
                    </div>
                  </div>
                </div>

                <div className="flex gap-3 pt-4 border-t border-border">
                  <Button className="bg-gradient-warm">
                    <Download className="h-4 w-4 mr-2" />
                    Export Playbook PDF
                  </Button>
                  <Button variant="outline">
                    Add to Salesforce
                  </Button>
                </div>
              </TabsContent>

              <TabsContent value="products" className="mt-0">
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Package className="h-5 w-5 text-primary" />
                    AI Products & Features
                  </h3>
                  <div className="grid gap-2">
                    {company.ai_insights.products.map((product, i) => (
                      <div key={i} className="p-3 bg-muted/30 rounded-lg border border-border hover:border-primary/50 transition-colors">
                        <div className="font-medium">{product.product_name}</div>
                        <p className="text-xs text-muted-foreground mt-1">{product.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="risks" className="mt-0">
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-warning" />
                    Risk Factors
                  </h3>
                  <div className="space-y-3">
                    {company.ai_insights.risks.map((riskItem, i) => (
                      <div key={i} className="p-4 bg-warning/5 border border-warning/20 rounded-lg">
                        <div className="font-semibold text-sm mb-1 capitalize">{riskItem.category}</div>
                        <p className="text-sm">{riskItem.risk}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="signals" className="mt-0 space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Radio className="h-5 w-5 text-primary" />
                      Current Hiring Signals
                    </h3>
                    <Badge variant={company.enrichment.hiring.hiring_urgency === 'HIGH' ? 'default' : 'secondary'}>
                      {company.enrichment.hiring.hiring_urgency} urgency
                    </Badge>
                  </div>

                  <div className="text-2xl font-bold mb-4">
                    {company.enrichment.hiring.ai_jobs} AI Roles Open
                  </div>

                  <div className="space-y-3">
                    {company.enrichment.hiring.ai_job_details.slice(0, 5).map((job, i) => (
                      <div key={i} className="p-4 bg-card border border-border rounded-lg hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-semibold">{job.title}</h4>
                            <p className="text-sm text-muted-foreground">{job.location}</p>
                          </div>
                          <ExternalLink className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <div className="flex flex-wrap gap-2 mt-3">
                          {job.tech_stack.map((tech, j) => (
                            <Badge key={j} variant="outline" className="text-xs">
                              {tech}
                            </Badge>
                          ))}
                        </div>
                        <p className="text-xs text-muted-foreground mt-2">Posted {job.posted_date}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {company.enrichment.recent_news.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Recent AI News</h3>
                    <div className="space-y-3">
                      {company.enrichment.recent_news.map((news, i) => (
                        <div key={i} className="p-4 bg-info/5 border border-info/20 rounded-lg">
                          <h4 className="font-semibold mb-1">{news.headline}</h4>
                          <div className="flex items-center gap-3 text-xs text-muted-foreground">
                            <span>{news.source}</span>
                            <span>•</span>
                            <span>{news.category}</span>
                            <span>•</span>
                            <span>{news.date}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="playbook" className="mt-0 space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <FileText className="h-5 w-5 text-primary" />
                    Discovery Questions
                  </h3>
                  <div className="space-y-2">
                    {company.sdr_playbook.discovery_questions.map((question, i) => (
                      <div key={i} className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
                        <p className="text-sm italic">"{question}"</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">Value Propositions</h3>
                  <div className="space-y-2">
                    {company.sdr_playbook.value_propositions.map((prop, i) => (
                      <div key={i} className="p-3 bg-success/5 border border-success/20 rounded-lg">
                        <p className="text-sm">✓ {prop}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">Competitive Angles</h3>
                  <div className="space-y-2">
                    {company.sdr_playbook.competitive_angles.map((angle, i) => (
                      <div key={i} className="p-3 bg-accent/5 border border-accent/20 rounded-lg">
                        <p className="text-sm">→ {angle}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>
            </div>
          </ScrollArea>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};
