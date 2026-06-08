const state = {
  fontScale: Number(localStorage.getItem("fontScale") || "1"),
  highContrast: localStorage.getItem("highContrast") === "true",
};

const pages = Array.from(document.querySelectorAll(".page-section"));
const search = document.querySelector("#guideSearch");
const searchStatus = document.querySelector("#searchStatus");
const contrastToggle = document.querySelector("#contrastToggle");

function applyPreferences() {
  document.documentElement.style.setProperty("--font-scale", String(state.fontScale));
  document.body.classList.toggle("high-contrast", state.highContrast);
  contrastToggle.setAttribute("aria-pressed", String(state.highContrast));
  localStorage.setItem("fontScale", String(state.fontScale));
  localStorage.setItem("highContrast", String(state.highContrast));
}

function filterPages(query = "") {
  const normalizedQuery = query.trim().toLocaleLowerCase("pt-BR");
  let count = 0;

  pages.forEach((page) => {
    const matches = !normalizedQuery || page.textContent.toLocaleLowerCase("pt-BR").includes(normalizedQuery);
    page.hidden = !matches;
    if (matches) count += 1;
  });

  if (normalizedQuery) {
    searchStatus.textContent = `${count} página${count === 1 ? "" : "s"} encontrada${count === 1 ? "" : "s"}.`;
  } else {
    searchStatus.textContent = `${pages.length} páginas carregadas.`;
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
    filterPages("");
    search.focus();
  });

  search.addEventListener("input", (event) => {
    filterPages(event.target.value);
  });

  document.querySelector("#toTop").addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

applyPreferences();
bindControls();
filterPages(search.value);
