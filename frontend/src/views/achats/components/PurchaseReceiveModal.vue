<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-3xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-emerald-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center text-lg">
            <fas-icon icon="dolly" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-base font-bold text-slate-800">Réceptionner la Commande</h2>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-100 text-emerald-800">
                {{ purchase?.reference }}
              </span>
            </div>
            <p class="text-xs text-slate-500">
              Contrôle des quantités livrées et mise à jour automatique des stocks
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
        <!-- Informations de réception -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 bg-slate-50 p-4 rounded-2xl border border-slate-200">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Dépôt de stockage *</label>
            <select
              v-model="form.location_id"
              required
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-emerald-600"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                {{ loc.code }} - {{ loc.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Date de livraison *</label>
            <input
              v-model="form.date"
              type="date"
              required
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-emerald-600"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">N° Bon de Livraison (BL)</label>
            <input
              v-model="form.receipt_number"
              type="text"
              placeholder="Auto / BL-XXXX"
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-emerald-600"
            />
          </div>
        </div>

        <!-- Tableau des articles à réceptionner -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-800">Contrôle des articles livrés</span>
            <button
              type="button"
              @click="receiveAllRemaining"
              class="text-[11px] font-bold text-emerald-700 hover:text-emerald-800 px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 border border-emerald-200"
            >
              Tout réceptionner (solde restant)
            </button>
          </div>

          <div class="overflow-x-auto rounded-2xl border border-slate-200">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-100 text-[11px] font-extrabold text-slate-600 uppercase border-b border-slate-200">
                  <th class="py-2.5 px-3">Article commandé</th>
                  <th class="py-2.5 px-3 text-right">Commandé</th>
                  <th class="py-2.5 px-3 text-right">Déjà reçu</th>
                  <th class="py-2.5 px-3 text-right">Reste</th>
                  <th class="py-2.5 px-3 text-right w-28">Reçu ce jour *</th>
                  <th class="py-2.5 px-3 text-right w-24">Rejeté</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="item in items" :key="item.purchase_line_id" class="hover:bg-slate-50/50">
                  <td class="py-2 px-3">
                    <div class="font-bold text-slate-800">{{ item.material_name }}</div>
                    <div class="text-[10px] text-slate-400">Unité : {{ item.unit_code }}</div>
                  </td>
                  <td class="py-2 px-3 text-right font-mono font-bold text-slate-700">
                    {{ item.quantity_ordered }}
                  </td>
                  <td class="py-2 px-3 text-right font-mono text-emerald-600 font-bold">
                    {{ item.quantity_received_total }}
                  </td>
                  <td class="py-2 px-3 text-right font-mono font-black text-amber-600">
                    {{ item.remaining }}
                  </td>
                  <td class="py-2 px-3 text-right">
                    <input
                      v-model.number="item.quantity_received"
                      type="number"
                      step="any"
                      min="0"
                      :max="item.remaining"
                      class="w-full px-2.5 py-1.5 rounded-lg bg-emerald-50/50 border border-emerald-300 font-bold text-right text-emerald-900 font-mono text-xs focus:outline-none focus:border-emerald-600"
                    />
                  </td>
                  <td class="py-2 px-3 text-right">
                    <input
                      v-model.number="item.quantity_rejected"
                      type="number"
                      step="any"
                      min="0"
                      class="w-full px-2 py-1.5 rounded-lg bg-slate-50 border border-slate-200 font-bold text-right text-slate-700 font-mono text-xs focus:outline-none"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Remarques de livraison -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Observations sur la livraison</label>
          <textarea
            v-model="form.notes"
            rows="2"
            placeholder="État des sacs, conformité des diamètres, état du scellé..."
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-emerald-600"
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
            class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold shadow-md shadow-emerald-700/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check-double" />
            <span>Valider la Réception & Incrémenter le Stock</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { purchaseService, stockService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  purchase: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const locations = ref([])
const items = ref([])

const form = reactive({
  location_id: null,
  date: new Date().toISOString().split('T')[0],
  receipt_number: '',
  notes: '',
})

const loadLocations = async () => {
  try {
    locations.value = await stockService.getLocations({ is_active: true })
    if (locations.value.length > 0 && !form.location_id) {
      form.location_id = locations.value[0].id
    }
  } catch (err) {
    console.error('Erreur chargement dépôts:', err)
  }
}

onMounted(() => {
  loadLocations()
})

watch(
  () => props.purchase,
  (p) => {
    if (p && p.lines) {
      items.value = p.lines.map((l) => {
        const remaining = Math.max(0, l.quantity - (l.quantity_received || 0))
        return {
          purchase_line_id: l.id,
          material_id: l.material_id,
          material_name: l.material?.name || `Matériau #${l.material_id}`,
          unit_code: l.material?.unit?.code || 'U',
          quantity_ordered: l.quantity,
          quantity_received_total: l.quantity_received || 0,
          remaining: remaining,
          quantity_received: remaining, // default propose receiving full remaining
          quantity_rejected: 0,
          rejection_reason: '',
        }
      })
    }
  },
  { immediate: true }
)

const receiveAllRemaining = () => {
  items.value.forEach((item) => {
    item.quantity_received = item.remaining
    item.quantity_rejected = 0
  })
}

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  const receivingAny = items.value.some((it) => it.quantity_received > 0)
  if (!receivingAny) {
    Swal.fire('Attention', 'Veuillez saisir au moins une quantité reçue supérieure à zéro', 'warning')
    return
  }

  saving.value = true
  try {
    const payload = {
      location_id: form.location_id,
      date: form.date,
      receipt_number: form.receipt_number || undefined,
      notes: form.notes || undefined,
      items: items.value
        .filter((it) => it.quantity_received > 0 || it.quantity_rejected > 0)
        .map((it) => ({
          purchase_line_id: it.purchase_line_id,
          quantity_received: it.quantity_received,
          quantity_rejected: it.quantity_rejected || 0,
          rejection_reason: it.rejection_reason || undefined,
        })),
    }

    const receipt = await purchaseService.createReceipt(props.purchase.id, payload)
    Swal.fire({
      icon: 'success',
      title: 'Réception validée !',
      text: `Bon ${receipt.receipt_number} enregistré. Les quantités ont été ajoutées au stock.`,
      timer: 2000,
      showConfirmButton: false,
    })

    emit('saved', receipt)
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
