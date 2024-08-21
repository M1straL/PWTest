import re

from playwright.sync_api import expect
import json

input_text_first = 'Blablabla'
input_text_second = '11111111'

def test_input_area(open_page_wout_cookies):
    url, page = open_page_wout_cookies

    with open('data_for_input_test.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    new_todo_input = page.get_by_placeholder('What needs to be done?')

    for text in data:
        new_todo_input.fill(text['entered'])
        new_todo_input.press('Enter')

        todo_item = page.get_by_test_id('todo-item')
        if not text['created']:
            expect(todo_item).to_have_count(0)
            return

        label = page.get_by_test_id('todo-title')

        expect(label).to_have_text(text['expected'])

        todo_item.hover()
        delete_button = todo_item.locator('.destroy')
        delete_button.click()


def add_todo(page, name):
    new_todo_input = page.get_by_placeholder('What needs to be done?')
    new_todo_input.fill(name)

    new_todo_input.press('Enter')

    assert get_todo_by_inner_text(page, name).count() == 1
    #TODO здесь бы желатель await, чтобы быть увренным, что он создался

def test_completion_checkbox(open_page_wout_cookies):
    url, page = open_page_wout_cookies

    add_todo(page, "complete")

    checkbox = page.get_by_label('Toggle Todo')
    single_item = page.get_by_test_id('todo-item')

    expect(checkbox).not_to_be_checked()
    expect(single_item).not_to_have_class('completed')

    checkbox.click()

    expect(single_item).not_to_have_css("color", "#4d4d4d")
    # TODO дописать проверку,что шрифт зачеркивается и background image соответсвует.Сейчас не раболтает
    expect(single_item).to_have_css("background-image",
                                    "#data:image/svg+xml;utf8,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2240%22%20height%3D%2240%22%20viewBox%3D%22-10%20-18%20100%20135%22%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2250%22%20r%3D%2250%22%20fill%3D%22none%22%20stroke%3D%22%23bddad5%22%20stroke-width%3D%223%22/%3E%3Cpath%20fill%3D%22%235dc2af%22%20d%3D%22M72%2025L42%2071%2027%2056l-4%204%2020%2020%2034-52z%22/%3E%3C/svg%3E")

    expect(checkbox).to_be_checked()
    expect(single_item).to_have_class('completed')

    checkbox.click()
    expect(checkbox).not_to_be_checked()
    expect(single_item).not_to_have_class('completed')


def test_complete_all_button(open_page_with_cookies):
    url, page = open_page_with_cookies

    toggle_all_checkbox = page.locator('#toggle-all')
    toggle_all_checkbox.click()

    for li in page.get_by_test_id('todo-item').all():
        expect(li).to_have_class('completed')
        expect(li.get_by_role("checkbox")).to_be_checked()


def test_footer(open_page_with_cookies):
    url, page = open_page_with_cookies

    filters = page.locator('.filters')

    check_tab(filters, page, 'Active', True, 2)
    check_tab(filters, page, 'All', False, 4)
    check_tab(filters, page, 'Completed', True, 2)

def check_tab(filters, page, tab_name,isUrl, count):
    active = filters.get_by_role('link').filter(has_text=tab_name)
    active.click()
    expect(active).to_have_class("selected")
    expect(page.get_by_test_id('todo-item')).to_have_count(count)
    url = "https://demo.playwright.dev/todomvc/#/"
    if isUrl:
        url = f'https://demo.playwright.dev/todomvc/#/{tab_name.lower()}'
    expect(page).to_have_url(url)

def test_todo_active_count(open_page_with_cookies, todo_name='New_active1', active_before='2',active_after='3'):
    url, page = open_page_with_cookies
    todo_count = page.get_by_test_id('todo-count')
    expect(todo_count).to_have_class('todo-count')
    expect(todo_count.locator('strong')).to_have_text(active_before, use_inner_text=True)
    expect(todo_count).to_have_text(f"{active_before} items left", use_inner_text=True)

    add_todo(page, todo_name)
    expect(todo_count.locator('strong')).to_have_text(active_after, use_inner_text=True)

    remove_todo(page, todo_name)
    expect(todo_count.locator('strong')).to_have_text(active_before, use_inner_text=True)

def test_editing_todo_name(open_page_wout_cookies, default_name="Default", edited_name="Edited"):
    url, page = open_page_wout_cookies

    add_todo(page, default_name)

    todo_item = get_todo_by_inner_text(page, default_name)
    todo_item.dblclick()

    edit_input = todo_item.get_by_role('input', name=default_name)
    expect(edit_input).to_have_class("edit")
    expect(edit_input).to_have_attribute("aria-label", "Edit")
    expect(edit_input).not_to_be_enabled()

    expect(todo_item).to_have_class("Editing")
    expect(edit_input).to_have_value(default_name)
    expect(edit_input).to_be_enabled()

    edit_input.fill(edited_name)
    expect(edit_input).to_have_value(edited_name)

    todo_item.press('Escape')
    expect(edit_input).not_to_have_class("edit")
    expect(edit_input).not_to_be_enabled()
    expect(todo_item.get_by_role("label")).to_have_value(default_name)

    todo_item.dblclick()
    edit_input.fill(default_name)
    todo_item.press("Enter")
    expect(todo_item.get_by_role("label")).to_have_text(edited_name)
def get_todo_by_inner_text(page, name):
    return page.get_by_test_id('todo-item').filter(has=page.get_by_test_id('todo-title')).filter(has_text=name)

def remove_todo(page, name):
    todo_item = get_todo_by_inner_text(page, name)

    expect(todo_item).to_have_count(1)

    todo_item.hover()
    delete_button = todo_item.locator('.destroy')
    delete_button.click()

# test adding a single element
# TODO Rewrite using Playwright locators recommendations
''' def test_add_todo(open_page_wout_cookies):
    url, page = open_page_wout_cookies

    new_todo_input = page.locator('.new-todo')
    new_todo_input.fill(input_text_first)

    expect(new_todo_input).to_have_value(input_text_first)

    new_todo_input.press('Enter')

    main = page.locator('.main')

    expect(main).to_have_count(1)
    expect(main).to_be_visible()

    check_toggle_all_button(main)

    toggle_label = main.locator(' > label')
    expect(toggle_label).to_have_text("Mark all as complete")

    #check main inner
    check_main_inner(main)

    #check default state completion toggle checkbox
    check_default_state_completion_toggle_checkbox(main)

    #check single item attributes and text
    toggle_single_item_label = main.locator('ul div label')
    expect(toggle_single_item_label).to_have_count(1)
    expect(toggle_single_item_label).to_have_attribute('data-testid', 'todo-title')
    expect(toggle_single_item_label).to_have_text(input_text_first) '''


def check_default_state_completion_toggle_checkbox(main):
    toggle_single_checkbox = main.locator('ul div input')
    expect(toggle_single_checkbox).to_have_count(1)
    expect(toggle_single_checkbox).to_have_role("checkbox")
    expect(toggle_single_checkbox).to_have_class("toggle")
    expect(toggle_single_checkbox).not_to_be_checked()
    expect(toggle_single_checkbox).to_have_attribute("aria-label", "Toggle Todo")


def check_main_inner(main):
    todo_list = main.locator('ul')
    expect(todo_list).to_have_class("todo-list")
    expect(todo_list).to_have_role("list")
    todo_list_item = todo_list.locator('li')
    expect(todo_list_item).to_have_attribute("data-testid", "todo-item")
    list_item_div = main.locator('ul div')
    expect(list_item_div).to_have_count(1)
    expect(list_item_div).to_have_class('view')


def check_toggle_all_button(main):
    toggle_all_checkbox = main.locator('#toggle-all')
    expect(toggle_all_checkbox).to_have_role("checkbox")
    expect(toggle_all_checkbox).to_have_class("toggle-all")
    expect(toggle_all_checkbox).not_to_be_checked()
