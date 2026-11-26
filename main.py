"""Front page for Thursday, 26 November 2026.

The bundled picture is laid out like a newspaper front page for that
day. The big lead story is Shenzhou-24 docking at China's Tiangong
station, carrying Muhammad Zeeshan Ali, the first Pakistani astronaut
to fly. Below it, a second row carries three stories side by side: a
Houthi drone striking a tower in Riyadh's financial district and
injuring eleven people; Wall Street tumbling as Nvidia leads a sell-off
in AI shares on the eve of Thanksgiving; and the BepiColombo probe
finally entering orbit around Mercury after an eight-year journey.
A strip along the bottom rounds the day out with Colombia marking ten
years of its peace deal, India celebrating Constitution Day, and an
earthquake shaking Nepal.
"""

import os
import sys
from pathlib import Path

SOURCE_NAME = "news.jpg"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"


def source_path() -> Path:
    """Return the bundled image sitting next to this program."""
    return Path(__file__).resolve().parent / SOURCE_NAME


def output_path() -> Path:
    """Return where the entry image must be written."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / OUTPUT_NAME


def load_source() -> bytes:
    """Read the bundled JPEG bytes into memory."""
    src = source_path()
    if not src.is_file():
        raise SystemExit(f"bundled image missing: {src}")
    return src.read_bytes()


def write_entry(data: bytes, dest: Path) -> None:
    """Write the image bytes to the output location, creating it if needed."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def check_source(data: bytes) -> None:
    """Refuse anything that is not a JPEG within the 1 MiB limit."""
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"bundled image too large: {len(data)} bytes (limit {MAX_BYTES})"
        )
    if not data.startswith(JPEG_MAGIC):
        raise SystemExit("bundled image is not a JPEG (bad magic bytes)")


def main() -> None:
    data = load_source()
    check_source(data)
    dest = output_path()
    write_entry(data, dest)
    written = dest.read_bytes()
    if written != data:
        raise SystemExit("output does not match the bundled image")
    print(f"Wrote {dest} ({len(written)} bytes, byte-identical to news.jpg)")


if __name__ == "__main__":
    main()
