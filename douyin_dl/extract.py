from typing import Optional, Tuple

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from .utils import MEDIA_HOST_PATTERN


def capture_media_url(page_url: str, timeout_ms: int = 15000, headless: bool = True) -> Tuple[str, str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        captured_url: Optional[str] = None

        def on_request(req):
            nonlocal captured_url
            url = req.url
            if captured_url is None and MEDIA_HOST_PATTERN.match(url):
                captured_url = url

        page.on("request", on_request)
        page.goto(page_url, wait_until="domcontentloaded", timeout=timeout_ms)
        try:
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            pass

        final_url = page.url
        if captured_url is None:
            try:
                page.wait_for_event("request", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                pass

        context.close()
        browser.close()

        if captured_url:
            return captured_url, final_url
        raise RuntimeError(f"Failed to capture media URL from: {final_url}")


