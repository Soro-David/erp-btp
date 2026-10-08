import apiClient from './api'

export const stockService = {
  /**
   * Lister les emplacements / dépôts
   */
  async getLocations(params = {}) {
    const response = await apiClient.get('/stocks/locations', { params })
    return response.data
  },

  /**
   * Créer un dépôt
   */
  async createLocation(payload) {
    const response = await apiClient.post('/stocks/locations', payload)
    return response.data
  },

  /**
   * Vue globale du stock par emplacement
   */
  async getStockOverview(locationId = null) {
    const params = locationId ? { location_id: locationId } : {}
    const response = await apiClient.get('/stocks/overview', { params })
    return response.data
  },

  /**
   * Historique & Journal des mouvements
   */
  async getMovements(params = {}) {
    const response = await apiClient.get('/stocks/movements', { params })
    return response.data
  },

  /**
   * Enregistrer un mouvement direct (ex: entrée directe, ajustement)
   */
  async createMovement(payload) {
    const response = await apiClient.post('/stocks/movements', payload)
    return response.data
  },

  /**
   * Sortie de stock vers un chantier et tâche
   */
  async issueStock(params) {
    const response = await apiClient.post('/stocks/issue', null, { params })
    return response.data
  },

  /**
   * Transfert entre dépôts
   */
  async transferStock(payload) {
    const response = await apiClient.post('/stocks/transfer', payload)
    return response.data
  },

  /**
   * Retour chantier vers dépôt
   */
  async returnStock(payload) {
    const response = await apiClient.post('/stocks/return', payload)
    return response.data
  },

  /**
   * Lister les inventaires
   */
  async getInventories(params = {}) {
    const response = await apiClient.get('/stocks/inventories', { params })
    return response.data
  },

  /**
   * Créer une session d'inventaire
   */
  async createInventory(payload) {
    const response = await apiClient.post('/stocks/inventories', payload)
    return response.data
  },

  /**
   * Détail d'un inventaire
   */
  async getInventoryById(id) {
    const response = await apiClient.get(`/stocks/inventories/${id}`)
    return response.data
  },

  /**
   * Valider un inventaire
   */
  async validateInventory(id) {
    const response = await apiClient.post(`/stocks/inventories/${id}/validate`)
    return response.data
  },

  /**
   * Statistiques dashboard stock
   */
  async getDashboardStats() {
    const response = await apiClient.get('/stocks/dashboard/stats')
    return response.data
  },
}

export default stockService
