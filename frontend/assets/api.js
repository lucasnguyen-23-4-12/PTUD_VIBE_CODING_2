const API_BASE = "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("access_token");
}

export function setSession({ access_token, librarian }) {
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("librarian", JSON.stringify(librarian));
}

export function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("librarian");
}

export function getLibrarian() {
  const raw = localStorage.getItem("librarian");
  return raw ? JSON.parse(raw) : null;
}

export async function apiFetch(path, { method = "GET", body, headers = {} } = {}) {
  const token = getToken();
  const finalHeaders = { ...headers };

  if (token) finalHeaders["Authorization"] = `Bearer ${token}`;
  if (body && !(body instanceof FormData)) finalHeaders["Content-Type"] = "application/json";

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: finalHeaders,
    body: body ? (body instanceof FormData ? body : JSON.stringify(body)) : undefined,
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const data = await res.json();
      detail = data.detail || JSON.stringify(data);
    } catch (_) {}
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

