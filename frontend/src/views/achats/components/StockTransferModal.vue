<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-indigo-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center text-lg">
            <fas-icon icon="right-left" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">Transfert Inter-Dépôts</h2>
            <p class="text-xs text-slate-500">
              Déplacement de stock entre dépôts ou magasins de chantier
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
        <!-- Matériau -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Matériau à transférer *</label>
          <select
            v-model="form.material_id"
            required
            @change="updateSourceStock"
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-indigo-600"
          >
            <option :value="null" disabled>Sélectionner le matériau</option>
            <option v-for="m in materials" :key="m.id" :value="m.id">
              {{ m.name }} ({{ m.unit?.code || 'U' }})
            </option>
          </select>
        </div>

        <!-- Dépôts Source et Destination -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Dépôt Source (Départ) *</label>
            <select
              v-model="form.source_location_id"
              required
              @change="updateSourceStock"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-indigo-600"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                {{ loc.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Dépôt Cible (Arrivée) *</label>
            <select
              v-model="form.dest_location_id"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-indigo-600"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id" :disabled="loc.id === form.source_location_id">
                {{ loc.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Stock dispo source -->
        <div v-if="form.material_id" class="p-3 rounded-2xl bg-indigo-50/70 border border-indigo-200 flex items-center justify-between">
          <span class="text-slate-600 font-bold">Disponible au départ :</span>
          <span class="font-black text-indigo-900 font-mono text-sm">
            {{ availableSourceStock }} {{ selectedMaterial?.unit?.code || 'unités' }}
          </span>
        </div>

        <!-- Quantité -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Quantité à transférer *</label>
          <input
            v-model.number="form.quantity"
            type="number"
            min="0.01"
            :max="availableSourceStock"
            step="any"
            required
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-black text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-indigo-600"
          />
        </div>

        <!-- Motifs -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Motif du transfert</label>
          <input
            v-model="form.reason"
            type="text"
            placeholder="Ex: Rééquilibrage stock base vie / magasin chantier"
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-indigo-600"
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
            :disabled="saving || form.source_location_id === form.dest_location_id || form.quantity > availableSourceStock"
            class="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold shadow-md shadow-indigo-700/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="right-left" />
            <span>Valider le Transfert</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { stockService, materialService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const locations = ref([])
const materials = ref([])
const availableSourceStock = ref(0)

const form = reactive({
  material_id: null,
  source_location_id: null,
  dest_location_id: null,
  quantity: 1,
  reason: '',
  notes: '',
})

const selectedMaterial = computed(() => {
  return materials.value.find((m) => m.id === form.material_id) || null
})

const loadData = async () => {
  try {
    const [locData, matData] = await Promise.all([
      stockService.getLocations({ is_active: true }),
      materialService.getMaterials({ is_active: true }),
    ])
    locations.value = locData
    materials.value = matData

    if (locations.value.length > 1) {
      form.source_location_id = locations.value[0].id
      form.dest_location_id = locations.value[1].id
    }
  } catch (err) {
    console.error('Erreur chargement données transfert:', err)
  }
}

onMounted(() => {
  loadData()
})

const updateSourceStock = async () => {
  if (!form.material_id || !form.source_location_id) {
    availableSourceStock.value = 0
    return
  }
  try {
    const overview = await stockService.getStockOverview(form.source_location_id)
    const match = overview.find((item) => item.material_id === form.material_id)
    availableSourceStock.value = match ? match.quantity : 0
  } catch (err) {
    console.error('Erreur calcul stock dispo:', err)
  }
}

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (form.source_location_id === form.dest_location_id) {
    Swal.fire('Erreur', 'Le dépôt source et destination doivent être différents', 'warning')
    return
  }

  saving.value = true
  try {
    const payload = {
      material_id: form.material_id,
      source_location_id: form.source_location_id,
      dest_location_id: form.dest_location_id,
      quantity: form.quantity,
      notes: form.reason,
    }
    const res = await stockService.transferStock(payload)
    Swal.fire({
      icon: 'success',
      title: 'Transfert effectué',
      text: `${form.quantity} unités transférées avec succès.`,
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
