from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attrs: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.headings: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        self.tags.append(tag)
        self.attrs.append((tag, attrs_dict))
        if "id" in attrs_dict:
            self.ids.append(attrs_dict["id"])
        if "href" in attrs_dict:
            self.hrefs.append(attrs_dict["href"])
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append(tag)


def luminance(hex_color: str) -> float:
    color = hex_color.lstrip("#")
    channels = [int(color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted([luminance(a), luminance(b)], reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> None:
    html = Path("public/index.html").read_text(encoding="utf-8")
    css = Path("public/styles.css").read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(html)
    internal_links = [href[1:] for href in parser.hrefs if href.startswith("#")]

    checks = {
        "html_lang_pt_BR": 'lang="pt-BR"' in html,
        "has_skip_link": "skip-link" in html,
        "has_main": "main" in parser.tags,
        "has_nav": "nav" in parser.tags,
        "has_search_label": 'for="guideSearch"' in html,
        "images_have_alt": all("alt" in attrs for tag, attrs in parser.attrs if tag == "img"),
        "no_iframes": "iframe" not in parser.tags,
        "has_focus_visible_styles": ":focus-visible" in css,
        "has_reduced_motion": "prefers-reduced-motion" in css,
        "has_responsive_layout": "@media (max-width: 56rem)" in css and "@media (max-width: 40rem)" in css,
        "no_viewport_scaled_fonts": "vw" not in css and "vmin" not in css and "vmax" not in css,
        "has_pdf_download_link": "cartilha-dignidade-e-cidadania-para-travestis-e-mulheres-trans-vf.pdf" in html,
        "content_pre_rendered": html.count('class="page-section"') == 109,
        "toc_pre_rendered": html.count("<li><a href=") >= 30,
        "ids_unique": len(parser.ids) == len(set(parser.ids)),
        "internal_links_valid": all(link in parser.ids for link in internal_links),
        "heading_hierarchy_starts_correctly": parser.headings[:3] == ["h1", "h2", "h2"],
    }
    contrast_checks = {
        "text_on_background": contrast("#1d1d1f", "#fbfaf7"),
        "accent_on_surface": contrast("#64162e", "#ffffff"),
        "muted_on_background": contrast("#55585f", "#fbfaf7"),
        "high_contrast_text": contrast("#ffffff", "#000000"),
    }

    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{name}: {passed}")
    for name, ratio in contrast_checks.items():
        print(f"{name}: {ratio:.2f}")
        if ratio < 4.5:
            failed.append(name)

    if failed:
        raise SystemExit("Failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
