<template>
  <div class="min-h-screen flex items-center justify-center p-4 sm:p-6 lg:p-8 bg-[#0b0f17] relative overflow-hidden">
    <!-- Arrière-plan architectural avec dégradé subtil -->
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,#1a243d_0%,#0b0f17_75%)] pointer-events-none"></div>
    <div class="absolute -top-32 -right-32 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-32 -left-32 w-96 h-96 bg-amber-600/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Carte principale -->
    <div class="w-full max-w-lg bg-slate-900/90 backdrop-blur-xl border border-slate-800 rounded-3xl p-7 sm:p-9 shadow-2xl shadow-black/80 relative z-10">
      <!-- En-tête -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/25 mb-4 text-2xl">
          <fas-icon icon="helmet-safety" />
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-bold mb-2">
          <fas-icon icon="sparkles" />
          <span>ACTIVATION DU COMPTE PROPRIÉTAIRE</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
          Bienvenue sur BTP Manager
        </h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1.5 font-medium">
          Renseignez vos informations personnelles et choisissez votre mot de passe pour finaliser l'accès à votre espace Direction.
        </p>
      </div>

      <!-- État de chargement initial de validation du jeton -->
      <div v-if="verifyingToken" class="py-12 text-center text-slate-400 text-sm flex flex-col items-center justify-center gap-3">
        <fas-icon icon="spinner" class="animate-spin text-3xl text-blue-500" />
        <span>Vérification de la validité de votre lien d'invitation...</span>
      </div>

      <!-- Erreur jeton invalide ou expiré -->
      <div v-else-if="tokenError" class="p-6 rounded-2xl bg-red-500/10 border border-red-500/30 text-center space-y-4">
        <div class="w-12 h-12 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center mx-auto text-xl">
          <fas-icon icon="circle-exclamation" />
        </div>
        <div>
          <h3 class="text-base font-bold text-red-300 mb-1">Lien d'invitation invalide</h3>
          <p class="text-xs text-red-400/90 leading-relaxed">{{ tokenError }}</p>
        </div>
        <div class="pt-2">
          <router-link
            to="/login"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs transition-colors"
          >
            <fas-icon icon="arrow-left" />
            <span>Retour à la page de connexion</span>
          </router-link>
        </div>
      </div>

      <!-- Formulaire de finalisation -->
      <form v-else @submit.prevent="handleComplete" class="space-y-4">
        <!-- Champ Email (Lecture Seule) -->
        <div>
          <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            Adresse Email Invitée
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="envelope" class="text-sm" />
            </div>
            <input
              :value="invitationData.email"
              disabled
              class="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-800/40 border border-slate-700 text-slate-400 text-sm cursor-not-allowed font-medium select-none"
            />
            <div class="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none text-emerald-400" title="Email vérifié">
              <fas-icon icon="circle-check" class="text-sm" />
            </div>
          </div>
        </div>

        <!-- Champ Code OTP (4 chiffres) -->
        <div class="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 space-y-2">
          <div class="flex items-center justify-between">
            <label class="block text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
              <fas-icon icon="key" class="text-xs text-amber-400" />
              <span>Code de Validation OTP (4 caractères) *</span>
            </label>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/30">
              Reçu par email
            </span>
          </div>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-400">
              <fas-icon icon="shield-halved" class="text-sm" />
            </div>
            <input
              v-model="form.otp"
              type="text"
              maxlength="4"
              required
              placeholder="0000"
              class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-amber-500/50 text-amber-300 font-mono text-base font-black tracking-[8px] focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/30 text-center sm:text-left"
            />
          </div>
          <p class="text-[11px] text-slate-400 leading-tight">
            Renseignez le code secret à 4 chiffres présent dans l'email d'invitation pour valider votre identité.
          </p>
        </div>

        <!-- Prénom & Nom -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Prénom *
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <fas-icon icon="user" class="text-sm" />
              </div>
              <input
                v-model="form.first_name"
                required
                placeholder="Votre prénom"
                class="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Nom *
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <fas-icon icon="user" class="text-sm" />
              </div>
              <input
                v-model="form.last_name"
                required
                placeholder="Votre nom"
                class="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
          </div>
        </div>

        <!-- Téléphone -->
        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Numéro de Téléphone
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="phone" class="text-sm" />
            </div>
            <input
              v-model="form.phone"
              type="tel"
              placeholder="+225 07 00 00 00 00"
              class="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>
        </div>

        <!-- Nom de l'Entreprise BTP -->
        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Nom de l'Entreprise BTP
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="building" class="text-sm" />
            </div>
            <input
              v-model="form.company_name"
              placeholder="ex: BTP Construction SARL"
              class="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>
        </div>

        <!-- Mot de passe -->
        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Créer un mot de passe *
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="lock" class="text-sm" />
            </div>
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              minlength="8"
              placeholder="Minimum 8 caractères"
              class="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-200"
            >
              <fas-icon :icon="showPassword ? 'eye-slash' : 'eye'" class="text-sm" />
            </button>
          </div>
          <!-- Barre d'estimation de robustesse -->
          <div class="mt-2 flex items-center gap-1.5">
            <div class="h-1 flex-1 rounded-full transition-all" :class="pwdStrength >= 1 ? 'bg-red-500' : 'bg-slate-700'"></div>
            <div class="h-1 flex-1 rounded-full transition-all" :class="pwdStrength >= 2 ? 'bg-amber-500' : 'bg-slate-700'"></div>
            <div class="h-1 flex-1 rounded-full transition-all" :class="pwdStrength >= 3 ? 'bg-emerald-500' : 'bg-slate-700'"></div>
            <span class="text-[10px] font-semibold text-slate-400 ml-1">{{ pwdStrengthLabel }}</span>
          </div>
        </div>

        <!-- Confirmation du mot de passe -->
        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Confirmer le mot de passe *
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="lock" class="text-sm" />
            </div>
            <input
              v-model="form.confirm_password"
              :type="showPassword ? 'text' : 'password'"
              required
              minlength="8"
              placeholder="Retapez le mot de passe"
              class="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
            <div 
              v-if="form.confirm_password" 
              class="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none"
              :class="passwordsMatch ? 'text-emerald-400' : 'text-red-400'"
            >
              <fas-icon :icon="passwordsMatch ? 'check' : 'xmark'" class="text-sm" />
            </div>
          </div>
          <p v-if="form.confirm_password && !passwordsMatch" class="text-red-400 text-xs mt-1">
            Les mots de passe ne correspondent pas.
          </p>
        </div>

        <!-- Message d'erreur de soumission -->
        <div v-if="submitError" class="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
          <fas-icon icon="circle-exclamation" class="flex-shrink-0" />
          <span>{{ submitError }}</span>
        </div>

        <!-- Bouton de validation -->
        <button
          type="submit"
          :disabled="submitting || !passwordsMatch || !form.password"
          class="w-full mt-2 py-3 px-4 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-sm shadow-lg shadow-blue-900/40 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <fas-icon v-if="submitting" icon="spinner" class="animate-spin" />
          <fas-icon v-else icon="check-to-slot" />
          <span>{{ submitting ? 'Activation de votre compte...' : 'Activer mon compte & Accéder à l\'ERP' }}</span>
        </button>
      </form>

      <!-- Pied de carte -->
      <div class="mt-6 pt-4 border-t border-slate-800/80 text-center">
        <p class="text-xs text-slate-500">
          Vous avez déjà un compte actif ? 
          <router-link to="/login" class="text-blue-400 hover:text-blue-300 font-semibold underline ml-1">
            Connectez-vous
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authService } from '@/services'
import { useAuthStore } from '@/stores/auth'
import { toast, alertSuccess } from '@/utils/alert'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const token = ref('')
const verifyingToken = ref(true)
const tokenError = ref(null)
const submitting = ref(false)
const submitError = ref(null)
const showPassword = ref(false)

