// auth.js — Frontend authentication helper
// Include this in any page that needs login/signup/logout
// Usage: <script src="../js/auth.js"></script>

const Auth = {

  getToken() { return localStorage.getItem('riq-token'); },

  getUser() {
    const raw = localStorage.getItem('riq-user');
    try { return raw ? JSON.parse(raw) : null; } catch { return null; }
  },

  isLoggedIn() { return !!this.getToken(); },

  _save(token, user) {
    localStorage.setItem('riq-token', token);
    localStorage.setItem('riq-user', JSON.stringify(user));
  },

  _clear() {
    localStorage.removeItem('riq-token');
    localStorage.removeItem('riq-user');
  },

  authHeaders() {
    const token = this.getToken();
    return token
      ? { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
      : { 'Content-Type': 'application/json' };
  },

  async signup(name, email, phone, password, confirmPassword) {
    const res = await fetch(`${API}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, password, confirm_password: confirmPassword })
    });
    return await res.json();
  },

  async login(identifier, password) {
    const res = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password })
    });
    const data = await res.json();
    if (data.success && data.data?.token) {
      this._save(data.data.token, { name: data.data.name, email: data.data.email });
    }
    return data;
  },

  async logout() {
    const token = this.getToken();
    if (token) {
      try {
        await fetch(`${API}/logout`, { method: 'POST', headers: this.authHeaders() });
      } catch {}
    }
    this._clear();
    window.location.href = 'login.html';
  },

  async getProfile() {
    if (!this.isLoggedIn()) return null;
    const res = await fetch(`${API}/profile`, { headers: this.authHeaders() });
    const data = await res.json();
    return data.success ? data.data : null;
  },

  async updateProfile(updates) {
    const res = await fetch(`${API}/profile`, {
      method: 'PUT',
      headers: this.authHeaders(),
      body: JSON.stringify(updates)
    });
    return await res.json();
  },

  async resetPassword(email, newPassword, confirmPassword) {
    const res = await fetch(`${API}/forgot-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, new_password: newPassword, confirm_password: confirmPassword })
    });
    return await res.json();
  },

  requireLogin(redirectTo = 'login.html') {
    if (!this.isLoggedIn()) { window.location.href = redirectTo; return false; }
    return true;
  },

  checkPasswordStrength(password) {
    const checks = {
      length:  password.length >= 8,
      upper:   /[A-Z]/.test(password),
      lower:   /[a-z]/.test(password),
      number:  /[0-9]/.test(password),
      special: /[!@#$%^&*()_+\-=\[\]{}|;':",./<>?]/.test(password)
    };
    return { score: Object.values(checks).filter(Boolean).length, checks };
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const user      = Auth.getUser();
  const avatarEl  = document.getElementById('navatar');
  const loginBtn  = document.getElementById('navLoginBtn');
  const logoutBtn = document.getElementById('navLogoutBtn');

  if (user) {
    const initials = user.name
      ? user.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) : '?';
    if (avatarEl)  avatarEl.textContent     = initials;
    if (loginBtn)  loginBtn.style.display   = 'none';
    if (logoutBtn) logoutBtn.style.display  = 'inline-flex';
  } else {
    if (loginBtn)  loginBtn.style.display   = 'inline-flex';
    if (logoutBtn) logoutBtn.style.display  = 'none';
  }
  if (logoutBtn) logoutBtn.addEventListener('click', () => Auth.logout());
});
