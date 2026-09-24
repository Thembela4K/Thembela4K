"""Generate the project timeline used in the GitHub profile README."""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "work-timeline-light.svg"

GROUPS = [
    (
        "2026",
        150,
        [
            (
                "AI / ANALYTICS",
                "ESPPRA AI Assistant & Operational Dashboard",
                "I built an assistant and dashboard that make live assessment records",
                "easier to explore, with reports reviewed before export.",
            ),
            (
                "OPERATIONS",
                "Operations Core CRM",
                "I brought clients, finance, approvals and team tasks into one place",
                "so the team can follow everyday work from start to finish.",
            ),
            (
                "DESKTOP SYSTEM",
                "DDW Gate Entry System",
                "I built an offline Windows app for visitor and contractor checks,",
                "entry decisions and a daily register staff can rely on.",
            ),
            (
                "CAREER ASSESSMENT",
                "Self-Directed Search System",
                "I connected sign-in, assessment, results and certificate download",
                "into one straightforward participant journey.",
            ),
        ],
    ),
    (
        "2025",
        697,
        [
            (
                "DATA / BI",
                "FINCORP Power BI Dashboards",
                "With the dashboard team, I checked source data and built Power BI",
                "pages that make KPIs and trends easier to explore.",
            ),
            (
                "PROPERTY MIS",
                "Estate Agents Management System",
                "I gave a property agency one place to manage tenants, rent,",
                "payments and arrears in its daily workflow.",
            ),
            (
                "WEB GIS",
                "Malkerns Municipal Web GIS",
                "I helped publish ward maps on the council website so people",
                "can explore them on a phone or desktop.",
            ),
        ],
    ),
    (
        "2024",
        1120,
        [
            (
                "FIELD DATA",
                "Water Use Survey Reporting",
                "I turned survey records into repeatable reports, working with",
                "GIS colleagues to keep the summaries close to field data.",
            ),
        ],
    ),
]


def add_text(parts: list[str], x: int, y: int, value: str, *, size: int, color: str,
             weight: int = 400, family: str = "Arial, Helvetica, sans-serif",
             spacing: int | None = None) -> None:
    tracking = f' letter-spacing="{spacing}"' if spacing is not None else ""
    parts.append(
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}"{tracking}>{escape(value)}</text>'
    )


def main() -> None:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1280" viewBox="0 0 1200 1280" role="img" aria-labelledby="title desc">',
        '<title id="title">Selected work, 2024 to 2026</title>',
        '<desc id="desc">A branching timeline of eight software, data, AI and GIS projects.</desc>',
        '<rect width="1200" height="1280" rx="18" fill="#ffffff"/>',
        '<rect x="1" y="1" width="1198" height="1278" rx="17" fill="none" stroke="#dce6e0"/>',
        '<path d="M 48 125 H 1152 M 48 1248 H 1152" stroke="#e2eae5"/>',
        '<path d="M 187 158 V 1232" stroke="#a9bfb1" stroke-width="2" stroke-dasharray="3 8"/>',
    ]
    add_text(parts, 54, 38, "SELECTED WORK", size=15, color="#39745a", weight=700, spacing=2)
    add_text(parts, 54, 93, "Work, over time.", size=38, color="#1b2d24", weight=700)
    add_text(parts, 943, 92, "2024–2026  /  PROJECTS", size=15, color="#64796d", weight=700)
    add_text(parts, 54, 1268, "BUILT IN ESWATINI", size=13, color="#718579", weight=700, spacing=2)

    for year, start, projects in GROUPS:
        add_text(parts, 56, start + 43, year, size=28, color="#24563e", weight=700)
        add_text(parts, 57, start + 64, f"{len(projects):02d} PROJECT{'S' if len(projects) != 1 else ''}", size=12, color="#6c8173", weight=700)
        for index, (category, title, first, second) in enumerate(projects):
            y = start + index * 124
            center = y + 55
            parts.extend(
                [
                    f'<path d="M 187 {center} H 238" stroke="#a9bfb1" stroke-width="2"/>',
                    f'<circle cx="187" cy="{center}" r="7" fill="#ffffff" stroke="#3c8865" stroke-width="2"/>',
                    f'<circle cx="187" cy="{center}" r="2" fill="#3c8865"/>',
                    f'<rect x="238" y="{y}" width="910" height="112" rx="12" fill="#f8faf8" stroke="#dce6e0"/>',
                    f'<path d="M 250 {y + 14} V {y + 98}" stroke="#3c8865" stroke-width="3" stroke-linecap="round"/>',
                ]
            )
            add_text(parts, 270, y + 25, category, size=12, color="#326d51", weight=700,
                     family="Consolas, DejaVu Sans Mono, monospace", spacing=1)
            add_text(parts, 270, y + 54, title, size=23, color="#1b2d24", weight=700)
            add_text(parts, 270, y + 80, first, size=17, color="#43564b")
            add_text(parts, 270, y + 101, second, size=17, color="#43564b")

    parts.append("</svg>")
    OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
