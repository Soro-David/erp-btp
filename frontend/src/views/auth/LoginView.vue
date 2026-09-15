<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-12rem)] py-6 sm:py-12">
    <div class="w-full max-w-md bg-dark-800 border border-dark-600 rounded-2xl p-6 sm:p-8 shadow-2xl shadow-black/60 relative overflow-hidden">
      <!-- Lueur décorative BTP -->
      <div class="absolute -top-24 -right-24 w-48 h-48 bg-btp-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- En-tête -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-btp-500/10 border border-btp-500/30 text-btp-400 text-xs font-bold mb-3">
          <span>🏗️</span>
          <span>BTP MANAGER</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">Connexion ERP</h2>
        <p class="text-slate-400 text-sm mt-1">Accédez à votre espace selon votre profil d'habilitation</p>
      </div>

      <!-- Message d'alerte d'erreur -->
      <div v-if="authStore.error" class="mb-5 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs sm:text-sm flex items-start gap-2">
        <span class="text-base">⚠️</span>
        <span>{{ authStore.error }}</span>
      </div>

      <!-- Formulaire de connexion -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Adresse Email
          </label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            required 
            placeholder="admin@gmail.com"
            class="w-full px-4 py-2.5 rounded-xl bg-dark-900/80 border border-dark-600 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-btp-500 focus:ring-1 focus:ring-btp-500 transition-all"
          />
        </div>

        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label for="password" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
              Mot de passe
            </label>
          </div>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            required 
            placeholder="••••••••"
            class="w-full px-4 py-2.5 rounded-xl bg-dark-900/80 border border-dark-600 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-btp-500 focus:ring-1 focus:ring-btp-500 transition-all"
          />
        </div>

        <button 
          type="submit" 
          :disabled="authStore.loading"
          class="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-btp-500 to-btp-600 hover:from-btp-400 hover:to-btp-500 text-slate-950 font-bold text-sm sm:text-base shadow-lg shadow-btp-500/25 transition-all transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <span v-if="authStore.loading" class="animate-spin text-lg">⏳</span>
          <span>{{ authStore.loading ? 'Authentification...' : 'Se connecter' }}</span>
          <span v-if="!authStore.loading">➔</span>
        </button>
      </form>

      <!-- Raccourcis de test prédéfinis -->
      <div class="mt-6 pt-5 border-t border-dark-600">
        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2.5">
          Comptes de test (cliquez pour remplir) :
        </div>
        <div class="flex flex-wrap gap-1.5">
          <button 
            type="button" 
            @click="fillCreds('admin@gmail.com', 'Password@1234')"
            class="px-2.5 py-1 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-xs font-medium hover:bg-red-500/20 transition-all"
          >
            👑 SuperAdmin
          </button>
          <button 
            type="button" 
            @click="fillCreds('owner@btp.ci', 'Password@1234')"
            class="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-medium hover:bg-amber-500/20 transition-all"
          >
            🏢 Owner
          </button>
          <button 
            type="button" 
            @click="fillCreds('director@btp.ci', 'Password@1234')"
            class="px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-medium hover:bg-purple-500/20 transition-all"
          >
            📐 Director
          </button>
          <button 
            type="button" 
            @click="fillCreds('manager@btp.ci', 'Password@1234')"
            class="px-2.5 py-1 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-medium hover:bg-blue-500/20 transition-all"
          >
            📋 Manager
          </button>
          <button 
            type="button" 
            @click="fillCreds('worker@btp.ci', 'Password@1234')"
            class="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium hover:bg-emerald-500/20 transition-all"
          >
            👷 Worker
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('admin@gmail.com')
const password = ref('Password@1234')

function fillCreds(e, p) {
  email.value = e
  password.value = p
}

async function handleLogin() {
  try {
    await authStore.login(email.value, password.value)
    const role = authStore.userRole
    if (role === 'SUPER_ADMIN') router.push('/superadmin/users')
    else if (role === 'OWNER') router.push('/owner')
    else if (role === 'DIRECTOR') router.push('/director')
    else if (role === 'MANAGER') router.push('/manager')
    else if (role === 'WORKER') router.push('/worker')
    else router.push('/')
  } catch (err) {
    // Erreur affichée via store
  }
}
</script>
