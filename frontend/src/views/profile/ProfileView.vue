<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- En-tête profil (Carte Blanche) -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm relative overflow-hidden">
      <div class="flex flex-col sm:flex-row sm:items-center gap-5 relative z-10">
        <!-- Avatar / Initiales ou Logo -->
        <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full border-2 border-orange-500/50 bg-[#0f294a] text-white font-black text-2xl sm:text-3xl flex items-center justify-center shadow-md shadow-orange-500/10 flex-shrink-0 overflow-hidden">
          <img 
            v-if="authStore.companyLogo" 
            :src="authStore.companyLogo" 
            alt="Logo Entreprise" 
            class="w-full h-full object-cover rounded-full"
          />
          <span v-else>{{ authStore.userInitials }}</span>
        </div>
        <div class="flex-1">
          <div class="flex flex-wrap items-center gap-2 mb-1">
            <h1 class="text-xl sm:text-2xl font-black text-slate-900">
              {{ authStore.userName || 'Utilisateur BTP' }}
            </h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider" :class="getRoleBadgeStyle(authStore.userRole)">
              {{ authStore.userRole }}
            </span>
          </div>
          <p class="text-xs sm:text-sm text-slate-500 font-mono">
            {{ authStore.userEmail }}
          </p>
          <div v-if="authStore.companyName" class="mt-1.5 inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-orange-50 border border-orange-200/80 text-orange-800 font-semibold text-xs">
            <fas-icon icon="building" class="text-[10px]" />
            <span>{{ authStore.companyName }}</span>
          </div>
        </div>

        <button 
          @click="refreshProfile" 
          :disabled="refreshing"
          class="px-4 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-2 border border-slate-300 transition-colors shadow-sm self-start sm:self-center"
        >
          <fas-icon icon="arrows-rotate" :class="refreshing ? 'animate-spin' : ''" />
          <span>{{ refreshing ? 'Actualisation...' : 'Actualiser le profil' }}</span>
        </button>
      </div>
    </div>

    <!-- Section Identité Entreprise (Owner & SuperAdmin) -->
    <div 
      v-if="authStore.userRole === 'OWNER' || authStore.userRole === 'SUPER_ADMIN'" 
      class="bg-white border-2 border-orange-500/40 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6"
    >
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-orange-50 border border-orange-200 text-orange-800 text-xs font-bold mb-1">
            <fas-icon icon="building" />
            <span>IDENTITÉ D'ENTREPRISE BTP</span>
          </div>
          <h2 class="text-base sm:text-lg font-black text-slate-900">
            Nom et Logo de l'Entreprise
          </h2>
          <p class="text-xs text-slate-500 mt-0.5">
            Personnalisez le logo grand format et le nom affiché sur le sidebar et le footer.
          </p>
        </div>
      </div>

      <form @submit.prevent="saveCompanyProfile" class="space-y-6">
        <!-- Logo rond et en grand format -->
        <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 p-4 rounded-2xl bg-orange-50/30 border border-orange-100">
          <div class="flex flex-col items-center gap-2">
            <!-- Grand conteneur rond du logo -->
            <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-full border-4 border-orange-500 shadow-xl overflow-hidden bg-white flex items-center justify-center relative flex-shrink-0">
              <img 
                v-if="companyForm.company_logo" 
                :src="companyForm.company_logo" 
                alt="Logo Entreprise" 
                class="w-full h-full object-cover rounded-full"
              />
              <div 
                v-else 
                class="w-full h-full rounded-full bg-gradient-to-tr from-amber-500 to-orange-600 text-white flex flex-col items-center justify-center font-black text-2xl shadow-inner"
              >
                <span>{{ companyInitialsPreview || 'BTP' }}</span>
                <span class="text-[9px] font-semibold text-orange-200 tracking-wider">ENTREPRISE</span>
              </div>
            </div>
            <span class="text-[11px] font-bold text-orange-800">Format Rond & Grand</span>
          </div>

          <div class="flex-1 space-y-3 w-full">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Téléverser un nouveau logo
              </label>
              <input 
                type="file" 
                accept="image/*" 
                @change="handleLogoFileSelect" 
                class="block w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-orange-500 file:text-white hover:file:bg-orange-600 file:cursor-pointer cursor-pointer transition-all"
              />
              <p class="text-[11px] text-slate-400 mt-1">
                Formats acceptés : PNG, JPG, WEBP, SVG (Max 2 Mo). L'image est automatiquement cadrée en cercle.
              </p>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">
                Ou saisir l'URL du logo :
              </label>
              <input 
                v-model="companyForm.company_logo" 
                type="url" 
                placeholder="https://votre-domaine.ci/logo.png" 
                class="w-full px-3.5 py-2 text-xs rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:outline-none focus:bg-white focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
              />
            </div>

            <div v-if="companyForm.company_logo" class="pt-1">
              <button 
                type="button" 
                @click="companyForm.company_logo = ''" 
                class="text-xs font-semibold text-rose-600 hover:text-rose-800 inline-flex items-center gap-1.5"
              >
                <fas-icon icon="trash-can" />
                <span>Supprimer le logo actuel</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Nom de l'entreprise -->
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
            Nom Officiel de l'Entreprise BTP *
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-orange-500">
              <fas-icon icon="building" class="text-sm" />
            </div>
            <input 
              v-model="companyForm.company_name" 
              type="text" 
              required 
              placeholder="ex: EBOMAF, SOGEA-SATOM, BATIR PLUS CI..." 
              class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm font-semibold focus:outline-none focus:bg-white focus:border-orange-500 focus:ring-2 focus:ring-orange-100"
            />
          </div>
          <p class="text-[11px] text-slate-400 mt-1">
            Ce nom s'affichera sur le sidebar à gauche et automatiquement à droite dans le footer.
          </p>
        </div>

        <!-- Bouton Sauvegarder -->
        <div class="flex justify-end pt-2 border-t border-slate-100">
          <button 
            type="submit" 
            :disabled="savingCompany || !companyForm.company_name" 
            class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs shadow-md shadow-orange-500/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <fas-icon v-if="savingCompany" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="floppy-disk" />
            <span>{{ savingCompany ? 'Enregistrement en cours...' : 'Enregistrer les modifications d\'entreprise' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Informations du compte (données réelles FastAPI) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Fiche d'identité -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <h2 class="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
          <fas-icon icon="address-card" class="text-blue-700 text-sm" />
          <span>Informations Administratives</span>
        </h2>

        <div class="space-y-3 text-xs sm:text-sm">
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Prénom :</span>
            <span class="font-bold text-slate-900">{{ authStore.user?.first_name || '—' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Nom de famille :</span>
            <span class="font-bold text-slate-900">{{ authStore.user?.last_name || '—' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Email professionnel :</span>
            <span class="font-semibold text-blue-700 font-mono">{{ authStore.user?.email || '—' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Téléphone de contact :</span>
            <span class="font-semibold text-slate-800">{{ authStore.user?.phone || 'Non renseigné' }}</span>
          </div>
          <div class="flex justify-between py-2">
            <span class="text-slate-500">Statut du compte :</span>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold" :class="authStore.user?.is_active ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'">
              <span class="w-1.5 h-1.5 rounded-full" :class="authStore.user?.is_active ? 'bg-emerald-500' : 'bg-rose-500'"></span>
              <span>{{ authStore.user?.is_active ? 'Compte Actif' : 'Désactivé' }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Sécurité & Session JWT -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <h2 class="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
          <fas-icon icon="shield-halved" class="text-emerald-700 text-sm" />
          <span>Sécurité & Session Active</span>
        </h2>

        <div class="space-y-3 text-xs sm:text-sm">
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Protocole d'authentification :</span>
            <span class="font-mono text-emerald-700 font-bold">FastAPI JWT (Bearer)</span>
          </div>
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Algorithme de signature :</span>
            <span class="font-mono text-slate-700">HS256 (24h)</span>
          </div>
          <div class="flex justify-between py-2 border-b border-slate-100">
            <span class="text-slate-500">Compte créé le :</span>
            <span class="font-semibold text-slate-700">{{ formatDate(authStore.user?.created_at) }}</span>
          </div>
          <div class="flex justify-between py-2">
            <span class="text-slate-500">Dernière mise à jour :</span>
            <span class="font-semibold text-slate-700">{{ formatDate(authStore.user?.updated_at) }}</span>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-100">
          <button 
            @click="confirmLogout"
            class="w-full py-2.5 px-4 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-bold transition-colors flex items-center justify-center gap-2"
          >
            <fas-icon icon="right-from-bracket" />
            <span>Fermer la session et se déconnecter</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast, confirmDialog, alertError } from '@/utils/alert'

const router = useRouter()
const authStore = useAuthStore()
const refreshing = ref(false)
const savingCompany = ref(false)

const companyForm = ref({
  company_name: '',
  company_logo: '',
})

function initCompanyForm() {
  companyForm.value.company_name = authStore.user?.company_name || ''
  companyForm.value.company_logo = authStore.user?.company_logo || ''
}

onMounted(() => {
  initCompanyForm()
})

watch(() => authStore.user, () => {
  initCompanyForm()
}, { deep: true })

const companyInitialsPreview = computed(() => {
  const name = companyForm.value.company_name
  if (!name) return 'BTP'
  const words = name.trim().split(/\s+/)
  if (words.length === 1) return words[0].substring(0, 2).toUpperCase()
  return (words[0][0] + words[1][0]).toUpperCase()
})

function handleLogoFileSelect(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    alertError('Fichier trop volumineux', 'La taille maximale autorisée pour le logo est de 2 Mo.')
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => {
    companyForm.value.company_logo = e.target.result
  }
  reader.readAsDataURL(file)
}

async function saveCompanyProfile() {
  savingCompany.value = true
  try {
    await authStore.updateProfile({
      company_name: companyForm.value.company_name.trim(),
      company_logo: companyForm.value.company_logo || null,
    })
    toast('Identité de l\'entreprise mise à jour avec succès !', 'success')
  } catch (err) {
    console.error('Erreur mise à jour profil entreprise:', err)
    alertError('Erreur de sauvegarde', err.response?.data?.detail || 'Impossible de mettre à jour les informations d\'entreprise.')
  } finally {
    savingCompany.value = false
  }
}

async function refreshProfile() {
  refreshing.value = true
  try {
    await authStore.fetchCurrentUser()
    initCompanyForm()
    toast('Profil actualisé depuis FastAPI', 'success')
  } catch (err) {
    toast('Erreur d\'actualisation du profil', 'error')
  } finally {
    refreshing.value = false
  }
}

async function confirmLogout() {
  const confirmed = await confirmDialog(
    'Déconnexion',
    'Voulez-vous vraiment vous déconnecter de BTP Manager ?',
    'Se déconnecter'
  )
  if (confirmed) {
    authStore.logout()
    router.push('/login')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return 'Date non disponible'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateStr
  }
}

function getRoleBadgeStyle(role) {
  switch (role) {
    case 'SUPER_ADMIN': return 'bg-rose-50 text-rose-700 border border-rose-200'
    case 'OWNER': return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'DIRECTOR': return 'bg-purple-50 text-purple-700 border border-purple-200'
    case 'MANAGER': return 'bg-blue-50 text-blue-700 border border-blue-200'
    case 'WORKER': return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    default: return 'bg-slate-100 text-slate-700'
  }
}
</script>
