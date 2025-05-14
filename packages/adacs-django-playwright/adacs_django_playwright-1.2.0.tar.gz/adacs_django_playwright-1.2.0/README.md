# ADACS Playwright Class

A Django python package that extends the Django
`StaticLiveServerTestCase` to use Playwright for testing.

## Why?

When using Playwright for testing with the Django test runner there are
common issues that need to be solved:

- Accessing the playwright object, browser object, and the browser context.
- Automatically closing the browser context after each test.
- Forcing login of a user for admin testing.
- Correctly setting cookies during login.
- Handling async requests and responses.

On top of the above this package also provides support for htmx by providing
methods to wait for htmx requests to finish.

## Usage

Instead of inheriting from Django's `StaticLiveServerTestCase` you should
inherit from either `PlaywrightTestCase` for synchronous tests or
`AsyncPlaywrightTestCase` for asynchronous tests. Both classes behave like
`StaticLiveServerTestCase` but with the added functionality of Playwright.

They adds 2 useful class properties:

```python
self.browser   # A browser object from playwright used for accessing the page.
self.playwright  # The return from sync_playwright().start()
```

They also add the following methods on both the sync and async classes:

- **`login`**  
  Logs in a Django user by setting session cookies in the browser context.  
  **Example:**

  ```python
  test_case.login(user)
  ```

- **`htmx_wait`**  
  Waits for HTMX to load and complete any ongoing operations on the page.  
  **Example:**

  ```python
  test_case.htmx_wait(page)
  ```

- **`htmx_settle`**  
  Ensures all HTMX operations (requests, DOM updates) are finished before
  proceeding.  
  **Example:**

  ```python
  test_case.htmx_settle(page)
  ```

## Example Test

```python
from adacs_django_playwright.adacs_django_playwright import PlaywrightTestCase

class MyTestCase(PlaywrightTestCase):

  def awesome_test(self):
    page = self.browser.new_page()
    page.goto(f"{self.live_server_url}")
```
