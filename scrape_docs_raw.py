from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://apis.hyperbots.com/docs", wait_until="networkidle")
    page.wait_for_timeout(5000)
    
    # Try to find common documentation-related classes or IDs
    body_text = page.inner_text("body")
    with open("docs_text.txt", "w") as f:
        f.write(body_text)
    
    print(f"Body text length: {len(body_text)}")
    print(f"Body text snippet: {body_text[:1000]}")
    
    # Also check if there's any JSON in network logs
    # We could do that but let's first check if text is enough
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
