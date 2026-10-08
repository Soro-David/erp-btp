import apiClient from './api'

export const chantierService = {
  /**
   * Récupère le prochain code chantier séquentiel disponible (ex: CH-2026-001)
   */
  async getNextCode() {
    const response = await apiClient.get('/chantiers/code/next')
    return response.data
  },

  /**
   * Récupère la liste des types de chantiers référentiels
   */
  async getTypes() {
    const response = await apiClient.get('/chantiers/types')
    return response.data
  },

  /**
   * Crée un nouveau type de chantier dynamique
   * @param {Object} payload { name, description }
   */
  async createType(payload) {
    const response = await apiClient.post('/chantiers/types', payload)
    return response.data
  },

  /**
   * Récupère la liste des responsables / intervenants
   * @param {string} [role] Filtrage optionnel par rôle
   */
  async getResponsables(role = null) {
    const params = role ? { role } : {}
    const response = await apiClient.get('/responsables', { params })
    return response.data
  },

  /**
   * Crée un nouveau responsable
   * @param {Object} payload { first_name, last_name, role_name, phone, email, company }
   */
  async createResponsable(payload) {
    const response = await apiClient.post('/responsables', payload)
    return response.data
  },

  /**
   * Récupère la liste des clients
   */
  async getClients() {
    const response = await apiClient.get('/clients')
    return response.data
  },

  /**
   * Crée un client
   */
  async createClient(payload) {
    const response = await apiClient.post('/clients', payload)
    return response.data
  },

  /**
   * Liste les chantiers
   */
  async getChantiers(params = {}) {
    const response = await apiClient.get('/chantiers', { params })
    return response.data
  },

  /**
   * Récupère les détails d'un chantier par son ID
   */
  async getChantier(id) {
    const response = await apiClient.get(`/chantiers/${id}`)
    return response.data
  },

  /**
   * Crée un nouveau chantier (ou brouillon)
   */
  async createChantier(payload) {
    const response = await apiClient.post('/chantiers', payload)
    return response.data
  },

  /**
   * Téléverse un document pour un chantier
   */
  async uploadDocument(chantierId, documentType, file) {
    const formData = new FormData()
    formData.append('document_type', documentType)
    formData.append('file', file)

    const response = await apiClient.post(`/chantiers/${chantierId}/documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

export default chantierService
