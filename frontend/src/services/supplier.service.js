import apiClient from './api'

export const supplierService = {
  /**
   * Lister les fournisseurs avec filtres optionnels
   */
  async getSuppliers(params = {}) {
    const response = await apiClient.get('/suppliers', { params })
    return response.data
  },

  /**
   * Récupérer un fournisseur par son identifiant
   */
  async getSupplierById(id) {
    const response = await apiClient.get(`/suppliers/${id}`)
    return response.data
  },

  /**
   * Créer un nouveau fournisseur
   */
  async createSupplier(payload) {
    const response = await apiClient.post('/suppliers', payload)
    return response.data
  },

  /**
   * Mettre à jour un fournisseur existant
   */
  async updateSupplier(id, payload) {
    const response = await apiClient.put(`/suppliers/${id}`, payload)
    return response.data
  },

  /**
   * Supprimer ou désactiver un fournisseur
   */
  async deleteSupplier(id) {
    const response = await apiClient.delete(`/suppliers/${id}`)
    return response.data
  },

  /**
   * Récupérer les statistiques financières d'un fournisseur
   */
  async getSupplierStats(id) {
    const response = await apiClient.get(`/suppliers/${id}/stats`)
    return response.data
  },
}

export default supplierService
