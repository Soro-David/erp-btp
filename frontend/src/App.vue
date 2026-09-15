<template>
  <div class="app-shell">
    <!-- En-tête Principal -->
    <header class="navbar">
      <div class="navbar-left">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🏗️</span>
          <div class="brand-meta">
            <span class="brand-name">BTP MANAGER</span>
            <span class="brand-tagline">ERP BTP & Génie Civil</span>
          </div>
        </router-link>

        <!-- Liens de navigation selon le rôle connecté -->
        <nav v-if="authStore.isAuthenticated" class="nav-links">
          <router-link 
            v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)" 
            to="/superadmin/users" 
            class="nav-item"
          >
            👑 Utilisateurs
          </router-link>
          <router-link 
            v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)" 
            to="/owner" 
            class="nav-item"
          >
            🏢 Espace Owner
          </router-link>
          <router-link 
            v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR'].includes(authStore.userRole)" 
            to="/director" 
            class="nav-item"
          >
            📐 Espace Director
          </router-link>
          <router-link 
            v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR', 'MANAGER'].includes(authStore.userRole)" 
            to="/manager" 
            class="nav-item"
          >
            📋 Espace Manager
          </router-link>
          <router-link 
            v-if="authStore.isAuthenticated" 
            to="/worker" 
            class="nav-item"
          >
            👷 Espace Worker
          </router-link>
        </nav>
      </div>

      <!-- Espace utilisateur / Déconnexion -->
      <div class="navbar-right">
        <template v-if="authStore.isAuthenticated">
          <div class="user-pill">
            <div class="avatar-circle">
              {{ authStore.user?.first_name?.charAt(0) || 'U' }}
            </div>
            <div class="user-meta">
              <span class="user-name">{{ authStore.userName }}</span>
              <span class="role-tag" :class="'role-' + authStore.userRole?.toLowerCase()">
                {{ authStore.userRole }}
              </span>
            </div>
          </div>
          <button class="btn-logout" title="Se déconnecter" @click="handleLogout">
            <span>Déconnexion</span>
            <span>🚪</span>
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn-login-nav">
            Se connecter
          </router-link>
        </template>
      </div>
    </header>

    <!-- Vue active -->
    <main class="main-wrapper">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(19, 27, 46, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.brand-icon {
  font-size: 1.8rem;
  padding: 0.4rem;
  background: rgba(245, 158, 11, 0.12);
  border-radius: 10px;
  border: 1px solid var(--accent-btp-glow);
}

.brand-meta {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-tagline {
  font-size: 0.72rem;
  color: var(--text-secondary);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.nav-item {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.nav-item:hover, .nav-item.router-link-active {
  color: #fff;
  background: rgba(255, 255, 255, 0.07);
}

.nav-item.router-link-active {
  color: var(--accent-btp);
  border: 1px solid var(--accent-btp-glow);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(11, 15, 23, 0.6);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.85rem 0.35rem 0.4rem;
  border-radius: 9999px;
}

.avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-btp) 0%, #d97706 100%);
  color: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #fff;
}

.role-tag {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
}

.role-super_admin { color: #f87171; }
.role-owner { color: #fbbf24; }
.role-director { color: #c084fc; }
.role-manager { color: #60a5fa; }
.role-worker { color: #34d399; }

.btn-logout {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.45rem 0.85rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  transition: all 0.15s ease;
}

.btn-logout:hover {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.btn-login-nav {
  background: linear-gradient(135deg, var(--accent-btp) 0%, #d97706 100%);
  color: #0f172a;
  text-decoration: none;
  font-weight: 700;
  padding: 0.5rem 1.1rem;
  border-radius: 8px;
  font-size: 0.85rem;
}

.main-wrapper {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

@media (max-width: 900px) {
  .navbar { flex-direction: column; gap: 1rem; align-items: flex-start; }
  .navbar-left { flex-direction: column; align-items: flex-start; gap: 0.8rem; }
  .nav-links { flex-wrap: wrap; }
}
</style>
