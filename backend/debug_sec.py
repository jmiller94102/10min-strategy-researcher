"""Debug SEC EDGAR page structure"""
import asyncio
from playwright.async_api import async_playwright


async def debug_sec_page():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # Non-headless to see
    context = await browser.new_context(
        user_agent="10K-Pipeline-Hackathon research@hackathon.dev"
    )
    page = await context.new_page()

    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K&dateb=&owner=exclude&count=40"

    print(f"Navigating to: {url}")
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(3)

    # Save screenshot
    await page.screenshot(path="sec_debug.png")
    print("Screenshot saved: sec_debug.png")

    # Get HTML content
    content = await page.content()

    # Save HTML
    with open("sec_debug.html", "w") as f:
        f.write(content)
    print("HTML saved: sec_debug.html")

    # Check for table classes
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    print("\nAll tables found:")
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        print(f"  Table {i}: class={table.get('class')}, id={table.get('id')}")

    print("\nAll divs with 'result' in class:")
    divs = soup.find_all('div', class_=lambda x: x and 'result' in x)
    for div in divs:
        print(f"  Div: class={div.get('class')}")

    await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_sec_page())
