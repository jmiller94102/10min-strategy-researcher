import { useState } from "react";
import { ChevronLeft, ChevronRight, Activity, Box, Zap } from "lucide-react";
import { WorkflowStep } from "@/types/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface DebugPanelProps {
  steps: WorkflowStep[];
  currentCompany?: string;
}

export const DebugPanel = ({ steps, currentCompany }: DebugPanelProps) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [selectedCompany, setSelectedCompany] = useState(currentCompany || 'MSFT');

  const companies = [
    { value: 'MSFT', label: 'MSFT - Microsoft' },
    { value: 'NVDA', label: 'NVDA - NVIDIA' },
    { value: 'AAPL', label: 'AAPL - Apple' },
  ];

  const getToolIcon = (tool: string) => {
    switch (tool) {
      case 'Browser Use':
        return <Activity className="h-4 w-4" />;
      case 'Daytona':
        return <Box className="h-4 w-4" />;
      case 'Agent':
        return <Zap className="h-4 w-4" />;
      default:
        return <Activity className="h-4 w-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'complete':
        return 'bg-success text-white';
      case 'running':
        return 'bg-primary text-primary-foreground';
      case 'error':
        return 'bg-destructive text-destructive-foreground';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  const getDuration = (step: WorkflowStep) => {
    if (!step.startTime) return null;
    const end = step.endTime || Date.now();
    const duration = (end - step.startTime) / 1000;
    return duration.toFixed(1) + 's';
  };

  return (
    <div
      className={`fixed right-0 top-0 h-screen bg-debug-bg text-debug-foreground border-l border-debug-border transition-all duration-300 z-50 ${
        isExpanded ? 'w-80' : 'w-12'
      }`}
    >
      <Button
        variant="ghost"
        size="icon"
        className="absolute -left-10 top-4 bg-debug-bg hover:bg-debug-bg/90 text-debug-foreground border border-debug-border"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {isExpanded ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
      </Button>

      {isExpanded && (
        <div className="flex flex-col h-full p-4">
          <div className="mb-4">
            <h2 className="text-lg font-semibold mb-1">Workflow Debug</h2>
            <p className="text-xs text-debug-foreground/70 mb-3">Live hackathon demo panel</p>

            <Select value={selectedCompany} onValueChange={setSelectedCompany}>
              <SelectTrigger className="w-full bg-debug-bg border-debug-border text-debug-foreground">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-debug-bg border-debug-border text-debug-foreground">
                {companies.map((company) => (
                  <SelectItem
                    key={company.value}
                    value={company.value}
                    className="text-debug-foreground hover:bg-debug-accent/20"
                  >
                    {company.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <ScrollArea className="flex-1">
            <div className="space-y-2">
              {steps.map((step, index) => (
                <div
                  key={step.id}
                  className={`p-3 rounded-lg border transition-all ${
                    step.status === 'running'
                      ? 'border-debug-accent bg-debug-accent/10 shadow-glow'
                      : 'border-debug-border bg-debug-bg/50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <div className={`p-1 rounded ${getStatusColor(step.status)}`}>
                        {getToolIcon(step.tool)}
                      </div>
                      <div>
                        <div className="text-sm font-medium">{step.name}</div>
                        <div className="text-xs text-debug-foreground/60">{step.tool}</div>
                      </div>
                    </div>
                    {getDuration(step) && (
                      <span className="text-xs text-debug-foreground/60">{getDuration(step)}</span>
                    )}
                  </div>
                  
                  {step.status === 'running' && (
                    <div className="flex items-center gap-2 mt-2">
                      <div className="animate-pulse h-1 flex-1 bg-debug-accent/30 rounded-full overflow-hidden">
                        <div className="h-full bg-debug-accent w-1/2 animate-[slide_1s_ease-in-out_infinite]" />
                      </div>
                    </div>
                  )}
                  
                  {step.details && (
                    <p className="text-xs text-debug-foreground/70 mt-2">{step.details}</p>
                  )}
                </div>
              ))}

              {steps.length === 0 && (
                <div className="text-center text-debug-foreground/50 text-sm py-8">
                  No workflow steps yet. Start a pipeline to see activity.
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="mt-4 pt-4 border-t border-debug-border">
            <div className="text-xs text-debug-foreground/50 space-y-1">
              <div>• Browser Use: SEC filing scraper</div>
              <div>• Daytona: Dev environment</div>
              <div>• Agent: AI processing steps</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
