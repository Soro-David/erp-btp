import apiClient from './api'

export const purchaseService = {
  /**
   * Lister les achats avec filtres
   */
  async getPurchases(params = {}) {
    const response = await apiClient.get('/purchases', { params })
    return response.data
  },

  /**
   * Détail complet d'un achat
   */
  async getPurchaseById(id) {
    const response = await apiClient.get(`/purchases/${id}`)
    return response.data
  },

  /**
   * Créer un achat standard
   */
  async createPurchase(payload) {
    const response = await apiClient.post('/purchases', payload)
    return response.data
  },

  /**
   * Créer un achat rapide terrain
   */
  async createQuickPurchase(payload) {
    const response = await apiClient.post('/purchases/quick', payload)
    return response.data
  },

  /**
   * Modifier un achat
   */
  async updatePurchase(id, payload) {
    const response = await apiClient.put(`/purchases/${id}`, payload)
    return response.data
  },

  /**
   * Supprimer un achat
   */
  async deletePurchase(id) {
    const response = await apiClient.delete(`/purchases/${id}`)
    return response.data
  },

  /**
   * Enregistrer une réception
   */
  async createReceipt(purchaseId, payload) {
    const response = await apiClient.post(`/purchases/${purchaseId}/receipts`, payload)
    return response.data
  },

  /**
   * Téléverser un document / justificatif
   */
  async uploadDocument(purchaseId, formData) {
    const response = await apiClient.post(`/purchases/${purchaseId}/documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Supprimer un document
   */
  async deleteDocument(documentId) {
    const response = await apiClient.delete(`/purchases/documents/${documentId}`)
    return response.data
  },

  /**
   * Statistiques dashboard achats
   */
  async getDashboardStats() {
    const response = await apiClient.get('/purchases/dashboard/stats')
    return response.data
  },

  /**
   * Consommation d'un chantier
   */
  async getChantierConsumption(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/consumption`)
    return response.data
  },
}

export default purchaseService
