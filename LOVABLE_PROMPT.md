# Lovable.dev Prompt: 10-K AI Intelligence Dashboard

**Use this prompt with Lovable.dev to generate the frontend starter code.**

---

## Project Overview

Build a modern, intuitive dashboard to visualize AI intelligence extracted from company 10-K filings. The dashboard shows company AI maturity scores, investments, products, hiring signals, and generates CRM-ready exports.

---

## Tech Stack Requirements

- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **UI Components:** shadcn/ui (install as needed)
- **State Management:** React Context API or Zustand (lightweight)
- **Data Fetching:** TanStack Query (React Query)
- **Routing:** React Router v6

---

## Core Features to Build

### 1. Dashboard Page (Main View)

**Layout:**
- Clean, modern design with a header bar
- Grid of company cards (3 columns on desktop, 1 on mobile)
- Floating action button to "Start Pipeline"
- Export buttons in header (Salesforce CSV, PDF Playbooks)

**Company Card Component:**
Each card shows:
- Company name and ticker (e.g., "Microsoft (MSFT)")
- AI Maturity Score (large number, e.g., "85/100")
- Progress bar showing maturity level
- Badge showing category: "Leader", "Fast Follower", "Emerging", or "Laggard"
- Quick stats:
  - 💰 Investment amount (e.g., "$50M invested")
  - 🚀 Number of AI products (e.g., "5 AI products")
  - 🔥 Open AI jobs (e.g., "23 open AI roles")
  - 📰 Recent news count (e.g., "3 news items")
- Click to view details

