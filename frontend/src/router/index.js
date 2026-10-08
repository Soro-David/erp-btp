import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView from '@/views/auth/LoginView.vue'
import ActivateAccountView from '@/views/auth/ActivateAccountView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import ModulePlaceholderView from '@/views/modules/ModulePlaceholderView.vue'
import ProfileView from '@/views/profile/ProfileView.vue'

import UsersManagementView from '@/views/superadmin/UsersManagementView.vue'
import ChantierDetailView from '@/views/chantiers/ChantierDetailView.vue'
import ChantierCreateView from '@/views/chantiers/ChantierCreateView.vue'
import TasksManagementView from '@/views/chantiers/TasksManagementView.vue'
import PlanningView from '@/views/chantiers/PlanningView.vue'
import OwnerDashboardView from '@/views/owner/OwnerDashboardView.vue'
import DirectorDashboardView from '@/views/director/DirectorDashboardView.vue'
import ManagerDashboardView from '@/views/manager/ManagerDashboardView.vue'
import WorkerDashboardView from '@/views/worker/WorkerDashboardView.vue'

import PurchasesListView from '@/views/achats/PurchasesListView.vue'
import PurchaseDetailView from '@/views/achats/PurchaseDetailView.vue'
import SuppliersListView from '@/views/achats/SuppliersListView.vue'
import SupplierDetailView from '@/views/achats/SupplierDetailView.vue'
import MaterialsListView from '@/views/achats/MaterialsListView.vue'
import StockManagementView from '@/views/achats/StockManagementView.vue'

const routes = [
  // Authentification
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true, layout: 'AuthLayout' },
  },
  {
    path: '/activer-compte',
    name: 'ActivateAccount',
    component: ActivateAccountView,
    meta: { layout: 'AuthLayout' },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },

  // Tableau de bord unifié BTP Manager
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },

  // Profil Utilisateur
  {
    path: '/profil',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },

  // 1. Projets & Chantiers
  {
    path: '/chantiers',
    name: 'Chantiers',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/chantiers/nouveau',
    name: 'ChantierCreate',
    component: ChantierCreateView,
    meta: { requiresAuth: true },
  },
  {
    path: '/chantiers/:id',
    name: 'ChantierDetail',
    component: ChantierDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/chantiers/taches',
    name: 'ChantiersTaches',
    component: TasksManagementView,
    meta: { requiresAuth: true },
  },
  {
    path: '/chantiers/planning',
    name: 'ChantiersPlanning',
    component: PlanningView,
    meta: { requiresAuth: true },
  },

  // 2. Marchés
  {
    path: '/marches',
    redirect: '/marches/appels-offres',
  },
  {
    path: '/marches/appels-offres',
    name: 'MarchesAppelsOffres',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/marches/contrats',
    name: 'MarchesContrats',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/marches/situations',
    name: 'MarchesSituations',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },

  // 3. Achats & Stocks (4 menus principaux)
  {
    path: '/achats',
    name: 'Achats',
    component: PurchasesListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/achats/:id',
    name: 'PurchaseDetail',
    component: PurchaseDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/achats/fournisseurs',
    name: 'Fournisseurs',
    component: SuppliersListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/achats/fournisseurs/:id',
    name: 'SupplierDetail',
    component: SupplierDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/achats/materiaux',
    name: 'Materiaux',
    component: MaterialsListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/achats/stock',
    name: 'Stock',
    component: StockManagementView,
    meta: { requiresAuth: true },
  },

  // Aliases et compatibilité rétroactive
  {
    path: '/achats-stocks',
    redirect: '/achats',
  },
  {
    path: '/achats-stocks/achats',
    redirect: '/achats',
  },
  {
    path: '/achats-stocks/fournisseurs',
    redirect: '/achats/fournisseurs',
  },
  {
    path: '/achats-stocks/materiaux',
    redirect: '/achats/materiaux',
  },
  {
    path: '/achats-stocks/stocks',
    redirect: '/achats/stock',
  },

  // 4. Engins & Équipements
  {
    path: '/engins',
    name: 'Engins',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/engins/maintenance',
    name: 'EnginsMaintenance',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },

  // 5. Ressources Humaines
  {
    path: '/rh',
    redirect: '/rh/employes',
  },
  {
    path: '/rh/employes',
    name: 'RHEmployes',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/rh/equipes',
    name: 'RHEquipes',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },

  // 6. Finance
  {
    path: '/finance',
    name: 'Finance',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER', 'DIRECTOR'] },
  },

  // 7. Rapports
  {
    path: '/rapports',
    name: 'Rapports',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },

  // 8. Paramètres & Préférences
  {
    path: '/parametres',
    name: 'Parametres',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },
  {
    path: '/preferences',
    name: 'Preferences',
    component: ModulePlaceholderView,
    meta: { requiresAuth: true },
  },

  // Vues de Rôles Spécifiques (Conservées)
  {
    path: '/superadmin/users',
    name: 'SuperAdminUsers',
    component: UsersManagementView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER'] },
  },
  {
    path: '/superadmin/proprietaires',
    name: 'SuperAdminProprietaires',
    component: UsersManagementView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER'] },
  },
  {
    path: '/owner',
    name: 'OwnerDashboard',
    component: OwnerDashboardView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER'] },
  },
  {
    path: '/director',
    name: 'DirectorDashboard',
    component: DirectorDashboardView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER', 'DIRECTOR'] },
  },
  {
    path: '/manager',
    name: 'ManagerDashboard',
    component: ManagerDashboardView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER', 'DIRECTOR', 'MANAGER'] },
  },
  {
    path: '/worker',
    name: 'WorkerDashboard',
    component: WorkerDashboardView,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'OWNER', 'DIRECTOR', 'MANAGER', 'WORKER'] },
  },

  // Redirection par défaut vers dashboard
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Si l'utilisateur a un token mais pas son profil en mémoire, on le charge
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch {
      // Si échec de chargement du profil, token expiré ou invalide
      authStore.logout()
      return next({ name: 'Login' })
    }
  }

  // Redirection si un utilisateur non authentifié tente d'accéder à une vue protégée
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // Redirection si un utilisateur déjà connecté visite la page de login
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next('/dashboard')
  }

  // Contrôle RBAC des habilitations
  if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    return next('/dashboard')
  }

  next()
})

export default router
