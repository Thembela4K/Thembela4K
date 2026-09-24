"""Build the terminal-style SVG source and animated GIF used in the profile README."""

from __future__ import annotations

from math import sin
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SIZE = (1200, 320)
BACKGROUND = "#080c0a"
INK = "#dce7dd"
MUTED = "#8caa95"
ACCENT = "#8acba2"
DIM = "#325842"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [Path("C:/Windows/Fonts/consolab.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")]
        if bold
        else [Path("C:/Windows/Fonts/consola.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")]
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("A Consolas or DejaVu Sans Mono font is required")


def name_dots() -> list[tuple[int, int]]:
    mask = Image.new("L", SIZE)
    draw = ImageDraw.Draw(mask)
    large = font(99, bold=True)
    draw.text((73, 58), "THEMBELA", font=large, fill=255)
    draw.text((73, 143), "MTHIMKHULU", font=large, fill=255)
    return [
        (x, y)
        for y in range(66, 247, 7)
        for x in range(77, 718, 7)
        if mask.getpixel((x, y)) > 110
    ]


def wave_dots() -> list[tuple[int, int, int]]:
    return [
        (x, round(134 + row * 21 + 24 * sin((x - 780) / 59 + row * 0.5)), row)
        for row in range(5)
        for x in range(790, 1142, 11)
    ]


def make_svg(name: list[tuple[int, int]], waves: list[tuple[int, int, int]]) -> None:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">',
        '<title id="title">Thembela Mthimkhulu</title>',
        '<desc id="desc">Terminal-inspired dot art spelling Thembela Mthimkhulu with a dotted wave.</desc>',
        f'<rect width="1200" height="320" rx="16" fill="{BACKGROUND}"/>',
        '<rect x="1" y="1" width="1198" height="318" rx="15" fill="none" stroke="#274030"/>',
        '<path d="M 46 47 H 1154 M 46 270 H 1154" stroke="#274030"/>',
        f'<text x="47" y="31" fill="{ACCENT}" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="16">&gt; whoami</text>',
        f'<text x="1153" y="31" text-anchor="end" fill="{MUTED}" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="15">THEMBELA4K  /  ESWATINI</text>',
        f'<text x="47" y="295" fill="{MUTED}" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="15">{escape("SOFTWARE  /  DATA  /  SYSTEMS")}</text>',
        f'<text x="1153" y="295" text-anchor="end" fill="{ACCENT}" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="15">●  BUILDING USEFUL SYSTEMS</text>',
    ]
    parts.extend(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{INK}"/>' for x, y in name)
    parts.extend(f'<circle cx="{x}" cy="{y}" r="{1.7 if row < 3 else 1.4}" fill="{DIM}"/>' for x, y, row in waves)
    parts.append("</svg>")
    (ASSETS / "terminal-banner.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def draw_frame(name: list[tuple[int, int]], waves: list[tuple[int, int, int]], phase: float) -> Image.Image:
    image = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 1199, 319), radius=15, outline="#274030", width=1)
    draw.line((46, 47, 1154, 47), fill="#274030", width=1)
    draw.line((46, 270, 1154, 270), fill="#274030", width=1)
    small = font(15)
    draw.text((47, 15), "> whoami", font=font(16), fill=ACCENT)
    draw.text((1153, 15), "THEMBELA4K  /  ESWATINI", font=small, fill=MUTED, anchor="ra")
    draw.text((47, 280), "SOFTWARE  /  DATA  /  SYSTEMS", font=small, fill=MUTED)
    draw.text((1153, 280), "●  BUILDING USEFUL SYSTEMS", font=small, fill=ACCENT, anchor="ra")

    for x, y in name:
        draw.ellipse((x - 2.4, y - 2.4, x + 2.4, y + 2.4), fill=INK)
    for x, y, row in waves:
        strength = abs(x - (790 + 350 * phase)) < 25
        color = MUTED if strength and row < 3 else DIM
        radius = 1.7 if row < 3 else 1.4
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    return image


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    name = name_dots()
    waves = wave_dots()
    make_svg(name, waves)
    frames = [draw_frame(name, waves, index / 40) for index in range(40)]
    palette = frames[0].quantize(colors=64)
    frames = [frame.quantize(palette=palette) for frame in frames]
    frames[0].save(
        ASSETS / "terminal-banner-wave.gif",
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=90,
        loop=0,
        disposal=2,
    )


if __name__ == "__main__":
    main()
