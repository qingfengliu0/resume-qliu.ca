from playwright.sync_api import sync_playwright 

def test_api():
    print("Starting Playwright test...")
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("Navigating to webpage...")
        page.goto("https://resumetest.qliu.ca")
        assert "Qingfeng Liu" in page.title()
        print("Webpage loaded successfully.")

        # Wait for element to be attached in DOM and visible
        try:
            page.wait_for_selector("#visitor-number", timeout=5000)
        except:
            print("Error: #visitor-number not found or timed out")
            browser.close()
            return
        
        page.wait_for_function(
            "element => parseInt(document.getElementById('visitor-number').textContent) !== 0",
            timeout=10000
        )
        raw_oldvalue = page.locator("#visitor-number").text_content()  # Initialize raw_oldvalue
        print(f"Raw old visitor number content: {raw_oldvalue}")
        
        oldvalue = int(raw_oldvalue)
        page.reload()
        print("Page reloaded.")
        # Wait for the visitor number to change
        page.wait_for_function(
            "element => document.getElementById('visitor-number').textContent !== element",
            arg=raw_oldvalue,  # Use the initialized raw_oldvalue
            timeout=10000
        )
        raw_newvault = page.locator("#visitor-number").text_content()
        print(f"Raw new visitor number content: {raw_newvault}")
        newvault = int(raw_newvault)

        if newvault == oldvalue + 1:
            print("✅ Visitor number is incremented")
        else:
            print("❌ Visitor number is not incremented")

        browser.close()
        print("Browser closed.")
