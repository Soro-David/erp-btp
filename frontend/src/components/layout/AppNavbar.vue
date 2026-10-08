<template>
  <header class="h-16 bg-[#047857] text-white border-b border-[#065f46] sticky top-0 z-40 px-4 sm:px-6 flex items-center justify-between shadow-sm select-none transition-all">
    <!-- Section Gauche : Bouton Hamburger & Marque BTP -->
    <div class="flex items-center gap-3 sm:gap-4">
      <!-- Bouton Menu Hamburger ☰ -->
      <button 
        type="button"
        @click="$emit('toggle-sidebar')" 
        class="p-2 rounded-xl text-white/90 hover:text-white hover:bg-black/10 transition-colors focus:outline-none focus:ring-2 focus:ring-white/40 text-lg"
        title="Basculer le menu latéral"
        aria-label="Toggle navigation"
      >
        <fas-icon icon="bars" />
      </button>

      <!-- Logo & Nom BTP Manager (Visible sur Mobile uniquement) -->
      <router-link to="/dashboard" class="flex items-center gap-2 lg:hidden group">
        <div class="w-8 h-8 rounded-xl bg-white text-[#047857] flex items-center justify-center font-black text-sm shadow-sm group-hover:scale-105 transition-transform">
          <fas-icon icon="helmet-safety" />
        </div>
        <span class="text-sm font-extrabold tracking-tight text-white leading-tight">
          BTP MANAGER
        </span>
      </router-link>

      <!-- Indicateur de portail BTP sur grand écran (La marque est déjà dans la sidebar) -->
      <div class="hidden lg:flex items-center gap-2.5 text-xs font-semibold text-emerald-100">
        <span class="w-2 h-2 rounded-full bg-emerald-300 animate-pulse"></span>
        <span class="tracking-wider uppercase text-[11px] font-bold text-white">PORTAIL OPÉRATIONNEL BTP</span>
      </div>
    </div>

    <!-- Section Centre / Droite : Recherche, Notifications, Aide, Utilisateur -->
    <div class="flex items-center gap-2 sm:gap-4">
      <!-- 🔍 Barre de Recherche Globale -->
      <div class="relative hidden md:block">
        <div class="relative flex items-center">
          <fas-icon icon="magnifying-glass" class="text-slate-400 absolute left-3 pointer-events-none text-xs" />
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Recherche générale (chantiers, marchés, stocks)..."
            @focus="searchFocused = true"
            @blur="setTimeout(() => searchFocused = false, 200)"
            class="w-64 lg:w-80 pl-9 pr-12 py-1.5 rounded-xl bg-white text-slate-800 placeholder-slate-400 text-xs border border-transparent focus:outline-none focus:ring-2 focus:ring-white/60 shadow-inner transition-all"
          />
          <kbd class="absolute right-2.5 px-1.5 py-0.5 text-[10px] font-semibold text-slate-400 bg-slate-100 border border-slate-200 rounded pointer-events-none">
            Ctrl+K
          </kbd>
        </div>

        <!-- Résultats rapides de recherche -->
        <div 
          v-if="searchFocused && searchQuery"
          class="absolute left-0 right-0 mt-2 bg-white border border-slate-200 rounded-2xl shadow-xl p-2 text-xs text-slate-700 z-50 animate-in fade-in duration-150"
        >
          <div class="px-2 py-1 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
            Recherche BTP rapide
          </div>
          <router-link 
            :to="`/chantiers?q=${searchQuery}`" 
            class="flex items-center gap-2 px-2.5 py-2 rounded-xl hover:bg-slate-50 text-slate-800 transition-colors"
          >
            <fas-icon icon="building" class="text-[#1d4ed8] text-xs" />
            <span>Rechercher "<strong>{{ searchQuery }}</strong>" dans les chantiers</span>
          </router-link>
          <router-link 
            :to="`/marches?q=${searchQuery}`" 
            class="flex items-center gap-2 px-2.5 py-2 rounded-xl hover:bg-slate-50 text-slate-800 transition-colors"
          >
            <fas-icon icon="file-contract" class="text-[#047857] text-xs" />
            <span>Trouver des marchés contenant "<strong>{{ searchQuery }}</strong>"</span>
          </router-link>
        </div>
      </div>

      <!-- Bouton recherche mobile -->
      <button 
        type="button"
        @click="showMobileSearch = !showMobileSearch"
        class="md:hidden p-2 rounded-xl text-white/90 hover:text-white hover:bg-black/10 transition-colors text-sm"
        title="Recherche"
      >
        <fas-icon icon="magnifying-glass" />
      </button>

      <!-- 🔔 Notifications -->
      <div class="relative" ref="notificationRef">
        <button 
          type="button"
          @click="toggleNotifications"
          class="p-2 rounded-xl text-white/90 hover:text-white hover:bg-black/10 transition-colors relative focus:outline-none text-base"
          title="Notifications"
          aria-label="Notifications"
        >
          <fas-icon icon="bell" />
          <span 
            v-if="unreadCount > 0"
            class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-amber-400 rounded-full ring-2 ring-[#047857]"
          ></span>
        </button>

        <!-- Dropdown Notifications (Fond Blanc Propre) -->
        <div 
          v-if="showNotifications"
          class="absolute right-0 mt-2 w-80 sm:w-88 bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 overflow-hidden text-slate-800 animate-in fade-in duration-150"
        >
          <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between bg-slate-50">
            <span class="text-xs font-bold text-slate-900 uppercase tracking-wider">Alertes Chantiers</span>
            <button 
              @click="markAllAsRead" 
              class="text-[11px] text-[#1d4ed8] hover:underline font-semibold"
            >
              Tout marquer comme lu
            </button>
          </div>

          <div class="max-h-80 overflow-y-auto divide-y divide-slate-100">
            <div 
              v-for="(notif, idx) in notifications" 
              :key="idx" 
              class="p-3.5 hover:bg-slate-50 transition-colors flex items-start gap-3 text-xs cursor-pointer"
            >
              <div class="p-2 rounded-xl text-sm flex-shrink-0" :class="notif.badgeBg">
                <fas-icon :icon="notif.icon" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-bold text-slate-900 leading-snug">{{ notif.title }}</p>
                <p class="text-slate-500 text-[11px] mt-0.5 line-clamp-2">{{ notif.desc }}</p>
                <span class="text-[10px] text-slate-400 mt-1 block">{{ notif.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ❓ Aide -->
      <div class="relative" ref="helpRef">
        <button 
          type="button"
          @click="toggleHelp"
          class="p-2 rounded-xl text-white/90 hover:text-white hover:bg-black/10 transition-colors focus:outline-none text-base"
          title="Centre d'aide"
          aria-label="Aide"
        >
          <fas-icon icon="circle-question" />
        </button>

        <!-- Dropdown Aide (Fond Blanc Propre) -->
        <div 
          v-if="showHelp"
          class="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 p-2 text-xs text-slate-700 animate-in fade-in duration-150"
        >
          <div class="px-3 py-2 border-b border-slate-100 mb-1">
            <div class="font-bold text-slate-900 text-xs">Support & Assistance</div>
            <div class="text-[10px] text-slate-500">Documentation BTP Manager</div>
          </div>

          <a 
            href="#guide" 
            @click.prevent="alertHelp('Le guide d\'utilisation BTP Manager est consultable auprès de votre administrateur.')"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="book" class="text-[#047857]" />
            <span>Guide d'utilisation</span>
          </a>
          <a 
            href="#hotline" 
            @click.prevent="alertHelp('Hotline technique chantiers disponible du lundi au samedi de 07h à 19h au +225 27 20 00 00 00.')"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="phone" class="text-[#1d4ed8]" />
            <span>Support Chantiers</span>
          </a>
          <a 
            href="#shortcuts" 
            @click.prevent="alertHelp('Raccourcis : Ctrl+K pour la recherche rapide, Échap pour fermer les menus.')"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="keyboard" class="text-amber-500" />
            <span>Raccourcis Clavier</span>
          </a>
        </div>
      </div>

      <div class="h-6 w-px bg-white/20 mx-1"></div>

      <!-- 👤 Avatar & Utilisateur -->
      <div class="relative" ref="userMenuRef">
        <button 
          type="button"
          @click="toggleUserMenu"
          class="flex items-center gap-2.5 p-1.5 sm:px-3 sm:py-1.5 rounded-xl hover:bg-black/10 border border-transparent transition-all focus:outline-none"
          aria-haspopup="true"
        >
          <div class="w-8 h-8 rounded-full bg-white text-[#047857] font-black text-xs flex items-center justify-center shadow-sm flex-shrink-0">
            {{ authStore.userInitials }}
          </div>
          <div class="hidden lg:flex flex-col text-left">
            <span class="text-xs font-bold text-white leading-tight">
              {{ authStore.userName || 'Utilisateur BTP' }}
            </span>
            <span class="text-[10px] font-semibold text-emerald-100 uppercase tracking-wider">
              {{ authStore.userRole || 'WORKER' }}
            </span>
          </div>
          <fas-icon icon="chevron-down" class="text-white/80 text-xs hidden sm:block" />
        </button>

        <!-- Dropdown Utilisateur (Fond Blanc Propre) -->
        <div 
          v-if="showUserMenu"
          class="absolute right-0 mt-2 w-56 bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 p-1.5 text-xs text-slate-700 animate-in fade-in duration-150"
        >
          <div class="px-3 py-2.5 border-b border-slate-100 mb-1 bg-slate-50 rounded-xl">
            <div class="font-bold text-slate-900 text-xs truncate">{{ authStore.userName }}</div>
            <div class="text-[11px] text-slate-500 truncate">{{ authStore.userEmail }}</div>
            <div class="mt-1.5 inline-block px-2 py-0.5 rounded-md text-[9px] font-extrabold uppercase bg-emerald-50 text-emerald-700 border border-emerald-200">
              {{ authStore.userRole }}
            </div>
          </div>

          <router-link 
            to="/profil" 
            @click="showUserMenu = false"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="user" class="text-slate-400" />
            <span>Profil</span>
          </router-link>

          <router-link 
            to="/preferences" 
            @click="showUserMenu = false"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="sliders" class="text-slate-400" />
            <span>Préférences</span>
          </router-link>

          <router-link 
            to="/parametres" 
            @click="showUserMenu = false"
            class="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-slate-50 text-slate-700 transition-colors"
          >
            <fas-icon icon="gear" class="text-slate-400" />
            <span>Paramètres</span>
          </router-link>

          <div class="h-px bg-slate-100 my-1"></div>

          <!-- Déconnexion Réelle -->
          <button 
            type="button"
            @click="handleLogout" 
            class="w-full text-left flex items-center gap-2.5 px-3 py-2 rounded-xl text-red-600 hover:bg-red-50 transition-colors font-semibold"
          >
            <fas-icon icon="right-from-bracket" />
            <span>Déconnexion</span>
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- Barre de recherche mobile dépliée -->
  <div v-if="showMobileSearch" class="md:hidden bg-[#065f46] border-b border-[#047857] p-3">
    <div class="relative flex items-center">
      <input 
        v-model="searchQuery"
        type="text"
        placeholder="Rechercher..."
        class="w-full pl-9 pr-4 py-2 rounded-xl bg-white text-slate-800 placeholder-slate-400 text-xs focus:outline-none"
      />
      <fas-icon icon="magnifying-glass" class="text-slate-400 absolute left-3 text-xs" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { alertInfo, confirmDialog, toast } from '@/utils/alert'

defineEmits(['toggle-sidebar'])

const router = useRouter()
const authStore = useAuthStore()

const searchQuery = ref('')
const searchFocused = ref(false)
const showMobileSearch = ref(false)

const showNotifications = ref(false)
const showHelp = ref(false)
const showUserMenu = ref(false)
const unreadCount = ref(3)

const notificationRef = ref(null)
const helpRef = ref(null)
const userMenuRef = ref(null)

const notifications = ref([
  {
    title: 'Coulage dalle — Tour Azur',
    desc: 'Validation béton armé requise par le chef de projet.',
    time: 'Il y a 15 min',
    icon: 'trowel-bricks',
    badgeBg: 'bg-emerald-50 text-[#047857]',
  },
  {
    title: 'Facture Fournisseur Lafarge',
    desc: 'Bon de commande #BC-2026-089 en attente d\'approbation.',
    time: 'Il y a 1 heure',
    icon: 'file-invoice-dollar',
    badgeBg: 'bg-blue-50 text-[#1d4ed8]',
  },
  {
    title: 'Alerte Météo Chantier Plateau',
    desc: 'Risque de fortes précipitations (sécurisation échafaudages).',
    time: 'Il y a 3 heures',
    icon: 'triangle-exclamation',
    badgeBg: 'bg-amber-50 text-amber-600',
  },
])

function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  showHelp.value = false
  showUserMenu.value = false
}

function toggleHelp() {
  showHelp.value = !showHelp.value
  showNotifications.value = false
  showUserMenu.value = false
}

function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
  showHelp.value = false
}

function markAllAsRead() {
  unreadCount.value = 0
}

function alertHelp(msg) {
  showHelp.value = false
  alertInfo('Aide & Support BTP', msg)
}

async function handleLogout() {
  showUserMenu.value = false
  const confirmed = await confirmDialog({
    title: 'Déconnexion',
    text: 'Voulez-vous vraiment vous déconnecter de votre session BTP Manager ?',
    confirmText: 'Se déconnecter',
    cancelText: 'Annuler',
    icon: 'question',
  })
  if (!confirmed) return

  authStore.logout()
  toast.fire({
    icon: 'info',
    title: 'Session fermée avec succès',
  })
  router.push('/login')
}

function handleClickOutside(e) {
  if (notificationRef.value && !notificationRef.value.contains(e.target)) {
    showNotifications.value = false
  }
  if (helpRef.value && !helpRef.value.contains(e.target)) {
    showHelp.value = false
  }
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
