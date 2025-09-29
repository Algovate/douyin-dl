from pathlib import Path
from typing import Optional

import requests
from requests import RequestException
from tqdm import tqdm

from .utils import DEFAULT_HEADERS, DOWNLOAD_CHUNK_BYTES


def download_media(media_url: str, output: Path, headers: Optional[dict] = None, timeout_seconds: int = 60, show_progress: bool = True) -> None:
    final_headers = dict(DEFAULT_HEADERS)
    if headers:
        final_headers.update(headers)

    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with requests.get(media_url, headers=final_headers, stream=True, timeout=timeout_seconds) as r:
            r.raise_for_status()

            total_bytes_header = r.headers.get("Content-Length")
            total_bytes = int(total_bytes_header) if total_bytes_header and total_bytes_header.isdigit() else None

            bytes_downloaded = 0

            with open(output, "wb") as f:
                if show_progress:
                    with tqdm(total=total_bytes, unit="B", unit_scale=True, unit_divisor=1024, desc="Downloading", disable=not show_progress) as bar:
                        for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_BYTES):
                            if not chunk:
                                continue
                            f.write(chunk)
                            size = len(chunk)
                            bytes_downloaded += size
                            bar.update(size)
                else:
                    for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_BYTES):
                        if not chunk:
                            continue
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
    except RequestException as exc:
        raise RuntimeError(f"Download failed: {exc}") from exc


