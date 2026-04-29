from typing import Optional, Tuple

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from .utils import MEDIA_HOST_PATTERN


def capture_media_url(page_url: str, timeout_ms: int = 15000, headless: bool = True) -> Tuple[str, str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        captured_url: Optional[str] = None
        fallback_url: Optional[str] = None

        def on_request(req):
            nonlocal fallback_url
            url = req.url
            if fallback_url is None and MEDIA_HOST_PATTERN.match(url):
                fallback_url = url

        def on_response(response):
            nonlocal captured_url
            if "aweme/v1/web/aweme/detail/" in response.url:
                try:
                    data = response.json()
                    aweme_detail = data.get("aweme_detail", {})
                    video = aweme_detail.get("video", {})
                    bit_rate = video.get("bit_rate", [])
                    if bit_rate:
                        def get_res(br_info):
                            import re
                            name = br_info.get("gear_name", "")
                            m = re.search(r'_(\d+)_', name)
                            return int(m.group(1)) if m else 0

                        bit_rate_sorted = sorted(bit_rate, key=get_res, reverse=True)
                        for br in bit_rate_sorted:
                            url_list = br.get("play_addr", {}).get("url_list", [])
                            if url_list:
                                captured_url = url_list[0]
                                # print(f"DEBUG: Selected {br.get('gear_name')}")
                                break
                except Exception:
                    pass

        page.on("request", on_request)
        page.on("response", on_response)
        page.goto(page_url, wait_until="domcontentloaded", timeout=timeout_ms)
        try:
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            pass

        final_url = page.url
        if captured_url is None and fallback_url is None:
            try:
                page.wait_for_event("request", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                pass

        context.close()
        browser.close()

        final_captured = captured_url or fallback_url
        if final_captured:
            return final_captured, final_url
        raise RuntimeError(f"Failed to capture media URL from: {final_url}")


