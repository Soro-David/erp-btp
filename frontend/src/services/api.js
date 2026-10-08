import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
})

// Intercepteur de requête pour insérer le token JWT
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('btp_token') || sessionStorage.getItem('btp_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Intercepteur de réponse pour gérer l'expiration du token (401)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Si la requête 401 ne provient pas de l'écran de login lui-même
      const isLoginRequest = error.config?.url?.includes('/auth/login')
      if (!isLoginRequest) {
        localStorage.removeItem('btp_token')
        localStorage.removeItem('btp_user')
        sessionStorage.removeItem('btp_token')
        sessionStorage.removeItem('btp_user')
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
