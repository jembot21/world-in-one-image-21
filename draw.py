"""Measured, deterministic Pillow composition for a single 1024px news page."""
from functools import lru_cache
from io import BytesIO
import json
from PIL import Image, ImageDraw, ImageFont

S = 3
BG = '#0C1425'
WHITE = '#F4F6FA'
PALE = '#C7D2E2'
MUTED = '#96A8BE'
GOLD = '#E9BD68'
CYAN = '#6ED6E3'
PALETTE = ('#79A9D7', '#60C6BA', '#E7B967', '#E68493', '#B69ADF', '#86C69D')


def render(root):
    data = json.loads((root / 'stories.json').read_text(encoding='utf-8'))
    assert len(data['leads']) == 12 and len(data['briefs']) == 38
    image = Image.new('RGB', (1024*S, 1024*S), BG)
    pen = ImageDraw.Draw(image)
    adjustments = []
    headlines = []

    @lru_cache(None)
    def font(kind, size):
        files = {'regular': 'Barlow-Regular.ttf', 'bold': 'Barlow-Bold.ttf',
                 'semi': 'Barlow-SemiBold.ttf', 'display': 'ArchivoBlack-Regular.ttf'}
        path = root / 'assets' / files[kind]
        if not path.is_file() or path.stat().st_size < 10000:
            path = '/usr/share/fonts/truetype/dejavu/DejaVuSans' + ('' if kind == 'regular' else '-Bold') + '.ttf'
        return ImageFont.truetype(str(path), round(size*S))

    def width(text, face):
        return pen.textlength(text, font=face) / S

    def rect(box, fill, outline=None, radius=0):
        coords = tuple(round(v*S) for v in box)
        pen.rounded_rectangle(coords, radius=round(radius*S), fill=fill, outline=outline, width=S)

    def line(text, x, y, w, size, kind='regular', color=WHITE, minimum=6):
        original = size
        while width(text, font(kind, size)) > w and size > minimum:
            size = max(minimum, size-0.25)
        face = font(kind, size)
        measured = width(text, face)
        assert measured <= w + 0.01, (text, measured, w)
        pen.text((round(x*S), round(y*S)), text, font=face, fill=color, anchor='lt')
        if size != original:
            adjustments.append(('font', text, size))
        return size

    def wrap(text, face, w):
        rows = []
        current = ''
        for word in text.split():
            candidate = (current + ' ' + word).strip()
            if current and width(candidate, face) > w:
                rows.append(current)
                current = word
            else:
                current = candidate
        if current:
            rows.append(current)
        return rows

    def paragraph(text, box, size, kind='regular', color=PALE, maxlines=3, headline=False):
        x, y, w, h = box
        while size >= 5:
            face = font(kind, size)
            rows = wrap(text, face, w)
            step = size*1.12
            if len(rows) <= maxlines and len(rows)*step <= h and all(width(r, face) <= w for r in rows):
                break
            size -= 0.25
        else:
            raise AssertionError('Text cannot fit: '+text)
        if headline:
            headlines.extend((r, face, w) for r in rows)
        for i, row in enumerate(rows):
            line(row, x, y+i*step, w, size, kind, color, minimum=size)
        adjustments.append(('paragraph', text, size))

    # The masthead names the single news day before any story is read.
    title = 'THE WORLD IN ONE IMAGE'
    face = font('semi', 21)
    tracking = 2.4
    x = 26
    for letter in title:
        advance = width(letter, face)
        line(letter, x, 22, advance+1, 21, 'semi', GOLD)
        x += advance+tracking
    line('SATURDAY 21 NOVEMBER 2026', 24, 54, 976, 66, 'display')
    line('50 STORIES · 7 REGIONS · 10 FIELDS · ONE PAGE', 26, 111, 972, 24, 'bold', CYAN)
    regions = ('EUROPE', 'NORTH AMERICA', 'MIDDLE EAST', 'ASIA-PACIFIC', 'AFRICA', 'LATIN AMERICA', 'OCEANIA')
    chip_widths = (99, 175, 146, 156, 96, 165, 111)
    x = 26
    for name, w in zip(regions, chip_widths):
        rect((x, 143, x+w, 162), '#192B41', radius=8)
        line(name, x+8, 147, w-16, 11.5, 'semi', PALE)
        x += w+4
    rect((26, 170, 998, 203), '#17263A', radius=4)
    line('THE DAY IN NUMBERS', 34, 176, 112, 9, 'bold', GOLD)
    for i, stat in enumerate(data['numbers']):
        x = 155+i*139.3
        line(stat['value'], x, 173, 130, 18, 'bold')
        line(stat['label'], x, 193, 130, 7, 'semi', MUTED)

    fields = ('CONFLICT', 'MARKETS', 'UKRAINE', 'ENERGY', 'SOCIETY', 'JUSTICE', 'POLITICS', 'MATHEMATICS', 'BOXING')
    for i, story in enumerate(data['leads']):
        x = 26+(i % 3)*327
        y = 211+(i // 3)*116
        w = 318
        field = story['tag'].split(' · ')[-1]
        accent = PALETTE[fields.index(field) % len(PALETTE)]
        rect((x, y, x+w, y+110), '#152238', radius=6)
        rect((x, y, x+3, y+110), accent, radius=1)
        line(story['tag'], x+11, y+8, w-47, 10.5, 'semi', accent)
        pen.ellipse((round((x+w-27)*S), round((y+6)*S), round((x+w-9)*S), round((y+24)*S)), fill=accent)
        line(field[0], x+w-22, y+10, 10, 10, 'bold', BG)
        paragraph(story['headline'], (x+11, y+25, w-22, 44), 22, 'bold', WHITE, headline=True)
        paragraph(story['summary'], (x+11, y+73, w-22, 33), 16.5)

    line('MORE OF THE DAY — 38 BRIEFS', 26, 675, 972, 14, 'bold', GOLD)
    for i, brief in enumerate(data['briefs']):
        x = 26+(i // 19)*491
        y = 696+(i % 19)*13
        # Preserve glyph proportions: reclaim the right inset at 12.5px,
        # then reduce type further only if the full column is still too narrow.
        column_width = 481
        available = column_width-10
        size = 14.5
        while size > 12.5 and width(brief, font('regular', size)) > available:
            size -= 0.25
        if width(brief, font('regular', size)) > available:
            available = column_width
        fitted = line(brief, x, y, available, size, minimum=6)
        adjustments.append(('brief', brief, fitted, available))
    rect((26, 947, 998, 980), '#101F31', outline='#506880', radius=4)
    paragraph(data['date_check'], (35, 953, 954, 25), 11, color=PALE, maxlines=2)
    paragraph(data['footer'], (26, 988, 972, 23), 9.5, color=MUTED, maxlines=2)

    # Independent assertion pass over every final headline line.
    assert headlines and len(data['numbers']) == 6
    assert [int(item.split('.')[0]) for item in data['briefs']] == list(range(13, 51))
    for text, face, w in headlines:
        assert pen.textlength(text, font=face) <= w*S, text
    image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format='PNG', optimize=False, compress_level=9)
    payload = buffer.getvalue()
    assert len(payload) <= 1048576, 'Competition image exceeds 1 MiB'
    print('Measured fit adjustments:', json.dumps(adjustments, ensure_ascii=False))
    return payload
