<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-3xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-violet-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-violet-100 text-violet-700 flex items-center justify-center text-lg">
            <fas-icon icon="clipboard-check" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">Inventaire Physique de Stock</h2>
            <p class="text-xs text-slate-500">
              Comptage réel, détection des écarts et régularisation automatique
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
        <!-- Dépôt & Date -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 bg-slate-50 p-4 rounded-2xl border border-slate-200">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Dépôt inventorié *</label>
            <select
              v-model="form.location_id"
              required
              @change="loadStockForLocation"
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-violet-600"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                {{ loc.code }} - {{ loc.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Date d'inventaire *</label>
            <input
              v-model="form.inventory_date"
              type="date"
              required
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-violet-600"
            />
          </div>
        </div>

        <!-- Tableau des comptages -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-800">Articles inventoriés ({{ items.length }})</span>
            <span class="text-[11px] text-slate-400">
              Saisissez la quantité physique constatée sur le terrain
            </span>
          </div>

          <div class="overflow-x-auto rounded-2xl border border-slate-200">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-100 text-[11px] font-extrabold text-slate-600 uppercase border-b border-slate-200">
                  <th class="py-2.5 px-3">Matériau</th>
                  <th class="py-2.5 px-3 text-right">Stock Théorique</th>
                  <th class="py-2.5 px-3 text-right w-32">Comptage Réel *</th>
                  <th class="py-2.5 px-3 text-right">Écart</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="item in items" :key="item.material_id" class="hover:bg-slate-50/50">
                  <td class="py-2 px-3">
                    <div class="font-bold text-slate-800">{{ item.material_name }}</div>
                    <div class="text-[10px] text-slate-400">{{ item.material_code }} • {{ item.unit_code }}</div>
                  </td>
                  <td class="py-2 px-3 text-right font-mono font-bold text-slate-600">
                    {{ item.theoretical_quantity }}
                  </td>
                  <td class="py-2 px-3 text-right">
                    <input
                      v-model.number="item.actual_quantity"
                      type="number"
                      step="any"
                      min="0"
                      required
                      class="w-full px-2.5 py-1.5 rounded-lg bg-violet-50/50 border border-violet-300 font-bold text-right text-violet-900 font-mono text-xs focus:outline-none focus:border-violet-600"
                    />
                  </td>
                  <td class="py-2 px-3 text-right font-mono font-bold">
                    <span
                      class="px-2 py-0.5 rounded-md text-xs"
                      :class="
                        item.actual_quantity - item.theoretical_quantity === 0
                          ? 'text-slate-500'
                          : item.actual_quantity - item.theoretical_quantity > 0
                          ? 'bg-emerald-100 text-emerald-800'
                          : 'bg-red-100 text-red-800'
                      "
                    >
                      {{ (item.actual_quantity - item.theoretical_quantity) > 0 ? '+' : '' }}{{ item.actual_quantity - item.theoretical_quantity }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Notes -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Notes / Équipe d'inventaire</label>
          <textarea
            v-model="form.notes"
            rows="2"
            placeholder="Responsable de l'inventaire, observations..."
            class="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-violet-600"
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
            :disabled="saving"
            class="px-6 py-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-white font-bold shadow-md shadow-violet-700/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check" />
            <span>Valider l'Inventaire & Régulariser le Stock</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { stockService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const locations = ref([])
const items = ref([])

const form = reactive({
  location_id: null,
  inventory_date: new Date().toISOString().split('T')[0],
  notes: '',
})

const loadLocations = async () => {
  try {
    locations.value = await stockService.getLocations({ is_active: true })
    if (locations.value.length > 0) {
      form.location_id = locations.value[0].id
      await loadStockForLocation()
    }
  } catch (err) {
    console.error('Erreur inventaire dépôts:', err)
  }
}

const loadStockForLocation = async () => {
  if (!form.location_id) return
  try {
    const overview = await stockService.getStockOverview(form.location_id)
    items.value = overview.map((item) => ({
      material_id: item.material_id,
      material_code: item.material_code,
      material_name: item.material_name,
      unit_code: item.unit_code,
      theoretical_quantity: item.quantity,
      actual_quantity: item.quantity, // default starts at theoretical
      unit_price: item.indicative_price,
    }))
  } catch (err) {
    console.error('Erreur chargement articles inventaire:', err)
  }
}

onMounted(() => {
  loadLocations()
})

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  saving.value = true
  try {
    // 1. Create inventory
    const payload = {
      location_id: form.location_id,
      inventory_date: form.inventory_date,
      notes: form.notes,
      items: items.value.map((i) => ({
        material_id: i.material_id,
        actual_quantity: i.actual_quantity,
        unit_price: i.unit_price,
      })),
    }

    const created = await stockService.createInventory(payload)

    // 2. Validate to apply adjustments
    const validated = await stockService.validateInventory(created.id)

    Swal.fire({
      icon: 'success',
      title: 'Inventaire validé !',
      text: `Réf: ${validated.reference}. Les stocks ont été ajustés avec les écarts réels.`,
      timer: 2000,
      showConfirmButton: false,
    })

    emit('saved', validated)
    close()
  } catch (error) {
    const detail = error.response?.data?.detail || error.message
    Swal.fire('Erreur', detail, 'error')
  } finally {
    saving.value = false
  }
}
</script>
