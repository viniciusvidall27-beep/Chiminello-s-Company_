/* ══════════════════════════════════════════════════════════════
   Chiminello — main.js
   Helpers globais: Toast, API, Nav
   ══════════════════════════════════════════════════════════════ */

// ── Toast ──────────────────────────────────────────────────────
window.toast = function(msg, tipo = 'ok', ms = 3000) {
  let el = document.getElementById('toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.className = `show t-${tipo}`;
  clearTimeout(el._timer);
  el._timer = setTimeout(() => el.className = '', ms);
};

// ── API helper ─────────────────────────────────────────────────
window.api = async function(url, opts = {}) {
  try {
    const res = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...opts.headers },
      credentials: 'include',
      ...opts,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.erro || `HTTP ${res.status}`);
    return data;
  } catch (err) {
    console.error('[API]', url, err);
    throw err;
  }
};

// ── Navegação pública ──────────────────────────────────────────
window.navTo = function(rota) {
  window.location.href = rota;
};

// ── Admin logout ───────────────────────────────────────────────
window.logout = async function() {
  await api('/api/auth/logout', { method: 'POST' }).catch(() => {});
  window.location.href = '/admin/login';
};

// ── Formatar data ──────────────────────────────────────────────
window.fmtDate = function(s) {
  if (!s) return '—';
  return s;
};
