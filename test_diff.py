import pytest
from playwright.sync_api import sync_playwright
import utils

expected_file_path = '/Users/mistral/diff_files/expected.html'


@pytest.mark.parametrize('open_todomvc', [False], indirect=True)
def test_playwright_diff(open_page):
    url, page_with_url = open_page
    current_html = page_with_url.content()
    expected_html = utils.read_html_from_file(expected_file_path)

    assert utils.compare_two_html(current_html, expected_html) is True
