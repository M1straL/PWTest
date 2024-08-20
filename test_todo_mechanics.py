import re

from playwright.sync_api import expect
import json

input_text_first = 'Blablabla'
input_text_second = '11111111'

'''def test_check_add_todo(page_with_url):
    url, page_with_url = page_with_url

    #check_the_toggle_checkbox default parameters
    toggle_all_checkbox = main.locator('#toggle-all')
    expect(toggle_all_checkbox).to_have_role("checkbox")
    expect(toggle_all_checkbox).to_have_class("toggle-all")
    expect(toggle_all_checkbox).not_to_be_checked()

    # check the label of all
    toggle_label = page_with_url.get_by_label("Mark all as complete")

    #check list with todos
    todo_list = main.locator('ul')
    expect(todo_list).to_have_class("todo-list")
    expect(todo_list).to_have_role("list")

    todo_list_item = todo_list.locator('li')
    expect(todo_list_item).to_have_attribute("data-testid", "todo-item")

    list_item_div = todo_list_item.locator('div')
    expect(list_item_div).to_have_count(1)
    expect(list_item_div).to_have_class('view')

    toggle_single_checkbox = list_item_div.locator('input')
    expect(toggle_single_checkbox).to_have_count(1)
    expect(toggle_single_checkbox).to_have_role("checkbox")
    expect(toggle_single_checkbox).to_have_class("toggle")
    expect(toggle_single_checkbox).not_to_be_checked()
    expect(toggle_single_checkbox).to_have_attribute("aria-label", "Toggle Todo")

    toggle_single_item_label = list_item_div.locator('label')
    expect(toggle_single_item_label).to_have_count(1)
    expect(toggle_single_item_label).to_have_attribute('data-testid', 'todo-title')
    expect(toggle_single_item_label).to_have_text(input_text_first)

    # check delete item button cant be found
    delete_button = page_with_url.locator('.destroy')
    expect(delete_button).not_to_be_visible()
    expect(delete_button).to_be_enabled()

    #check delete_button attributes
    expect(delete_button).to_have_class("destroy")
    expect(delete_button).to_have_role("button")
    expect(delete_button).to_have_class("destroy")
    expect(delete_button).to_have_attribute("aria-label", "Delete")

    #check visibility of delete item button when hover
    todo_list.hover()
    expect(delete_button).to_be_visible()
    expect(delete_button).to_be_enabled()

    #check edit input
    edit_input = todo_list_item.locator('input.edit')
    expect(edit_input).to_have_class("edit")
    expect(edit_input).to_have_attribute("aria-label", "Edit")
    expect(edit_input).to_have_value(input_text_first)

    expect(edit_input).not_to_be_visible()
    expect(edit_input).to_be_enabled()

    #check edit input enabling
    toggle_single_item_label.dblclick()
    expect(edit_input).to_be_visible()

    #check editing mode
    expect(list_item_div).not_to_be_visible()
    expect(todo_list_item).to_have_class('editing')
    edit_input.fill('input_text_second')
    expect(edit_input).to_have_value('input_text_second')

    #check return to previous value by pressing escape
    edit_input.press('Escape')
    expect(list_item_div).to_be_visible()
    expect(todo_list_item).not_to_have_class('editing')
    expect(toggle_single_item_label).to_have_text(input_text_first)
    expect(edit_input).not_to_be_visible()

    # Check that changes was applied
    toggle_single_item_label.dblclick()
    edit_input.fill('111111')
    edit_input.press('Enter')
    expect(edit_input).not_to_be_visible()
    expect(list_item_div).to_be_visible()
    expect(todo_list_item).not_to_have_class('editing')
    expect(toggle_single_item_label).to_have_text('111111')
'''


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
        delete_button = page.locator('.destroy')
        delete_button.click()


def single_add_todo(page, text):
    new_todo_input = page.get_by_placeholder('What needs to be done?')
    new_todo_input.fill(text)

    new_todo_input.press('Enter')


def test_completion_checkbox(open_page_wout_cookies):
    url, page = open_page_wout_cookies

    single_add_todo(page, "complete")

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
    all_switcher = filters.get_by_role('link').filter(has_text="All")
    expect(all_switcher).to_have_class("selected")
    expect(page.get_by_test_id('todo-item')).to_have_count(4)

    active = filters.get_by_role('link').filter(has_text="Active")
    active.click()
    expect(active).to_have_class("selected")
    expect(page.get_by_test_id('todo-item')).to_have_count(2)
    expect(page).to_have_url(re.compile(".*active"))

    completed = filters.get_by_role('link').filter(has_text="Completed")
    completed.click()
    expect(completed).to_have_class("selected")
    expect(page.get_by_test_id('todo-item')).to_have_count(2)
    expect(page).to_have_url(re.compile(".*completed"))


# test adding a single element
# TODO Rewrite using Playwright locators recommendations
def test_add_todo(open_page_wout_cookies):
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
    expect(toggle_single_item_label).to_have_text(input_text_first)


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


'''def test_check_no_elements_state(page_with_url):
    url, page_with_url = page_with_url
    todoapp = page_with_url.locator('body section')
    expect(todoapp).to_have_count(1)
    expect(todoapp).to_have_class('todoapp')

    todoapp_div = todoapp.locator("div")
    expect(todoapp).to_have_count(1)

    header = todoapp_div.locator('header')
    expect(header).to_have_count(1)
    expect(header).to_have_class('header')

    h1 = header.locator('h1')
    expect(h1).to_have_text('todos')
    expect(h1).to_have_count(1)

    input_new_todo = header.locator("input")
    expect(input_new_todo).to_have_count(1)
    expect(input_new_todo).to_have_class('new-todo')
    expect(input_new_todo).to_have_attribute("placeholder", "What needs to be done?")
    expect(input_new_todo).to_be_visible()

    todo_main = todoapp_div.locator('main')
    expect(todo_main).to_have_count(0)

    todo_footer = todoapp_div.locator('footer')
    expect(todo_footer).to_have_count(0)

    footer = page_with_url.locator('body footer')
    expect(footer).to_have_count(1)
    expect(footer).to_have_class('info')
    expect(footer.locator('p')).to_have_text(
        ["Double-click to edit a todo", 'Created by Remo H. Jansen', 'Part of TodoMVC'])
    expect(footer.locator('p:first-child')).to_contain_text("Double-click to edit a todo")
    expect(footer.locator('p > a')).to_have_text(['Remo H. Jansen', 'TodoMVC'])
    first_link = footer.locator('p:nth-child(2) > a')
    expect(first_link).to_have_attribute('href', 'http://github.com/remojansen/')
    second_link = footer.locator('p:nth-child(3) > a')
    expect(second_link).to_have_attribute('href', 'http://todomvc.com')
'''
