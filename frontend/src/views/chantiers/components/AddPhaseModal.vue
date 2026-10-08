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
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-lg">
            <fas-icon icon="layer-group" />
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900">Ajouter une Phase / Lot</h3>
            <p class="text-xs text-slate-500">Structurer l'organisation des travaux du chantier</p>
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
              placeholder="PHS-01"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 text-xs font-mono font-bold focus:outline-none"
            />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Nom du lot / phase <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="Ex: Fondations, Gros Œuvre, Peintures..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
              :class="{ 'border-rose-400': errors.name }"
            />
            <p v-if="errors.name" class="text-[11px] text-rose-500 mt-1">{{ errors.name }}</p>
          </div>
        </div>

        <!-- Responsable -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-bold text-slate-700">Responsable / Conducteur de lot</label>
            <button
              type="button"
              @click="$emit('requestAddResponsable')"
              class="text-[11px] text-[#1d4ed8] font-bold hover:underline flex items-center gap-1"
            >
              <fas-icon icon="plus" class="text-[10px]" />
              <span>Nouveau</span>
            </button>
          </div>
          <select
            v-model="form.responsible_id"
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
          >
            <option :value="null">-- Non assigné --</option>
            <option v-for="r in responsables" :key="r.id" :value="r.id">
              {{ r.first_name }} {{ r.last_name }} ({{ r.role_name }})
            </option>
          </select>
        </div>

        <!-- Dates prévisionnelles -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Début prévisionnel</label>
            <input
              v-model="form.start_date_planned"
              type="date"
              class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Fin prévisionnelle</label>
            <input
              v-model="form.end_date_planned"
              type="date"
              class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
        </div>

        <!-- Ordre & Description -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Ordre</label>
            <input
              v-model.number="form.display_order"
              type="number"
              min="1"
              class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs text-center focus:outline-none"
            />
          </div>
          <div class="sm:col-span-3">
            <label class="block text-xs font-semibold text-slate-700 mb-1">Description / Notes</label>
            <input
              v-model="form.description"
              type="text"
              placeholder="Périmètre d'intervention..."
              class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
        </div>

        <!-- Boutons d'action -->
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
            class="px-4 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <fas-icon v-if="loading" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="plus" />
            <span>{{ loading ? 'Création...' : 'Créer la phase' }}</span>
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

const emit = defineEmits(['update:modelValue', 'created', 'requestAddResponsable'])

const form = reactive({
  code: '',
  name: '',
  description: '',
  responsible_id: null,
  start_date_planned: '',
  end_date_planned: '',
  display_order: 1,
})

const errors = reactive({
  name: '',
})

const loading = ref(false)

watch(
  () => props.modelValue,
  async (val) => {
    if (val && props.chantierId) {
      form.name = ''
      form.description = ''
      form.responsible_id = null
      form.start_date_planned = ''
      form.end_date_planned = ''
      form.display_order = 1
      errors.name = ''

      try {
        const res = await taskService.getNextPhaseCode(props.chantierId)
        if (res && res.code) {
          form.code = res.code
        }
      } catch (e) {
        form.code = 'PHS-01'
      }
    }
  }
)

function close() {
  emit('update:modelValue', false)
}

async function handleSubmit() {
  errors.name = ''
  if (!form.name.trim()) {
    errors.name = 'Le nom de la phase est obligatoire'
    return
  }

  loading.value = true
  try {
    const created = await taskService.createPhase(props.chantierId, {
      code: form.code.trim() || undefined,
      name: form.name.trim(),
      description: form.description.trim() || null,
      responsible_id: form.responsible_id || null,
      start_date_planned: form.start_date_planned || null,
      end_date_planned: form.end_date_planned || null,
      display_order: form.display_order || 1,
      chantier_id: Number(props.chantierId),
    })
    toast(`Phase « ${created.name} » créée avec succès`, 'success')
    emit('created', created)
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la création de la phase'
    errors.name = typeof detail === 'string' ? detail : 'Données invalides'
  } finally {
    loading.value = false
  }
}
</script>
