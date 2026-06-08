from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "public" / "guide.json"
OUT = ROOT / "public" / "index.html"
PDF_URL = "https://www.gov.br/mulheres/pt-br/central-de-conteudos/publicacoes/cartilha-dignidade-e-cidadania-para-travestis-e-mulheres-trans-vf.pdf"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_toc(nav: list[dict[str, object]]) -> str:
    return "\n".join(
        f'            <li><a href="#{esc(str(item["id"]))}">{esc(str(item["title"]))}</a></li>'
        for item in nav
    )


def render_pages(pages: list[dict[str, object]], page_count: int) -> str:
    articles = []
    for page in pages:
        page_id = esc(str(page["id"]))
        title = esc(str(page["title"]))
        page_number = int(page["page"])
        paragraphs = page.get("paragraphs") or []
        if paragraphs:
            body = "\n".join(f"          <p>{esc(str(paragraph))}</p>" for paragraph in paragraphs)
        else:
            body = "          <p>Esta página contém elementos gráficos ou créditos sem texto extraível.</p>"
        articles.append(
            f"""        <article class="page-section" id="{page_id}" aria-labelledby="{page_id}-title">
          <p class="page-meta">Página {page_number} de {page_count}</p>
          <h3 id="{page_id}-title">{title}</h3>
{body}
        </article>"""
        )
    return "\n".join(articles)


def main() -> None:
    data = json.loads(GUIDE.read_text(encoding="utf-8"))
    toc = render_toc(data["nav"])
    pages = render_pages(data["pages"], int(data["pageCount"]))
    page_count = int(data["pageCount"])

    OUT.write_text(
        f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark">
    <meta
      name="description"
      content="Versão HTML acessível do guia Todas as Mulheres: Dignidade, Cidadania e Direitos Humanos para Travestis e Mulheres Trans."
    >
    <title>Todas as Mulheres | Guia acessível</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <a class="skip-link" href="#conteudo">Pular para o conteúdo principal</a>

    <header class="site-header" role="banner">
      <div class="header-inner">
        <p class="eyebrow">Guia acessível</p>
        <h1>Todas as Mulheres</h1>
        <p class="lead">
          Dignidade, cidadania e direitos humanos para travestis e mulheres trans.
        </p>
        <div class="header-actions" aria-label="Ações principais">
          <a class="button primary" href="#conteudo">Ler guia em HTML</a>
          <a class="button" href="{PDF_URL}">Baixar PDF original</a>
        </div>
      </div>
    </header>

    <nav class="utility-bar" aria-label="Controles de acessibilidade">
      <button class="control" type="button" id="contrastToggle" aria-pressed="false">
        Alto contraste
      </button>
      <button class="control" type="button" id="fontDecrease" aria-label="Diminuir tamanho do texto">
        A-
      </button>
      <button class="control" type="button" id="fontIncrease" aria-label="Aumentar tamanho do texto">
        A+
      </button>
      <button class="control" type="button" id="resetPrefs">Restaurar</button>
    </nav>

    <div class="layout">
      <aside class="sidebar" aria-label="Sumário do guia">
        <div class="sidebar-panel">
          <h2>Sumário</h2>
          <ol id="tableOfContents" class="toc">
{toc}
          </ol>
        </div>
      </aside>

      <main id="conteudo" tabindex="-1">
        <section class="notice" aria-labelledby="a11y-title">
          <h2 id="a11y-title">Conteúdo em formato acessível</h2>
          <p>
            Esta página transforma o PDF em texto HTML navegável, pesquisável e compatível
            com teclado e leitores de tela. O PDF original permanece disponível como
            documento secundário.
          </p>
        </section>

        <section class="search-section" aria-labelledby="search-title">
          <h2 id="search-title">Buscar no guia</h2>
          <label for="guideSearch">Digite uma palavra ou expressão</label>
          <div class="search-row">
            <input id="guideSearch" name="guideSearch" type="search" autocomplete="off">
            <button class="button" type="button" id="clearSearch">Limpar</button>
          </div>
          <p id="searchStatus" class="status" role="status" aria-live="polite">
            {page_count} páginas carregadas.
          </p>
        </section>

        <section aria-labelledby="guide-title">
          <h2 id="guide-title">Guia completo</h2>
          <div id="guideContent" class="guide-content">
{pages}
          </div>
        </section>
      </main>
    </div>

    <button class="to-top" type="button" id="toTop">Voltar ao topo</button>

    <footer class="site-footer">
      <p>
        Versão web acessível gerada a partir do documento original. Meta de acessibilidade:
        WCAG 2.2 AA.
      </p>
    </footer>

    <script src="app.js" defer></script>
  </body>
</html>
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
