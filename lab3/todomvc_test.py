from playwright.sync_api import sync_playwright


def test_add_new_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        page.goto("https://todomvc.com/examples/react/dist/")

        page.fill(".new-todo", "Buy Milk")
        page.keyboard.press("Enter")

        assert page.locator(".todo-list li").count() == 1
        assert page.locator(".todo-list li label").inner_text() == "Buy Milk"

        browser.close()


def test_complete_todo_and_filter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        page.goto("https://todomvc.com/examples/react/dist/")

        page.fill(".new-todo", "Write Report")
        page.keyboard.press("Enter")

        page.click(".toggle")

        assert "completed" in page.locator(".todo-list li").get_attribute("class")

        page.click("text=Active")
        assert page.locator(".todo-list li").count() == 0

        page.click("text=Completed")
        assert page.locator(".todo-list li").count() == 1

        browser.close()


def test_delete_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        page.goto("https://todomvc.com/examples/react/dist/")

        page.fill(".new-todo", "Task to delete")
        page.keyboard.press("Enter")

        page.hover(".todo-list li")
        page.click(".destroy", force=True)

        assert page.locator(".todo-list li").count() == 0

        browser.close()


def test_add_empty_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto("https://todomvc.com/examples/react/dist/")

        page.fill(".new-todo", " ")
        page.keyboard.press("Enter")

        assert page.locator(".todo-list li").count() == 0

        browser.close()

