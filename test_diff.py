import pytest
from playwright.sync_api import sync_playwright
import comare_html

expected_file_path = '/Users/mistral/diff_files/expected.html'

def test_playwright_diff(page_with_url):
    url, page_with_url = page_with_url
    current_html = page_with_url.content()
    expected_html = comare_html.read_html_from_file(expected_file_path)

    assert comare_html.compare_two_html(current_html, expected_html) is True


