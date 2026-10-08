<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
    @click.self="close"
  >
    <div
      class="bg-white border border-slate-200 rounded-2xl w-full max-w-lg p-6 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150"
    >
      <!-- En-tête -->
      <div class="flex items-center justify-between pb-3.5 mb-4 border-b border-slate-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-lg">
            <fas-icon icon="flag" />
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900">Ajouter un Jalon Clé</h3>
            <p class="text-xs text-slate-500">Repères contractuels et jalons d'avancement majeurs</p>
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

      <!-- Formulaire -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Code & Nom -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Code</label>
            <input
              v-model="form.code"
              type="text"
              placeholder="JAL-01"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 text-xs font-mono font-bold focus:outline-none"
            />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Intitulé du jalon <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="Ex: Hors d'eau / Hors d'air, RPT..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
              :class="{ 'border-rose-400': errors.name }"
            />
            <p v-if="errors.name" class="text-[11px] text-rose-500 mt-1">{{ errors.name }}</p>
          </div>
        </div>

        <!-- Date cible & Statut -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Date cible prévue <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.planned_date"
              type="date"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              :class="{ 'border-rose-400': errors.planned_date }"
            />
            <p v-if="errors.planned_date" class="text-[11px] text-rose-500 mt-1">{{ errors.planned_date }}</p>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Statut initial</label>
            <select
              v-model="form.status"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option value="À venir">À venir</option>
              <option value="Atteint">Atteint</option>
              <option value="En retard">En retard</option>
            </select>
          </div>
        </div>

        <!-- Responsable -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Responsable garant</label>
          <select
            v-model="form.responsible_id"
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600"
          >
            <option :value="null">-- Non assigné --</option>
            <option v-for="r in responsables" :key="r.id" :value="r.id">
              {{ r.first_name }} {{ r.last_name }} ({{ r.role_name }})
            </option>
          </select>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Critères d'atteinte / Objectifs</label>
          <textarea
            v-model="form.description"
            rows="2"
            placeholder="Conditions requises pour valider ce jalon..."
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600 resize-none"
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100">
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
            class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <fas-icon v-if="loading" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="flag" />
            <span>{{ loading ? 'Enregistrement...' : 'Créer le jalon' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
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
  responsables: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue', 'created'])

const form = reactive({
  code: '',
  name: '',
  description: '',
  planned_date: '',
  status: 'À venir',
  responsible_id: null,
})

const errors = reactive({
  name: '',
  planned_date: '',
})

const loading = ref(false)

watch(
  () => props.modelValue,
  async (val) => {
    if (val && props.chantierId) {
      form.name = ''
      form.description = ''
      form.planned_date = ''
      form.status = 'À venir'
      form.responsible_id = null
      errors.name = ''
      errors.planned_date = ''

      try {
        const res = await taskService.getNextMilestoneCode(props.chantierId)
        if (res && res.code) {
          form.code = res.code
        }
      } catch (e) {
        form.code = 'JAL-01'
      }
    }
  }
)

function close() {
  emit('update:modelValue', false)
}

async function handleSubmit() {
  errors.name = ''
  errors.planned_date = ''

  if (!form.name.trim()) {
    errors.name = "L'intitulé du jalon est obligatoire"
    return
  }
  if (!form.planned_date) {
    errors.planned_date = 'La date cible est obligatoire'
    return
  }

  loading.value = true
  try {
    const created = await taskService.createMilestone(props.chantierId, {
      code: form.code.trim() || undefined,
      name: form.name.trim(),
      description: form.description.trim() || null,
      planned_date: form.planned_date,
      status: form.status,
      responsible_id: form.responsible_id || null,
      chantier_id: Number(props.chantierId),
    })
    toast(`Jalon « ${created.name} » ajouté avec succès`, 'success')
    emit('created', created)
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la création du jalon'
    errors.name = typeof detail === 'string' ? detail : 'Données invalides'
  } finally {
    loading.value = false
  }
}
</script>
