<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête avec badge Urgence Terrain -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-amber-50 to-orange-50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 text-white flex items-center justify-center text-lg shadow-sm">
            <fas-icon icon="bolt" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-base font-black text-slate-800">Achat Rapide Terrain</h2>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-orange-100 text-orange-800">
                Mode Urgence
              </span>
            </div>
            <p class="text-xs text-slate-500">
              Saisie simplifiée sur site avec photo du reçu ou ticket de caisse
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
        <!-- 1. Chantier & Tâche -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Chantier d'affectation *</label>
            <select
              v-model="form.chantier_id"
              required
              @change="onChantierChange"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            >
              <option :value="null" disabled>Sélectionner un chantier</option>
              <option v-for="c in chantiers" :key="c.id" :value="c.id">
                {{ c.code }} - {{ c.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Tâche concernée (optionnel)</label>
            <select
              v-model="form.task_id"
              :disabled="!form.chantier_id || loadingTasks"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500 disabled:opacity-50"
            >
              <option :value="null">-- Non spécifiée --</option>
              <option v-for="t in tasks" :key="t.id" :value="t.id">
                {{ t.code }} - {{ t.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- 2. Fournisseur (existant ou nouveau immédiat) -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label class="font-bold text-slate-700">Fournisseur *</label>
            <button
              type="button"
              @click="toggleCustomSupplier"
              class="text-[11px] font-bold text-orange-600 hover:text-orange-800"
            >
              {{ isCustomSupplier ? 'Choisir dans la liste' : '+ Nouveau fournisseur direct' }}
            </button>
          </div>

          <div v-if="!isCustomSupplier">
            <select
              v-model="form.supplier_id"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            >
              <option :value="null" disabled>Sélectionner le fournisseur...</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">
                {{ s.code }} - {{ s.name }}
              </option>
            </select>
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <input
              v-model="form.supplier_name"
              type="text"
              required
              placeholder="Nom / Enseigne du commerçant"
              class="w-full px-3.5 py-2.5 rounded-xl bg-orange-50/40 border border-orange-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            />
            <input
              v-model="form.supplier_phone"
              type="text"
              placeholder="Téléphone (ex: +225 07...)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-orange-50/40 border border-orange-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            />
          </div>
        </div>

        <!-- 3. Matériau / Article (existant ou nouveau direct) -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label class="font-bold text-slate-700">Matériau ou Article *</label>
            <button
              type="button"
              @click="toggleCustomMaterial"
              class="text-[11px] font-bold text-orange-600 hover:text-orange-800"
            >
              {{ isCustomMaterial ? 'Choisir dans le catalogue' : '+ Article non répertorié' }}
            </button>
          </div>

          <div v-if="!isCustomMaterial">
            <select
              v-model="form.material_id"
              required
              @change="onMaterialChange"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            >
              <option :value="null" disabled>Sélectionner le matériau...</option>
              <option v-for="m in materials" :key="m.id" :value="m.id">
                {{ m.name }} ({{ m.unit?.code || 'U' }}) - Réf: {{ m.code }}
              </option>
            </select>
          </div>

          <div v-else>
            <input
              v-model="form.material_name"
              type="text"
              required
              placeholder="Désignation de l'article (ex: Disque diamant 230mm, 5kg pointes de coffrage...)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-orange-50/40 border border-orange-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            />
          </div>
        </div>

        <!-- 4. Quantité, Prix unitaire & Total -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Quantité *</label>
            <input
              v-model.number="form.quantity"
              type="number"
              min="0.01"
              step="any"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-bold focus:outline-none focus:bg-white focus:border-orange-500 font-mono"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Prix Unitaire (FCFA) *</label>
            <input
              v-model.number="form.unit_price"
              type="number"
              min="0"
              step="any"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-bold focus:outline-none focus:bg-white focus:border-orange-500 font-mono"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Montant Total</label>
            <div class="px-3.5 py-2.5 rounded-xl bg-orange-100/60 border border-orange-200 font-black text-orange-950 font-mono text-center">
              {{ formatNumber(computedTotal) }} FCFA
            </div>
          </div>
        </div>

        <!-- 5. Mode de règlement & Date -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Mode de règlement</label>
            <select
              v-model="form.payment_mode"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            >
              <option value="Espèces">Espèces (Caisse chantier)</option>
              <option value="Mobile Money">Mobile Money (Wave / Orange)</option>
              <option value="Chèque">Chèque</option>
              <option value="Virement">Virement bancaire</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Date d'achat</label>
            <input
              v-model="form.date"
              type="date"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-orange-500"
            />
          </div>
        </div>

        <!-- 6. Options automatiques de réception en stock -->
        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="form.auto_receive"
              class="w-4 h-4 rounded text-orange-600 focus:ring-orange-500 border-slate-300"
            />
            <span class="font-bold text-slate-800">
              Réceptionner et intégrer immédiatement dans le stock
            </span>
          </label>

          <div v-if="form.auto_receive" class="pt-1">
            <label class="block text-[11px] font-bold text-slate-600 mb-1">Dépôt de réception :</label>
            <select
              v-model="form.location_id"
              class="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 font-semibold text-xs focus:outline-none focus:border-orange-500"
            >
              <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                {{ loc.code }} - {{ loc.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- 7. Photo du reçu / ticket (Mobile Camera) -->
        <div class="space-y-1.5">
          <label class="block font-bold text-slate-700">Justificatif / Photo du ticket</label>
          <div class="flex items-center gap-3">
            <button
              type="button"
              @click="$refs.receiptCamera.click()"
              class="flex-1 py-3 px-4 rounded-2xl border-2 border-dashed border-orange-300 hover:border-orange-500 bg-orange-50/50 hover:bg-orange-50 text-orange-800 font-bold flex items-center justify-center gap-2 transition-colors"
            >
              <fas-icon icon="camera" class="text-base" />
              <span>{{ receiptPhoto ? 'Photo sélectionnée ✓' : 'Prendre en photo le ticket' }}</span>
            </button>
            <input
              ref="receiptCamera"
              type="file"
              accept="image/*"
              capture="environment"
              class="hidden"
              @change="onPhotoSelected"
            />
          </div>
          <p v-if="receiptPhoto" class="text-[11px] text-green-700 font-semibold flex items-center gap-1">
            <fas-icon icon="circle-check" />
            <span>{{ receiptPhoto.name }} ({{ (receiptPhoto.size / 1024).toFixed(0) }} Ko)</span>
          </p>
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
            class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-extrabold shadow-md shadow-orange-600/30 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="bolt" />
            <span>Valider l'Achat Terrain</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { purchaseService, supplierService, materialService, chantierService, taskService, stockService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  defaultChantierId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const loadingTasks = ref(false)
const isCustomSupplier = ref(false)
const isCustomMaterial = ref(false)
const receiptPhoto = ref(null)

const chantiers = ref([])
const tasks = ref([])
const suppliers = ref([])
const materials = ref([])
const locations = ref([])

const form = reactive({
  chantier_id: null,
  task_id: null,
  supplier_id: null,
  supplier_name: '',
  supplier_phone: '',
  material_id: null,
  material_name: '',
  quantity: 1,
  unit_price: 0,
  date: new Date().toISOString().split('T')[0],
  payment_mode: 'Espèces',
  auto_receive: true,
  location_id: null,
})

const computedTotal = computed(() => {
  return Math.round((Number(form.quantity) || 0) * (Number(form.unit_price) || 0))
})

const formatNumber = (val) => {
  return new Intl.NumberFormat('fr-FR').format(val || 0)
}

const loadData = async () => {
  try {
    const [chData, supData, matData, locData] = await Promise.all([
      chantierService.getChantiers(),
      supplierService.getSuppliers({ is_active: true }),
      materialService.getMaterials({ is_active: true }),
      stockService.getLocations({ is_active: true }),
    ])
    chantiers.value = chData.items || chData || []
    suppliers.value = supData
    materials.value = matData
    locations.value = locData

    if (locations.value.length > 0) {
      form.location_id = locations.value[0].id
    }

    if (!form.chantier_id && props.defaultChantierId) {
      form.chantier_id = props.defaultChantierId
      await loadTasksForChantier(form.chantier_id)
    } else if (!form.chantier_id && chantiers.value.length > 0) {
      form.chantier_id = chantiers.value[0].id
      await loadTasksForChantier(form.chantier_id)
    }
  } catch (err) {
    console.error('Erreur chargement données:', err)
  }
}

onMounted(() => {
  loadData()
})

const loadTasksForChantier = async (chantierId) => {
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
  await loadTasksForChantier(form.chantier_id)
}

const onMaterialChange = () => {
  const m = materials.value.find((mat) => mat.id === form.material_id)
  if (m) {
    form.unit_price = Number(m.indicative_price) || 0
  }
}

const toggleCustomSupplier = () => {
  isCustomSupplier.value = !isCustomSupplier.value
  if (isCustomSupplier.value) form.supplier_id = null
  else {
    form.supplier_name = ''
    form.supplier_phone = ''
  }
}

const toggleCustomMaterial = () => {
  isCustomMaterial.value = !isCustomMaterial.value
  if (isCustomMaterial.value) form.material_id = null
  else form.material_name = ''
}

const onPhotoSelected = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    receiptPhoto.value = file
  }
}

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  saving.value = true
  try {
    // 1. Prepare payload
    const payload = {
      chantier_id: form.chantier_id,
      task_id: form.task_id || undefined,
      supplier_id: isCustomSupplier.value ? undefined : form.supplier_id,
      supplier_name: isCustomSupplier.value ? form.supplier_name : undefined,
      supplier_phone: isCustomSupplier.value ? form.supplier_phone : undefined,
      date: form.date,
      payment_mode: form.payment_mode,
      auto_receive: form.auto_receive,
      location_id: form.auto_receive ? form.location_id : undefined,
      items: [
        {
          material_id: isCustomMaterial.value ? undefined : form.material_id,
          material_name: isCustomMaterial.value ? form.material_name : undefined,
          quantity: form.quantity,
          unit_price: form.unit_price,
        },
      ],
    }

    const createdPurchase = await purchaseService.createQuickPurchase(payload)

    // 2. If photo attached, upload it
    if (receiptPhoto.value && createdPurchase?.id) {
      try {
        const formData = new FormData()
        formData.append('file', receiptPhoto.value)
        formData.append('document_type', 'Reçu')
        formData.append('document_number', `TICKET-${createdPurchase.reference}`)
        await purchaseService.uploadDocument(createdPurchase.id, formData)
      } catch (uploadErr) {
        console.error('Erreur upload photo ticket:', uploadErr)
      }
    }

    Swal.fire({
      icon: 'success',
      title: 'Achat rapide enregistré !',
      text: `Réf: ${createdPurchase.reference} - Montant: ${formatNumber(createdPurchase.total_amount)} FCFA. Stock mis à jour.`,
      timer: 2200,
      showConfirmButton: false,
    })

    emit('saved', createdPurchase)
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
