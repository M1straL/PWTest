import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Playwright
import asyncio

URL = 'https://demo.playwright.dev/todomvc/#/'
SCRIPT_PATH = "./preload.js"
HEADLESS = False
SLOWMO_SEC = 1000

@pytest_asyncio.fixture
async def open_page(request):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS, slow_mo=SLOWMO_SEC)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.context.clear_cookies()
            if request:
                await page.add_init_script(SCRIPT_PATH)
            await page.goto(URL)
            yield page.url, page
        finally:
            await page.close()
            await context.close()
            await browser.close()
