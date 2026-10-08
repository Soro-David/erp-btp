import { defineStore } from 'pinia'
import { authService } from '@/services'

export const useAuthStore = defineStore('auth', {
  state: () => {
    const localToken = localStorage.getItem('btp_token')
    const sessionToken = sessionStorage.getItem('btp_token')
    const token = localToken || sessionToken || null

    const localUser = localStorage.getItem('btp_user')
    const sessionUser = sessionStorage.getItem('btp_user')
    let user = null
    try {
      user = JSON.parse(localUser || sessionUser || 'null')
    } catch {
      user = null
    }

    const savedEmail = localStorage.getItem('btp_remember_email') || ''

    return {
      token,
      user,
      loading: false,
      error: null,
      savedEmail,
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    userName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name} ${state.user.last_name}`.trim()
    },
    userEmail: (state) => state.user?.email || '',
    userInitials: (state) => {
      if (!state.user) return 'U'
      const first = state.user.first_name?.charAt(0) || ''
      const last = state.user.last_name?.charAt(0) || ''
      return (first + last).toUpperCase() || 'U'
    },
    companyName: (state) => state.user?.company_name || 'BTP MANAGER',
    companyLogo: (state) => state.user?.company_logo || null,
  },

  actions: {
    async login(email, password, rememberMe = false) {
      this.loading = true
      this.error = null

      try {
        const data = await authService.login({ email, password })
        this.token = data.access_token

        if (rememberMe) {
          localStorage.setItem('btp_token', this.token)
          localStorage.setItem('btp_remember_email', email.trim())
          sessionStorage.removeItem('btp_token')
        } else {
          sessionStorage.setItem('btp_token', this.token)
          localStorage.removeItem('btp_token')
          localStorage.removeItem('btp_remember_email')
        }

        // Récupération immédiate du profil complet via Axios authService
        await this.fetchCurrentUser(rememberMe)
        return true
      } catch (err) {
        let msg = 'Une erreur est survenue lors de la connexion'
        if (err.response?.data?.detail) {
          const detail = err.response.data.detail
          if (typeof detail === 'string') {
            msg = detail
          } else if (Array.isArray(detail) && detail[0]?.msg) {
            msg = detail[0].msg
          }
        } else if (err.message === 'Network Error' || !err.response) {
          msg = 'Impossible de joindre le serveur API FastAPI (Vérifiez la connexion réseau)'
        }
        this.error = msg
        throw new Error(msg)
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentUser(rememberMe = null) {
      if (!this.token) return null
      try {
        const user = await authService.getMe()
        this.user = user

        const isLocal = rememberMe === true || !!localStorage.getItem('btp_token')
        if (isLocal) {
          localStorage.setItem('btp_user', JSON.stringify(this.user))
          sessionStorage.removeItem('btp_user')
        } else {
          sessionStorage.setItem('btp_user', JSON.stringify(this.user))
          localStorage.removeItem('btp_user')
        }

        return this.user
      } catch (err) {
        this.logout()
        throw err
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.error = null

      localStorage.removeItem('btp_token')
      localStorage.removeItem('btp_user')
      sessionStorage.removeItem('btp_token')
      sessionStorage.removeItem('btp_user')
    },

    async updateProfile(profileData) {
      this.loading = true
      try {
        const updatedUser = await authService.updateMe(profileData)
        this.user = { ...this.user, ...updatedUser }

        if (localStorage.getItem('btp_token')) {
          localStorage.setItem('btp_user', JSON.stringify(this.user))
        } else if (sessionStorage.getItem('btp_token')) {
          sessionStorage.setItem('btp_user', JSON.stringify(this.user))
        }
        return this.user
      } finally {
        this.loading = false
      }
    },
  },
})
