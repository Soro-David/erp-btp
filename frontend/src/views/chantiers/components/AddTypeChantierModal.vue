<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
    @click.self="close"
  >
    <div
      class="bg-white border border-slate-200 rounded-2xl w-full max-w-md p-6 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150"
    >
      <!-- En-tête Modal -->
      <div class="flex items-center justify-between pb-3.5 mb-4 border-b border-slate-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-lg">
            <fas-icon icon="layer-group" />
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900">Ajouter un type de chantier</h3>
            <p class="text-xs text-slate-500">Nouveau référentiel pour classifier vos projets</p>
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
        <!-- Nom du type * -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">
            Nom du type de chantier <span class="text-rose-500">*</span>
          </label>
          <input
            v-model="form.name"
            type="text"
            required
            placeholder="Ex: Génie civil, Voirie, Hydraulique..."
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            :class="{ 'border-rose-400': errors.name }"
          />
          <p v-if="errors.name" class="text-[11px] text-rose-500 mt-1">{{ errors.name }}</p>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">
            Description <span class="text-slate-400 font-normal">(optionnelle)</span>
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Précisez la nature des travaux ou les corps d'état associés..."
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs sm:text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all resize-none"
          ></textarea>
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
            <span>{{ loading ? 'Enregistrement...' : 'Ajouter le type' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { chantierService } from '@/services'
import { toast } from '@/utils/alert'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'created'])

const form = reactive({
  name: '',
  description: '',
})

const errors = reactive({
  name: '',
})

const loading = ref(false)

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.name = ''
      form.description = ''
      errors.name = ''
    }
  }
)

function close() {
  emit('update:modelValue', false)
}

async function handleSubmit() {
  errors.name = ''
  if (!form.name.trim()) {
    errors.name = 'Le nom du type est obligatoire'
    return
  }

  loading.value = true
  try {
    const created = await chantierService.createType({
      name: form.name.trim(),
      description: form.description.trim() || null,
    })
    toast(`Type « ${created.name} » ajouté avec succès`, 'success')
    emit('created', created)
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la création du type'
    errors.name = typeof detail === 'string' ? detail : 'Données invalides'
  } finally {
    loading.value = false
  }
}
</script>
