import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def open_page_wout_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.context.storage_state().clear()
        page.goto('https://demo.playwright.dev/todomvc/#/')
        page.wait_for_load_state("domcontentloaded")
        url = page.url
        yield url, page
        browser.close()


@pytest.fixture()
def open_page_with_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.context.storage_state().clear()
        page.add_init_script(path="./preload.js")
        page.goto('https://demo.playwright.dev/todomvc/#/')
        page.wait_for_load_state("domcontentloaded")
        url = page.url
        yield url, page
        browser.close()

