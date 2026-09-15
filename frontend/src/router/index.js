import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView from '@/views/auth/LoginView.vue'
import UsersManagementView from '@/views/superadmin/UsersManagementView.vue'
import OwnerDashboardView from '@/views/owner/OwnerDashboardView.vue'
import DirectorDashboardView from '@/views/director/DirectorDashboardView.vue'
import ManagerDashboardView from '@/views/manager/ManagerDashboardView.vue'
import WorkerDashboardView from '@/views/worker/WorkerDashboardView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/superadmin/users',
    name: 'SuperAdminUsers',
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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Si l'utilisateur a un token mais pas son profil chargé
  if (authStore.token && !authStore.user) {
    await authStore.fetchCurrentUser()
  }

  // Redirection si invité accède à une page privée
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'Login' })
  }

  // Redirection si connecté accède à login
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    const role = authStore.userRole
    if (role === 'SUPER_ADMIN') return next('/superadmin/users')
    if (role === 'OWNER') return next('/owner')
    if (role === 'DIRECTOR') return next('/director')
    if (role === 'MANAGER') return next('/manager')
    if (role === 'WORKER') return next('/worker')
    return next('/')
  }

  // Vérification des rôles autorisés (RBAC)
  if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    alert(`Accès restreint. Votre rôle (${authStore.userRole}) ne vous autorise pas à accéder à cette vue.`)
    return next(false)
  }

  next()
})

export default router
