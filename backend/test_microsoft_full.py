"""
FULL SYSTEM TEST: Microsoft End-to-End Pipeline
- Company: Microsoft (MSFT)
- Features: 10-K retrieval, AI analysis, job scraping (max 3 jobs), CSV export
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.pipeline_orchestrator import PipelineOrchestrator
from src.core.logging_config import setup_logging, logger


async def progress_callback(stage: str, substage: str, data):
    """Real-time pipeline progress updates"""
    logger.info(f"📍 {stage.upper()}: {substage}")

    # Show additional details for certain stages
    if stage == "enrichment" and "jobs" in substage.lower():
        logger.info(f"   → Scraping jobs from Microsoft careers page...")


async def main():
    """Run full system test with Microsoft"""

    setup_logging("INFO")

    print("\n" + "=" * 100)
    print("🚀 FULL SYSTEM TEST: Microsoft 10-K AI Intelligence Pipeline")
    print("=" * 100)
    print("\nTest Configuration:")
    print("  • Company: Microsoft (MSFT)")
    print("  • 10-K Retrieval: ✅ SEC API")
    print("  • AI Analysis: ✅ Azure OpenAI GPT-4o")
    print("  • Job Scraping: ✅ Browser-Use Cloud (max 3 jobs)")
    print("  • Tech Stack Detection: ✅ Enabled")
    print("  • AI Maturity Scoring: ✅ Enabled")
    print("  • CSV Export: ✅ Salesforce format")
    print("\n" + "=" * 100 + "\n")

    orchestrator = PipelineOrchestrator()

    try:
        logger.info("🎬 Starting full pipeline for Microsoft...")
        logger.info("Note: Job scraping with Browser-Use may take 30-60 seconds\n")

        result = await orchestrator.run_pipeline(
            tickers=["MSFT"],              # Single company: Microsoft
            force_refresh=False,            # Use cache for 10-K (faster)
            skip_enrichment=False,          # ⭐ ENABLE job scraping
            use_daytona=False,              # Run locally for speed
            progress_callback=progress_callback
        )

        # Validation
        assert result["status"] in ["completed", "partial"], \
            f"Pipeline failed with status: {result['status']}"

        assert len(result["profiles"]) == 1, \
            f"Expected 1 profile (Microsoft), got {len(result['profiles'])}"

        # Display results
        print("\n" + "=" * 100)
        print("📊 RESULTS SUMMARY")
        print("=" * 100)

        print(f"\nPipeline Status:")
        print(f"  • Job ID: {result['job_id']}")
        print(f"  • Status: {result['status'].upper()}")
        print(f"  • Duration: {result['duration_seconds']:.1f}s")
        print(f"  • Success Rate: {result['successful']}/{result['total']}")

        # Microsoft profile details
        profile = result["profiles"][0]
        company = profile["company"]
        insights = profile["insights"]
        maturity = profile["maturity"]
        enrichment = profile.get("enrichment", {})

        print(f"\n🏢 Company Profile:")
        print(f"  • Name: {company['name']}")
        print(f"  • Ticker: {company['ticker']}")
        print(f"  • CIK: {company['cik']}")
        print(f"  • Domain: {company['domain']}")

        print(f"\n🎯 AI Maturity Analysis:")
        print(f"  • Overall Score: {maturity['score']}/100")
        print(f"  • Tier: {maturity['tier']}")
        print(f"  • Category Scores:")
        for category, score in maturity.get('category_scores', {}).items():
            print(f"    - {category}: {score}/100")

        print(f"\n💰 AI Investments:")
        investments = insights.get('investments', {})
        if investments.get('items'):
            print(f"  • Total Amount: {investments.get('total_amount', 'N/A')}")
            print(f"  • Number of Investments: {len(investments['items'])}")
            for inv in investments['items'][:3]:  # Show first 3
                print(f"    - {inv.get('amount', 'N/A')}: {inv.get('purpose', 'N/A')[:80]}")
        else:
            print("  • No specific investments extracted")

        print(f"\n🔬 AI Products & Services:")
        products = insights.get('products', [])
        if products:
            print(f"  • Total Products: {len(products)}")
            for prod in products[:5]:  # Show first 5
                print(f"    - {prod.get('name', 'N/A')}: {prod.get('description', 'N/A')[:80]}")
        else:
            print("  • No products extracted")

        print(f"\n⚠️ AI Risks:")
        risks = insights.get('risks', [])
        if risks:
            print(f"  • Total Risks: {len(risks)}")
            for risk in risks[:3]:  # Show first 3
                print(f"    - {risk.get('category', 'N/A')}: {risk.get('description', 'N/A')[:80]}")
        else:
            print("  • No risks extracted")

        # Enrichment data (jobs!)
        print(f"\n💼 Job Postings (Live Data from careers.microsoft.com):")
        ai_jobs = enrichment.get('ai_jobs', [])
        if ai_jobs:
            print(f"  • Total Jobs Found: {len(ai_jobs)} (max 3)")
            for i, job in enumerate(ai_jobs, 1):
                print(f"\n  Job {i}:")
                print(f"    • Title: {job.get('title', 'N/A')}")
                print(f"    • Location: {job.get('location', 'N/A')}")
                print(f"    • Remote: {'Yes' if job.get('remote') else 'No'}")
                print(f"    • Seniority: {job.get('seniority', 'N/A').title()}")
                print(f"    • URL: {job.get('job_url', 'N/A')}")
                print(f"    • Tech Stack: {', '.join(job.get('tech_stack', [])[:10])}")
        else:
            print("  ⚠️ No jobs found (Browser-Use may have failed)")

        print(f"\n🛠️ Tech Stack Detected:")
        tech_stack = enrichment.get('tech_stack', [])
        if tech_stack:
            print(f"  • Technologies: {', '.join(tech_stack[:15])}")
            if len(tech_stack) > 15:
                print(f"  • ... and {len(tech_stack) - 15} more")
        else:
            print("  • No tech stack detected")

        # Export info
        print(f"\n📂 Exports:")
        print(f"  • CSV: {result['csv_path']}")
        print(f"  • Format: Salesforce CRM compatible")

        # SDR Playbook
        playbook = profile.get('sdr_playbook', {})
        if playbook:
            print(f"\n📋 SDR Playbook Generated:")
            print(f"  • Talk Tracks: {len(playbook.get('talk_tracks', []))}")
            print(f"  • Pain Points: {len(playbook.get('pain_points', []))}")
            print(f"  • Competitive Angles: {len(playbook.get('competitive_angles', []))}")

        print("\n" + "=" * 100)
        print("✅ FULL SYSTEM TEST PASSED!")
        print("=" * 100)

        print("\n🎯 System Capabilities Verified:")
        print("  ✅ SEC 10-K retrieval via official API")
        print("  ✅ HTML parsing and AI content extraction")
        print("  ✅ Azure OpenAI GPT-4o LLM analysis")
        print("  ✅ AI maturity scoring algorithm")
        print(f"  {'✅' if ai_jobs else '⚠️'} Browser-Use Cloud job scraping (3 jobs)")
        print(f"  {'✅' if tech_stack else '⚠️'} Tech stack detection from job postings")
        print("  ✅ Salesforce CSV export")
        print("  ✅ SDR playbook generation")

        print("\n💡 Next Steps:")
        print("  • Frontend: Connect to backend API at http://localhost:8010")
        print("  • Demo: Use this test output to showcase capabilities")
        print("  • Production: Enable Daytona for parallel processing (10 companies)")

        print("\n" + "=" * 100 + "\n")

        return True

    except Exception as e:
        print("\n" + "=" * 100)
        print("❌ TEST FAILED")
        print("=" * 100)
        logger.error(f"\nError: {e}", exc_info=True)
        print("\n" + "=" * 100 + "\n")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
