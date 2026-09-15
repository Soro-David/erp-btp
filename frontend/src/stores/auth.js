import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('btp_token') || null,
    user: JSON.parse(localStorage.getItem('btp_user') || 'null'),
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    userName: (state) => state.user ? `${state.user.first_name} ${state.user.last_name}` : '',
  },

  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
          email,
          password,
        })
        const data = response.data
        this.token = data.access_token
        localStorage.setItem('btp_token', this.token)

        // Récupérer le profil complet de l'utilisateur
        await this.fetchCurrentUser()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Erreur lors de la connexion'
        throw new Error(this.error)
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentUser() {
      if (!this.token) return
      try {
        const response = await axios.get(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        this.user = response.data
        localStorage.setItem('btp_user', JSON.stringify(this.user))
      } catch (err) {
        this.logout()
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('btp_token')
      localStorage.removeItem('btp_user')
    },
  },
})
