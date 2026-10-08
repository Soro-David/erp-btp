<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-teal-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center text-lg">
            <fas-icon icon="rotate-left" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">Retour Matériel de Chantier</h2>
            <p class="text-xs text-slate-500">
              Réintégration de surplus non consommés dans un dépôt
            </p>
          </div>
        </div>
        <button
          type="button"
          @click="close"
          class="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100 transition-colors"
        >
          <fas-icon icon="xmark" class="text-base" />
        </button>
      </div>

      <!-- Corps du formulaire -->
      <form @submit.prevent="handleSubmit" class="p-6 overflow-y-auto space-y-4 text-xs flex-1">
        <!-- Chantier d'origine -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Chantier d'origine *</label>
          <select
            v-model="form.chantier_id"
            required
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-teal-600"
          >
            <option :value="null" disabled>Sélectionner le chantier</option>
            <option v-for="c in chantiers" :key="c.id" :value="c.id">
              {{ c.code }} - {{ c.name }}
            </option>
          </select>
        </div>

        <!-- Matériau retourné -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Matériau retourné *</label>
          <select
            v-model="form.material_id"
            required
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-teal-600"
          >
            <option :value="null" disabled>Sélectionner le matériau</option>
            <option v-for="m in materials" :key="m.id" :value="m.id">
              {{ m.name }} ({{ m.unit?.code || 'U' }})
            </option>
          </select>
        </div>

        <!-- Dépôt de réintégration -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Dépôt de réintégration *</label>
          <select
            v-model="form.location_id"
            required
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-teal-600"
          >
            <option v-for="loc in locations" :key="loc.id" :value="loc.id">
              {{ loc.name }}
            </option>
          </select>
        </div>

        <!-- Quantité -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Quantité réintégrée *</label>
          <input
            v-model.number="form.quantity"
            type="number"
            min="0.01"
            step="any"
            required
            placeholder="Ex: 25"
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-black text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-teal-600"
          />
        </div>

        <!-- Motif -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Motif du retour</label>
          <input
            v-model="form.reason"
            type="text"
            placeholder="Ex: Fin de phase coffrage, surplus de fers non coupés"
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-teal-600"
          />
        </div>

        <!-- Pied de modal -->
        <div class="pt-4 border-t border-slate-100 flex items-center justify-end gap-2.5">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 font-bold transition-colors"
          >
            Annuler
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold shadow-md shadow-teal-700/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="rotate-left" />
            <span>Réintégrer au Stock</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { stockService, materialService, chantierService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const locations = ref([])
const materials = ref([])
const chantiers = ref([])

const form = reactive({
  chantier_id: null,
  material_id: null,
  location_id: null,
  quantity: 1,
  reason: '',
  notes: '',
})

const loadData = async () => {
  try {
    const [locData, matData, chData] = await Promise.all([
      stockService.getLocations({ is_active: true }),
      materialService.getMaterials({ is_active: true }),
      chantierService.getChantiers(),
    ])
    locations.value = locData
    materials.value = matData
    chantiers.value = chData.items || chData || []

    if (locations.value.length > 0) form.location_id = locations.value[0].id
    if (chantiers.value.length > 0) form.chantier_id = chantiers.value[0].id
  } catch (err) {
    console.error('Erreur chargement données retour:', err)
  }
}

onMounted(() => {
  loadData()
})

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  saving.value = true
  try {
    const res = await stockService.returnStock(form)
    Swal.fire({
      icon: 'success',
      title: 'Retour enregistré',
      text: `${form.quantity} unités réintégrées au stock. Réf: ${res.reference}`,
      timer: 1800,
      showConfirmButton: false,
    })
    emit('saved', res)
    close()
  } catch (error) {
    const detail = error.response?.data?.detail || error.message
    Swal.fire('Erreur', detail, 'error')
  } finally {
    saving.value = false
  }
}
</script>
