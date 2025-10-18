import { Building2, TrendingUp, Briefcase, Newspaper, Activity } from "lucide-react";
import { CompanyProfile } from "@/types/api";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface CompanyCardProps {
  company: CompanyProfile;
  onClick: () => void;
}

export const CompanyCard = ({ company, onClick }: CompanyCardProps) => {
  const getMaturityColor = (label: string) => {
    switch (label) {
      case 'Leader':
        return 'bg-maturity-leader text-white';
      case 'Fast Follower':
        return 'bg-maturity-follower text-white';
      case 'Emerging':
        return 'bg-maturity-emerging text-white';
      case 'Laggard':
        return 'bg-maturity-laggard text-white';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  const totalInvestment = company.ai_insights.investments.reduce((sum, inv) => sum + inv.amount_numeric, 0);
  const jobCount = company.enrichment?.hiring?.ai_jobs || 0;
  const newsCount = company.enrichment?.recent_news?.length || 0;

  return (
    <Card
      className="group cursor-pointer bg-gradient-card border-border hover:shadow-lg hover:scale-[1.02] transition-all duration-300"
      onClick={onClick}
    >
      <div className="p-6 space-y-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Building2 className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-lg">{company.company.name}</h3>
              <p className="text-sm text-muted-foreground">{company.company.ticker}</p>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Workflow Status
            </span>
            <Badge className={
              company.workflow_status === 'Complete' ? 'bg-success text-white' :
              company.workflow_status === 'Enriching' ? 'bg-orange-500 text-white' :
              company.workflow_status === 'Analyzing' ? 'bg-orange-500 text-white' :
              'bg-muted text-muted-foreground'
            }>
              {company.workflow_status || 'Pending'}
            </Badge>
          </div>

          <div className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">{company.workflow_message || 'Waiting to start'}</span>
              <span className="font-semibold">{company.workflow_progress || 0}%</span>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-warm transition-all duration-500"
                style={{ width: `${company.workflow_progress || 0}%` }}
              />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-border/50">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-primary" />
            <div>
              <div className="text-xs text-muted-foreground">Investment</div>
              <div className="text-sm font-semibold">${(totalInvestment / 1_000_000).toFixed(0)}M</div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Briefcase className="h-4 w-4 text-primary" />
            <div>
              <div className="text-xs text-muted-foreground">AI Jobs</div>
              <div className="text-sm font-semibold">{jobCount}</div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-sm text-muted-foreground pt-2">
          <Newspaper className="h-4 w-4" />
          <span>{newsCount} recent news items</span>
        </div>

        <Button 
          variant="outline" 
          className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
        >
          View Details →
        </Button>
      </div>
    </Card>
  );
};
