import apiClient from './api'

export const dashboardService = {
  /**
   * Vue synthétique pour le Propriétaire / Direction Générale
   * @returns {Promise<Object>}
   */
  async getOwnerSummary() {
    const response = await apiClient.get('/owner/dashboard-summary')
    return response.data
  },

  /**
   * Vue synthétique pour la Direction Technique
   * @returns {Promise<Object>}
   */
  async getDirectorOverview() {
    const response = await apiClient.get('/director/projects-overview')
    return response.data
  },

  /**
   * Chantiers et tâches sous la responsabilité du Manager / Conducteur de travaux
   * @returns {Promise<Object>}
   */
  async getManagerSites() {
    const response = await apiClient.get('/manager/assigned-sites')
    return response.data
  },

  /**
   * Tâches du jour et saisies de terrain pour l'Ouvrier / Chef de chantier
   * @returns {Promise<Object>}
   */
  async getWorkerTasks() {
    const response = await apiClient.get('/worker/daily-tasks')
    return response.data
  },

  /**
   * Statut de santé de l'API FastAPI et de la base de données PostgreSQL
   * @returns {Promise<Object>}
   */
  async getHealth() {
    const response = await apiClient.get('/health')
    return response.data
  },
}

export default dashboardService
