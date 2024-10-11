from playwright.async_api import expect

import TodoPage


async def get_todo_by_inner_text(page, name):
    return await page.get_by_test_id(TodoPage.LocatorsHelper.NEW_TODO_ITEM_TEST_ID).filter(has=page.get_by_test_id(
        TodoPage.LocatorsHelper.NEW_TODO_TITLE_TEST_ID)).filter(has_text=name)


def check_tab(filters, page, tab_name, isUrl, count):
    active = filters.get_by_role('link').filter(has_text=tab_name)
    active.click()
    expect(active).to_have_class(TodoPage.LocatorsHelper.SELECTED)
    expect(page.get_by_test_id(TodoPage.LocatorsHelper.NEW_TODO_ITEM_TEST_ID)).to_have_count(count)
    url = "https://demo.playwright.dev/todomvc/#/"
    if isUrl:
        url = f'https://demo.playwright.dev/todomvc/#/{tab_name.lower()}'
    expect(page).to_have_url(url)


def remove_todo(page, name):
    todo_item = get_todo_by_inner_text(page, name)

    todo_item.hover()
    delete_button = todo_item.locator(TodoPage.LocatorsHelper.DESTROY_BUTTON)
    delete_button.click()


async def add_todo(page, name):
    new_todo_input = TodoPage.LocatorsHelper.get_new_todo_text_placeholder(page)
    await new_todo_input.fill(name)
    await new_todo_input.press(TodoPage.LocatorsHelper.ENTER_BTN)
