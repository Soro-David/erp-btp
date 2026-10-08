import apiClient from './api'

export const userService = {
  /**
   * Récupère la liste des utilisateurs avec pagination et filtres optionnels
   * @param {Object} params - { skip, limit, role, is_active }
   * @returns {Promise<Array>} Liste d'utilisateurs
   */
  async getUsers(params = {}) {
    const response = await apiClient.get('/superadmin/users', { params })
    return response.data
  },

  /**
   * Récupère les détails d'un utilisateur par son ID
   * @param {number|string} id
   * @returns {Promise<Object>}
   */
  async getUserById(id) {
    const response = await apiClient.get(`/superadmin/users/${id}`)
    return response.data
  },

  /**
   * Crée un nouvel utilisateur (SuperAdmin, Owner, Director, Manager, Worker)
   * @param {Object} userData - { email, first_name, last_name, phone, role, password }
   * @returns {Promise<Object>} Utilisateur créé
   */
  async createUser(userData) {
    const response = await apiClient.post('/superadmin/users', userData)
    return response.data
  },

  /**
   * Met à jour les informations d'un utilisateur
   * @param {number|string} id
   * @param {Object} userData
   * @returns {Promise<Object>} Utilisateur mis à jour
   */
  async updateUser(id, userData) {
    const response = await apiClient.put(`/superadmin/users/${id}`, userData)
    return response.data
  },

  /**
   * Invite un profil Propriétaire (Owner) et lui envoie un email d'activation
   * @param {Object} data - { email, first_name, last_name }
   * @returns {Promise<Object>} { user, invitation_link, message }
   */
  async inviteOwner(data) {
    const response = await apiClient.post('/superadmin/invite-owner', data)
    return response.data
  },

  /**
   * Renvoie un email d'invitation avec un nouveau jeton d'activation
   * @param {number|string} id
   * @returns {Promise<Object>} { user, invitation_link, message }
   */
  async resendInvitation(id) {
    const response = await apiClient.post(`/superadmin/users/${id}/resend-invitation`)
    return response.data
  },

  /**
   * Supprime un utilisateur
   * @param {number|string} id
   * @returns {Promise<Object>}
   */
  async deleteUser(id) {
    const response = await apiClient.delete(`/superadmin/users/${id}`)
    return response.data
  },
}

export default userService
