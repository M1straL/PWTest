from playwright.async_api import Page


class LocatorsHelper:
    NEW_TODO_PLACEHOLDER_TEXT = 'What needs to be done?'
    NEW_TODO_ITEM_TEST_ID = 'todo-item'
    NEW_TODO_TITLE_TEST_ID = 'todo-title'
    DESTROY_BUTTON = '.destroy'
    TODO_COUNT = 'todo-count'
    STRONG = 'strong'

    ENTER_BTN = 'Enter'
    ESCAPE_BTN = 'Escape'
    SELECTED = 'selected'

    async def get_new_todo_text_placeholder(self: Page):
        return self.get_by_placeholder(LocatorsHelper.NEW_TODO_PLACEHOLDER_TEXT)
