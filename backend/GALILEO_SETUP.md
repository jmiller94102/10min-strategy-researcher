# Galileo Observability Setup Guide

## Overview

Galileo observability has been integrated into the 10-K Pipeline to track and monitor LLM calls for:
- **Azure OpenAI** (LLM-powered insight extraction from 10-K filings)
- **Browser-Use** (Anthropic-powered job scraping)

## What Gets Tracked

### 1. LLM Insight Extraction (`llm_extractor.py`)
- **Input**: 10-K text chunks for AI analysis
- **Output**: Extracted investments, products, and risks
- **Metrics**: Token usage, latency, model performance
- **Traces**: Named by company (e.g., "Extract AI Insights - Microsoft")

### 2. Job Scraping (`job_scraper.py`)
- **Input**: Career page scraping tasks
- **Output**: Extracted job postings and tech stacks
- **Metrics**: Estimated token usage, execution time
- **Traces**: Named by company (e.g., "Scrape Jobs - Microsoft")

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs `galileo>=0.1.0` along with other dependencies.

### 2. Get Your Galileo API Key

1. Visit: https://app.galileo.ai/onboarding/start-logging
2. Sign up or log in
3. Copy your API key

### 3. Configure Environment Variables

Add to your `.env` file:

```bash
# Galileo Observability (Optional)
GALILEO_API_KEY=your-galileo-api-key-here
GALILEO_PROJECT=10K-Pipeline
GALILEO_LOG_STREAM=production
GALILEO_CONSOLE_URL=https://app.galileo.ai
```

**Note**: Galileo is **optional**. If `GALILEO_API_KEY` is not set, the system will run normally without observability tracking.

### 4. Run Your Application

```bash
python main.py
```

Galileo will automatically:
- Initialize on first LLM call
- Create the project and log stream if they don't exist
- Track all LLM interactions
- Flush logs after each operation

### 5. View Your Logs

After running your pipeline, check the console output for Galileo URLs:

```
🚀 GALILEO LOG INFORMATION:
🔗 Project   : https://app.galileo.ai/project/{project_id}
📝 Log Stream: https://app.galileo.ai/project/{project_id}/log-streams/{log_stream_id}
```

Click these links to view:
- **Token usage** and costs
- **Latency** metrics
- **Input/output** traces
- **Error tracking**
- **Model comparisons**

## Configuration Options

### Project and Log Stream Names

You can customize these in your `.env`:

```bash
GALILEO_PROJECT=MyCustomProject
GALILEO_LOG_STREAM=development  # or staging, production, etc.
```

### Disable Galileo

Simply remove or comment out `GALILEO_API_KEY`:

```bash
# GALILEO_API_KEY=your-key-here
```

The system will detect this and skip all Galileo tracking.

## What You'll See in Galileo

### Traces
Each LLM operation creates a trace with:
- **Name**: Operation type and company name
- **Input**: Task description or prompt
- **Output**: LLM response or summary
- **Duration**: Execution time in nanoseconds
- **Tokens**: Input, output, and total token counts

### Sessions
Each scraping or extraction operation creates a session that groups related traces together.

### Metrics
- **Cost tracking**: Token usage × model pricing
- **Latency analysis**: Response times
- **Error rates**: Failed operations
- **Model performance**: Quality metrics

## Troubleshooting

### Galileo Not Logging

1. **Check API Key**: Ensure `GALILEO_API_KEY` is set correctly
2. **Check Logs**: Look for "Galileo observability enabled" in console
3. **Network Issues**: Verify internet connectivity to `app.galileo.ai`

### Import Errors

If you see `ModuleNotFoundError: No module named 'galileo'`:

```bash
pip install galileo
```

### Token Estimation for Browser-Use

Browser-Use doesn't expose token counts, so we estimate:
- **Formula**: `characters / 4` (rough approximation)
- **Purpose**: Tracking relative usage, not exact billing

## Benefits

✅ **Track LLM costs** across different operations  
✅ **Monitor performance** and latency  
✅ **Debug failures** with full trace history  
✅ **Compare models** (Azure OpenAI vs Browser-Use)  
✅ **Optimize prompts** based on output quality  
✅ **Audit usage** for compliance and reporting  

## Example Output

When Galileo is enabled, you'll see logs like:

```
INFO - Galileo observability enabled for LLM extraction
INFO - Galileo observability enabled for job scraping
INFO - Extracting AI insights for Microsoft from 25,000 chars
INFO - Extracted 3 investments, 5 products, 4 risks

🚀 GALILEO LOG INFORMATION:
🔗 Project   : https://app.galileo.ai/project/abc123
📝 Log Stream: https://app.galileo.ai/project/abc123/log-streams/xyz789
```

## Support

- **Galileo Docs**: https://docs.galileo.ai
- **Galileo Support**: support@galileo.ai
- **Project Issues**: Create an issue in this repository

---

**Note**: Galileo is completely optional. The pipeline works perfectly without it, but you'll miss out on valuable observability insights.
