<template>
  <!-- Conteneur Sidebar Principal (Flottant avec marge à gauche et bordures arrondies) -->
  <aside 
    class="fixed lg:sticky top-0 inset-y-0 left-0 z-50 flex flex-col bg-[#0f294a] text-white transition-all duration-300 select-none flex-shrink-0 overflow-hidden"
    :class="[
      isMobileOpen 
        ? 'translate-x-0 w-72 h-screen rounded-r-2xl border-r border-[#163b66] shadow-2xl' 
        : '-translate-x-full lg:translate-x-0',
      isCollapsed ? 'lg:w-20' : 'lg:w-72',
      'lg:my-0 lg:ml-0 lg:mr-1 lg:h-screen lg:rounded-none lg:border-r lg:border-[#163b66]/60'
    ]"
  >
    <!-- Backdrop Mobile (Téléporté au body pour garantir un stacking context parfait) -->
    <Teleport to="body">
      <transition
        enter-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="isMobileOpen" 
          @click="$emit('close-mobile')" 
          class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          aria-hidden="true"
        ></div>
      </transition>
    </Teleport>

    <!-- En-tête Sidebar : Logo dynamique rond & grand format, et Nom Entreprise dynamique -->
    <div class="h-20 flex items-center justify-between px-3.5 border-b border-[#163b66] bg-[#0b1f38] flex-shrink-0">
      <router-link 
        to="/dashboard" 
        class="flex items-center gap-3 overflow-hidden group w-full"
        :class="isCollapsed ? 'justify-center' : ''"
      >
        <!-- Logo rond et grand format dynamique -->
        <div 
          class="rounded-full overflow-hidden flex items-center justify-center flex-shrink-0 shadow-lg shadow-orange-500/20 border-2 border-orange-400/80 transition-transform group-hover:scale-105 bg-gradient-to-br from-orange-500 via-amber-500 to-orange-600 text-white"
          :class="isCollapsed ? 'w-11 h-11' : 'w-13 h-13 sm:w-14 sm:h-14'"
        >
          <img 
            v-if="authStore.companyLogo" 
            :src="authStore.companyLogo" 
            alt="Logo Entreprise" 
            class="w-full h-full object-cover rounded-full"
          />
          <span v-else-if="companyInitials" class="font-black text-sm tracking-wider">
            {{ companyInitials }}
          </span>
          <fas-icon v-else icon="helmet-safety" class="text-xl" />
        </div>

        <div v-if="!isCollapsed" class="flex flex-col min-w-0 transition-opacity">
          <span class="font-extrabold text-sm text-white tracking-wide leading-tight truncate">
            {{ authStore.companyName }}
          </span>
          <span class="text-[9px] font-bold text-orange-300 uppercase tracking-widest leading-none truncate mt-0.5">
            {{ subtitleText }}
          </span>
        </div>
      </router-link>

      <!-- Bouton fermer sur Mobile -->
      <button 
        @click="$emit('close-mobile')" 
        class="lg:hidden p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-white/10 ml-2"
        aria-label="Fermer le menu"
      >
        <fas-icon icon="xmark" class="text-base" />
      </button>
    </div>

    <!-- Navigation & Liste des Menus avec défilement interne complet -->
    <nav class="flex-1 overflow-y-auto overflow-x-hidden p-3 space-y-1 text-xs scrollbar-thin">
      <template v-for="item in displayedMenuItems" :key="item.id">
        <!-- Vérification du rôle / permission -->
        <div v-if="!item.roles || item.roles.includes(authStore.userRole)">
          <!-- 1. Élément simple (sans sous-menus) -->
          <router-link
            v-if="!item.children"
            :to="item.to"
            @click="handleLinkClick"
            class="group relative flex items-center gap-3 px-3 py-2.5 rounded-xl font-semibold transition-all duration-150"
            :class="[
              isActive(item.to)
                ? 'bg-[#1d4ed8] text-white shadow-md shadow-blue-900/40'
                : 'text-slate-200 hover:text-white hover:bg-[#163b66]',
              isCollapsed ? 'justify-center px-2' : ''
            ]"
          >
            <fas-icon 
              :icon="item.icon" 
              class="text-base flex-shrink-0 group-hover:scale-110 transition-transform w-5 text-center" 
              :class="isActive(item.to) ? 'text-white' : 'text-slate-300'"
            />
            <span v-if="!isCollapsed" class="truncate font-medium text-xs">
              {{ item.label }}
            </span>

            <!-- Badge éventuel -->
            <span 
              v-if="!isCollapsed && item.badge"
              class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold"
              :class="item.badgeClass || 'bg-blue-800 text-blue-100'"
            >
              {{ item.badge }}
            </span>

            <!-- Infobulle en mode réduit (Desktop) -->
            <div 
              v-if="isCollapsed" 
              class="hidden lg:group-hover:flex absolute left-full ml-3 px-2.5 py-1.5 bg-[#0b1f38] border border-[#163b66] text-white text-xs font-semibold rounded-lg shadow-xl whitespace-nowrap z-50 pointer-events-none"
            >
              {{ item.label }}
            </div>
          </router-link>

          <!-- 2. Élément avec sous-menus dépliables/repliables -->
          <div v-else class="space-y-1">
            <!-- Bouton Parent de l'accordéon -->
            <button
              type="button"
              @click="toggleSubmenu(item.id)"
              class="w-full group relative flex items-center gap-3 px-3 py-2.5 rounded-xl font-semibold transition-all duration-150 text-left"
              :class="[
                isChildActive(item)
                  ? 'bg-[#163b66] text-white font-bold'
                  : 'text-slate-200 hover:text-white hover:bg-[#163b66]/60',
                isCollapsed ? 'justify-center px-2' : ''
              ]"
            >
              <fas-icon 
                :icon="item.icon" 
                class="text-base flex-shrink-0 group-hover:scale-110 transition-transform w-5 text-center" 
                :class="isChildActive(item) ? 'text-blue-300' : 'text-slate-300'"
              />
              <span v-if="!isCollapsed" class="truncate font-medium text-xs flex-1">
                {{ item.label }}
              </span>
              <fas-icon 
                v-if="!isCollapsed"
                icon="chevron-down"
                class="text-xs text-slate-300 transition-transform duration-200"
                :class="openSubmenus[item.id] ? 'rotate-180 text-blue-300' : ''"
              />

              <!-- Infobulle en mode réduit (Desktop) -->
              <div 
                v-if="isCollapsed" 
                class="hidden lg:group-hover:flex absolute left-full ml-3 px-2.5 py-1.5 bg-[#0b1f38] border border-[#163b66] text-white text-xs font-semibold rounded-lg shadow-xl whitespace-nowrap z-50 pointer-events-none"
              >
                {{ item.label }}
              </div>
            </button>

            <!-- Liste des sous-menus (Dépliée / Repliée) -->
            <div 
              v-if="!isCollapsed && openSubmenus[item.id]" 
              class="ml-6 pl-3 border-l border-[#1d4ed8]/40 space-y-1 pt-1 animate-in fade-in slide-in-from-top-1 duration-150"
            >
              <router-link
                v-for="sub in item.children"
                :key="sub.to"
                :to="sub.to"
                @click="handleLinkClick"
                class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all"
                :class="[
                  isActive(sub.to)
                    ? 'bg-[#1d4ed8] text-white font-semibold shadow-sm'
                    : 'text-slate-300 hover:text-white hover:bg-[#163b66]/50'
                ]"
              >
                <fas-icon 
                  v-if="sub.icon" 
                  :icon="sub.icon" 
                  class="text-[10px] w-3.5 text-center"
                  :class="isActive(sub.to) ? 'text-white' : 'text-slate-400'" 
                />
                <span v-else class="w-1.5 h-1.5 rounded-full" :class="isActive(sub.to) ? 'bg-white' : 'bg-slate-400'"></span>
                <span class="truncate">{{ sub.label }}</span>
              </router-link>
            </div>
          </div>
        </div>
      </template>
    </nav>

    <!-- Pied de Sidebar : Profil compact + Bouton Réduire/Agrandir (Prend sa place fixe en bas) -->
    <div class="p-3 border-t border-[#163b66] bg-[#0b1f38] flex-shrink-0 space-y-2">
      <!-- Utilisateur connecté (si non réduit) -->
      <div v-if="!isCollapsed" class="flex items-center gap-2.5 px-2 py-1.5 rounded-xl bg-[#0f294a]/80 border border-[#163b66]/60">
        <div class="w-7 h-7 rounded-lg bg-[#1d4ed8] text-white text-xs font-bold flex items-center justify-center flex-shrink-0 shadow-sm">
          {{ authStore.userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-xs font-bold text-white truncate">{{ authStore.userName }}</div>
          <div class="text-[10px] text-blue-300 truncate uppercase font-semibold">{{ authStore.userRole }}</div>
        </div>
      </div>

      <!-- Bouton Réduire / Déplier (Desktop) -->
      <button
        type="button"
        @click="$emit('toggle-collapse')"
        class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-[#163b66] transition-colors text-xs font-medium hidden lg:flex"
        :class="isCollapsed ? 'justify-center px-1' : ''"
        title="Réduire ou étendre la barre latérale"
      >
        <fas-icon :icon="isCollapsed ? 'angles-right' : 'angles-left'" class="text-sm flex-shrink-0" />
        <span v-if="!isCollapsed" class="truncate">
          Réduire le menu
        </span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { reactive, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
  isMobileOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close-mobile', 'toggle-collapse'])

const route = useRoute()
const authStore = useAuthStore()

const companyInitials = computed(() => {
  const name = authStore.user?.company_name
  if (!name) return ''
  const words = name.trim().split(/\s+/)
  if (words.length === 1) return words[0].substring(0, 2).toUpperCase()
  return (words[0][0] + words[1][0]).toUpperCase()
})

const subtitleText = computed(() => {
  if (authStore.userRole === 'SUPER_ADMIN') return 'ADMINISTRATION CENTRALE'
  if (authStore.userRole === 'OWNER') return 'DIRECTION GÉNÉRALE'
  return 'ERP GÉNIE CIVIL'
})

// État des accordéons ouverts
const openSubmenus = reactive({
  proprietaires: true,
  supervision_btp: false,
  projets: true,
  marches: false,
  achats: false,
  engins: false,
  rh: false,
})

// Menu dédié pour le SUPER_ADMIN
const superAdminMenuItems = [
  {
    id: 'dashboard',
    label: 'Tableau de bord',
    icon: 'gauge-high',
    to: '/dashboard',
  },
  {
    id: 'proprietaires',
    label: 'Propriétaires',
    icon: 'user-tie',
    badge: 'Admin',
    badgeClass: 'bg-blue-500/20 text-blue-200 border border-blue-500/30',
    children: [
      { label: 'Liste des propriétaires', icon: 'users', to: '/superadmin/users' },
      { label: 'Inviter un propriétaire', icon: 'paper-plane', to: '/superadmin/users?invite=open' },
    ],
  },
  {
    id: 'rapports',
    label: 'Rapports',
    icon: 'chart-pie',
    to: '/rapports',
  },
  {
    id: 'parametres',
    label: 'Paramètres',
    icon: 'gear',
    to: '/parametres',
  },
  {
    id: 'supervision_btp',
    label: 'Supervision Chantiers',
    icon: 'trowel-bricks',
    children: [
      { label: 'Chantiers', icon: 'building', to: '/chantiers' },
      { label: 'Marchés & Contrats', icon: 'file-contract', to: '/marches/contrats' },
      { label: 'Suivi Financier', icon: 'wallet', to: '/finance' },
    ],
  },
  {
    id: 'achats',
    label: 'Achats & Stocks',
    icon: 'boxes-stacked',
    children: [
      { label: 'Achat', icon: 'cart-shopping', to: '/achats' },
      { label: 'Fournisseur', icon: 'handshake', to: '/achats/fournisseurs' },
      { label: 'Matériaux', icon: 'cubes', to: '/achats/materiaux' },
      { label: 'Stock', icon: 'warehouse', to: '/achats/stock' },
    ],
  },
]

// Arborescence complète pour les entreprises et autres rôles (OWNER, DIRECTOR, MANAGER, etc.)
const standardMenuItems = [
  {
    id: 'dashboard',
    label: 'Tableau de bord',
    icon: 'gauge-high',
    to: '/dashboard',
  },
  {
    id: 'projets',
    label: 'Projets & Chantiers',
    icon: 'trowel-bricks',
    children: [
      { label: 'Chantiers', icon: 'building', to: '/chantiers' },
      { label: 'Tâches', icon: 'list-check', to: '/chantiers/taches' },
      { label: 'Planning', icon: 'calendar-days', to: '/chantiers/planning' },
    ],
  },
  {
    id: 'marches',
    label: 'Marchés',
    icon: 'file-contract',
    children: [
      { label: 'Appels d\'offres', icon: 'file-lines', to: '/marches/appels-offres' },
      { label: 'Contrats', icon: 'signature', to: '/marches/contrats' },
      { label: 'Situations', icon: 'receipt', to: '/marches/situations' },
    ],
  },
  {
    id: 'achats',
    label: 'Achats & Stocks',
    icon: 'boxes-stacked',
    children: [
      { label: 'Achat', icon: 'cart-shopping', to: '/achats' },
      { label: 'Fournisseur', icon: 'handshake', to: '/achats/fournisseurs' },
      { label: 'Matériaux', icon: 'cubes', to: '/achats/materiaux' },
      { label: 'Stock', icon: 'warehouse', to: '/achats/stock' },
    ],
  },
  {
    id: 'engins',
    label: 'Engins & Équipements',
    icon: 'truck-pickup',
    children: [
      { label: 'Engins', icon: 'truck-monster', to: '/engins' },
      { label: 'Maintenance', icon: 'wrench', to: '/engins/maintenance' },
    ],
  },
  {
    id: 'rh',
    label: 'Ressources humaines',
    icon: 'users-gear',
    children: [
      { label: 'Employés', icon: 'user-group', to: '/rh/employes' },
      { label: 'Équipes', icon: 'people-group', to: '/rh/equipes' },
    ],
  },
  {
    id: 'finance',
    label: 'Finance',
    icon: 'wallet',
    to: '/finance',
    roles: ['OWNER', 'DIRECTOR'],
  },
  {
    id: 'rapports',
    label: 'Rapports',
    icon: 'chart-pie',
    to: '/rapports',
  },
  {
    id: 'parametres',
    label: 'Paramètres',
    icon: 'gear',
    to: '/parametres',
  },
]

// Détermination dynamique des menus selon le profil connecté
const displayedMenuItems = computed(() => {
  if (authStore.userRole === 'SUPER_ADMIN') {
    return superAdminMenuItems
  }
  return standardMenuItems.filter(item => !item.roles || item.roles.includes(authStore.userRole))
})

function toggleSubmenu(id) {
  openSubmenus[id] = !openSubmenus[id]
}

function isActive(path) {
  return route.path === path
}

function isChildActive(item) {
  if (!item.children) return false
  return item.children.some((child) => route.path === child.to)
}

function handleLinkClick() {
  emit('close-mobile')
}

function autoExpandActiveSubmenu() {
  displayedMenuItems.value.forEach((item) => {
    if (item.children && isChildActive(item)) {
      openSubmenus[item.id] = true
    }
  })
}

watch(() => route.path, () => {
  autoExpandActiveSubmenu()
})

onMounted(() => {
  autoExpandActiveSubmenu()
})
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 5px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #163b66;
  border-radius: 9999px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #1d4ed8;
}
</style>