const invitationData = ref({
  email: '',
  first_name: '',
  last_name: '',
  company_name: '',
  company_logo: '',
})

const form = ref({
  otp: '',
  first_name: '',
  last_name: '',
  company_name: '',
  company_logo: '',
  phone: '',
  password: '',
  confirm_password: '',
})

const passwordsMatch = computed(() => {
  if (!form.value.confirm_password) return false
  return form.value.password === form.value.confirm_password
})

const pwdStrength = computed(() => {
  const p = form.value.password
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p) && /[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p) && p.length >= 10) score++
  return score
})

const pwdStrengthLabel = computed(() => {
  switch (pwdStrength.value) {
    case 1: return 'Faible'
    case 2: return 'Moyen'
    case 3: return 'Fort'
    default: return ''
  }
})

async function checkToken() {
  verifyingToken.value = true
  tokenError.value = null

  await router.isReady()

  // 1. Récupération via vue-router
  let rawToken = route.query.token
  let rawOtp = route.query.otp

  // 2. Fallback direct via URLSearchParams si le navigateur ouvre depuis un client mail externe
  if ((!rawToken || !rawOtp) && typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search)
    if (!rawToken) rawToken = urlParams.get('token')
    if (!rawOtp) rawOtp = urlParams.get('otp')
  }

  token.value = rawToken ? String(rawToken).trim() : ''
  if (rawOtp) {
    form.value.otp = String(rawOtp).trim()
  }

  if (!token.value) {
    tokenError.value = "Aucun jeton d'invitation n'a été trouvé dans l'adresse URL."
    verifyingToken.value = false
    return
  }

  try {
    const data = await authService.getInvitationInfo(token.value)
    invitationData.value = data
    if (data.first_name) form.value.first_name = data.first_name
    if (data.last_name) form.value.last_name = data.last_name
    if (data.company_name) form.value.company_name = data.company_name
    if (data.company_logo) form.value.company_logo = data.company_logo
  } catch (err) {
    tokenError.value = err.response?.data?.detail || "Ce lien d'invitation est invalide ou a expiré."
  } finally {
    verifyingToken.value = false
  }
}

async function handleComplete() {
  if (!form.value.otp || form.value.otp.trim().length !== 4) {
    submitError.value = "Veuillez renseigner le code OTP de validation à 4 chiffres."
    return
  }

  if (!passwordsMatch.value) {
    submitError.value = "Les deux mots de passe ne sont pas identiques."
    return
  }

  submitting.value = true
  submitError.value = null

  try {
    const payload = {
      token: token.value,
      otp: form.value.otp.trim(),
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      company_name: form.value.company_name || null,
      company_logo: form.value.company_logo || null,
      phone: form.value.phone || null,
      password: form.value.password,
    }

    const tokenResponse = await authService.completeInvitation(payload)

    // Déconnexion d'une éventuelle ancienne session SuperAdmin et connexion immédiate de l'Owner
    authStore.token = tokenResponse.access_token
    sessionStorage.setItem('btp_token', tokenResponse.access_token)
    localStorage.removeItem('btp_token')
    await authStore.fetchCurrentUser()

    await alertSuccess(
      'Compte activé avec succès !',
      'Votre profil Propriétaire a été configuré. Bienvenue sur votre espace BTP Manager.'
    )

    // Redirection vers le tableau de bord
    router.push('/owner')
  } catch (err) {
    submitError.value = err.response?.data?.detail || "Une erreur est survenue lors de l'activation du compte."
  } finally {
    submitting.value = false
  }
}

watch(() => route.query.token, () => {
  checkToken()
})

onMounted(() => {
  checkToken()
})
</script>
