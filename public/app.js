const state = {
  data: null,
  fontScale: Number(localStorage.getItem("fontScale") || "1"),
  highContrast: localStorage.getItem("highContrast") === "true",
};

const content = document.querySelector("#guideContent");
const toc = document.querySelector("#tableOfContents");
const search = document.querySelector("#guideSearch");
const searchStatus = document.querySelector("#searchStatus");
const contrastToggle = document.querySelector("#contrastToggle");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function highlight(value, query) {
  const safe = escapeHtml(value);
  if (!query) return safe;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return safe.replace(new RegExp(`(${escaped})`, "gi"), "<mark>$1</mark>");
}

function applyPreferences() {
  document.documentElement.style.setProperty("--font-scale", String(state.fontScale));
  document.body.classList.toggle("high-contrast", state.highContrast);
  contrastToggle.setAttribute("aria-pressed", String(state.highContrast));
  localStorage.setItem("fontScale", String(state.fontScale));
  localStorage.setItem("highContrast", String(state.highContrast));
}

function renderToc() {
  toc.innerHTML = state.data.nav
    .map((item) => `<li><a href="#${item.id}">${escapeHtml(item.title)}</a></li>`)
    .join("");
}

function renderPages(query = "") {
  const normalizedQuery = query.trim().toLocaleLowerCase("pt-BR");
  let count = 0;
  content.innerHTML = state.data.pages
    .map((page) => {
      const matches = !normalizedQuery || page.text.toLocaleLowerCase("pt-BR").includes(normalizedQuery);
      if (matches) count += 1;
      const paragraphs = page.paragraphs.length
        ? page.paragraphs.map((p) => `<p>${highlight(p, query)}</p>`).join("")
        : "<p>Esta página contém elementos gráficos ou créditos sem texto extraível.</p>";
      return `
        <article class="page-section" id="${page.id}" aria-labelledby="${page.id}-title" ${matches ? "" : "hidden"}>
          <p class="page-meta">Página ${page.page} de ${state.data.pageCount}</p>
          <h3 id="${page.id}-title">${escapeHtml(page.title)}</h3>
          ${paragraphs}
        </article>
      `;
    })
    .join("");

  if (normalizedQuery) {
    searchStatus.textContent = `${count} página${count === 1 ? "" : "s"} encontrada${count === 1 ? "" : "s"}.`;
  } else {
    searchStatus.textContent = `${state.data.pageCount} páginas carregadas.`;
  }
}

function bindControls() {
  contrastToggle.addEventListener("click", () => {
    state.highContrast = !state.highContrast;
    applyPreferences();
  });

  document.querySelector("#fontIncrease").addEventListener("click", () => {
    state.fontScale = Math.min(1.4, Math.round((state.fontScale + 0.1) * 10) / 10);
    applyPreferences();
  });

  document.querySelector("#fontDecrease").addEventListener("click", () => {
    state.fontScale = Math.max(0.9, Math.round((state.fontScale - 0.1) * 10) / 10);
    applyPreferences();
  });

  document.querySelector("#resetPrefs").addEventListener("click", () => {
    state.fontScale = 1;
    state.highContrast = false;
    applyPreferences();
  });

  document.querySelector("#clearSearch").addEventListener("click", () => {
    search.value = "";
    renderPages("");
    search.focus();
  });

  search.addEventListener("input", (event) => {
    renderPages(event.target.value);
  });

  document.querySelector("#toTop").addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

async function init() {
  applyPreferences();
  bindControls();
  const response = await fetch("guide.json");
  state.data = await response.json();
  renderToc();
  renderPages();
}

init().catch(() => {
  content.innerHTML = "<p>Não foi possível carregar o conteúdo do guia.</p>";
  searchStatus.textContent = "Erro ao carregar conteúdo.";
});