**Color Coding:**
- Leader: Green (#10b981)
- Fast Follower: Blue (#3b82f6)
- Emerging: Yellow (#f59e0b)
- Laggard: Red (#ef4444)

---

### 2. Company Detail Modal

**Opens when clicking a company card**

**Tabbed Interface:**
1. **Overview Tab:**
   - Large AI maturity gauge (circular progress indicator)
   - Score breakdown (4 categories: Investment, Product, Strategic, Organizational)
   - Total investment amount with breakdown
   - Filing date and analysis timestamp
   - Executive summary text
   - Export buttons (PDF, Add to Salesforce)

2. **Products Tab:**
   - List of AI products/features
   - Each product shows:
     - Product name
     - Description
     - Launch status (Available, Beta, Planned)
     - Target market (Enterprise, Consumer, Developer)

3. **Risks Tab:**
   - List of AI-related risks from 10-K
   - Each risk shows:
     - Category (Competitive, Implementation, Regulatory, Ethical)
     - Risk description
     - Severity indicator (High, Medium, Low)

4. **Live Signals Tab:**
   - **Hiring Signals Section:**
     - Count of open AI roles with urgency indicator (HIGH/NORMAL/LOW)
     - List of top job postings:
       - Job title
       - Location and remote status
       - Tech stack mentioned
       - Posted date
   - **Recent News Section:**
     - List of news items from last 30 days:
       - Headline
       - Source and date
       - Category badge (Product Launch, Investment, Partnership, etc.)
       - Link to article

5. **SDR Playbook Tab:**
   - Talking points (bulleted list)
   - Discovery questions (numbered list)
   - Value propositions (formatted nicely)
   - Objection handlers (key-value pairs)
   - Executive summary

---

### 3. Pipeline Progress Modal

**Shows when "Start Pipeline" is clicked**

**Features:**
- Title: "Processing X Companies..."
- Overall progress bar (percentage complete)
- List of companies with status icons:
  - ✅ Complete (green checkmark)
  - 🔄 In Progress (spinner, shows current stage like "Analyzing..." or "Enriching...")
  - ⏳ Pending (gray)
  - ❌ Failed (red X with error message)
- Estimated time remaining
- Auto-closes on completion with success notification

**Real-time Updates:**
- Connect via WebSocket (or polling fallback)
- Update progress as companies complete
- Show which stage each company is in

---

### 4. Comparison View Page

**Side-by-side company comparison**

**Table Columns:**
- Rank (with medals for top 3)
- Company name
- AI Maturity Score (with progress bar)
- Total Investment
- Number of Products
- Open AI Jobs
- Hiring Urgency indicator

**Features:**
- Sortable columns (click header to sort)
- Color-coded rows by maturity level
- Export to CSV button
- Filter by maturity category

---

### 5. Company Selection Interface

**Before starting pipeline:**
- Checkbox grid of 10 pre-selected companies:
  - Microsoft (MSFT)
  - Apple (AAPL)
  - NVIDIA (NVDA)
  - Alphabet (GOOGL)
  - Amazon (AMZN)
  - Meta (META)
  - Tesla (TSLA)
  - Salesforce (CRM)
  - Adobe (ADBE)
  - Netflix (NFLX)
- "Select All" / "Deselect All" buttons
- "Start Pipeline" button (disabled if none selected)

---

## Design Guidelines

### Visual Style
- **Modern and clean** - Inspired by Notion, Linear, or Vercel dashboards
- **Spacious** - Generous whitespace, not cramped
- **Card-based** - Use card components for sections
- **Subtle shadows** - Soft shadows on cards, deeper on hover
- **Rounded corners** - 8px border radius on cards

### Typography
- **Headings:** Inter or DM Sans font family
- **Body:** System font stack for performance
- **Size scale:** Use Tailwind's default scale (text-sm, text-base, text-lg, etc.)

### Color Palette
- **Background:** Neutral gray (#f9fafb or #f3f4f6)
- **Cards:** White (#ffffff) with border
- **Primary:** Blue (#3b82f6) for buttons and links
- **Maturity colors:** As defined above
- **Text:** Dark gray (#111827 for headings, #6b7280 for body)

### Spacing
- **Cards:** p-6 padding
- **Grid gap:** gap-6 on desktop, gap-4 on mobile
- **Section spacing:** mb-8 between major sections

---

## Components to Create

**Use shadcn/ui for these:**
1. `Button` - Primary, secondary, and ghost variants
2. `Card` - CardHeader, CardTitle, CardContent
3. `Dialog` - For company detail modal
4. `Tabs` - For tabbed interface in detail modal
5. `Progress` - Progress bars for maturity scores
6. `Badge` - For categories and status indicators
7. `Table` - For comparison view
8. `Checkbox` - For company selection

**Custom Components:**
1. `CompanyCard` - Company summary card
2. `MaturityGauge` - Circular progress indicator for AI maturity
3. `ProgressTracker` - Pipeline progress modal
4. `CompanySelector` - Multi-select company picker
5. `ComparisonTable` - Enhanced table with sorting

---

## Responsive Design

**Breakpoints:**
- Mobile: < 640px (1 column, stacked layout)
- Tablet: 640px - 1024px (2 columns)
- Desktop: > 1024px (3 columns)

**Mobile Considerations:**
- Company detail opens as full-screen modal (not dialog)
- Bottom sheet for quick actions
- Simplified cards (fewer stats)
- Touch-friendly tap targets (min 44x44px)

---

## Mock Data

**Include realistic mock data for:**
- 3 companies (Microsoft, Apple, NVIDIA) with complete profiles
- Sample AI investments ($50M, $35M, $75M)
- Sample products (Copilot, Vision Pro, AI chips)
- Sample job postings (5 per company)
- Sample news items (3 per company)

**Data structure example:**
```typescript
interface CompanyProfile {
  company: {
    name: string;
    ticker: string;
    domain: string;
  };
  ai_maturity: {
    total_score: number; // 0-100
    breakdown: {
      investment: number; // 0-25
      product: number; // 0-25
      strategic_importance: number; // 0-25
      organizational_readiness: number; // 0-25
    };
    label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
  };
  ai_insights: {
    investments: Array<{
      amount: string; // "$50M"
      amount_numeric: number;
      purpose: string;
      timeframe: string;
    }>;
    products: Array<{
      product_name: string;
      description: string;
      launch_status: "available" | "beta" | "planned";
    }>;
    // ... more fields
  };
  enrichment: {
    hiring: {
      ai_jobs: number;
      hiring_urgency: "HIGH" | "NORMAL" | "LOW";
      ai_job_details: Array<{
        title: string;
        location: string;
        tech_stack: string[];
        remote: boolean;
      }>;
    };
    recent_news: Array<{
      headline: string;
      source: string;
      date: string;
      category: string;
    }>;
  };
}
```

---

## API Integration (For Later)

**Initially:** Use mock data in components
**Later:** Replace with API calls using TanStack Query

**API Base URL:** `http://localhost:8000/api/v1`

**Key Endpoints:**
- `POST /pipeline/start` - Start pipeline
- `GET /pipeline/status/{job_id}` - Get progress
- `GET /companies/{ticker}` - Get company profile
- `GET /comparison?tickers=MSFT,AAPL,NVDA` - Compare companies
- `POST /export/salesforce` - Generate CSV

**WebSocket:** `ws://localhost:8000/ws/pipeline/{job_id}` for real-time updates

---

## Accessibility

- Semantic HTML (button, nav, main, etc.)
- ARIA labels for icons and interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Screen reader friendly
- Color contrast meets WCAG AA standards

---

## Performance

- Code splitting by route (React.lazy)
- Memoize expensive components (React.memo)
- Virtualize long lists if needed (react-virtual)
- Optimize images (use WebP, lazy loading)

---

## File Structure

```
src/
├── pages/
│   ├── Dashboard.tsx
│   ├── Comparison.tsx
│   └── NotFound.tsx
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── CompanyCard.tsx
│   ├── MaturityGauge.tsx
│   ├── CompanyDetail.tsx
│   ├── ProgressTracker.tsx
│   ├── CompanySelector.tsx
│   └── ComparisonTable.tsx
├── hooks/
│   └── useCompanies.ts  # Mock data hook (replace with API later)
├── lib/
│   └── utils.ts         # cn() utility
├── types/
│   └── index.ts         # TypeScript types
└── App.tsx
```

---

## Additional Notes

- **Focus on UI/UX polish** - This is a demo dashboard, make it beautiful
- **Smooth animations** - Use Tailwind's transition classes
- **Loading states** - Skeletons for loading content
- **Empty states** - Friendly messages when no data
- **Error handling** - Graceful error messages
- **Dark mode** - Optional but nice to have

---

## Success Criteria

- ✅ Dashboard loads with 3 mock companies
- ✅ Company cards display correctly
- ✅ Clicking card opens detailed modal
- ✅ All tabs in detail modal work
- ✅ Progress tracker shows mock progress
- ✅ Comparison view displays table
- ✅ Company selection works
- ✅ Responsive on mobile and desktop
- ✅ No TypeScript errors
- ✅ Accessible (keyboard navigation works)

---

## What Lovable Should Generate

1. Full React + Vite + TypeScript project
2. TailwindCSS configured
3. shadcn/ui components installed
4. All pages and components as described
5. Mock data for 3 companies
6. Routing setup (React Router)
7. Responsive layout
8. Beautiful, modern design

---

**Copy this entire prompt into Lovable.dev and it should generate a complete frontend starter!**
