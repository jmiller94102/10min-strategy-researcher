import { AIMaturity } from "@/types/api";

interface MaturityGaugeProps {
  maturity: AIMaturity;
}

export const MaturityGauge = ({ maturity }: MaturityGaugeProps) => {
  const categories = [
    { label: 'Investment', value: maturity.breakdown.investment },
    { label: 'Product', value: maturity.breakdown.product },
    { label: 'Strategic', value: maturity.breakdown.strategic },
    { label: 'Organizational', value: maturity.breakdown.organizational },
  ];

  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-warm shadow-glow">
          <div className="w-28 h-28 rounded-full bg-card flex items-center justify-center">
            <div>
              <div className="text-4xl font-bold text-primary">{maturity.total_score}</div>
              <div className="text-sm text-muted-foreground">/100</div>
            </div>
          </div>
        </div>
        <div className="mt-4">
          <div className="text-2xl font-semibold">{maturity.label}</div>
        </div>
      </div>

      <div className="space-y-3">
        {categories.map((cat) => (
          <div key={cat.label}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-muted-foreground">{cat.label}</span>
              <span className="font-semibold">{cat.value}/25</span>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-warm transition-all duration-500"
                style={{ width: `${(cat.value / 25) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
