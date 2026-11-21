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

The six requested Google Fonts downloads were attempted during the build, but the network proxy was unreachable. Rendering therefore uses system DejaVu Sans and DejaVu Sans Bold; `assets/` is reserved for the requested downloaded fonts. No downloaded font files or font licences are present.

The output is a deterministic 1024×1024 RGB PNG with no timestamps or random state. The default destination is this repository; the contest's `/output` directory takes precedence when present, and `MAKEFUN_OUTPUT_DIR` can override either. The offline, standard-library-only contest harness can copy the checked-in `entry.png` when Pillow is unavailable. Install Pillow to regenerate the artwork from source. No network is used at runtime.

![make.fun](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/jembot21/world-in-one-image-21/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/jembot21/world-in-one-image-21/reward.svg)
