<template>
  <div
    v-if="modelValue && task"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto"
    @click.self="close"
  >
    <div
      class="bg-white border border-slate-200 rounded-2xl w-full max-w-3xl my-6 p-6 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150 max-h-[90vh] flex flex-col"
    >
      <!-- En-tête -->
      <div class="flex items-start justify-between pb-3.5 mb-4 border-b border-slate-100 flex-shrink-0">
        <div class="space-y-1">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-mono text-xs font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
              {{ task.code }}
            </span>
            <span
              class="text-[11px] font-bold px-2 py-0.5 rounded-full"
              :class="{
                'bg-emerald-50 text-emerald-700 border border-emerald-200': task.status === 'Terminée',
                'bg-blue-50 text-blue-700 border border-blue-200': task.status === 'En cours',
                'bg-amber-50 text-amber-700 border border-amber-200': task.status === 'En attente' || task.status === 'À faire',
                'bg-rose-50 text-rose-700 border border-rose-200': task.status === 'Bloquée',
                'bg-slate-100 text-slate-600': task.status === 'Annulée',
              }"
            >
              {{ task.status }}
            </span>
            <span
              class="text-[11px] font-bold px-2 py-0.5 rounded-full"
              :class="{
                'bg-slate-100 text-slate-600': task.priority === 'Faible',
                'bg-blue-100 text-blue-700': task.priority === 'Normale',
                'bg-amber-100 text-amber-800': task.priority === 'Importante',
                'bg-rose-100 text-rose-800': task.priority === 'Critique',
              }"
            >
              Priorité : {{ task.priority }}
            </span>
            <span v-if="task.delay_days > 0" class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-rose-500 text-white flex items-center gap-1 animate-pulse">
              <fas-icon icon="triangle-exclamation" class="text-[10px]" />
              Retard : {{ task.delay_days }} j
            </span>
          </div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900">{{ task.name }}</h2>
          <p class="text-xs text-slate-500">
            Phase : <strong class="text-slate-700">{{ task.phase_name || 'Non spécifiée' }}</strong>
            <span v-if="task.parent_task_name"> | Sous-tâche de : <strong class="text-slate-700">{{ task.parent_task_name }}</strong></span>
          </p>
        </div>

        <button
          type="button"
          @click="close"
          class="text-slate-400 hover:text-slate-700 p-1 transition-colors"
          title="Fermer"
        >
          <fas-icon icon="xmark" class="text-lg" />
        </button>
      </div>

      <!-- Navigation Onglets Détails / Historique -->
      <div class="flex items-center gap-4 border-b border-slate-100 pb-2 mb-4 text-xs font-bold flex-shrink-0">
        <button
          type="button"
          @click="activeTab = 'general'"
          class="pb-1 border-b-2 transition-colors flex items-center gap-1.5"
          :class="activeTab === 'general' ? 'border-[#1d4ed8] text-[#1d4ed8]' : 'border-transparent text-slate-400 hover:text-slate-700'"
        >
          <fas-icon icon="sliders" />
          <span>Suivi & Paramètres</span>
        </button>
        <button
          type="button"
          @click="loadHistory"
          class="pb-1 border-b-2 transition-colors flex items-center gap-1.5"
          :class="activeTab === 'history' ? 'border-[#1d4ed8] text-[#1d4ed8]' : 'border-transparent text-slate-400 hover:text-slate-700'"
        >
          <fas-icon icon="clock-rotate-left" />
          <span>Journal des modifications</span>
        </button>
      </div>

      <!-- CONTENU ONGLET 1 : SUIVI & PARAMÈTRES -->
      <div v-if="activeTab === 'general'" class="space-y-5 overflow-y-auto pr-1 flex-1">
        <!-- Barre de Progression & Statut Rapide -->
        <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">Avancement Réalisé</span>
            <span class="text-sm font-black font-mono text-[#1d4ed8]">{{ editForm.progress }}%</span>
          </div>

          <div class="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-300"
              :class="editForm.progress >= 100 ? 'bg-emerald-500' : 'bg-[#1d4ed8]'"
              :style="{ width: editForm.progress + '%' }"
            ></div>
          </div>

          <div class="flex items-center gap-3">
            <input
              v-model.number="editForm.progress"
              type="range"
              min="0"
              max="100"
              step="5"
              class="w-full accent-[#1d4ed8]"
              @input="onProgressChange"
            />
            <div class="flex items-center gap-1">
              <button
                type="button"
                @click="setProgress(25)"
                class="px-2 py-0.5 text-[10px] font-bold rounded bg-white border border-slate-200 hover:bg-slate-50"
              >25%</button>
              <button
                type="button"
                @click="setProgress(50)"
                class="px-2 py-0.5 text-[10px] font-bold rounded bg-white border border-slate-200 hover:bg-slate-50"
              >50%</button>
              <button
                type="button"
                @click="setProgress(75)"
                class="px-2 py-0.5 text-[10px] font-bold rounded bg-white border border-slate-200 hover:bg-slate-50"
              >75%</button>
              <button
                type="button"
                @click="setProgress(100)"
                class="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-600 text-white hover:bg-emerald-700"
              >100%</button>
            </div>
          </div>
        </div>

        <!-- Statut, Priorité & Responsable -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Statut</label>
            <select
              v-model="editForm.status"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
              @change="onStatusChange"
            >
              <option value="À faire">À faire</option>
              <option value="En cours">En cours</option>
              <option value="En attente">En attente</option>
              <option value="Bloquée">Bloquée</option>
              <option value="Terminée">Terminée</option>
              <option value="Annulée">Annulée</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Priorité</label>
            <select
              v-model="editForm.priority"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option value="Faible">Faible</option>
              <option value="Normale">Normale</option>
              <option value="Importante">Importante</option>
              <option value="Critique">Critique</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Responsable</label>
            <select
              v-model="editForm.responsible_id"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option :value="null">-- Non assigné --</option>
              <option v-for="r in responsables" :key="r.id" :value="r.id">
                {{ r.first_name }} {{ r.last_name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Dates de Réalisation & Retard -->
        <div class="border border-slate-100 rounded-xl p-3.5 bg-slate-50/50 space-y-3">
          <div class="flex items-center justify-between text-xs font-bold text-slate-600">
            <span>Dates & Calendrier d'Exécution</span>
            <span class="text-slate-400 font-normal">Durée : {{ task.estimated_duration_days }} jours</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 mb-1">Début prévisionnel</label>
              <input
                v-model="editForm.planned_start_date"
                type="date"
                class="w-full px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-800"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 mb-1">Fin prévisionnelle</label>
              <input
                v-model="editForm.planned_end_date"
                type="date"
                class="w-full px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-800"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 mb-1">Début effectif (réel)</label>
              <input
                v-model="editForm.actual_start_date"
                type="date"
                class="w-full px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-800"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 mb-1">Fin effective (réelle)</label>
              <input
                v-model="editForm.actual_end_date"
                type="date"
                class="w-full px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-800"
              />
            </div>
          </div>
        </div>

        <!-- Blocage & Alerte -->
        <div class="border border-rose-200 rounded-xl p-3.5 bg-rose-50/40 space-y-2">
          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer text-xs font-bold text-rose-800">
              <input
                type="checkbox"
                v-model="editForm.is_blocked"
                class="rounded text-rose-600 focus:ring-rose-500"
              />
              <span>Signaler comme Bloquée</span>
            </label>
            <span v-if="task.is_blocked" class="text-[10px] font-bold text-rose-600 uppercase">Blocage actif</span>
          </div>

          <div v-if="editForm.is_blocked" class="space-y-2 pt-1">
            <input
              v-model="editForm.blocking_reason"
              type="text"
              placeholder="Motif du blocage..."
              class="w-full px-3 py-1.5 rounded-lg bg-white border border-rose-200 text-xs text-slate-900"
            />
            <input
              v-model="editForm.blocking_impact"
              type="text"
              placeholder="Impact potentiel sur le chantier..."
              class="w-full px-3 py-1.5 rounded-lg bg-white border border-rose-200 text-xs text-slate-900"
            />
          </div>
        </div>

        <!-- Dépendances (Fin -> Début) -->
        <div class="border border-slate-200 rounded-xl p-3.5 bg-white space-y-2.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5 text-xs font-bold text-slate-800">
              <fas-icon icon="link" class="text-blue-600" />
              <span>Dépendances antérieures (Doivent être finies avant)</span>
            </div>
          </div>

          <div v-if="task.dependencies && task.dependencies.length > 0" class="divide-y divide-slate-100">
            <div
              v-for="dep in task.dependencies"
              :key="dep.id"
              class="flex items-center justify-between py-1.5 text-xs"
            >
              <div class="flex items-center gap-2">
                <span class="font-mono font-bold text-slate-500">{{ dep.predecessor_code }}</span>
                <span class="text-slate-800 font-medium">{{ dep.predecessor_name }}</span>
                <span
                  class="text-[10px] px-1.5 py-0.2 rounded font-bold"
                  :class="dep.predecessor_status === 'Terminée' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'"
                >
                  {{ dep.predecessor_status }} ({{ dep.predecessor_progress }}%)
                </span>
              </div>
              <button
                type="button"
                @click="removeDependency(dep.id)"
                class="text-slate-400 hover:text-rose-600 p-1"
                title="Supprimer la dépendance"
              >
                <fas-icon icon="trash-can" />
              </button>
            </div>
          </div>
          <p v-else class="text-xs text-slate-400 italic">Aucune dépendance configurée.</p>
        </div>

        <!-- Sous-tâches -->
        <div class="border border-slate-200 rounded-xl p-3.5 bg-white space-y-2.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5 text-xs font-bold text-slate-800">
              <fas-icon icon="diagram-project" class="text-blue-600" />
              <span>Sous-tâches ({{ task.subtasks ? task.subtasks.length : 0 }})</span>
            </div>
            <button
              type="button"
              @click="$emit('requestAddSubtask', task)"
              class="text-[11px] text-[#1d4ed8] font-bold hover:underline flex items-center gap-1"
            >
              <fas-icon icon="plus" class="text-[9px]" />
              <span>Ajouter une sous-tâche</span>
            </button>
          </div>

          <div v-if="task.subtasks && task.subtasks.length > 0" class="space-y-2">
            <div
              v-for="sub in task.subtasks"
              :key="sub.id"
              class="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-100 text-xs"
            >
              <div class="flex items-center gap-2 flex-1">
                <span class="font-mono font-bold text-slate-400">{{ sub.code }}</span>
                <span class="font-medium text-slate-800">{{ sub.name }}</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="font-mono font-bold text-slate-600">{{ sub.progress }}%</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded" :class="sub.status === 'Terminée' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'">
                  {{ sub.status }}
                </span>
              </div>
            </div>
          </div>
          <p v-else class="text-xs text-slate-400 italic">Aucune sous-tâche rattachée.</p>
        </div>
      </div>

      <!-- CONTENU ONGLET 2 : HISTORIQUE -->
      <div v-else-if="activeTab === 'history'" class="space-y-3 overflow-y-auto pr-1 flex-1">
        <div v-if="loadingHistory" class="py-12 text-center text-slate-400 text-xs">
          <fas-icon icon="spinner" class="animate-spin text-lg mb-2" />
          <p>Chargement du journal d'audit...</p>
        </div>

        <div v-else-if="historyList.length > 0" class="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
          <div v-for="h in historyList" :key="h.id" class="relative text-xs">
            <div class="absolute -left-6 top-1 w-3 h-3 rounded-full bg-[#1d4ed8] border-2 border-white ring-2 ring-blue-100"></div>
            <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100 space-y-1">
              <div class="flex items-center justify-between text-[11px] text-slate-400">
                <span class="font-bold text-slate-700">{{ h.user_name || 'Utilisateur' }}</span>
                <span>{{ formatDate(h.created_at) }}</span>
              </div>
              <div class="text-slate-700">
                <span class="font-semibold text-slate-900">{{ h.field_name }}</span> :
                <span class="text-rose-600 line-through mr-1" v-if="h.old_value">{{ h.old_value }}</span>
                <span class="text-emerald-600 font-bold" v-if="h.new_value">{{ h.new_value }}</span>
              </div>
              <p v-if="h.comment" class="text-[11px] text-slate-500 italic">{{ h.comment }}</p>
            </div>
          </div>
        </div>

        <div v-else class="py-12 text-center text-slate-400 text-xs italic">
          Aucun historique enregistré pour le moment.
        </div>
      </div>

      <!-- Actions Pied de page -->
      <div class="flex items-center justify-between pt-4 border-t border-slate-100 flex-shrink-0">
        <button
          type="button"
          @click="confirmDelete"
          class="px-3.5 py-2 rounded-xl text-xs font-semibold text-rose-600 hover:bg-rose-50 transition-colors flex items-center gap-1.5"
          :disabled="loading"
        >
          <fas-icon icon="trash-can" />
          <span>Supprimer</span>
        </button>

        <div class="flex items-center gap-2">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
            :disabled="loading"
          >
            Fermer
          </button>
          <button
            type="button"
            @click="saveChanges"
            :disabled="loading"
            class="px-5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <fas-icon v-if="loading" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check" />
            <span>{{ loading ? 'Sauvegarde...' : 'Enregistrer les modifications' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { taskService } from '@/services'
import { toast, confirm } from '@/utils/alert'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  task: {
    type: Object,
    default: null,
  },
  responsables: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue', 'updated', 'deleted', 'requestAddSubtask'])

const activeTab = ref('general')
const loading = ref(false)
const loadingHistory = ref(false)
const historyList = ref([])

const editForm = reactive({
  status: 'À faire',
  priority: 'Normale',
  progress: 0,
  responsible_id: null,
  planned_start_date: '',
  planned_end_date: '',
  actual_start_date: '',
  actual_end_date: '',
  is_blocked: false,
  blocking_reason: '',
  blocking_impact: '',
})

watch(
  () => props.task,
  (t) => {
    if (t) {
      activeTab.value = 'general'
      editForm.status = t.status || 'À faire'
      editForm.priority = t.priority || 'Normale'
      editForm.progress = Number(t.progress) || 0
      editForm.responsible_id = t.responsible_id || null
      editForm.planned_start_date = t.planned_start_date || ''
      editForm.planned_end_date = t.planned_end_date || ''
      editForm.actual_start_date = t.actual_start_date || ''
      editForm.actual_end_date = t.actual_end_date || ''
      editForm.is_blocked = !!t.is_blocked
      editForm.blocking_reason = t.blocking_reason || ''
      editForm.blocking_impact = t.blocking_impact || ''
    }
  },
  { immediate: true }
)

function close() {
  emit('update:modelValue', false)
}

function setProgress(val) {
  editForm.progress = val
  onProgressChange()
}

function onProgressChange() {
  if (editForm.progress >= 100) {
    editForm.status = 'Terminée'
    if (!editForm.actual_end_date) {
      editForm.actual_end_date = new Date().toISOString().split('T')[0]
    }
  } else if (editForm.progress > 0 && editForm.status === 'À faire') {
    editForm.status = 'En cours'
  } else if (editForm.progress === 0 && editForm.status === 'Terminée') {
    editForm.status = 'À faire'
  }
}

function onStatusChange() {
  if (editForm.status === 'Terminée') {
    editForm.progress = 100
    if (!editForm.actual_end_date) {
      editForm.actual_end_date = new Date().toISOString().split('T')[0]
    }
  } else if (editForm.status === 'Bloquée') {
    editForm.is_blocked = true
  } else if (editForm.status === 'À faire' && editForm.progress > 0) {
    editForm.progress = 0
  }
}

async function loadHistory() {
  activeTab.value = 'history'
  if (!props.task?.id) return
  loadingHistory.value = true
  try {
    historyList.value = await taskService.getTaskHistory(props.task.id)
  } catch (err) {
    toast("Impossible de charger l'historique", 'error')
  } finally {
    loadingHistory.value = false
  }
}

async function saveChanges() {
  if (!props.task?.id) return
  loading.value = true
  try {
    const updated = await taskService.updateTask(props.task.id, {
      status: editForm.status,
      priority: editForm.priority,
      progress: Number(editForm.progress),
      responsible_id: editForm.responsible_id ? Number(editForm.responsible_id) : null,
      planned_start_date: editForm.planned_start_date || undefined,
      planned_end_date: editForm.planned_end_date || undefined,
      actual_start_date: editForm.actual_start_date || null,
      actual_end_date: editForm.actual_end_date || null,
      is_blocked: editForm.is_blocked,
      blocking_reason: editForm.is_blocked ? editForm.blocking_reason : null,
      blocking_impact: editForm.is_blocked ? editForm.blocking_impact : null,
    })
    toast('Tâche mise à jour avec succès', 'success')
    emit('updated', updated)
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la mise à jour'
    toast(typeof detail === 'string' ? detail : 'Erreur de mise à jour', 'error')
  } finally {
    loading.value = false
  }
}

async function removeDependency(depId) {
  try {
    await taskService.deleteDependency(depId)
    toast('Dépendance supprimée', 'success')
    const refetched = await taskService.getTask(props.task.id)
    emit('updated', refetched)
  } catch (err) {
    toast('Erreur lors de la suppression de la dépendance', 'error')
  }
}

async function confirmDelete() {
  const isConfirmed = await confirm(
    'Supprimer cette tâche ?',
    `Voulez-vous vraiment supprimer la tâche « ${props.task.name} » ? Ses éventuelles sous-tâches et dépendances seront également supprimées.`,
    'Supprimer'
  )
  if (isConfirmed) {
    loading.value = true
    try {
      await taskService.deleteTask(props.task.id)
      toast('Tâche supprimée avec succès', 'success')
      emit('deleted', props.task.id)
      close()
    } catch (err) {
      toast('Erreur lors de la suppression', 'error')
    } finally {
      loading.value = false
    }
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
