import argparse
import re
import sys
from pathlib import Path
from typing import Type

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .download import download_media
from .extract import capture_media_url


def derive_video_id(media_url: str, page_url: str) -> str:
    vid_match = re.search(r"__vid=(\d+)", media_url)
    if not vid_match:
        vid_match = re.search(r"/video/(\d+)", page_url)
    return vid_match.group(1) if vid_match else "douyin_video"


def retry_with_backoff(operation, *, retries: int, base_delay: float, exceptions: tuple[Type[Exception], ...]):
    import time

    attempt = 0
    last_error: Exception | None = None
    while attempt <= max(0, retries):
        try:
            return operation()
        except exceptions as exc:  # type: ignore[misc]
            last_error = exc
        if attempt < retries:
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
        attempt += 1
    if last_error:
        raise last_error
    raise RuntimeError("Operation failed after retries")


def main() -> None:
    parser = argparse.ArgumentParser(description="Douyin 视频下载器（命令行）")
    parser.add_argument("url", help="抖音短链或视频页链接，如 https://v.douyin.com/... 或 https://www.douyin.com/video/...")
    parser.add_argument("-o", "--output", help="输出文件名（若指定则优先使用）")
    parser.add_argument("--outdir", help="输出目录（默认：当前目录）")
    parser.add_argument("--timeout", type=int, default=15, help="页面加载超时（秒），默认 15")
    parser.add_argument("--headful", action="store_true", help="显示浏览器窗口（默认无头模式）")
    parser.add_argument("--quiet", action="store_true", help="静默模式：不显示下载进度")
    parser.add_argument("--retries", type=int, default=2, help="失败重试次数，默认 2")
    args = parser.parse_args()

    page_url = args.url.strip()
    if not re.match(r"^https?://", page_url):
        raise SystemExit("链接无效：必须以 http:// 或 https:// 开头")

    timeout_ms = max(1, args.timeout) * 1000

    media_url, final_url = retry_with_backoff(
        lambda: capture_media_url(page_url, timeout_ms=timeout_ms, headless=not args.headful),
        retries=max(0, args.retries),
        base_delay=0.5,
        exceptions=(PlaywrightTimeoutError, RuntimeError),
    )

    vid = derive_video_id(media_url, final_url)

    if args.output:
        out_path = Path(args.output)
    else:
        out_dir = Path(args.outdir) if args.outdir else Path.cwd()
        out_path = out_dir / f"{vid}.mp4"

    retry_with_backoff(
        lambda: download_media(media_url, out_path, show_progress=not args.quiet),
        retries=max(0, args.retries),
        base_delay=0.5,
        exceptions=(RuntimeError,),
    )

    print(str(out_path))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, PlaywrightTimeoutError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


