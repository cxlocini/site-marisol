from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = Path(r"C:\Users\rafac\OneDrive\Documentos\document.pdf")
OUT = ROOT / "public" / "guide.json"


SECTION_PAGES = {
    1: "Créditos e apresentação",
    3: "Resumo",
    4: "Saudações da ANTRA",
    5: "Palavras da SENATP",
    6: "Sobre a ANTRA",
    7: "Sobre a SENATP",
    8: "Sobre a campanha Livres & Iguais",
    9: "Os direitos da mulher são direitos humanos",
    11: "Sobre este guia",
    12: "Sumário",
    13: "1. Introdução",
    16: "2. Direitos humanos e cidadania",
    17: "2.1. Proteção contra discriminação",
    31: "2.2. Medidas especiais temporárias",
    33: "2.3. Autodeterminação de gênero",
    37: "2.4. Retificação de nome e gênero",
    39: "2.5. Nome social",
    45: "2.6. Participação política e vida pública",
    51: "2.7. Proteção contra violência e acesso à justiça",
    57: "2.8. Proteção contra tortura e tratamentos cruéis",
    61: "2.9. Direitos das meninas trans",
    64: "2.10. Direito à saúde",
    68: "2.11. Autonomia econômica, trabalho decente e justiça climática",
    74: "2.12. Direito à educação",
    76: "2.13. Direito à moradia",
    78: "2.14. Direito de defender direitos humanos",
    83: "3. Todo mundo começa em algum lugar",
    101: "Glossário",
    103: "4. Conclusão",
    104: "5. Recomendações",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "secao"


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?- ?\n ?", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("Comisssariado", "Comissariado")
    text = text.replace("Humafios", "Humanos")
    text = text.replace("Vice-President e", "Vice-Presidente")
    text = text.replace("Márci a", "Márcia")
    text = text.replace("Coordenador a", "Coordenadora")
    return text.strip()


def paragraphs(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    blocks: list[str] = []
    current: list[str] = []
    for line in lines:
        if not line:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            continue
        if re.match(r"^(\.|-|•)?\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ][^.!?]{0,90}:$", line) and current:
            blocks.append(" ".join(current).strip())
            current = [line]
            continue
        current.append(line)
    if current:
        blocks.append(" ".join(current).strip())
    return [re.sub(r"\s+", " ", block).strip() for block in blocks if block.strip()]


def main() -> None:
    reader = PdfReader(str(PDF_PATH))
    pages = []
    nav = []
    current_section = None

    for index, page in enumerate(reader.pages, start=1):
        raw = clean_text(page.extract_text() or "")
        title = SECTION_PAGES.get(index)
        if title:
            current_section = {"page": index, "title": title, "id": slugify(title)}
            nav.append(current_section)
        pages.append(
            {
                "page": index,
                "sectionId": current_section["id"] if current_section else f"pagina-{index}",
                "title": title or f"Página {index}",
                "id": slugify(title or f"pagina-{index}"),
                "paragraphs": paragraphs(raw),
                "text": raw,
            }
        )

    data = {
        "title": "Todas as Mulheres: Dignidade, Cidadania e Direitos Humanos para Travestis e Mulheres Trans",
        "source": "Guia do Ministério das Mulheres e da Associação Nacional de Travestis e Transexuais (ANTRA), 2025.",
        "accessibilityTarget": "WCAG 2.2 AA",
        "pageCount": len(pages),
        "nav": nav,
        "pages": pages,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
