# Product Requirements Document: Intelligence Dashboard UI

**Version:** 1.0.0
**Date:** October 18, 2025
**Hackathon Timeline:** 12 hours
**Dependencies:** API Contract, Lovable.dev base code
**Tech Stack:** React, TypeScript, TailwindCSS

---

## Executive Summary

Build an intuitive dashboard to visualize AI intelligence from 10-K analysis. Display company insights, maturity scores, enrichment data, and enable CRM exports. Integrate with Lovable.dev starter code for rapid UI development.

---

## Objectives

### Primary Goals
1. Real-time pipeline progress visualization
2. Company AI intelligence display (insights, scores, enrichment)
3. Multi-company comparison views
4. Export functionality (Salesforce CSV, PDF playbooks)
5. Responsive design (desktop-first, mobile-friendly)

### Success Metrics
- **Usability:** Non-technical user can understand insights in <30 seconds
- **Performance:** Dashboard loads in <2 seconds
- **Completeness:** All backend data visualized effectively
- **Polish:** Demo-ready UI quality

---

## User Flows

### Flow 1: Start Intelligence Pipeline

```
1. User lands on dashboard → sees company selection grid
2. User selects 3-10 companies (checkboxes)
3. User clicks "Start Intelligence Pipeline"
4. Progress modal appears with real-time updates
5. Companies populate dashboard as they complete
6. Success notification when all complete
```

### Flow 2: Explore Company Intelligence

```
1. User sees company cards on dashboard (grid layout)
2. User clicks on "Microsoft" card
3. Detail modal/page opens with:
   - AI Maturity Score (visual gauge)
   - Investment breakdown
   - Products list
   - Risk factors
   - Live signals (jobs, news)
   - SDR playbook
4. User can export individual playbook PDF
```

### Flow 3: Compare Companies

```
1. User switches to "Compare" view
2. Table shows all companies side-by-side:
   - Maturity scores
   - Investment amounts
   - AI jobs count
   - Products count
3. Sortable columns
4. Visual indicators (Leader/Follower badges)
```

### Flow 4: Export CRM Data

```
1. User clicks "Export to Salesforce" button
2. Modal confirms selection (all companies or subset)
3. CSV generates and downloads
4. Success message with import instructions link
```

---

## Component Architecture

### Page Structure

```
src/
├── pages/
│   ├── Dashboard.tsx          # Main dashboard
│   ├── CompanyDetail.tsx      # Detailed company view
│   └── Comparison.tsx         # Side-by-side comparison
├── components/
│   ├── CompanyCard.tsx        # Company summary card
│   ├── MaturityGauge.tsx      # AI maturity visualization
│   ├── InsightsPanel.tsx      # AI insights display
│   ├── EnrichmentPanel.tsx    # Jobs/news display
│   ├── PlaybookViewer.tsx     # SDR playbook display
│   ├── ProgressTracker.tsx    # Pipeline progress modal
│   ├── CompanySelector.tsx    # Multi-select company picker
│   ├── ExportButtons.tsx      # Export functionality
│   └── ComparisonTable.tsx    # Comparison view table
├── hooks/
│   ├── usePipeline.ts         # Pipeline management hook
│   ├── useCompanies.ts        # Company data hook
│   ├── useWebSocket.ts        # Real-time updates hook
│   └── useExport.ts           # Export functionality hook
├── services/
│   ├── api.ts                 # API client
│   └── websocket.ts           # WebSocket client
├── types/
│   └── api.ts                 # TypeScript types from API contract
└── utils/
    ├── formatters.ts          # Data formatters
    └── validators.ts          # Input validators
```

---

## Component Specifications

### 1. Dashboard Page

