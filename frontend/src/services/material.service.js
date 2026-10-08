import apiClient from './api'

export const materialService = {
  /**
   * Lister les matériaux avec calcul du stock
   */
  async getMaterials(params = {}) {
    const response = await apiClient.get('/materials', { params })
    return response.data
  },

  /**
   * Détail d'un matériau
   */
  async getMaterialById(id) {
    const response = await apiClient.get(`/materials/${id}`)
    return response.data
  },

  /**
   * Créer un matériau
   */
  async createMaterial(payload) {
    const response = await apiClient.post('/materials', payload)
    return response.data
  },

  /**
   * Modifier un matériau
   */
  async updateMaterial(id, payload) {
    const response = await apiClient.put(`/materials/${id}`, payload)
    return response.data
  },

  /**
   * Supprimer un matériau
   */
  async deleteMaterial(id) {
    const response = await apiClient.delete(`/materials/${id}`)
    return response.data
  },

  /**
   * Lister les catégories de matériaux
   */
  async getCategories() {
    const response = await apiClient.get('/materials/categories')
    return response.data
  },

  /**
   * Créer une catégorie dynamique
   */
  async createCategory(payload) {
    const response = await apiClient.post('/materials/categories', payload)
    return response.data
  },

  /**
   * Lister les unités de mesure
   */
  async getUnits() {
    const response = await apiClient.get('/materials/units')
    return response.data
  },

  /**
   * Créer une unité de mesure dynamique
   */
  async createUnit(payload) {
    const response = await apiClient.post('/materials/units', payload)
    return response.data
  },
}

export default materialService
