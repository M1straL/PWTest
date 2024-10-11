import json

import TodoPage
import pytest
from playwright.async_api import expect

from mechanics_helper import remove_todo, add_todo, get_todo_by_inner_text

input_text_first = 'Blablabla'
input_text_second = '11111111'

pytestmark = pytest.mark.asyncio
test_data_input_path = 'data_for_input_test.json'
USED_FIXTURE = 'open_page'


@pytest.mark.parametrize(USED_FIXTURE, False, indirect=True)
@pytest.mark.asyncio
async def test_input_area(open_page):
    url, page = open_page

    with open(test_data_input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    text_input = await TodoPage.LocatorsHelper.get_new_todo_text_placeholder(page)

    for text in data:
        await text_input.fill(text['entered'])
        await text_input.press(TodoPage.LocatorsHelper.ENTER_BTN)

        todo_item = await page.get_by_test_id(TodoPage.LocatorsHelper.NEW_TODO_ITEM_TEST_ID)
        if not text['created']:
            await expect(todo_item).to_have_count(0)
            return

        label = await page.get_by_test_id(TodoPage.LocatorsHelper.NEW_TODO_TITLE_TEST_ID)
        expected = text['expected']
        await expect(label).to_have_text(expected)

        await todo_item.hover()
        await remove_todo(page, expected)


@pytest.mark.parametrize(USED_FIXTURE, True, indirect=True)
@pytest.mark.asyncio
async def test_completion_checkbox(open_page):
    url, page = open_page

    text_input = await TodoPage.LocatorsHelper.get_new_todo_text_placeholder(page)
    await text_input.fill(input_text_first)
    await text_input.press(TodoPage.LocatorsHelper.ENTER_BTN)

    single_item = await get_todo_by_inner_text(page, input_text_first)

    checkbox = await single_item.locator('input[type=checkbox]')
    await checkbox.check()

    await expect(single_item).to_have_class("completed")

    await checkbox.uncheck()

    await expect(single_item).not_to_have_class("completed")


@pytest.mark.parametrize(USED_FIXTURE, [True], indirect=True)
async def test_todo_active_count(open_page, todo_name='New_active1', active_before='2', active_after='3'):
    url, page = await open_page
    todo_count = page.get_by_test_id(TodoPage.LocatorsHelper.TODO_COUNT)
    await expect(todo_count).to_have_class(TodoPage.LocatorsHelper.TODO_COUNT)
    await expect(todo_count.locator(TodoPage.LocatorsHelper.STRONG)).to_have_text(active_before, use_inner_text=True)
    await expect(todo_count).to_have_text(f"{active_before} items left", use_inner_text=True)

    await add_todo(page, todo_name)
    await expect(todo_count.locator(TodoPage.LocatorsHelper.STRONG)).to_have_text(active_after, use_inner_text=True)

    await remove_todo(page, todo_name)
    await expect(todo_count.locator(TodoPage.LocatorsHelper.STRONG)).to_have_text(active_before, use_inner_text=True)


@pytest.mark.parametrize(USED_FIXTURE, False, indirect=True)
async def test_editing_todo_name(open_page, default_name='Default', edited_name='Edited'):
    url, page = open_page

    await add_todo(page, default_name)

    todo_item = await get_todo_by_inner_text(page, default_name)
    await todo_item.dblclick()

    edit_input = await todo_item.get_by_role('input', name=default_name)
    await expect(edit_input).to_have_class("edit")
    await expect(edit_input).to_have_attribute("aria-label", "Edit")
    await expect(edit_input).not_to_be_enabled()

    await expect(todo_item).to_have_class("Editing")
    await expect(edit_input).to_have_value(default_name)
    await expect(edit_input).to_be_enabled()

    await edit_input.fill(edited_name)
    await expect(edit_input).to_have_value(edited_name)

    await todo_item.press(TodoPage.LocatorsHelper.ESCAPE_BTN)
    await expect(edit_input).not_to_have_class("edit")
    await expect(edit_input).not_to_be_enabled()
    await expect(todo_item.get_by_role("label")).to_have_value(default_name)

    await todo_item.dblclick()
    await edit_input.fill(default_name)
    await todo_item.press(TodoPage.LocatorsHelper.ENTER_BTN)
    await expect(todo_item.get_by_role("label")).to_have_text(edited_name)