**Purpose:** Main view showing all processed companies.

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  🤖 10-K AI Intelligence Dashboard              │
│  [Start Pipeline] [Compare View] [Export All]  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ MSFT     │  │ AAPL     │  │ NVDA     │    │
│  │ Score:85 │  │ Score:78 │  │ Score:92 │    │
│  │ 🔥23 jobs│  │ 🔥15 jobs│  │ 🔥47 jobs│    │
│  └──────────┘  └──────────┘  └──────────┘    │
│                                                 │
│  [+ Add more companies]                         │
└─────────────────────────────────────────────────┘
```

**State:**
```typescript
interface DashboardState {
  companies: CompanyProfile[];
  loading: boolean;
  selectedCompanies: string[]; // tickers
  pipelineJobId: string | null;
}
```

**Key Features:**
- Grid of company cards (responsive: 3 cols desktop, 1 col mobile)
- Floating action button to start pipeline
- Filter/sort companies by maturity score
- Loading skeletons during pipeline execution

---

### 2. CompanyCard Component

**Purpose:** Compact company summary for dashboard grid.

**Props:**
```typescript
interface CompanyCardProps {
  company: CompanyProfile;
  onClick: () => void;
}
```

**Visual Design:**
```
┌────────────────────────┐
│ 🏢 Microsoft (MSFT)    │
│                        │
│ AI Maturity: 85/100    │
│ ████████░░ Leader      │
│                        │
│ 💰 $50M invested       │
│ 🚀 5 AI products       │
│ 🔥 23 open AI roles    │
│ 📰 3 recent news items │
│                        │
│ [View Details →]       │
└────────────────────────┘
```

**Interactions:**
- Hover: Subtle shadow/lift effect
- Click: Opens CompanyDetail modal/page
- Badge: "Leader" / "Fast Follower" / "Emerging"

---

### 3. CompanyDetail Modal/Page

**Purpose:** Full intelligence view for one company.

**Tabs:**
1. **Overview** - AI maturity, investments, executive summary
2. **Products** - AI products/features mentioned
3. **Risks** - Risk factors from 10-K
4. **Live Signals** - Job postings + recent news
5. **SDR Playbook** - Discovery questions, value props

**Tab 1: Overview**
```
┌─────────────────────────────────────────────────┐
│ Microsoft (MSFT)                       [Close X]│
├─────────────────────────────────────────────────┤
│ Overview | Products | Risks | Signals | Playbook│
├─────────────────────────────────────────────────┤
│                                                 │
│  AI Maturity Score: 85/100 (Leader)            │
│  ┌─────────────────────────────────┐          │
│  │       ████████████████████░░░░  │          │
│  │       Investment:       23/25   │          │
│  │       Product:          22/25   │          │
│  │       Strategic:        21/25   │          │
│  │       Organizational:   19/25   │          │
│  └─────────────────────────────────┘          │
│                                                 │
│  📈 Total AI Investment: $50M                  │
│  └─ Research & Development: $30M               │
│  └─ AI Infrastructure: $20M                    │
│                                                 │
│  📄 Filing Date: July 30, 2024                 │
│  ⏱️ Analyzed: Oct 18, 2025 (3 minutes ago)    │
│                                                 │
│  Executive Summary:                             │
│  Microsoft is an AI Leader (85/100) with...    │
│                                                 │
│  [Export Playbook PDF]  [Add to Salesforce]    │
└─────────────────────────────────────────────────┘
```

**Tab 4: Live Signals**
```
┌─────────────────────────────────────────────────┐
│  🔥 Current Hiring Signals                      │
│                                                 │
│  23 AI Roles Open (HIGH urgency)               │
│                                                 │
│  • Senior ML Engineer - Seattle, WA (Remote)   │
│    Stack: Python, TensorFlow, Azure ML         │
│    Posted: 5 days ago                          │
│                                                 │
│  • AI Research Scientist - Redmond, WA         │
│    Stack: PyTorch, CUDA, Distributed Training  │
│    Posted: 1 week ago                          │
│                                                 │
│  [View all 23 jobs →]                          │
│                                                 │
├─────────────────────────────────────────────────┤
│  📰 Recent AI News (Last 30 days)              │
│                                                 │
│  • Oct 15: Microsoft announces Copilot Pro     │
│    Source: TechCrunch | Product Launch         │
│    [Read article →]                            │
│                                                 │
│  • Oct 8: $1.5B AI investment in France        │
│    Source: Bloomberg | Investment              │
│    [Read article →]                            │
└─────────────────────────────────────────────────┘
```

---

### 4. ProgressTracker Component

**Purpose:** Real-time pipeline execution visualization.

**Modal Design:**
```
┌─────────────────────────────────────────────────┐
│  Processing 10 Companies...            [X]      │
├─────────────────────────────────────────────────┤
│                                                 │
│  Overall Progress: 6/10 companies (60%)         │
│  ████████████░░░░░░░░                          │
│                                                 │
│  ✅ Microsoft (MSFT) - Complete (18s)          │
│  ✅ Apple (AAPL) - Complete (21s)              │
│  ✅ NVIDIA (NVDA) - Complete (15s)             │
│  ✅ Alphabet (GOOGL) - Complete (19s)          │
│  ✅ Amazon (AMZN) - Complete (23s)             │
│  ✅ Meta (META) - Complete (17s)               │
│  🔄 Tesla (TSLA) - Enriching... (Career scrape)│
│  ⏳ Salesforce (CRM) - Analyzing...            │
│  ⏳ Adobe (ADBE) - Pending                     │
│  ⏳ Netflix (NFLX) - Pending                   │
│                                                 │
│  Estimated completion: 1m 45s                   │
└─────────────────────────────────────────────────┘
```

**Features:**
- Live updates via WebSocket
- Per-company status icons
- Estimated time remaining
- Error handling (red icon + error message)
- Auto-close on completion (with success message)

---

### 5. ComparisonTable Component

**Purpose:** Side-by-side company comparison.

**Table Columns:**
```
┌───────┬─────────┬──────────┬─────────┬──────────┬──────────┐
│ Rank  │ Company │ Maturity │ Invest  │ Products │ AI Jobs  │
├───────┼─────────┼──────────┼─────────┼──────────┼──────────┤
│  🥇 1 │ NVDA    │ 92 ████  │ $75M    │ 8        │ 47       │
│  🥈 2 │ MSFT    │ 85 ████  │ $50M    │ 5        │ 23       │
│  🥉 3 │ GOOGL   │ 82 ███   │ $40M    │ 6        │ 31       │
│    4  │ AAPL    │ 78 ███   │ $35M    │ 4        │ 15       │
│    5  │ AMZN    │ 75 ███   │ $30M    │ 3        │ 19       │
└───────┴─────────┴──────────┴─────────┴──────────┴──────────┘
```

**Features:**
- Sortable columns (click header to sort)
- Visual progress bars for maturity score
- Color coding (green=high, yellow=medium, red=low)
- Export to CSV button
- Filter by maturity label (Leader/Follower/etc.)

---

## State Management

**Recommended: React Context + Custom Hooks**

```typescript
// src/context/AppContext.tsx
interface AppState {
  companies: CompanyProfile[];
  pipelineJob: PipelineJob | null;
  loading: boolean;
  error: string | null;
}

