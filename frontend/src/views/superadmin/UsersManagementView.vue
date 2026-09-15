<template>
  <div class="management-container">
    <div class="view-header">
      <div>
        <h2>👑 Espace SuperAdmin — Gestion des Utilisateurs</h2>
        <p>Création, attribution des rôles (Owner, Director, Manager, Worker) et contrôle des accès</p>
      </div>
      <button class="btn-create" @click="showModal = true">
        <span>➕</span>
        <span>Nouvel Utilisateur</span>
      </button>
    </div>

    <!-- Bannière rôle & informations -->
    <div class="stats-bar">
      <div class="stat-card">
        <span class="stat-val">{{ users.length }}</span>
        <span class="stat-lbl">Utilisateurs au total</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{{ users.filter(u => u.is_active).length }}</span>
        <span class="stat-lbl">Comptes Actifs</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{{ users.filter(u => u.role === 'OWNER').length }}</span>
        <span class="stat-lbl">Owners</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{{ users.filter(u => u.role === 'DIRECTOR').length }}</span>
        <span class="stat-lbl">Directors</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{{ users.filter(u => u.role === 'MANAGER').length }}</span>
        <span class="stat-lbl">Managers</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{{ users.filter(u => u.role === 'WORKER').length }}</span>
        <span class="stat-lbl">Workers</span>
      </div>
    </div>

    <!-- Tableau des utilisateurs -->
    <div class="table-card">
      <div v-if="loading" class="loading-state">
        Chargement des utilisateurs en cours...
      </div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom & Prénom</th>
            <th>Email</th>
            <th>Téléphone</th>
            <th>Rôle</th>
            <th>Statut</th>
            <th>Date Création</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>#{{ user.id }}</td>
            <td class="font-bold">{{ user.first_name }} {{ user.last_name }}</td>
            <td class="code">{{ user.email }}</td>
            <td>{{ user.phone || '—' }}</td>
            <td>
              <span class="role-badge" :class="'role-' + user.role.toLowerCase()">
                {{ user.role }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? 'Actif' : 'Désactivé' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <button 
                class="btn-action btn-danger" 
                title="Supprimer" 
                :disabled="user.role === 'SUPER_ADMIN'"
                @click="deleteUser(user.id)"
              >
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de création d'utilisateur -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Créer un nouvel utilisateur BTP</h3>
          <button class="btn-close" @click="showModal = false">✕</button>
        </div>

        <form @submit.prevent="createUser" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label>Prénom *</label>
              <input v-model="form.first_name" required placeholder="ex: Jean" />
            </div>
            <div class="form-group">
              <label>Nom *</label>
              <input v-model="form.last_name" required placeholder="ex: Konan" />
            </div>
          </div>

          <div class="form-group">
            <label>Adresse Email *</label>
            <input v-model="form.email" type="email" required placeholder="ex: j.konan@btp.ci" />
          </div>

          <div class="form-group">
            <label>Téléphone (optionnel)</label>
            <input v-model="form.phone" placeholder="+225 07 00 00 00 00" />
          </div>

          <div class="form-group">
            <label>Rôle attribué *</label>
            <select v-model="form.role" required>
              <option value="OWNER">🏢 OWNER (Propriétaire / Direction)</option>
              <option value="DIRECTOR">📐 DIRECTOR (Directeur Technique)</option>
              <option value="MANAGER">📋 MANAGER (Chef de Projet / Conduite)</option>
              <option value="WORKER">👷 WORKER (Chef de Chantier / Terrain)</option>
              <option value="SUPER_ADMIN">👑 SUPER_ADMIN (Administrateur)</option>
            </select>
          </div>

          <div class="form-group">
            <label>Mot de passe temporaire *</label>
            <input v-model="form.password" type="password" required minlength="8" placeholder="Minimum 8 caractères" />
          </div>

          <div v-if="createError" class="alert-error">
            ⚠️ {{ createError }}
          </div>

          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showModal = false">Annuler</button>
            <button type="submit" class="btn-submit" :disabled="creating">
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

<style scoped>
.management-container {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-header h2 {
  font-size: 1.6rem;
  color: #fff;
  margin-bottom: 0.3rem;
}

.view-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.btn-create {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, var(--accent-btp) 0%, #d97706 100%);
  color: #0f172a;
  border: none;
  padding: 0.8rem 1.4rem;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px var(--accent-btp-glow);
}

.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.stat-val {
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
}

.stat-lbl {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.table-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}

.data-table th {
  background: rgba(11, 15, 23, 0.6);
  padding: 1rem 1.25rem;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color);
}

.data-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(30, 45, 74, 0.5);
  color: var(--text-primary);
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.font-bold {
  font-weight: 600;
}

.code {
  font-family: monospace;
  color: #38bdf8;
}

.role-badge {
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
}

.role-super_admin { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
.role-owner { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
.role-director { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
.role-manager { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
.role-worker { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

.status-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 600;
}

.status-active { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-inactive { background: rgba(239, 68, 68, 0.15); color: #f87171; }

.btn-action {
  background: transparent;
  border: 1px solid var(--border-color);
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-action:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.btn-action:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 520px;
  padding: 2rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h3 {
  font-size: 1.3rem;
  color: #fff;
}

.btn-close {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1.2rem;
  cursor: pointer;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.form-group input, .form-group select {
  background: #0b0f17;
  border: 1px solid var(--border-color);
  color: #fff;
  padding: 0.75rem 0.9rem;
  border-radius: 8px;
  outline: none;
}

.form-group input:focus, .form-group select:focus {
  border-color: var(--accent-btp);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-cancel {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
}

.alert-error {
  background: var(--status-error-bg);
  border: 1px solid var(--status-error);
  color: #fca5a5;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
}
</style>
