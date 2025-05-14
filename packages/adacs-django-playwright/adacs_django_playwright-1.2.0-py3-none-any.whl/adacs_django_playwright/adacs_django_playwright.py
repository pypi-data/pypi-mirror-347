import functools
import os
import time
from asyncio import sleep as async_sleep
from time import sleep as sync_sleep
from typing import Optional
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.async_api import BrowserContext, async_playwright
from playwright.async_api import expect as async_expect
from playwright.sync_api import expect as sync_expect
from playwright.sync_api import sync_playwright


class PlaywrightTestCase(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.browser_context = cls.browser.new_context()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def login(self, user):
        """
        Logs the specified Django User object in to the browser and sets the corresponding session cookie
        """
        self.client.force_login(user)
        cookies = []
        for name, cookie in self.client.cookies.items():
            max_age = self.client.session.get_expiry_age()
            expires_time = time.time() + max_age
            cookies.append(
                {
                    "name": name,
                    "value": cookie.value,
                    "max_age": max_age,
                    "expires": int(expires_time),
                    "domain": urlparse(self.live_server_url).netloc,
                    "path": settings.SESSION_COOKIE_PATH or "",
                    "secure": settings.SESSION_COOKIE_SECURE or False,
                    "httponly": settings.SESSION_COOKIE_HTTPONLY or False,
                    "samesite": settings.SESSION_COOKIE_SAMESITE or "",
                }
            )

        self.browser_context.clear_cookies()
        self.browser_context.add_cookies(cookies)

    def htmx_wait(self, page, retries=100, sleep_time=0.1):
        """
        Waits for HTMX to be available on the page and then waits for any HTMX operations to complete.

        Args:
            page: The Playwright page object
            retries: Number of times to check for HTMX availability
            seep_time: Time to wait between checks

        Raises:
            Exception: If HTMX fails to load after retries are exhausted
        """
        for _ in range(retries):
            if page.evaluate("window.htmx") is None:
                sync_sleep(sleep_time)
                continue

            break
        else:
            raise Exception(
                "htmx failed to load"
            )  # pylint: disable=broad-exception-raised

        self.htmx_settle(page)

    def htmx_settle(self, page):
        """
        Waits for all HTMX operations to complete by checking for HTMX-specific CSS classes.

        This function ensures that HTMX has finished all requests, swapping operations,
        and DOM updates before proceeding with the test.

        Args:
            page: The Playwright page object
        """
        sync_expect(
            page.locator(".htmx-request, .htmx-settling, .htmx-swapping, .htmx-added")
        ).to_have_count(0)


class AsyncPlaywrightTestCase(StaticLiveServerTestCase):
    serialized_rollback = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playwright = None
        self.browser = None
        self.browser_context: Optional[BrowserContext] = None

    async def login(self, user):
        """
        Logs the specified Django User object in to the browser and sets the corresponding session cookie
        """
        await self.client.aforce_login(user)
        cookies = []
        for name, cookie in self.client.cookies.items():
            max_age = await self.client.session.aget_expiry_age()
            expires_time = time.time() + max_age
            cookies.append(
                {
                    "name": name,
                    "value": cookie.value,
                    "max_age": max_age,
                    "expires": int(expires_time),
                    "domain": urlparse(self.live_server_url).netloc,
                    "path": settings.SESSION_COOKIE_PATH or "",
                    "secure": settings.SESSION_COOKIE_SECURE or False,
                    "httponly": settings.SESSION_COOKIE_HTTPONLY or False,
                    "samesite": settings.SESSION_COOKIE_SAMESITE or "",
                }
            )

        await self.browser_context.clear_cookies()
        await self.browser_context.add_cookies(cookies)

    async def htmx_wait(self, page, retries=100, sleep_time=0.1):
        """
        Waits for HTMX to be available on the page and then waits for any HTMX operations to complete.

        Args:
            page: The Playwright page object
            retries: Number of times to check for HTMX availability
            seep_time: Time to wait between checks

        Raises:
            Exception: If HTMX fails to load after retries are exhausted
        """
        for _ in range(retries):
            if await page.evaluate("window.htmx") is None:
                await async_sleep(sleep_time)
                continue

            break
        else:
            raise Exception(
                "htmx failed to load"
            )  # pylint: disable=broad-exception-raised

        await self.htmx_settle(page)

    async def htmx_settle(self, page):
        """
        Waits for all HTMX operations to complete by checking for HTMX-specific CSS classes.

        This function ensures that HTMX has finished all requests, swapping operations,
        and DOM updates before proceeding with the test.

        Args:
            page: The Playwright page object
        """
        await async_expect(
            page.locator(".htmx-request, .htmx-settling, .htmx-swapping, .htmx-added")
        ).to_have_count(0)


# Async test decorator to get async setup and tear down working. Note that creating the playwright
# instance and browser will slow down tests tremendously.
def async_playwright_test(coroutine):
    @functools.wraps(coroutine)
    async def inner(*args):
        cls = args[0]
        cls.playwright = await async_playwright().start()
        cls.browser = await cls.playwright.chromium.launch()
        cls.browser_context = await cls.browser.new_context()

        if hasattr(cls, "asetUp"):
            await cls.asetUp()

        result = await coroutine(*args)

        if hasattr(cls, "atearDown"):
            await cls.atearDown()

        await cls.browser.close()
        await cls.playwright.stop()

        return result

    return inner
