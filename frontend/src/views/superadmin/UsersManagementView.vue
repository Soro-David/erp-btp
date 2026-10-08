<template>
  <div class="space-y-6">
    <!-- En-tête de la vue (Carte Blanche) -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold mb-1">
          <fas-icon icon="user-shield" />
          <span>ADMINISTRATION CENTRALE</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Gestion des Utilisateurs</h1>
        <p class="text-slate-500 text-xs sm:text-sm mt-0.5">Invitez et gérez les comptes des propriétaires d'entreprises BTP</p>
      </div>
      <button 
        @click="openInviteModal"
        class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm flex items-center justify-center gap-2 transition-all"
      >
        <fas-icon icon="paper-plane" />
        <span>Inviter un Propriétaire (Owner)</span>
      </button>
    </div>

    <!-- Barre d'indicateurs KPI (Cartes Blanches) -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
      <div class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col shadow-sm">
        <span class="text-2xl font-black text-slate-900">{{ users.length }}</span>
        <span class="text-xs text-slate-500 font-medium">Total Utilisateurs</span>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col shadow-sm">
        <span class="text-2xl font-black text-emerald-600">{{ users.filter(u => u.is_active).length }}</span>
        <span class="text-xs text-slate-500 font-medium">Comptes Actifs</span>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col shadow-sm">
        <span class="text-2xl font-black text-amber-600">{{ users.filter(u => !u.is_active).length }}</span>
        <span class="text-xs text-slate-500 font-medium">En attente d'activation</span>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col shadow-sm">
        <span class="text-2xl font-black text-blue-700">{{ users.filter(u => u.role === 'OWNER').length }}</span>
        <span class="text-xs text-slate-500 font-medium">Owners (Propriétaires)</span>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col shadow-sm">
        <span class="text-2xl font-black text-slate-600">{{ users.filter(u => u.role !== 'OWNER').length }}</span>
        <span class="text-xs text-slate-500 font-medium">Autres Profils</span>
      </div>
    </div>

    <!-- Tableau des Utilisateurs Partagé (DataTable) -->
    <DataTable
      :columns="columns"
      :items="users"
      :loading="loading"
      searchable
      search-placeholder="Rechercher par nom, email, rôle..."
      actions
      actions-header="Actions"
      actions-align="right"
      :page-size="10"
      empty-title="Aucun utilisateur trouvé"
      empty-subtitle="Aucun compte ne correspond à vos critères de recherche."
    >
      <!-- Slot ID -->
      <template #cell(id)="{ value }">
        <span class="text-slate-400 font-mono">#{{ value }}</span>
      </template>

      <!-- Slot Nom & Prénom -->
      <template #cell(first_name)="{ item }">
        <div class="flex items-center gap-2">
          <span class="font-bold text-slate-900">{{ item.first_name }} {{ item.last_name }}</span>
          <span v-if="!item.is_active" class="text-[10px] text-amber-600 font-normal bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
            Non finalisé
          </span>
        </div>
      </template>

      <!-- Slot Entreprise -->
      <template #cell(company_name)="{ item }">
        <div class="flex items-center gap-2">
          <div v-if="item.company_logo" class="w-6 h-6 rounded-full overflow-hidden border border-orange-300 flex-shrink-0">
            <img :src="item.company_logo" class="w-full h-full object-cover" alt="Logo" />
          </div>
          <span v-if="item.company_name" class="font-bold text-slate-800 text-xs">
            {{ item.company_name }}
          </span>
          <span v-else class="text-slate-400 text-xs italic">—</span>
        </div>
      </template>

      <!-- Slot Email -->
      <template #cell(email)="{ value }">
        <span class="font-mono text-blue-700 text-xs">{{ value }}</span>
      </template>

      <!-- Slot Téléphone -->
      <template #cell(phone)="{ value }">
        <span class="text-slate-600">{{ value || '—' }}</span>
      </template>

      <!-- Slot Rôle -->
      <template #cell(role)="{ value }">
        <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold" :class="getRoleBadgeClass(value)">
          {{ value }}
        </span>
      </template>

      <!-- Slot Statut -->
      <template #cell(is_active)="{ value }">
        <span 
          class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold"
          :class="value ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'"
        >
          <span class="w-1.5 h-1.5 rounded-full" :class="value ? 'bg-emerald-500' : 'bg-amber-500 animate-pulse'"></span>
          {{ value ? 'Actif' : 'En attente d\'activation' }}
        </span>
      </template>

      <!-- Slot Date Création -->
      <template #cell(created_at)="{ value }">
        <span class="text-slate-500 text-xs">{{ formatDate(value) }}</span>
      </template>

      <!-- Slot Actions -->
      <template #actions="{ item }">
        <div class="flex items-center justify-end gap-1.5">
          <!-- Renvoyer l'invitation par email (si en attente) -->
          <button
            v-if="!item.is_active"
            @click="resendInvitation(item)"
            :disabled="resendingId === item.id"
            class="p-2 rounded-xl border border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100 transition-all text-xs font-medium inline-flex items-center gap-1.5"
            title="Renvoyer l'email d'activation"
          >
            <fas-icon v-if="resendingId === item.id" icon="spinner" class="animate-spin text-xs" />
            <fas-icon v-else icon="paper-plane" class="text-xs" />
            <span class="hidden sm:inline">Renvoyer email</span>
          </button>

          <!-- Supprimer -->
          <button 
            @click="deleteUser(item.id)"
            :disabled="item.role === 'SUPER_ADMIN'"
            class="p-2 rounded-xl border border-slate-200 text-slate-400 hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50 transition-all disabled:opacity-20 disabled:cursor-not-allowed"
            title="Supprimer l'utilisateur"
          >
            <fas-icon icon="trash-can" class="text-xs" />
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Modal d'invitation d'un Propriétaire (Owner) -->
    <div v-if="showModal" class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white border border-slate-200 rounded-2xl w-full max-w-lg p-6 sm:p-7 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150">
        <!-- En-tête Modal -->
        <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-lg">
              <fas-icon icon="envelope-open-text" />
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900">Inviter un Propriétaire (Owner)</h3>
              <p class="text-xs text-slate-500">Un lien sécurisé lui sera envoyé par email pour activer son compte</p>
            </div>
          </div>
          <button @click="showModal = false" class="text-slate-400 hover:text-slate-700 text-lg p-1">
            <fas-icon icon="xmark" />
          </button>
        </div>

        <!-- Formulaire d'invitation -->
        <form @submit.prevent="inviteOwner" class="space-y-4">
          <!-- Rôle verrouillé -->
          <div class="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200/80 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <fas-icon icon="shield-halved" class="text-blue-700" />
              <div>
                <div class="text-[11px] uppercase font-bold text-blue-600 tracking-wider">Rôle attribué</div>
                <div class="text-xs font-bold text-slate-900">OWNER — Propriétaire / Direction BTP</div>
              </div>
            </div>
            <span class="px-2.5 py-1 rounded-lg bg-blue-600 text-white font-black text-[11px]">
              Verrouillé
            </span>
          </div>

          <!-- Email (Obligatoire) -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Adresse Email Professionnelle *
            </label>
            <input 
              v-model="inviteForm.email" 
              type="email" 
              required 
              placeholder="ex: direction@entreprise-btp.ci" 
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100" 
            />
          </div>

          <!-- Nom de l'Entreprise BTP (Obligatoire) -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Nom de l'Entreprise BTP *
            </label>
            <input 
              v-model="inviteForm.company_name" 
              type="text" 
              required 
              placeholder="ex: BATIR PLUS CI, EBOMAF, SOGEA-SATOM..." 
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-orange-500 focus:ring-2 focus:ring-orange-100" 
            />
          </div>

          <!-- Logo de l'Entreprise (Optionnel) -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Logo de l'Entreprise <span class="text-slate-400 font-normal">(optionnel, format rond)</span>
            </label>
            <div class="flex items-center gap-3 p-2.5 bg-slate-50 border border-slate-200 rounded-xl">
              <!-- Aperçu du logo rond et grand -->
              <div class="w-14 h-14 rounded-full border-2 border-orange-500 overflow-hidden bg-white flex items-center justify-center flex-shrink-0 shadow-sm">
                <img v-if="inviteForm.company_logo" :src="inviteForm.company_logo" class="w-full h-full object-cover rounded-full" alt="Aperçu Logo" />
                <fas-icon v-else icon="image" class="text-slate-400 text-xl" />
              </div>
              <div class="flex-1 space-y-1.5">
                <input 
                  type="file" 
                  accept="image/*" 
                  @change="handleModalLogoUpload" 
                  class="block w-full text-xs text-slate-500 file:mr-2 file:py-1 file:px-2.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100 cursor-pointer"
                />
                <input 
                  v-model="inviteForm.company_logo" 
                  type="url" 
                  placeholder="Ou URL du logo (https://...)" 
                  class="w-full px-2.5 py-1 text-xs rounded-lg bg-white border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500"
                />
              </div>
            </div>
          </div>

          <!-- Prénom & Nom (Optionnels au départ) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">
                Prénom <span class="text-slate-400 font-normal">(optionnel)</span>
              </label>
              <input 
                v-model="inviteForm.first_name" 
                placeholder="ex: Jean-Luc" 
                class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600" 
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">
                Nom <span class="text-slate-400 font-normal">(optionnel)</span>
              </label>
              <input 
                v-model="inviteForm.last_name" 
                placeholder="ex: Kouassi" 
                class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600" 
              />
            </div>
          </div>

          <!-- Note explicative sur le mot de passe -->
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-600 text-xs flex items-start gap-2.5">
            <fas-icon icon="info-circle" class="text-blue-600 mt-0.5 flex-shrink-0 text-sm" />
            <span class="leading-relaxed">
              <strong>Mot de passe :</strong> Aucun mot de passe n'est exigé ici. L'invité recevra un courriel sécurisé contenant un lien valable 72 heures pour configurer son propre mot de passe et finaliser ses informations personnelles.
            </span>
          </div>

          <!-- Erreur API -->
          <div v-if="inviteError" class="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
            <fas-icon icon="circle-exclamation" />
            <span>{{ inviteError }}</span>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-2.5 pt-3 border-t border-slate-100">
            <button 
              type="button" 
              @click="showModal = false" 
              class="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-medium"
            >
              Annuler
            </button>
            <button 
              type="submit" 
              :disabled="inviting || !inviteForm.email" 
              class="px-5 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm transition-all disabled:opacity-50 flex items-center gap-2"
            >
              <fas-icon v-if="inviting" icon="spinner" class="animate-spin" />
              <fas-icon v-else icon="paper-plane" />
              <span>{{ inviting ? 'Envoi en cours...' : 'Envoyer l\'invitation' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { userService } from '@/services'
import { useAuthStore } from '@/stores/auth'
import { toast, confirmDialog, alertError, alertSuccess } from '@/utils/alert'
import Swal from 'sweetalert2'

const route = useRoute()
const authStore = useAuthStore()

const columns = [
  { key: 'id', label: 'ID', sortable: true, width: '70px' },
  { key: 'first_name', label: 'Nom & Prénom', sortable: true },
  { key: 'company_name', label: 'Entreprise BTP', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'phone', label: 'Téléphone' },
  { key: 'role', label: 'Rôle', sortable: true },
  { key: 'is_active', label: 'Statut', sortable: true },
  { key: 'created_at', label: 'Date Création', sortable: true }
]

const users = ref([])
const loading = ref(false)
const showModal = ref(false)
const inviting = ref(false)
const inviteError = ref(null)
const resendingId = ref(null)

const inviteForm = ref({
  email: '',
  company_name: '',
  company_logo: '',
  first_name: '',
  last_name: '',
})

function handleModalLogoUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    alertError('Fichier trop lourd', 'La taille maximale autorisée pour le logo est de 2 Mo.')
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => {
    inviteForm.value.company_logo = e.target.result
  }
  reader.readAsDataURL(file)
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

function getRoleBadgeClass(role) {
  switch (role) {
    case 'SUPER_ADMIN': return 'bg-rose-50 text-rose-700 border border-rose-200'
    case 'OWNER': return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'DIRECTOR': return 'bg-purple-50 text-purple-700 border border-purple-200'
    case 'MANAGER': return 'bg-blue-50 text-blue-700 border border-blue-200'
    case 'WORKER': return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    default: return 'bg-slate-100 text-slate-700'
  }
}

function openInviteModal() {
  inviteError.value = null
  inviteForm.value = {
    email: '',
    company_name: '',
    company_logo: '',
    first_name: '',
    last_name: '',
  }
  showModal.value = true
}

async function fetchUsers() {
  loading.value = true
  try {
    const data = await userService.getUsers()
    users.value = data
  } catch (err) {
    console.error('Erreur chargement utilisateurs via Axios:', err)
  } finally {
    loading.value = false
  }
}

async function inviteOwner() {
  inviting.value = true
  inviteError.value = null

  try {
    const res = await userService.inviteOwner(inviteForm.value)
    showModal.value = false
    await fetchUsers()

    // Notification enrichie avec code OTP et lien direct en mode dev
    if (res.invitation_link) {
      await Swal.fire({
        icon: 'success',
        title: 'Invitation envoyée !',
        html: `
          <div class="text-left text-xs text-slate-600 space-y-3">
            <p>Un email d'invitation a été préparé pour <strong>${inviteForm.value.email}</strong>.</p>
            <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 flex items-center justify-between">
              <div>
                <div class="text-[10px] font-bold text-amber-700 uppercase tracking-wider">Code de validation OTP :</div>
                <div class="text-xl font-black font-mono text-amber-900 tracking-widest">${res.otp_code || '—'}</div>
              </div>
              <span class="text-[10px] text-amber-800 bg-amber-200/60 px-2 py-0.5 rounded-full font-bold">4 chiffres</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-[11px] font-bold text-slate-700 mb-1">Lien d'activation (pour test immédiat) :</div>
              <input type="text" readonly value="${res.invitation_link}" class="w-full text-xs font-mono p-1.5 border rounded bg-white select-all text-blue-700" onclick="this.select()" />
            </div>
          </div>
        `,
        confirmButtonText: 'Fermer',
        confirmButtonColor: '#1d4ed8',
      })
    } else {
      toast('Invitation envoyée avec succès !', 'success')
    }
  } catch (err) {
    inviteError.value = err.response?.data?.detail || "Erreur lors de l'envoi de l'invitation"
    alertError("Erreur d'invitation", inviteError.value)
  } finally {
    inviting.value = false
  }
}

async function resendInvitation(user) {
  resendingId.value = user.id
  try {
    const res = await userService.resendInvitation(user.id)
    if (res.invitation_link) {
      await Swal.fire({
        icon: 'success',
        title: 'Nouvelle invitation générée !',
        html: `
          <div class="text-left text-xs text-slate-600 space-y-3">
            <p>L'email d'activation a été réémis pour <strong>${user.email}</strong>.</p>
            <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 flex items-center justify-between">
              <div>
                <div class="text-[10px] font-bold text-amber-700 uppercase tracking-wider">Nouveau code OTP :</div>
                <div class="text-xl font-black font-mono text-amber-900 tracking-widest">${res.otp_code || '—'}</div>
              </div>
              <span class="text-[10px] text-amber-800 bg-amber-200/60 px-2 py-0.5 rounded-full font-bold">4 chiffres</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-[11px] font-bold text-slate-700 mb-1">Lien d'activation (pour test immédiat) :</div>
              <input type="text" readonly value="${res.invitation_link}" class="w-full text-xs font-mono p-1.5 border rounded bg-white select-all text-blue-700" onclick="this.select()" />
            </div>
          </div>
        `,
        confirmButtonText: 'Fermer',
        confirmButtonColor: '#1d4ed8',
      })
    } else {
      toast('Invitation renvoyée avec succès !', 'success')
    }
  } catch (err) {
    alertError("Erreur", err.response?.data?.detail || "Impossible de renvoyer l'invitation")
  } finally {
    resendingId.value = null
  }
}

async function deleteUser(id) {
  const confirmed = await confirmDialog(
    'Supprimer cet utilisateur ?',
    'Cette suppression est irréversible dans la base de données ERP.',
    'Oui, supprimer'
  )
  if (!confirmed) return

  try {
    await userService.deleteUser(id)
    toast('Utilisateur supprimé.', 'success')
    await fetchUsers()
  } catch (err) {
    alertError('Erreur de suppression', err.response?.data?.detail || 'Impossible de supprimer cet utilisateur.')
  }
}

function checkInviteQuery() {
  if (route.query.invite === 'open' || route.query.invite === '1' || route.query.invite === 'true') {
    openInviteModal()
  }
}

onMounted(() => {
  fetchUsers()
  checkInviteQuery()
})

watch(() => route.query.invite, () => {
  checkInviteQuery()
})
</script>
