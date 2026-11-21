"""Rebuild the dated news page with an offline, wheel-backed Pillow import."""
import os
import sys
import zipfile
import tempfile
import glob

# Safe-path mode (-P) deliberately omits the script directory from sys.path.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.dont_write_bytecode = True

try:
    import PIL
except ImportError as missing_pillow:
    tag = sys.implementation.cache_tag.replace("cpython-", "cp", 1)
    wheels = sorted(glob.glob(os.path.join(SCRIPT_DIR, "vendor", "[Pp]illow-*.whl")))
    # Both interpreter and ABI must match: cp313t is not the normal cp313 ABI.
    matched = [wheel for wheel in wheels
               if f"-{tag}-{tag}-" in os.path.basename(wheel)]
    candidates = matched or wheels
    if not candidates:
        raise ImportError(f"Pillow is missing and no vendored wheel is available for {tag}") from missing_pillow
    wheel_dir = tempfile.mkdtemp(prefix="world-news-pillow-")
    with zipfile.ZipFile(candidates[0]) as archive:
        archive.extractall(wheel_dir)
    sys.path.insert(0, wheel_dir)
    import PIL

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    configured_output = os.environ.get("MAKEFUN_OUTPUT_DIR")
    output = Path(configured_output) if configured_output else ROOT
    output.mkdir(parents=True, exist_ok=True)
    from draw import render
    payload = render()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n") or len(payload) > 1048576:
        raise ValueError("Expected a complete competition-sized PNG")
    (output / "entry.png").write_bytes(payload)
    if configured_output:
        try:
            (ROOT / "entry.png").write_bytes(payload)
        except OSError:
            # The contest mounts the source tree read-only; /output is primary.
            pass
    print(f"Wrote {output / 'entry.png'} ({len(payload):,} bytes)")


if __name__ == "__main__":
    main()
