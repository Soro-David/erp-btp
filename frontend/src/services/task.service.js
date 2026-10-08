import apiClient from './api'

export const taskService = {
  // ---------------------------------------------------------------------------
  // 1. Codes
  // ---------------------------------------------------------------------------
  async getNextTaskCode(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/tasks/next-code`)
    return response.data
  },

  async getNextPhaseCode(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/phases/next-code`)
    return response.data
  },

  async getNextMilestoneCode(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/milestones/next-code`)
    return response.data
  },

  // ---------------------------------------------------------------------------
  // 2. Phases / Lots
  // ---------------------------------------------------------------------------
  async getPhases(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/phases`)
    return response.data
  },

  async createPhase(chantierId, payload) {
    const response = await apiClient.post(`/chantiers/${chantierId}/phases`, payload)
    return response.data
  },

  async updatePhase(phaseId, payload) {
    const response = await apiClient.put(`/phases/${phaseId}`, payload)
    return response.data
  },

  async deletePhase(phaseId) {
    const response = await apiClient.delete(`/phases/${phaseId}`)
    return response.data
  },

  // ---------------------------------------------------------------------------
  // 3. Tâches & Sous-tâches
  // ---------------------------------------------------------------------------
  async getTasks(chantierId, params = {}) {
    const response = await apiClient.get(`/chantiers/${chantierId}/tasks`, { params })
    return response.data
  },

  async getTaskTree(chantierId, params = {}) {
    const response = await apiClient.get(`/chantiers/${chantierId}/tasks/tree`, { params })
    return response.data
  },

  async getTask(taskId) {
    const response = await apiClient.get(`/tasks/${taskId}`)
    return response.data
  },

  async createTask(chantierId, payload) {
    const response = await apiClient.post(`/chantiers/${chantierId}/tasks`, payload)
    return response.data
  },

  async updateTask(taskId, payload) {
    const response = await apiClient.put(`/tasks/${taskId}`, payload)
    return response.data
  },

  async deleteTask(taskId) {
    const response = await apiClient.delete(`/tasks/${taskId}`)
    return response.data
  },

  async getTaskHistory(taskId) {
    const response = await apiClient.get(`/tasks/${taskId}/history`)
    return response.data
  },

  // ---------------------------------------------------------------------------
  // 4. Dépendances
  // ---------------------------------------------------------------------------
  async addDependency(successorId, payload) {
    const response = await apiClient.post(`/tasks/${successorId}/dependencies`, payload)
    return response.data
  },

  async deleteDependency(dependencyId) {
    const response = await apiClient.delete(`/task-dependencies/${dependencyId}`)
    return response.data
  },

  // ---------------------------------------------------------------------------
  // 5. Jalons
  // ---------------------------------------------------------------------------
  async getMilestones(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/milestones`)
    return response.data
  },

  async createMilestone(chantierId, payload) {
    const response = await apiClient.post(`/chantiers/${chantierId}/milestones`, payload)
    return response.data
  },

  async updateMilestone(milestoneId, payload) {
    const response = await apiClient.put(`/milestones/${milestoneId}`, payload)
    return response.data
  },

  async deleteMilestone(milestoneId) {
    const response = await apiClient.delete(`/milestones/${milestoneId}`)
    return response.data
  },

  // ---------------------------------------------------------------------------
  // 6. Planning & Recalcul
  // ---------------------------------------------------------------------------
  async getPlanning(chantierId) {
    const response = await apiClient.get(`/chantiers/${chantierId}/planning`)
    return response.data
  },

  async recalculatePlanning(chantierId) {
    const response = await apiClient.post(`/chantiers/${chantierId}/planning/recalculate`)
    return response.data
  },
}

export default taskService
