<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto"
    @click.self="close"
  >
    <div
      class="bg-white border border-slate-200 rounded-2xl w-full max-w-3xl my-6 p-6 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150 max-h-[90vh] flex flex-col"
    >
      <!-- En-tête -->
      <div class="flex items-center justify-between pb-3.5 mb-4 border-b border-slate-100 flex-shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-lg">
            <fas-icon icon="list-check" />
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900">
              {{ defaultParentTaskId ? 'Ajouter une Sous-tâche' : 'Créer une Nouvelle Tâche' }}
            </h3>
            <p class="text-xs text-slate-500">Planification des travaux, affectation et suivi opérationnel</p>
          </div>
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

      <!-- Corps du formulaire avec scroll -->
      <form @submit.prevent="handleSubmit" class="space-y-6 overflow-y-auto pr-1 flex-1">
        <!-- SECTION 1 : IDENTIFICATION & RATTACHEMENT -->
        <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-100 space-y-3">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/60 pb-1.5">
            <fas-icon icon="circle-info" class="text-[#1d4ed8]" />
            <span>1. Identification & Rattachement</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Code</label>
              <input
                v-model="form.code"
                type="text"
                placeholder="TSK-2026-..."
                class="w-full px-3 py-2 rounded-xl bg-slate-200/60 border border-slate-200 text-slate-800 text-xs font-mono font-bold focus:outline-none"
              />
            </div>
            <div class="sm:col-span-3">
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Intitulé de la tâche <span class="text-rose-500">*</span>
              </label>
              <input
                v-model="form.name"
                type="text"
                required
                placeholder="Ex: Coulage béton radier, Pose disjoncteurs..."
                class="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
                :class="{ 'border-rose-400': errors.name }"
              />
              <p v-if="errors.name" class="text-[11px] text-rose-500 mt-1">{{ errors.name }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <!-- Phase / Lot -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block text-xs font-bold text-slate-700">
                  Phase / Lot <span class="text-rose-500">*</span>
                </label>
                <button
                  type="button"
                  @click="$emit('requestAddPhase')"
                  class="text-[11px] text-[#1d4ed8] font-bold hover:underline flex items-center gap-1"
                >
                  <fas-icon icon="plus" class="text-[9px]" />
                  <span>Ajouter une phase</span>
                </button>
              </div>
              <select
                v-model="form.phase_id"
                required
                class="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:border-blue-600"
                :class="{ 'border-rose-400': errors.phase_id }"
              >
                <option :value="null" disabled>Sélectionner une phase</option>
                <option v-for="p in phases" :key="p.id" :value="p.id">
                  {{ p.code }} - {{ p.name }}
                </option>
              </select>
              <p v-if="errors.phase_id" class="text-[11px] text-rose-500 mt-1">{{ errors.phase_id }}</p>
            </div>

            <!-- Tâche Parente (optionnelle pour sous-tâche) -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">
                Tâche parente <span class="text-slate-400 font-normal">(laisser vide si tâche mère)</span>
              </label>
              <select
                v-model="form.parent_task_id"
                class="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:border-blue-600"
              >
                <option :value="null">-- Aucune (Tâche principale) --</option>
                <option v-for="t in availableParentTasks" :key="t.id" :value="t.id">
                  {{ t.code }} - {{ t.name }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Description / Objectifs détaillés</label>
            <textarea
              v-model="form.description"
              rows="2"
              placeholder="Spécifications techniques, mode opératoire ou consignes particulières..."
              class="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600 resize-none"
            ></textarea>
          </div>
        </div>

        <!-- SECTION 2 : RESPONSABLE, STATUT & PRIORITÉ -->
        <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-100 space-y-3">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/60 pb-1.5">
            <fas-icon icon="user-gear" class="text-[#1d4ed8]" />
            <span>2. Responsable, Priorité & Avancement</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <!-- Responsable -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block text-xs font-bold text-slate-700">Responsable</label>
                <button
                  type="button"
                  @click="$emit('requestAddResponsable')"
                  class="text-[11px] text-[#1d4ed8] font-bold hover:underline flex items-center gap-1"
                >
                  <fas-icon icon="plus" class="text-[9px]" />
                  <span>Nouveau</span>
                </button>
              </div>
              <select
                v-model="form.responsible_id"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              >
                <option :value="null">-- Non assigné --</option>
                <option v-for="r in responsables" :key="r.id" :value="r.id">
                  {{ r.first_name }} {{ r.last_name }} ({{ r.role_name }})
                </option>
              </select>
            </div>

            <!-- Priorité -->
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Priorité</label>
              <select
                v-model="form.priority"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600 font-semibold"
                :class="{
                  'text-emerald-700': form.priority === 'Faible',
                  'text-blue-700': form.priority === 'Normale',
                  'text-amber-700': form.priority === 'Importante',
                  'text-rose-700': form.priority === 'Critique',
                }"
              >
                <option value="Faible">Faible</option>
                <option value="Normale">Normale</option>
                <option value="Importante">Importante</option>
                <option value="Critique">Critique</option>
              </select>
            </div>

            <!-- Statut -->
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Statut d'exécution</label>
              <select
                v-model="form.status"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600 font-semibold"
                @change="handleStatusChange"
              >
                <option value="À faire">À faire</option>
                <option value="En cours">En cours</option>
                <option value="En attente">En attente</option>
                <option value="Bloquée">Bloquée</option>
                <option value="Terminée">Terminée</option>
                <option value="Annulée">Annulée</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <!-- Avancement slider / input -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block text-xs font-bold text-slate-700">Progression</label>
                <span class="text-xs font-mono font-bold text-[#1d4ed8]">{{ form.progress }}%</span>
              </div>
              <div class="flex items-center gap-2">
                <input
                  v-model.number="form.progress"
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  class="w-full accent-[#1d4ed8]"
                  @input="handleProgressChange"
                />
                <input
                  v-model.number="form.progress"
                  type="number"
                  min="0"
                  max="100"
                  class="w-16 px-2 py-1 text-xs border rounded-lg text-center"
                  @change="handleProgressChange"
                />
              </div>
            </div>

            <!-- Poids dans la phase -->
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Poids de la tâche <span class="text-slate-400 font-normal">(pondération dans l'avancement global)</span>
              </label>
              <input
                v-model.number="form.weight"
                type="number"
                step="0.1"
                min="0.1"
                placeholder="1.0"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              />
            </div>
          </div>
        </div>

        <!-- SECTION 3 : CALENDRIER & DÉLAIS -->
        <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-100 space-y-3">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/60 pb-1.5">
            <fas-icon icon="calendar-days" class="text-[#1d4ed8]" />
            <span>3. Planification des Délais</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Début prévisionnel <span class="text-rose-500">*</span>
              </label>
              <input
                v-model="form.planned_start_date"
                type="date"
                required
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
                :class="{ 'border-rose-400': errors.planned_start_date }"
                @change="computeDuration"
              />
              <p v-if="errors.planned_start_date" class="text-[11px] text-rose-500 mt-1">{{ errors.planned_start_date }}</p>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Fin prévisionnelle <span class="text-rose-500">*</span>
              </label>
              <input
                v-model="form.planned_end_date"
                type="date"
                required
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
                :class="{ 'border-rose-400': errors.planned_end_date }"
                @change="computeDuration"
              />
              <p v-if="errors.planned_end_date" class="text-[11px] text-rose-500 mt-1">{{ errors.planned_end_date }}</p>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Durée calculée</label>
              <div class="px-3 py-2 rounded-xl bg-blue-50/70 border border-blue-200 text-[#1d4ed8] text-xs font-bold flex items-center justify-between">
                <span>{{ calculatedDuration }} jours ouvrés</span>
                <fas-icon icon="clock" class="text-blue-400" />
              </div>
            </div>
          </div>
        </div>

        <!-- SECTION 4 : DÉPENDANCES ANTÉRIEURES (FIN -> DÉBUT) -->
        <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-100 space-y-3">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/60 pb-1.5">
            <fas-icon icon="arrows-turn-right" class="text-[#1d4ed8]" />
            <span>4. Dépendances (Fin → Début)</span>
          </div>

          <p class="text-xs text-slate-500">
            Sélectionnez les tâches qui doivent obligatoirement être terminées avant que celle-ci ne commence :
          </p>

          <div v-if="availablePredecessors.length > 0" class="max-h-36 overflow-y-auto border border-slate-200 rounded-xl bg-white p-2 divide-y divide-slate-100">
            <label
              v-for="pred in availablePredecessors"
              :key="pred.id"
              class="flex items-center gap-2.5 p-1.5 hover:bg-slate-50 rounded-lg cursor-pointer text-xs"
            >
              <input
                type="checkbox"
                :value="pred.id"
                v-model="form.predecessor_ids"
                class="rounded text-[#1d4ed8] focus:ring-blue-500"
              />
              <span class="font-mono font-bold text-slate-500">{{ pred.code }}</span>
              <span class="text-slate-800 font-medium truncate flex-1">{{ pred.name }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded font-bold" :class="pred.status === 'Terminée' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'">
                {{ pred.status }}
              </span>
            </label>
          </div>
          <p v-else class="text-xs text-slate-400 italic">Aucune autre tâche disponible pour créer une dépendance.</p>
        </div>

        <!-- SECTION 5 : RESSOURCES & ÉQUIPES -->
        <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-100 space-y-3">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/60 pb-1.5">
            <fas-icon icon="truck-pickup" class="text-[#1d4ed8]" />
            <span>5. Ressources & Moyens Matériels</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Équipe assignée</label>
              <input
                v-model="form.team_name"
                type="text"
                placeholder="Ex: Équipe Coffreurs 1"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre d'ouvriers</label>
              <input
                v-model.number="form.workers_count"
                type="number"
                min="0"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600 text-center"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Budget estimé (FCFA)</label>
              <input
                v-model.number="form.budget_estimated"
                type="number"
                min="0"
                placeholder="0"
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Matériaux requis</label>
              <input
                v-model="form.materials"
                type="text"
                placeholder="Béton, aciers, briques..."
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Matériels / Équipements</label>
              <input
                v-model="form.equipment"
                type="text"
                placeholder="Grue, benne, échafaudage..."
                class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-900 text-xs focus:outline-none focus:border-blue-600"
              />
            </div>
          </div>
        </div>

        <!-- SECTION 6 : GESTION DES BLOCAGES (CONDITIONNELLE) -->
        <div class="bg-rose-50/60 p-4 rounded-xl border border-rose-100 space-y-3">
          <div class="flex items-center justify-between border-b border-rose-200/60 pb-1.5">
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-rose-700">
              <fas-icon icon="triangle-exclamation" />
              <span>6. Signalement d'un Blocage</span>
            </div>
            <label class="flex items-center gap-2 cursor-pointer text-xs font-bold text-rose-700">
              <input
                type="checkbox"
                v-model="form.is_blocked"
                class="rounded text-rose-600 focus:ring-rose-500"
                @change="handleBlockedToggle"
              />
              <span>Tâche bloquée</span>
            </label>
          </div>

          <div v-if="form.is_blocked" class="space-y-3 pt-1">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold text-rose-900 mb-1">Motif du blocage *</label>
                <input
                  v-model="form.blocking_reason"
                  type="text"
                  placeholder="Ex: Attente livraison acier, Intempéries..."
                  class="w-full px-3 py-2 rounded-xl bg-white border border-rose-200 text-slate-900 text-xs focus:outline-none focus:border-rose-500"
                />
              </div>
              <div>
                <label class="block text-xs font-semibold text-rose-900 mb-1">Impact estimé</label>
                <input
                  v-model="form.blocking_impact"
                  type="text"
                  placeholder="Ex: Risque décalage coulage dalle"
                  class="w-full px-3 py-2 rounded-xl bg-white border border-rose-200 text-slate-900 text-xs focus:outline-none focus:border-rose-500"
                />
              </div>
            </div>
            <div>
              <label class="block text-xs font-semibold text-rose-900 mb-1">Commentaire explicatif</label>
              <textarea
                v-model="form.blocking_comment"
                rows="2"
                placeholder="Détails du problème rencontré et actions correctives en cours..."
                class="w-full px-3 py-2 rounded-xl bg-white border border-rose-200 text-slate-900 text-xs focus:outline-none focus:border-rose-500 resize-none"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="flex items-center justify-end gap-2.5 pt-4 border-t border-slate-100 flex-shrink-0">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
            :disabled="loading"
          >
            Annuler
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-5 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <fas-icon v-if="loading" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check" />
            <span>{{ loading ? 'Enregistrement...' : 'Enregistrer la tâche' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { taskService } from '@/services'
import { toast } from '@/utils/alert'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  chantierId: {
    type: [Number, String],
    required: true,
  },
  phases: {
    type: Array,
    default: () => [],
  },
  tasks: {
    type: Array,
    default: () => [],
  },
  responsables: {
    type: Array,
    default: () => [],
  },
  defaultPhaseId: {
    type: [Number, String],
    default: null,
  },
  defaultParentTaskId: {
    type: [Number, String],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'created', 'requestAddPhase', 'requestAddResponsable'])

const form = reactive({
  code: '',
  name: '',
  description: '',
  phase_id: null,
  parent_task_id: null,
  responsible_id: null,
  status: 'À faire',
  priority: 'Normale',
  progress: 0,
  weight: 1.0,
  planned_start_date: '',
  planned_end_date: '',
  predecessor_ids: [],
  team_name: '',
  workers_count: 0,
  equipment: '',
  materials: '',
  budget_estimated: 0,
  is_blocked: false,
  blocking_reason: '',
  blocking_impact: '',
  blocking_comment: '',
})

const errors = reactive({
  name: '',
  phase_id: '',
  planned_start_date: '',
  planned_end_date: '',
})

const loading = ref(false)

const availableParentTasks = computed(() => {
  return props.tasks.filter((t) => !t.parent_task_id)
})

const availablePredecessors = computed(() => {
  return props.tasks.filter((t) => !t.parent_task_id || t.id !== form.parent_task_id)
})

const calculatedDuration = computed(() => {
  if (form.planned_start_date && form.planned_end_date) {
    const start = new Date(form.planned_start_date)
    const end = new Date(form.planned_end_date)
    const diff = Math.round((end - start) / (1000 * 60 * 60 * 24)) + 1
    return diff > 0 ? diff : 0
  }
  return 1
})

function computeDuration() {
  if (form.planned_start_date && form.planned_end_date) {
    if (new Date(form.planned_end_date) < new Date(form.planned_start_date)) {
      errors.planned_end_date = 'La date de fin doit être postérieure à la date de début'
    } else {
      errors.planned_end_date = ''
    }
  }
}

function handleStatusChange() {
  if (form.status === 'Terminée') {
    form.progress = 100
  } else if (form.status === 'Bloquée') {
    form.is_blocked = true
  } else if (form.status === 'À faire' && form.progress > 0) {
    form.progress = 0
  }
}

function handleProgressChange() {
  if (form.progress === 100) {
    form.status = 'Terminée'
  } else if (form.progress > 0 && form.status === 'À faire') {
    form.status = 'En cours'
  } else if (form.progress === 0 && form.status === 'Terminée') {
    form.status = 'À faire'
  }
}

function handleBlockedToggle() {
  if (form.is_blocked) {
    form.status = 'Bloquée'
  } else if (form.status === 'Bloquée') {
    form.status = form.progress > 0 ? 'En cours' : 'À faire'
  }
}

watch(
  () => props.modelValue,
  async (val) => {
    if (val && props.chantierId) {
      form.name = ''
      form.description = ''
      form.phase_id = props.defaultPhaseId || (props.phases.length > 0 ? props.phases[0].id : null)
      form.parent_task_id = props.defaultParentTaskId || null
      form.responsible_id = null
      form.status = 'À faire'
      form.priority = 'Normale'
      form.progress = 0
      form.weight = 1.0
      form.predecessor_ids = []
      form.team_name = ''
      form.workers_count = 0
      form.equipment = ''
      form.materials = ''
      form.budget_estimated = 0
      form.is_blocked = false
      form.blocking_reason = ''
      form.blocking_impact = ''
      form.blocking_comment = ''

      // Dates par défaut (aujourd'hui -> +7 jours)
      const now = new Date()
      const in7Days = new Date()
      in7Days.setDate(now.getDate() + 7)
      form.planned_start_date = now.toISOString().split('T')[0]
      form.planned_end_date = in7Days.toISOString().split('T')[0]

      errors.name = ''
      errors.phase_id = ''
      errors.planned_start_date = ''
      errors.planned_end_date = ''

      try {
        const res = await taskService.getNextTaskCode(props.chantierId)
        if (res && res.code) {
          form.code = res.code
        }
      } catch (e) {
        form.code = 'TSK-2026-001'
      }
    }
  }
)

function close() {
  emit('update:modelValue', false)
}

async function handleSubmit() {
  errors.name = ''
  errors.phase_id = ''
  errors.planned_start_date = ''
  errors.planned_end_date = ''

  if (!form.name.trim()) {
    errors.name = "L'intitulé de la tâche est obligatoire"
    return
  }
  if (!form.phase_id) {
    errors.phase_id = 'La phase associée est obligatoire'
    return
  }
  if (!form.planned_start_date) {
    errors.planned_start_date = 'La date de début prévisionnelle est obligatoire'
    return
  }
  if (!form.planned_end_date) {
    errors.planned_end_date = 'La date de fin prévisionnelle est obligatoire'
    return
  }
  if (new Date(form.planned_end_date) < new Date(form.planned_start_date)) {
    errors.planned_end_date = 'La date de fin doit être postérieure à la date de début'
    return
  }

  loading.value = true
  try {
    const payload = {
      code: form.code.trim() || undefined,
      name: form.name.trim(),
      description: form.description.trim() || null,
      chantier_id: Number(props.chantierId),
      phase_id: Number(form.phase_id),
      parent_task_id: form.parent_task_id ? Number(form.parent_task_id) : null,
      responsible_id: form.responsible_id ? Number(form.responsible_id) : null,
      status: form.status,
      priority: form.priority,
      progress: Number(form.progress),
      weight: Number(form.weight) || 1.0,
      planned_start_date: form.planned_start_date,
      planned_end_date: form.planned_end_date,
      estimated_duration_days: calculatedDuration.value,
      predecessor_ids: form.predecessor_ids,
      team_name: form.team_name.trim() || null,
      workers_count: Number(form.workers_count) || 0,
      equipment: form.equipment.trim() || null,
      materials: form.materials.trim() || null,
      budget_estimated: Number(form.budget_estimated) || 0,
      is_blocked: form.is_blocked,
      blocking_reason: form.is_blocked ? form.blocking_reason.trim() : null,
      blocking_impact: form.is_blocked ? form.blocking_impact.trim() : null,
      blocking_comment: form.is_blocked ? form.blocking_comment.trim() : null,
    }

    const created = await taskService.createTask(props.chantierId, payload)
    toast(`Tâche « ${created.name} » enregistrée avec succès`, 'success')
    emit('created', created)
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la création de la tâche'
    if (typeof detail === 'string') {
      toast(detail, 'error')
    } else {
      toast('Données invalides, veuillez vérifier le formulaire', 'error')
    }
  } finally {
    loading.value = false
  }
}
</script>
