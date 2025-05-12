import os
import re
import time
import atexit
import requests
import asyncio
import concurrent.futures
from urllib.parse import urlparse
from readability import Document
from lxml import html as lxml_html
from playwright.async_api import async_playwright, Browser
from cneura_ai.logger import logger

class Research:
    def __init__(self, google_api_key, search_engine_id, max_workers=4):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.playwright = None
        self.browser: Browser = None
        self.max_workers = max_workers

    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def google_search(self, query, num_results=5):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.search_engine_id}&num={num_results}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return [(item["title"], item["link"]) for item in data.get("items", [])]
        except requests.RequestException as e:
            logger.error(f"Google Search API error: {e}")
            return []

    def duckduckgo_search(self, query, num_results=5):
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results)
                return [(r["title"], r["href"]) for r in results]
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    async def scrape_page(self, url, retries=2):
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"[Playwright] Attempt {attempt} scraping {url}")
                page = await self.browser.new_page()
                await page.goto(url, timeout=60000)
                await page.wait_for_selector("body", timeout=10000)
                await asyncio.sleep(1.5)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2);")
                await asyncio.sleep(1)
                html = await page.content()
                await page.close()
                if re.search(r"captcha|verify you are human|cloudflare", html, re.IGNORECASE):
                    logger.warning("CAPTCHA or challenge detected.")
                    continue
                return html
            except Exception as e:
                logger.warning(f"[Playwright] Failed attempt {attempt} on {url}: {e}")
                await asyncio.sleep(1)

        try:
            logger.info(f"[Fallback] Trying requests for {url}")
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                return resp.text
            else:
                logger.warning(f"[Fallback] Non-200 status: {resp.status_code}")
        except Exception as e:
            logger.warning(f"[Fallback] Request failed: {e}")

        logger.error(f"[Error] Final failure scraping {url}")
        return None

    def extract_main_content(self, html: str) -> str:
        try:
            doc = Document(html)
            summary_html = doc.summary()
            tree = lxml_html.fromstring(summary_html)
            text = tree.text_content()
            return re.sub(r'\s+', ' ', text).strip()
        except Exception as e:
            logger.error(f"Readability extraction failed: {e}")
            return ""

    async def process_results(self, query, engine="google", num_results=5):
        logger.info(f"Searching: '{query}' with {engine}")
        if engine == "google":
            results = self.google_search(query, num_results)
        elif engine == "duckduckgo":
            results = self.duckduckgo_search(query, num_results)
        else:
            raise ValueError("Invalid engine. Use 'google' or 'duckduckgo'.")

        if not results:
            logger.warning("No results found.")
            return {"query": query, "results": []}

        output = []

        async def process(title_link):
            title, link = title_link
            domain = urlparse(link).netloc
            logger.info(f"[Process] Scraping {domain}")
            html = await self.scrape_page(link)
            if not html:
                return None
            text = self.extract_main_content(html)
            if len(re.findall(r'\w+', text)) < 30:
                logger.info(f"Skipping short content from {link}")
                return None
            return {
                "title": title,
                "url": link,
                "content": text,
                "token_count": len(re.findall(r'\w+', text))
            }

        tasks = [process(item) for item in results]
        completed = await asyncio.gather(*tasks)
        output.extend([res for res in completed if res])

        return {"query": query, "results": output}
