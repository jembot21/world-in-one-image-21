"""Rebuild the dated news page, or serve it in the offline contest sandbox."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output" if Path("/output").is_dir() else str(ROOT)))
    output.mkdir(parents=True, exist_ok=True)
    try:
        from draw import render
    except ModuleNotFoundError as exc:
        if exc.name != "PIL":
            raise
        payload = (ROOT / "entry.png").read_bytes()
    else:
        payload = render(ROOT)
    if not payload.startswith(b"\x89PNG\r\n\x1a\n") or len(payload) > 1048576:
        raise ValueError("Expected a complete competition-sized PNG")
    (output / "entry.png").write_bytes(payload)
    print(f"Wrote {output / 'entry.png'} ({len(payload):,} bytes)")


if __name__ == "__main__":
    main()
