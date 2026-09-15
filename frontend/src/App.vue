<template>
  <div class="min-h-screen flex flex-col bg-dark-900 text-slate-100">
    <!-- En-tête Principal Navigation Responsive -->
    <header class="sticky top-0 z-50 bg-dark-800/95 backdrop-blur-md border-b border-dark-600">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo & Marque -->
          <div class="flex items-center gap-6">
            <router-link to="/" class="flex items-center gap-3 group">
              <span class="text-2xl p-2 bg-btp-500/10 border border-btp-500/30 rounded-xl group-hover:scale-105 transition-transform">
                🏗️
              </span>
              <div class="flex flex-col">
                <span class="text-lg font-extrabold tracking-wide bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                  BTP MANAGER
                </span>
                <span class="text-[10px] text-slate-400 font-medium tracking-wider uppercase">
                  ERP BTP & Génie Civil
                </span>
              </div>
            </router-link>

            <!-- Navigation Desktop -->
            <nav v-if="authStore.isAuthenticated" class="hidden md:flex items-center gap-1 ml-4">
              <router-link 
                v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)" 
                to="/superadmin/users" 
                class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
                :class="$route.path === '/superadmin/users' ? 'bg-btp-500/15 text-btp-400 border border-btp-500/40' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
              >
                👑 Utilisateurs
              </router-link>
              <router-link 
                v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)" 
                to="/owner" 
                class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
                :class="$route.path === '/owner' ? 'bg-btp-500/15 text-btp-400 border border-btp-500/40' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
              >
                🏢 Owner
              </router-link>
              <router-link 
                v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR'].includes(authStore.userRole)" 
                to="/director" 
                class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
                :class="$route.path === '/director' ? 'bg-btp-500/15 text-btp-400 border border-btp-500/40' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
              >
                📐 Director
              </router-link>
              <router-link 
                v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR', 'MANAGER'].includes(authStore.userRole)" 
                to="/manager" 
                class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
                :class="$route.path === '/manager' ? 'bg-btp-500/15 text-btp-400 border border-btp-500/40' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
              >
                📋 Manager
              </router-link>
              <router-link 
                v-if="authStore.isAuthenticated" 
                to="/worker" 
                class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
                :class="$route.path === '/worker' ? 'bg-btp-500/15 text-btp-400 border border-btp-500/40' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
              >
                👷 Worker
              </router-link>
            </nav>
          </div>

          <!-- Section Profil & Actions Desktop -->
          <div class="hidden md:flex items-center gap-4">
            <template v-if="authStore.isAuthenticated">
              <div class="flex items-center gap-3 bg-dark-900/60 border border-dark-600 px-3 py-1.5 rounded-full">
                <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-btp-600 to-btp-400 text-slate-950 font-bold flex items-center justify-center text-sm shadow-md shadow-btp-500/20">
                  {{ authStore.user?.first_name?.charAt(0) || 'U' }}
                </div>
                <div class="flex flex-col text-left">
                  <span class="text-xs font-semibold text-white leading-tight">{{ authStore.userName }}</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider" :class="getRoleColor(authStore.userRole)">
                    {{ authStore.userRole }}
                  </span>
                </div>
              </div>
              <button 
                @click="handleLogout"
                class="px-3 py-1.5 rounded-lg border border-dark-600 text-slate-400 hover:text-red-400 hover:border-red-500/50 hover:bg-red-500/10 text-xs font-medium transition-all flex items-center gap-1.5"
                title="Se déconnecter"
              >
                <span>Déconnexion</span>
                <span>🚪</span>
              </button>
            </template>
            <template v-else>
              <router-link 
                to="/login"
                class="px-4 py-2 rounded-lg bg-gradient-to-r from-btp-500 to-btp-600 text-slate-950 font-bold text-sm hover:from-btp-400 hover:to-btp-500 shadow-md shadow-btp-500/20 transition-all"
              >
                Se connecter
              </router-link>
            </template>
          </div>

          <!-- Bouton Menu Mobile (Hamburger) -->
          <div class="flex md:hidden items-center gap-2">
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-dark-700 border border-dark-600 transition-colors"
              aria-label="Toggle menu"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Menu Déroulant Mobile -->
      <div v-if="mobileMenuOpen" class="md:hidden border-b border-dark-600 bg-dark-800 px-4 pt-2 pb-4 space-y-2">
        <template v-if="authStore.isAuthenticated">
          <div class="flex items-center gap-3 p-3 bg-dark-900 rounded-xl border border-dark-600 mb-3">
            <div class="w-10 h-10 rounded-full bg-btp-500 text-slate-950 font-bold flex items-center justify-center">
              {{ authStore.user?.first_name?.charAt(0) || 'U' }}
            </div>
            <div>
              <div class="text-sm font-bold text-white">{{ authStore.userName }}</div>
              <div class="text-xs font-semibold" :class="getRoleColor(authStore.userRole)">{{ authStore.userRole }}</div>
            </div>
          </div>

          <div class="flex flex-col space-y-1">
            <router-link 
              v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)"
              to="/superadmin/users" 
              @click="mobileMenuOpen = false"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-200 hover:bg-dark-700"
            >
              👑 Gestion Utilisateurs
            </router-link>
            <router-link 
              v-if="['SUPER_ADMIN', 'OWNER'].includes(authStore.userRole)"
              to="/owner" 
              @click="mobileMenuOpen = false"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-200 hover:bg-dark-700"
            >
              🏢 Espace Owner
            </router-link>
            <router-link 
              v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR'].includes(authStore.userRole)"
              to="/director" 
              @click="mobileMenuOpen = false"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-200 hover:bg-dark-700"
            >
              📐 Espace Director
            </router-link>
            <router-link 
              v-if="['SUPER_ADMIN', 'OWNER', 'DIRECTOR', 'MANAGER'].includes(authStore.userRole)"
              to="/manager" 
              @click="mobileMenuOpen = false"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-200 hover:bg-dark-700"
            >
              📋 Espace Manager
            </router-link>
            <router-link 
              to="/worker" 
              @click="mobileMenuOpen = false"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-200 hover:bg-dark-700"
            >
              👷 Espace Worker
            </router-link>
          </div>

          <div class="pt-3 border-t border-dark-700">
            <button 
              @click="handleLogout(); mobileMenuOpen = false"
              class="w-full text-left px-3 py-2 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10 flex items-center justify-between"
            >
              <span>Se déconnecter</span>
              <span>🚪</span>
            </button>
          </div>
        </template>
        <template v-else>
          <router-link 
            to="/login"
            @click="mobileMenuOpen = false"
            class="block text-center py-2.5 rounded-lg bg-btp-500 text-slate-950 font-bold text-sm"
          >
            Se connecter
          </router-link>
        </template>
      </div>
    </header>

    <!-- Zone de Contenu Principal -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <router-view />
    </main>

    <!-- Pied de Page Responsive -->
    <footer class="border-t border-dark-600 bg-dark-900/60 py-4 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-2">
        <span>BTP MANAGER © 2026 — Système ERP BTP & Travaux Publics</span>
        <span class="flex items-center gap-1.5">
          <span class="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>
          Tailwind CSS v3 • Vue 3 • FastAPI • PostgreSQL
        </span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

function getRoleColor(role) {
  switch (role) {
    case 'SUPER_ADMIN': return 'text-red-400'
    case 'OWNER': return 'text-amber-400'
    case 'DIRECTOR': return 'text-purple-400'
    case 'MANAGER': return 'text-blue-400'
    case 'WORKER': return 'text-emerald-400'
    default: return 'text-slate-400'
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
