import apiClient from './api'

export const authService = {
  /**
   * Authentifie un utilisateur avec son email et son mot de passe
   * @param {Object} credentials - { email, password }
   * @returns {Promise<Object>} { access_token, token_type, role, user_id, email }
   */
  async login(credentials) {
    const response = await apiClient.post('/auth/login', {
      email: credentials.email.trim(),
      password: credentials.password,
    })
    return response.data
  },

  /**
   * Récupère le profil de l'utilisateur actuellement connecté
   * @returns {Promise<Object>} UserResponse
   */
  async getMe() {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  /**
   * Vérifie la validité d'un jeton d'invitation et récupère les données pré-remplies
   * @param {string} token
   * @returns {Promise<Object>} { email, first_name, last_name }
   */
  async getInvitationInfo(token) {
    const response = await apiClient.get('/auth/invitation-info', {
      params: { token },
    })
    return response.data
  },

  /**
   * Finalise l'inscription de l'Owner avec son mot de passe et ses coordonnées
   * @param {Object} data - { token, first_name, last_name, phone, password, company_name, company_logo }
   * @returns {Promise<Object>} Token
   */
  async completeInvitation(data) {
    const response = await apiClient.post('/auth/complete-invitation', data)
    return response.data
  },

  /**
   * Met à jour le profil de l'utilisateur connecté (nom, prénom, téléphone, nom d'entreprise, logo)
   * @param {Object} data - { first_name, last_name, phone, company_name, company_logo }
   * @returns {Promise<Object>} UserResponse
   */
  async updateMe(data) {
    const response = await apiClient.put('/auth/me', data)
    return response.data
  },
}

export default authService
