<template>
  <div class="space-y-6">
    <!-- En-tête Vue Planning & Gantt -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="chart-gantt" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Planning Directeur & Gantt BTP</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">Directeur</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Ordonnancement chronologique, gestion des chemins critiques et suivi des jalons de chantier
          </p>
        </div>
      </div>

      <!-- Sélecteur de Chantier & Liens Rapides -->
      <div class="flex items-center gap-3">
        <select
          v-model="selectedChantierId"
          class="px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold text-slate-800 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all shadow-xs"
          @change="loadChantierPlanning"
        >
          <option v-for="c in chantiersList" :key="c.id" :value="c.id">
            {{ c.code }} - {{ c.name }}
          </option>
        </select>

        <router-link
          :to="{ path: '/chantiers/taches', query: { chantier_id: selectedChantierId } }"
          class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold shadow-xs flex items-center gap-1.5 transition-colors"
        >
          <fas-icon icon="list" />
          <span>Gestion des Tâches</span>
        </router-link>

        <button
          type="button"
          @click="openAddTaskModal()"
          class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all"
        >
          <fas-icon icon="plus" />
          <span>Nouvelle tâche</span>
        </button>
      </div>
    </div>

    <!-- Synthèse Avancement & Métriques Clés -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Avancement Global</span>
          <fas-icon icon="gauge-high" class="text-blue-600" />
        </div>
        <div class="text-2xl font-black text-slate-900 font-mono">{{ Math.round(planningData.physical_progress || 0) }}%</div>
        <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden mt-2">
          <div class="h-full bg-[#1d4ed8] rounded-full" :style="{ width: (planningData.physical_progress || 0) + '%' }"></div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Tâches Réalisées</span>
          <fas-icon icon="check-double" class="text-emerald-500" />
        </div>
        <div class="text-2xl font-black text-emerald-600 font-mono">
          {{ planningData.completed_tasks || 0 }} / {{ planningData.total_tasks || 0 }}
        </div>
        <span class="text-[11px] text-slate-400 mt-1 block">Tâches contractuelles terminées</span>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs" :class="{ 'border-rose-200 bg-rose-50/20': planningData.delayed_tasks > 0 }">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Retards Détectés</span>
          <fas-icon icon="triangle-exclamation" class="text-rose-500" />
        </div>
        <div class="text-2xl font-black text-rose-600 font-mono">{{ planningData.delayed_tasks || 0 }}</div>
        <span class="text-[11px] font-semibold text-rose-600 mt-1 block">
          {{ planningData.delayed_tasks > 0 ? 'Tâches en dépassement' : 'Planning conforme aux délais' }}
        </span>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Jalons Stratégiques</span>
          <fas-icon icon="flag" class="text-amber-500" />
        </div>
        <div class="text-2xl font-black text-amber-600 font-mono">{{ planningData.milestones ? planningData.milestones.length : 0 }}</div>
        <span class="text-[11px] text-slate-400 mt-1 block">Points d'arrêt et réceptions</span>
      </div>
    </div>

    <!-- Composant Gantt Chart Interactif -->
    <GanttChart
      :phases="planningData.phases || []"
      :tasks-tree="planningData.tasks_tree || []"
      :milestones="planningData.milestones || []"
      @select-task="openTaskDetail"
    />

    <!-- Timeline des Jalons Clés Contractuels -->
    <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 class="text-sm font-bold text-slate-900">Jalons & Engagements Contractuels</h3>
          <p class="text-xs text-slate-500">Dates cibles contractuelles pour le chantier {{ planningData.chantier_name }}</p>
        </div>
        <button
          type="button"
          @click="showAddMilestoneModal = true"
          class="px-3 py-1.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5"
        >
          <fas-icon icon="flag" />
          <span>Ajouter jalon</span>
        </button>
      </div>

      <div v-if="planningData.milestones && planningData.milestones.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div
          v-for="m in planningData.milestones"
          :key="m.id"
          class="p-3.5 rounded-xl border border-slate-200 hover:border-amber-400 transition-all bg-slate-50/50 space-y-2"
        >
          <div class="flex items-center justify-between">
            <span class="font-mono text-xs font-bold text-amber-800 bg-amber-100/70 px-2 py-0.5 rounded">{{ m.code }}</span>
            <span
              class="text-[10px] font-bold px-2 py-0.5 rounded"
              :class="{
                'bg-emerald-100 text-emerald-800': m.status === 'Atteint',
                'bg-amber-100 text-amber-800': m.status === 'À venir',
                'bg-rose-100 text-rose-800': m.status === 'En retard',
              }"
            >
              {{ m.status }}
            </span>
          </div>
          <h4 class="font-bold text-xs text-slate-900">{{ m.name }}</h4>
          <div class="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-200/60">
            <span>Prévu le : <strong>{{ formatDate(m.planned_date) }}</strong></span>
            <span>{{ m.responsible_name || 'Non assigné' }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-6 text-slate-400 text-xs italic">
        Aucun jalon enregistré pour ce chantier.
      </div>
    </div>

    <!-- Modals -->
    <AddTaskModal
      v-model="showAddTaskModal"
      :chantier-id="selectedChantierId"
      :phases="planningData.phases || []"
      :tasks="allFlatTasks"
      :responsables="responsablesList"
      @created="loadChantierPlanning"
      @request-add-phase="showAddPhaseModal = true"
    />

    <AddPhaseModal
      v-model="showAddPhaseModal"
      :chantier-id="selectedChantierId"
      :responsables="responsablesList"
      @created="loadChantierPlanning"
    />

    <AddMilestoneModal
      v-model="showAddMilestoneModal"
      :chantier-id="selectedChantierId"
      :responsables="responsablesList"
      @created="loadChantierPlanning"
    />

    <TaskDetailModal
      v-model="showTaskDetailModal"
      :task="selectedTask"
      :responsables="responsablesList"
      @updated="loadChantierPlanning"
      @deleted="loadChantierPlanning"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { chantierService, taskService } from '@/services'
import { toast } from '@/utils/alert'

import GanttChart from './components/GanttChart.vue'
import AddTaskModal from './components/AddTaskModal.vue'
import AddPhaseModal from './components/AddPhaseModal.vue'
import AddMilestoneModal from './components/AddMilestoneModal.vue'
import TaskDetailModal from './components/TaskDetailModal.vue'

const route = useRoute()

const chantiersList = ref([])
const selectedChantierId = ref(null)
const responsablesList = ref([])

const showAddTaskModal = ref(false)
const showAddPhaseModal = ref(false)
const showAddMilestoneModal = ref(false)
const showTaskDetailModal = ref(false)
const selectedTask = ref(null)

const planningData = reactive({
  chantier_id: null,
  chantier_code: '',
  chantier_name: '',
  physical_progress: 0,
  total_phases: 0,
  total_tasks: 0,
  completed_tasks: 0,
  delayed_tasks: 0,
  blocked_tasks: 0,
  phases: [],
  tasks_tree: [],
  milestones: [],
})

const allFlatTasks = computed(() => {
  const result = []
  function flatten(tasks) {
    tasks.forEach((t) => {
      result.push(t)
      if (t.subtasks && t.subtasks.length > 0) {
        flatten(t.subtasks)
      }
    })
  }
  flatten(planningData.tasks_tree || [])
  return result
})

async function loadChantiers() {
  try {
    const data = await chantierService.getChantiers()
    const list = data.items || data || []
    chantiersList.value = list

    if (list.length > 0) {
      const paramId = route.query.chantier_id
      if (paramId && list.some((c) => c.id === Number(paramId))) {
        selectedChantierId.value = Number(paramId)
      } else {
        selectedChantierId.value = list[0].id
      }
      await loadChantierPlanning()
    }
  } catch (err) {
    toast('Erreur lors du chargement des chantiers', 'error')
  }
}

async function loadResponsables() {
  try {
    responsablesList.value = await chantierService.getResponsables()
  } catch (err) {
    console.error(err)
  }
}

async function loadChantierPlanning() {
  if (!selectedChantierId.value) return
  try {
    const plan = await taskService.getPlanning(selectedChantierId.value)
    Object.assign(planningData, plan)
  } catch (err) {
    toast('Erreur lors du chargement du planning', 'error')
  }
}

function openAddTaskModal() {
  showAddTaskModal.value = true
}

function openTaskDetail(task) {
  selectedTask.value = task
  showTaskDetailModal.value = true
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

onMounted(async () => {
  await loadResponsables()
  await loadChantiers()
})
</script>
