from playwright.sync_api import sync_playwright
import time
import json 

def nse_preopen(retries=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-http2'])
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="123", "Not;A=Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        })

        try:
            print("visiting NSE homepage...")
            page.goto("https://www.nseindia.com/", wait_until="domcontentloaded")
            time.sleep(10)

            print("visiting pre-open market page....")
            page.goto("https://www.nseindia.com/market-data/pre-open-market-cm-and-emerge-market", wait_until="domcontentloaded")
            time.sleep(10)
            time.sleep(10)

            print("Fetching pre-open market data....")
            response = page.request.get(
                "https://www.nseindia.com/api/market-data-pre-open?key=NIFTY",
                headers={
                    "Referer": "https://www.nseindia.com/market-data/pre-open-market-cm-and-emerge-market",
                    "Accept": "application/json, text/plain, */*",
                    "X-Requested-With": "XMLHttpRequest"
                },
                timeout=50000
            )

            if response.ok:
                data = response.json()
            else:
                print("API request failed with status {response.status}: {response.text()}")
                return None

            print(json.dumps(data, indent=2))
            return data
        
        except Exception as e:
            print(f"An error occured:{e}")

        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    for retry in range(3):
        print(f"Attempt {retry+1}/3")
        result = nse_preopen()
        if result:
            break
        else:
            print("Retrying in 10 seconds...")
            time.sleep(10)
