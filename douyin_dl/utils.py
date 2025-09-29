import re

MEDIA_HOST_PATTERN = re.compile(r"https?://v\d+-web\.douyinvod\.com/[^\s'\"]+")

DEFAULT_HEADERS = {
    "Referer": "https://www.douyin.com/",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

DOWNLOAD_CHUNK_BYTES = 1024 * 128



