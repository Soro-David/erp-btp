<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-blue-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-lg">
            <fas-icon icon="arrow-right-from-bracket" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">Sortie de Stock vers Chantier</h2>
            <p class="text-xs text-slate-500">
              Affectation et consommation de matériaux sur un chantier ou une tâche
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
        <!-- 1. Dépôt source & Matériau -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Dépôt source *</label>
            <select
              v-model="form.location_id"
              required
              @change="updateAvailableStock"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                {{ loc.code }} - {{ loc.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Matériau *</label>
            <select
              v-model="form.material_id"
              required
              @change="updateAvailableStock"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option :value="null" disabled>Sélectionner le matériau</option>
              <option v-for="m in materials" :key="m.id" :value="m.id">
                {{ m.name }} ({{ m.unit?.code || 'U' }})
              </option>
            </select>
          </div>
        </div>

        <!-- Jauge Stock Disponible -->
        <div v-if="selectedMaterial" class="p-3 rounded-2xl bg-blue-50/70 border border-blue-200 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <fas-icon icon="warehouse" class="text-blue-600 text-sm" />
            <div>
              <span class="text-slate-600 font-bold">Stock disponible au dépôt :</span>
              <span class="ml-1.5 font-black text-blue-900 font-mono text-sm">
                {{ availableStock }} {{ selectedMaterial.unit?.code || 'U' }}
              </span>
            </div>
          </div>
          <span
            class="px-2 py-0.5 rounded-full text-[10px] font-extrabold"
            :class="availableStock > 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'"
          >
            {{ availableStock > 0 ? 'Disponible' : 'Rupture' }}
          </span>
        </div>

        <!-- 2. Chantier destinataire & Tâche (filtrée) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Chantier destinataire *</label>
            <select
              v-model="form.chantier_id"
              required
              @change="onChantierChange"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option :value="null" disabled>Sélectionner un chantier</option>
              <option v-for="c in chantiers" :key="c.id" :value="c.id">
                {{ c.code }} - {{ c.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Tâche du chantier (optionnel)</label>
            <select
              v-model="form.task_id"
              :disabled="!form.chantier_id || loadingTasks"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 disabled:opacity-50"
            >
              <option :value="null">-- Non spécifiée (Chantier global) --</option>
              <option v-for="t in tasks" :key="t.id" :value="t.id">
                {{ t.code }} - {{ t.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- 3. Quantité à sortir -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">
            Quantité à sortir *
            <span v-if="selectedMaterial" class="text-slate-400 font-normal">({{ selectedMaterial.unit?.name || 'unités' }})</span>
          </label>
          <input
            v-model.number="form.quantity"
            type="number"
            min="0.01"
            :max="availableStock"
            step="any"
            required
            placeholder="Ex: 50"
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-black text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-blue-600"
          />
          <p v-if="form.quantity > availableStock" class="text-[11px] text-red-600 font-bold mt-1">
            ⚠️ La quantité demandée dépasse le stock disponible au dépôt ({{ availableStock }}).
          </p>
        </div>

        <!-- 4. Motif & Notes -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Motif / Phase d'utilisation</label>
          <input
            v-model="form.reason"
            type="text"
            placeholder="Ex: Bétonnage semelles de fondation axe A-D"
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
          />
        </div>

        <div>
          <label class="block font-bold text-slate-700 mb-1">Notes complémentaires</label>
          <textarea
            v-model="form.notes"
            rows="2"
            placeholder="Nom du chef d'équipe ayant retiré le matériel, véhicule..."
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
          ></textarea>
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
            :disabled="saving || availableStock <= 0 || form.quantity > availableStock"
            class="px-6 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-blue-700 text-white font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check" />
            <span>Valider la Sortie de Stock</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { stockService, materialService, chantierService, taskService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  preselectedMaterialId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const loadingTasks = ref(false)

const locations = ref([])
const materials = ref([])
const chantiers = ref([])
const tasks = ref([])
const availableStock = ref(0)

const form = reactive({
  location_id: null,
  material_id: null,
  chantier_id: null,
  task_id: null,
  quantity: 1,
  reason: '',
  notes: '',
})

const selectedMaterial = computed(() => {
  return materials.value.find((m) => m.id === form.material_id) || null
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

    if (locations.value.length > 0 && !form.location_id) {
      form.location_id = locations.value[0].id
    }
    if (chantiers.value.length > 0 && !form.chantier_id) {
      form.chantier_id = chantiers.value[0].id
      await loadTasks(form.chantier_id)
    }
  } catch (err) {
    console.error('Erreur données sortie stock:', err)
  }
}

onMounted(() => {
  loadData()
})

const loadTasks = async (chantierId) => {
  if (!chantierId) {
    tasks.value = []
    return
  }
  loadingTasks.value = true
  try {
    tasks.value = (await taskService.getTasks(chantierId)) || []
  } catch {
    tasks.value = []
  } finally {
    loadingTasks.value = false
  }
}

const onChantierChange = async () => {
  form.task_id = null
  await loadTasks(form.chantier_id)
}

const updateAvailableStock = async () => {
  if (!form.material_id || !form.location_id) {
    availableStock.value = 0
    return
  }
  try {
    const overview = await stockService.getStockOverview(form.location_id)
    const match = overview.find((item) => item.material_id === form.material_id)
    availableStock.value = match ? match.quantity : 0
  } catch (err) {
    console.error('Erreur calcul stock dispo:', err)
  }
}

watch(
  () => props.preselectedMaterialId,
  (mid) => {
    if (mid) {
      form.material_id = mid
      updateAvailableStock()
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (form.quantity > availableStock.value) {
    Swal.fire('Stock insuffisant', 'La quantité dépasse le stock disponible', 'warning')
    return
  }

  saving.value = true
  try {
    const params = {
      material_id: form.material_id,
      location_id: form.location_id,
      chantier_id: form.chantier_id,
      task_id: form.task_id || undefined,
      quantity: form.quantity,
      reason: form.reason || undefined,
      notes: form.notes || undefined,
    }

    const movement = await stockService.issueStock(params)
    Swal.fire({
      icon: 'success',
      title: 'Sortie effectuée !',
      text: `${form.quantity} ${selectedMaterial.value?.unit?.code || 'unités'} affectés au chantier. Mvt: ${movement.reference}`,
      timer: 2000,
      showConfirmButton: false,
    })

    emit('saved', movement)
    close()
  } catch (error) {
    const detail = error.response?.data?.detail || error.message
    Swal.fire({
      icon: 'error',
      title: 'Erreur',
      text: detail,
    })
  } finally {
    saving.value = false
  }
}
</script>
