<template>
  <div class="space-y-6">
    <!-- En-tête de la vue -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-dark-800/80 p-5 rounded-2xl border border-dark-600">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-bold mb-1">
          <span>👑</span>
          <span>ADMINISTRATION CENTRALE</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Gestion des Utilisateurs & Rôles</h2>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Créez et configurez les accès des profils Owner, Director, Manager et Worker</p>
      </div>
      <button 
        @click="showModal = true"
        class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-gradient-to-r from-btp-500 to-btp-600 hover:from-btp-400 hover:to-btp-500 text-slate-950 font-bold text-sm shadow-md shadow-btp-500/20 flex items-center justify-center gap-2 transition-all"
      >
        <span>➕</span>
        <span>Nouvel Utilisateur</span>
      </button>
    </div>

    <!-- Barre d'indicateurs KPI Responsive -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-white">{{ users.length }}</span>
        <span class="text-xs text-slate-400">Total Utilisateurs</span>
      </div>
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-emerald-400">{{ users.filter(u => u.is_active).length }}</span>
        <span class="text-xs text-slate-400">Comptes Actifs</span>
      </div>
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-amber-400">{{ users.filter(u => u.role === 'OWNER').length }}</span>
        <span class="text-xs text-slate-400">Owners</span>
      </div>
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-purple-400">{{ users.filter(u => u.role === 'DIRECTOR').length }}</span>
        <span class="text-xs text-slate-400">Directors</span>
      </div>
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-blue-400">{{ users.filter(u => u.role === 'MANAGER').length }}</span>
        <span class="text-xs text-slate-400">Managers</span>
      </div>
      <div class="bg-dark-800 border border-dark-600 rounded-xl p-3.5 flex flex-col">
        <span class="text-2xl font-black text-emerald-400">{{ users.filter(u => u.role === 'WORKER').length }}</span>
        <span class="text-xs text-slate-400">Workers</span>
      </div>
    </div>

    <!-- Tableau Responsive des Utilisateurs -->
    <div class="bg-dark-800 border border-dark-600 rounded-2xl overflow-hidden shadow-xl">
      <div v-if="loading" class="p-8 text-center text-slate-400 text-sm">
        Chargement des données en cours...
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm whitespace-nowrap">
          <thead class="bg-dark-900/80 border-b border-dark-600 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <tr>
              <th class="px-5 py-3.5">ID</th>
              <th class="px-5 py-3.5">Nom & Prénom</th>
              <th class="px-5 py-3.5">Email</th>
              <th class="px-5 py-3.5">Téléphone</th>
              <th class="px-5 py-3.5">Rôle</th>
              <th class="px-5 py-3.5">Statut</th>
              <th class="px-5 py-3.5">Date Création</th>
              <th class="px-5 py-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-600/50">
            <tr v-for="user in users" :key="user.id" class="hover:bg-slate-800/40 transition-colors">
              <td class="px-5 py-3.5 text-slate-400">#{{ user.id }}</td>
              <td class="px-5 py-3.5 font-bold text-white">{{ user.first_name }} {{ user.last_name }}</td>
              <td class="px-5 py-3.5 font-mono text-cyan-400 text-xs">{{ user.email }}</td>
              <td class="px-5 py-3.5 text-slate-300">{{ user.phone || '—' }}</td>
              <td class="px-5 py-3.5">
                <span class="inline-block px-2.5 py-1 rounded-md text-xs font-bold" :class="getRoleBadgeClass(user.role)">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-5 py-3.5">
                <span 
                  class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="user.is_active ? 'bg-emerald-500/15 text-emerald-300' : 'bg-red-500/15 text-red-300'"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="user.is_active ? 'bg-emerald-400' : 'bg-red-400'"></span>
                  {{ user.is_active ? 'Actif' : 'Désactivé' }}
                </span>
              </td>
              <td class="px-5 py-3.5 text-slate-400 text-xs">{{ formatDate(user.created_at) }}</td>
              <td class="px-5 py-3.5 text-right">
                <button 
                  @click="deleteUser(user.id)"
                  :disabled="user.role === 'SUPER_ADMIN'"
                  class="p-1.5 rounded-lg border border-dark-600 text-slate-400 hover:text-red-400 hover:border-red-500/50 hover:bg-red-500/10 transition-all disabled:opacity-20 disabled:cursor-not-allowed"
                  title="Supprimer l'utilisateur"
                >
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Responsive de création d'utilisateur -->
    <div v-if="showModal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-dark-800 border border-dark-600 rounded-2xl w-full max-w-lg p-6 sm:p-7 shadow-2xl relative">
        <div class="flex items-center justify-between pb-4 mb-4 border-b border-dark-600">
          <h3 class="text-lg font-bold text-white flex items-center gap-2">
            <span>➕</span>
            <span>Créer un profil BTP</span>
          </h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-white text-xl p-1">✕</button>
        </div>

        <form @submit.prevent="createUser" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1">Prénom *</label>
              <input v-model="form.first_name" required placeholder="ex: Jean" class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1">Nom *</label>
              <input v-model="form.last_name" required placeholder="ex: Konan" class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Adresse Email *</label>
            <input v-model="form.email" type="email" required placeholder="ex: j.konan@btp.ci" class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500" />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Téléphone</label>
            <input v-model="form.phone" placeholder="+225 07 00 00 00 00" class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500" />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Rôle Attribué *</label>
            <select v-model="form.role" required class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500">
              <option value="OWNER">🏢 OWNER — Direction / Propriétaire</option>
              <option value="DIRECTOR">📐 DIRECTOR — Direction Technique</option>
              <option value="MANAGER">📋 MANAGER — Chef de Projet / Conduite</option>
              <option value="WORKER">👷 WORKER — Chef de Chantier / Terrain</option>
              <option value="SUPER_ADMIN">👑 SUPER_ADMIN — Administrateur</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Mot de passe temporaire *</label>
            <input v-model="form.password" type="password" required minlength="8" placeholder="Au moins 8 caractères" class="w-full px-3 py-2 rounded-lg bg-dark-900 border border-dark-600 text-white text-sm focus:outline-none focus:border-btp-500" />
          </div>

          <div v-if="createError" class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-xs">
            ⚠️ {{ createError }}
          </div>

          <div class="flex justify-end gap-3 pt-3 border-t border-dark-600">
            <button type="button" @click="showModal = false" class="px-4 py-2 rounded-lg border border-dark-600 text-slate-300 hover:bg-dark-700 text-sm">
              Annuler
            </button>
            <button type="submit" :disabled="creating" class="px-5 py-2 rounded-lg bg-btp-500 hover:bg-btp-400 text-slate-950 font-bold text-sm shadow-md transition-all disabled:opacity-50">
              {{ creating ? 'Création...' : 'Créer l\'utilisateur' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const users = ref([])
const loading = ref(false)
const showModal = ref(false)
const creating = ref(false)
const createError = ref(null)

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  role: 'MANAGER',
  password: 'Password@1234',
})

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

function getRoleBadgeClass(role) {
  switch (role) {
    case 'SUPER_ADMIN': return 'bg-red-500/15 text-red-300 border border-red-500/30'
    case 'OWNER': return 'bg-amber-500/15 text-amber-300 border border-amber-500/30'
    case 'DIRECTOR': return 'bg-purple-500/15 text-purple-300 border border-purple-500/30'
    case 'MANAGER': return 'bg-blue-500/15 text-blue-300 border border-blue-500/30'
    case 'WORKER': return 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
    default: return 'bg-slate-700 text-slate-300'
  }
}

async function fetchUsers() {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/superadmin/users`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    users.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function createUser() {
  creating.value = true
  createError.value = null
  try {
    await axios.post(`${API_BASE}/superadmin/users`, form.value, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    showModal.value = false
    form.value = {
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      role: 'MANAGER',
      password: 'Password@1234',
    }
    await fetchUsers()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Erreur lors de la création'
  } finally {
    creating.value = false
  }
}

async function deleteUser(id) {
  if (!confirm('Confirmez-vous la suppression de cet utilisateur ?')) return
  try {
    await axios.delete(`${API_BASE}/superadmin/users/${id}`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    await fetchUsers()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erreur lors de la suppression')
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
