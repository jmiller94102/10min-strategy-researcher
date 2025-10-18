"""Test Galileo observability integration"""
import asyncio
from src.services.analysis.llm_extractor import AIInsightExtractor
from src.core.logging_config import logger

async def test_galileo_integration():
    """Test that Galileo is tracking LLM calls"""
    
    logger.info("=" * 60)
    logger.info("Testing Galileo Observability Integration")
    logger.info("=" * 60)
    
    # Initialize the LLM extractor (should initialize Galileo)
    extractor = AIInsightExtractor()
    
    if not extractor.galileo_enabled:
        logger.error("❌ Galileo is NOT enabled!")
        logger.error("Check that GALILEO_API_KEY is set in your .env file")
        return False
    
    logger.info("✅ Galileo is enabled and initialized")
    
    # Test with a small sample text
    sample_text = """
    Microsoft Corporation announced a $10 billion investment in artificial intelligence 
    infrastructure and research. The company is developing Azure AI services including 
    GPT-4 integration and custom AI models. Key risks include competition from Google 
    and Amazon in the cloud AI market.
    """
    
    logger.info("\n📊 Running test extraction with Galileo tracking...")
    
    try:
        result = await extractor.extract_insights(sample_text, "Microsoft (Test)")
        
        logger.info("\n✅ Extraction completed successfully!")
        logger.info(f"   - Investments: {len(result.get('investments', {}).get('details', []))}")
        logger.info(f"   - Products: {len(result.get('products', []))}")
        logger.info(f"   - Risks: {len(result.get('risks', []))}")
        
        # Print Galileo information
        from src.core.config import settings
        project_url = f"{settings.galileo_console_url}/project/{extractor.galileo_logger.project_id}"
        log_stream_url = f"{project_url}/log-streams/{extractor.galileo_logger.log_stream_id}"
        
        logger.info("\n" + "=" * 60)
        logger.info("🚀 GALILEO OBSERVABILITY ACTIVE")
        logger.info("=" * 60)
        logger.info(f"🔗 Project   : {project_url}")
        logger.info(f"📝 Log Stream: {log_stream_url}")
        logger.info("=" * 60)
        logger.info("\n✅ Visit the URLs above to see your LLM traces in Galileo!")
        logger.info("   You should see:")
        logger.info("   - Token usage and costs")
        logger.info("   - Input/output traces")
        logger.info("   - Latency metrics")
        logger.info("   - Model performance data")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_galileo_integration())
    exit(0 if success else 1)