interface PipelineJob {
  jobId: string;
  status: 'in_progress' | 'completed' | 'failed';
  progress: {
    current_stage: string;
    companies_processed: number;
    companies_total: number;
    percentage: number;
  };
}
```

**Alternative:** Zustand for simpler state management

---

## API Integration

### usePipeline Hook

```typescript
// src/hooks/usePipeline.ts

export function usePipeline() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatus | null>(null);

  const startPipeline = async (tickers: string[]) => {
    const response = await api.post('/pipeline/start', {
      company_tickers: tickers
    });
    const { job_id } = response.data;
    setJobId(job_id);

    // Connect WebSocket for updates
    connectWebSocket(job_id);
  };

  const connectWebSocket = (jobId: string) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/pipeline/${jobId}`);

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleWebSocketMessage(message);
    };
  };

  return { startPipeline, jobId, status };
}
```

### useCompanies Hook

```typescript
// src/hooks/useCompanies.ts

export function useCompanies() {
  const [companies, setCompanies] = useState<CompanyProfile[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchCompany = async (ticker: string) => {
    const response = await api.get(`/companies/${ticker}`);
    return response.data;
  };

  const fetchAllCompanies = async (tickers: string[]) => {
    const promises = tickers.map(fetchCompany);
    const results = await Promise.all(promises);
    setCompanies(results);
  };

  return { companies, fetchCompany, fetchAllCompanies, loading };
}
```

