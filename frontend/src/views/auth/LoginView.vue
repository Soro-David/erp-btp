<template>
  <div class="min-h-screen flex items-center justify-center p-4 sm:p-6 lg:p-8 bg-[#0b0f17] relative overflow-hidden">
    <!-- Arrière-plan architectural avec dégradé subtil -->
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,#1a243d_0%,#0b0f17_75%)] pointer-events-none"></div>
    <div class="absolute -top-32 -right-32 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-32 -left-32 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Carte de connexion principale -->
    <div class="w-full max-w-md bg-slate-900/90 backdrop-blur-xl border border-slate-800 rounded-3xl p-7 sm:p-9 shadow-2xl shadow-black/80 relative z-10">
      <!-- Logo et Identité BTP Manager -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-400 text-slate-950 shadow-lg shadow-amber-500/25 mb-4 text-2xl">
          <fas-icon icon="helmet-safety" />
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white flex items-center justify-center gap-2">
          <span>BTP Manager</span>
        </h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1 font-medium">
          Portail de gestion et suivi des opérations de chantier
        </p>
      </div>

      <!-- Message d'alerte Erreur API -->
      <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div 
          v-if="errorMessage" 
          class="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs sm:text-sm flex items-start justify-between gap-3 shadow-sm"
          role="alert"
        >
          <div class="flex items-start gap-2.5">
            <fas-icon icon="circle-exclamation" class="text-red-400 text-base flex-shrink-0 mt-0.5" />
            <span class="leading-relaxed font-medium">{{ errorMessage }}</span>
          </div>
          <button 
            type="button"
            @click="errorMessage = ''"
            class="text-red-400/70 hover:text-red-300 transition-colors p-0.5 rounded"
            aria-label="Fermer"
          >
            <fas-icon icon="xmark" />
          </button>
        </div>
      </transition>

      <!-- Formulaire de Connexion -->
      <form @submit.prevent="handleSubmit" class="space-y-5" novalidate>
        <!-- Champ Email -->
        <div>
          <label for="email" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Email
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="envelope" class="text-sm" />
            </div>
            <input
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              required
              placeholder="nom@entreprise.ci"
              :disabled="authStore.loading"
              class="w-full pl-11 pr-4 py-3 rounded-xl bg-slate-950/70 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            />
          </div>
        </div>

        <!-- Champ Mot de passe -->
        <div>
          <label for="password" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Mot de passe
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <fas-icon icon="lock" class="text-sm" />
            </div>
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              required
              placeholder="••••••••••••"
              :disabled="authStore.loading"
              class="w-full pl-11 pr-11 py-3 rounded-xl bg-slate-950/70 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-200 transition-colors"
              :aria-label="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
            >
              <fas-icon :icon="showPassword ? 'eye-slash' : 'eye'" class="text-sm" />
            </button>
          </div>
        </div>

        <!-- Options : Toggle Se souvenir de moi & Mot de passe oublié -->
        <div class="flex items-center justify-between pt-1">
          <!-- Toggle Se souvenir de moi -->
          <label class="flex items-center gap-2.5 cursor-pointer group select-none">
            <div class="relative inline-flex items-center">
              <input
                type="checkbox"
                v-model="form.rememberMe"
                :disabled="authStore.loading"
                class="sr-only peer"
              />
              <div class="w-9 h-5 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-amber-500"></div>
            </div>
            <span class="text-xs font-medium text-slate-300 group-hover:text-white transition-colors">
              Se souvenir de moi
            </span>
          </label>

          <!-- Lien Mot de passe oublié -->
          <button
            type="button"
            @click="handleForgotPassword"
            class="text-xs font-semibold text-amber-400 hover:text-amber-300 hover:underline transition-colors"
          >
            Mot de passe oublié ?
          </button>
        </div>

        <!-- Bouton Se connecter -->
        <button
          type="submit"
          :disabled="authStore.loading || !form.email || !form.password"
          class="w-full mt-3 py-3.5 px-4 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm sm:text-base shadow-lg shadow-amber-500/25 transition-all transform active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2.5 group"
        >
          <fas-icon v-if="authStore.loading" icon="spinner" class="animate-spin text-lg" />
          <span>{{ authStore.loading ? 'Connexion en cours...' : 'Se connecter' }}</span>
          <fas-icon v-if="!authStore.loading" icon="arrow-right" class="text-sm transition-transform group-hover:translate-x-1" />
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast, alertInfo, alertError } from '@/utils/alert'

const router = useRouter()
const authStore = useAuthStore()

const showPassword = ref(false)
const errorMessage = ref('')

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

onMounted(() => {
  if (authStore.savedEmail) {
    form.email = authStore.savedEmail
    form.rememberMe = true
  }
})

function handleForgotPassword() {
  alertInfo(
    'Procédure de Réinitialisation',
    'Pour des raisons de sécurité ERP BTP, veuillez contacter votre administrateur ou le support : support@btp-manager.ci (+225 27 20 00 00 00)'
  )
}

async function handleSubmit() {
  errorMessage.value = ''
  
  if (!form.email || !form.password) {
    errorMessage.value = 'Veuillez renseigner votre email et mot de passe.'
    return
  }

  try {
    await authStore.login(form.email, form.password, form.rememberMe)
    toast.fire({
      icon: 'success',
      title: `Bienvenue, ${authStore.userName || 'Utilisateur'} !`,
    })
    router.push('/dashboard')
  } catch (err) {
    errorMessage.value = authStore.error || 'Identifiants invalides ou service indisponible.'
    toast.fire({
      icon: 'error',
      title: 'Erreur de connexion',
      text: errorMessage.value,
    })
  }
}
</script>
