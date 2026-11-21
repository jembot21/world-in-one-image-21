# The World in One Image — Saturday 21 November 2026

A make.fun news-image-20261121 entry.

## Run

```sh
pip install pillow
python3 main.py
```

The page contains 50 stories: 12 lead cards and 38 numbered briefs, plus six numbers, a date check and a source footer. Content is supplied by the commissioning brief; the program does not fetch or independently verify news.

Sources named in the supplied brief: Reuters · AP · AFP · RFE/RL · CNA · DAZN · UKMTO · BBC.

## Reproducibility and layout

`stories.json` holds all editorial content. `draw.py` measures every rendered line with Pillow, wraps and shrinks lead text, and asserts that final headline lines fit. Briefs shrink in 0.25px steps without horizontal distortion. At 12.5px, a line can reclaim the 10px right inset to use its full 481px column; only if that still fails does the type shrink further. No text is shortened or clipped. The dense 50-story specification requires smaller type inside the cards than the suggested nominal sizes.

A 300×300 inspection confirms that the date remains clear, but the numbers are marginal and the card details and briefs are too small for comfortable reading. Use the full-resolution image to read all 50 stories.

The six requested Google Fonts downloads were attempted during the build, but the network proxy was unreachable. The same DejaVu Sans and DejaVu Sans Bold used for the artwork are now bundled in `assets/`, with their font licence. Font loading tries repository assets first, then system DejaVu paths, then Pillow's default font as a last resort. The bundled fonts preserve the existing artwork without requiring system font packages.

The output is a deterministic 1024×1024 RGB PNG with no timestamps or random state. `MAKEFUN_OUTPUT_DIR`, when set, is the primary destination; otherwise the image is written beside `main.py`. With that variable set, an additional repository-side copy is attempted, and an `OSError` from that optional copy is ignored so a read-only source mount works. Imports and asset reads are independent of the working directory, including under `python3 -P -s`. No network is used at runtime.

If Pillow is missing, `main.py` selects a wheel from `vendor/` using `sys.implementation.cache_tag`, preferring an exact interpreter and ABI match (for example `cp313-cp313`, excluding `cp313t`). If no matching wheel exists, it tries the first available Pillow wheel. The wheel is unpacked into a fresh temporary directory, which is added to the import path. No install or source-tree writes are needed. Missing or incompatible Pillow fails visibly rather than copying a pre-rendered image.

Dependency availability: the CPython 3.12 Pillow 13.0.0 wheel was recovered from the local cache. Fetching PyPI metadata and the required CPython 3.13 wheel is currently blocked by the unavailable proxy and direct network access. The CPython 3.13 vendoring requirement remains incomplete until that wheel is supplied.

![make.fun](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/jembot21/world-in-one-image-21/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/jembot21/world-in-one-image-21/reward.svg)