---

## Styling & Design System

### Theme

```typescript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',  // Blue
          600: '#2563eb',
        },
        success: '#10b981',  // Green
        warning: '#f59e0b',  // Yellow
        danger: '#ef4444',   // Red
        maturity: {
          leader: '#10b981',
          follower: '#3b82f6',
          emerging: '#f59e0b',
          laggard: '#ef4444',
        }
      }
    }
  }
}
```

### Component Library

**Use shadcn/ui** for pre-built components:
- Button, Card, Badge, Progress
- Modal/Dialog, Table, Tabs
- Skeleton loaders

**Custom Components:**
- MaturityGauge (circular progress indicator)
- JobListItem, NewsListItem
- PlaybookSection

---

## Responsive Design

**Breakpoints:**
- Mobile: < 640px (stack all cards vertically)
- Tablet: 640px - 1024px (2 column grid)
- Desktop: > 1024px (3-4 column grid)

**Mobile Considerations:**
- Simplified company cards (fewer metrics)
- Bottom sheet instead of modals
- Touch-friendly button sizes (min 44x44px)

---

## Lovable.dev Integration Notes

**What Lovable Provides:**
- Base React + Vite setup
- TailwindCSS configured
- Component scaffolding
- Routing setup

**What We Need to Add:**
- API integration layer
- WebSocket client
- Custom business components
- TypeScript types from API contract

**Strategy:**
1. Use Lovable base for layout/navigation
2. Replace placeholder components with real data components
3. Add API hooks for data fetching
4. Integrate WebSocket for real-time updates

---

## Testing Strategy

### Unit Tests (Vitest)

```typescript
// CompanyCard.test.tsx
describe('CompanyCard', () => {
  it('renders company name and ticker', () => {
    const company = mockCompanyProfile;
    render(<CompanyCard company={company} onClick={vi.fn()} />);
    expect(screen.getByText('Microsoft (MSFT)')).toBeInTheDocument();
  });

  it('displays maturity score', () => {
    const company = { ...mockCompanyProfile, ai_maturity: { total_score: 85 } };
    render(<CompanyCard company={company} onClick={vi.fn()} />);
    expect(screen.getByText('85/100')).toBeInTheDocument();
  });
});
```

### Integration Tests

```typescript
// Dashboard.integration.test.tsx
describe('Dashboard', () => {
  it('starts pipeline and shows progress', async () => {
    render(<Dashboard />);

    // Select companies
    fireEvent.click(screen.getByLabelText('MSFT'));
    fireEvent.click(screen.getByLabelText('AAPL'));

    // Start pipeline
    fireEvent.click(screen.getByText('Start Pipeline'));

    // Expect progress modal
    await waitFor(() => {
      expect(screen.getByText('Processing 2 Companies...')).toBeInTheDocument();
    });
  });
});
```

### E2E Tests (Playwright - Optional)

```typescript
test('complete pipeline flow', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('text=Start Pipeline');
  await page.waitForSelector('text=Complete');
  await expect(page.locator('.company-card')).toHaveCount(10);
});
```

---

## Implementation Phases

### Phase 1: Setup & Scaffolding (30 minutes)
- [ ] Integrate Lovable.dev base code
- [ ] Setup TypeScript types from API contract
- [ ] Configure API client with mock data
- [ ] Create component stubs

