import { clearSession, getLibrarian, getToken } from "./api.js";

function applyTheme(theme) {
  const t = theme === "dark" ? "dark" : "light";
  document.documentElement.setAttribute("data-bs-theme", t);
  localStorage.setItem("theme", t);
}

export function initTheme() {
  const saved = localStorage.getItem("theme");
  applyTheme(saved || "light");
}

export function requireAuth() {
  if (!getToken()) {
    window.location.href = "login.html";
    return false;
  }
  return true;
}

export function renderNav(active) {
  initTheme();
  const user = getLibrarian();
  const role = user?.role || "";
  const isAdmin = role === "admin";

  const links = [
    ["dashboard.html", "Dashboard", "dashboard"],
    ["readers.html", "Readers", "readers"],
    ["books.html", "Books", "books"],
    ["borrows.html", "Borrow/Return", "borrows"],
    ["reports.html", "Reports", "reports"],
  ];
  if (isAdmin) links.push(["admin.html", "Admin", "admin"]);

  const nav = document.getElementById("app-nav");
  if (!nav) return;

  nav.innerHTML = `
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="dashboard.html">Uni Library</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          ${links
            .map(([href, label, key]) => {
              const cls = key === active ? "nav-link active" : "nav-link";
              return `<li class="nav-item"><a class="${cls}" href="${href}">${label}</a></li>`;
            })
            .join("")}
        </ul>
        <div class="d-flex align-items-center text-white">
          <button class="btn btn-outline-light btn-sm me-2" id="themeBtn" title="Toggle theme">
            <i class="bi bi-moon-stars"></i>
          </button>
          <span class="me-3 small">${user ? `${user.name} (${user.username}) - ${user.role}` : ""}</span>
          <button class="btn btn-outline-light btn-sm" id="logoutBtn">Logout</button>
        </div>
      </div>
    </div>
  </nav>`;

  const btn = document.getElementById("logoutBtn");
  if (btn) {
    btn.addEventListener("click", () => {
      clearSession();
      window.location.href = "login.html";
    });
  }

  const themeBtn = document.getElementById("themeBtn");
  if (themeBtn) {
    const icon = themeBtn.querySelector("i");
    const syncIcon = () => {
      const t = document.documentElement.getAttribute("data-bs-theme") || "light";
      icon.className = t === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    };
    syncIcon();
    themeBtn.addEventListener("click", () => {
      const cur = document.documentElement.getAttribute("data-bs-theme") || "light";
      applyTheme(cur === "dark" ? "light" : "dark");
      syncIcon();
    });
  }
}

export function showError(el, message) {
  el.innerHTML = `<div class="alert alert-danger d-flex align-items-start gap-2" role="alert">
    <i class="bi bi-exclamation-triangle-fill mt-1"></i>
    <div>
      <div class="fw-semibold">Error</div>
      <div class="small">${escapeHtml(message)}</div>
    </div>
  </div>`;
}

export function showSuccess(el, message) {
  el.innerHTML = `<div class="alert alert-success d-flex align-items-start gap-2" role="alert">
    <i class="bi bi-check-circle-fill mt-1"></i>
    <div>
      <div class="fw-semibold">Success</div>
      <div class="small">${escapeHtml(message)}</div>
    </div>
  </div>`;
}

export function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