### Phase 2: Core Components (90 minutes)
- [ ] Implement CompanyCard component
- [ ] Implement CompanyDetail modal
- [ ] Implement Dashboard page layout
- [ ] Add basic styling with Tailwind

### Phase 3: Pipeline Integration (60 minutes)
- [ ] Implement usePipeline hook
- [ ] Build ProgressTracker component
- [ ] Add WebSocket connection
- [ ] Handle real-time updates

### Phase 4: Data Visualization (60 minutes)
- [ ] Build MaturityGauge component
- [ ] Create InsightsPanel (investments, products, risks)
- [ ] Build EnrichmentPanel (jobs, news)
- [ ] Implement PlaybookViewer

### Phase 5: Comparison & Export (45 minutes)
- [ ] Build ComparisonTable component
- [ ] Implement export functionality
- [ ] Add CSV download
- [ ] PDF download integration

### Phase 6: Polish & Testing (45 minutes)
- [ ] Responsive design tweaks
- [ ] Loading states and skeletons
- [ ] Error handling UI
- [ ] Write critical tests
- [ ] Demo preparation

**Total Estimated Time:** 5.5 hours

---

## Demo Script

```
"Let me show you the dashboard.

[Open browser]

Here we have our intelligence pipeline. I'll select 3 companies to analyze.

[Check MSFT, NVDA, AAPL]

Watch this - I'm clicking Start Pipeline, and you'll see real-time updates as we scrape the 10-Ks and enrich the data.

[Progress modal appears]

See? Microsoft just completed in 18 seconds. NVIDIA done. Apple done.

[Modal closes, cards populate]

Now we have these beautiful cards showing AI maturity scores. Microsoft is an 85 - that's a Leader. They have 23 open AI roles RIGHT NOW and invested $50 million last year.

[Click on MSFT card]

Click into Microsoft and you get the full intelligence brief. Here are their 5 AI products, their risk factors mentioning competitors, and look at this SDR playbook - these are specific discovery questions based on their 10-K.

[Click Playbook tab]

'I noticed you invested $50M in AI infrastructure - what's been the ROI?'
'Your 10-K mentions competitive pressure from Google AI - how are you differentiating?'

These aren't generic questions. These are researched, specific, and based on facts we extracted from 500 pages of legal documents.

[Click Export]

And when you're ready, export to Salesforce - one click, CSV is ready, import instructions included.

[Show comparison view]

Or compare all companies side-by-side. NVIDIA leads with a 92 maturity score and 47 open AI roles. They're scaling FAST.

From 10-K filing to actionable intelligence in under 10 minutes, fully automated."
```

---

## Accessibility

- Semantic HTML (`<button>`, `<nav>`, `<main>`)
- ARIA labels for interactive elements
- Keyboard navigation support
- Screen reader friendly
- Color contrast ratios meet WCAG AA

---

## Performance Optimization

- React.memo for expensive components
- Virtualized lists for large datasets (job postings)
- Lazy loading for detail modals
- Image optimization (company logos)
- Code splitting by route

---

## Known Limitations

1. **No historical data:** Only shows latest 10-K analysis
2. **Limited filtering:** Basic filter/sort only
3. **No user accounts:** No saved preferences
4. **Desktop-first:** Mobile is functional but not optimized

---

## Success Criteria

✅ Pipeline progress visible in real-time
✅ All company data displayed accurately
✅ Comparison view enables quick insights
✅ Export generates valid Salesforce CSV
✅ UI is polished and demo-ready
✅ Responsive on tablet and desktop

---

**Next Steps:**
1. Frontend team: Start with mock data and component development
2. Backend team: Implement API endpoints per contract
3. Integration: Connect real API once ready
4. Demo: Practice full flow and refine UX

---

**Questions for Clarification:**
1. Should we persist company selections (localStorage)?
2. Do we need user authentication?
3. Should we support custom company additions (beyond the 10)?
4. Do we need data refresh capability (re-analyze same company)?
