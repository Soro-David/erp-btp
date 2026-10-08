<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-4xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-lg">
            <fas-icon :icon="isEdit ? 'pen-to-square' : 'cart-shopping'" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">
              {{ isEdit ? 'Modifier le Bon de Commande' : 'Nouvel Achat / Bon de Commande BTP' }}
            </h2>
            <p class="text-xs text-slate-500">
              Rattachement au chantier, sélection des matériaux et engagement financier
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
      <form @submit.prevent="handleSubmit" class="p-6 overflow-y-auto space-y-5 text-xs flex-1">
        <!-- 1. Informations Générales & Chantier -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80">
          <!-- Chantier (Obligatoire) -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Chantier d'affectation *</label>
            <select
              v-model="form.chantier_id"
              required
              @change="onChantierChange"
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            >
              <option :value="null" disabled>Sélectionner un chantier</option>
              <option v-for="c in chantiers" :key="c.id" :value="c.id">
                {{ c.code }} - {{ c.name }}
              </option>
            </select>
          </div>

          <!-- Tâche du chantier (Optionnelle, filtrée strictly sur ce chantier) -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">
              Tâche concernée <span class="text-slate-400 font-normal">(optionnel)</span>
            </label>
            <select
              v-model="form.task_id"
              :disabled="!form.chantier_id || loadingTasks"
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs disabled:bg-slate-100 disabled:text-slate-400"
            >
              <option :value="null">-- Aucune tâche spécifique --</option>
              <option v-for="t in tasks" :key="t.id" :value="t.id">
                {{ t.code }} - {{ t.name }}
              </option>
            </select>
          </div>

          <!-- Fournisseur avec bouton [+] rapide -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="font-bold text-slate-700">Fournisseur *</label>
              <button
                type="button"
                @click="openAddSupplierModal = true"
                class="text-[11px] font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                title="Ajouter un nouveau fournisseur"
              >
                <fas-icon icon="plus" class="text-[10px]" />
                <span>Nouveau</span>
              </button>
            </div>
            <select
              v-model="form.supplier_id"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            >
              <option :value="null" disabled>Sélectionner un fournisseur</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">
                {{ s.code }} - {{ s.name }}
              </option>
            </select>
          </div>

          <!-- Date de commande -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Date d'émission *</label>
            <input
              v-model="form.date"
              type="date"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            />
          </div>

          <!-- Mode de règlement -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Mode de règlement</label>
            <select
              v-model="form.payment_mode"
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            >
              <option value="Virement">Virement bancaire</option>
              <option value="Chèque">Chèque d'entreprise</option>
              <option value="Espèces">Espèces / Caisse chantier</option>
              <option value="Mobile Money">Mobile Money (Wave / Orange)</option>
            </select>
          </div>

          <!-- Statut de paiement -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Statut du Paiement</label>
            <select
              v-model="form.payment_status"
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            >
              <option value="Non payé">Non payé</option>
              <option value="Partiellement payé">Partiellement payé</option>
              <option value="Payé">Payé intégralement</option>
            </select>
          </div>

          <!-- Objet synthétique -->
          <div class="sm:col-span-2 md:col-span-3">
            <label class="block font-bold text-slate-700 mb-1">Objet synthétique de l'achat</label>
            <input
              v-model="form.subject"
              type="text"
              placeholder="Ex: Fourniture d'armatures pour semelles de fondation et longrines"
              class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 shadow-2xs"
            />
          </div>
        </div>

        <!-- 2. Lignes d'articles commandés (Matériaux) -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="font-bold text-slate-800 text-sm">Articles & Matériaux commandés</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-blue-100 text-blue-800">
                {{ form.lines.length }} article(s)
              </span>
            </div>
            <div class="flex items-center gap-2">
              <button
                type="button"
                @click="openAddMaterialModal = true"
                class="text-xs font-bold text-slate-600 hover:text-slate-800 px-2.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 flex items-center gap-1.5 transition-colors"
                title="Créer un nouveau matériau dans le catalogue"
              >
                <fas-icon icon="plus" class="text-[10px]" />
                <span>Nouveau Matériau</span>
              </button>
              <button
                type="button"
                @click="addLine"
                class="text-xs font-bold text-blue-700 hover:text-blue-800 px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 border border-blue-200 flex items-center gap-1.5 transition-colors"
              >
                <fas-icon icon="plus" />
                <span>Ajouter une ligne</span>
              </button>
            </div>
          </div>

          <!-- Tableau dynamique des lignes -->
          <div class="overflow-x-auto rounded-2xl border border-slate-200">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-100/80 text-[11px] font-extrabold text-slate-600 uppercase tracking-wider border-b border-slate-200">
                  <th class="py-2.5 px-3">Matériau *</th>
                  <th class="py-2.5 px-3 w-28 text-right">Quantité *</th>
                  <th class="py-2.5 px-3 w-36 text-right">Prix Unitaire (FCFA) *</th>
                  <th class="py-2.5 px-3 w-36 text-right">Montant Total</th>
                  <th class="py-2.5 px-2 w-12 text-center"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="(line, index) in form.lines" :key="index" class="hover:bg-slate-50/50">
                  <!-- Matériau select -->
                  <td class="py-2 px-3">
                    <select
                      v-model="line.material_id"
                      required
                      @change="onMaterialSelected(line)"
                      class="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 font-semibold focus:outline-none focus:border-blue-600 text-xs"
                    >
                      <option :value="null" disabled>Sélectionner un matériau</option>
                      <option v-for="m in materials" :key="m.id" :value="m.id">
                        {{ m.name }} ({{ m.unit?.code || 'U' }}) - Stock dispo: {{ m.current_stock }}
                      </option>
                    </select>
                  </td>

                  <!-- Quantité -->
                  <td class="py-2 px-3 text-right">
                    <input
                      v-model.number="line.quantity"
                      type="number"
                      step="any"
                      min="0.01"
                      required
                      @input="recalculateLine(line)"
                      class="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 font-bold text-right focus:outline-none focus:border-blue-600 text-xs font-mono"
                    />
                  </td>

                  <!-- Prix unitaire -->
                  <td class="py-2 px-3 text-right">
                    <input
                      v-model.number="line.unit_price"
                      type="number"
                      min="0"
                      step="any"
                      required
                      @input="recalculateLine(line)"
                      class="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 font-bold text-right focus:outline-none focus:border-blue-600 text-xs font-mono"
                    />
                  </td>

                  <!-- Total ligne -->
                  <td class="py-2 px-3 text-right font-black text-slate-800 font-mono text-xs">
                    {{ formatNumber(line.total_price || 0) }} FCFA
                  </td>

                  <!-- Supprimer ligne -->
                  <td class="py-2 px-2 text-center">
                    <button
                      type="button"
                      @click="removeLine(index)"
                      :disabled="form.lines.length <= 1"
                      class="p-1.5 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50 disabled:opacity-30 disabled:cursor-not-allowed"
                      title="Supprimer la ligne"
                    >
                      <fas-icon icon="trash-can" class="text-xs" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Total Global -->
          <div class="flex justify-end p-4 rounded-2xl bg-blue-50/60 border border-blue-100 items-center gap-6">
            <span class="text-xs font-bold text-slate-600 uppercase tracking-wider">
              Total Commande TTC :
            </span>
            <span class="text-xl font-black text-blue-900 font-mono">
              {{ formatNumber(computedTotalAmount) }} FCFA
            </span>
          </div>
        </div>

        <!-- 3. Notes internes -->
        <div>
          <label class="block font-bold text-slate-700 mb-1">Notes / Instructions de livraison</label>
          <textarea
            v-model="form.notes"
            rows="2"
            placeholder="Consignes de livraison, contact réceptionnaire sur site..."
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
            :disabled="saving"
            class="px-6 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-700 text-white font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else :icon="isEdit ? 'check' : 'cart-arrow-down'" />
            <span>{{ isEdit ? 'Enregistrer les modifications' : 'Créer le Bon de Commande' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Inline Add Supplier Modal -->
    <AddSupplierModal
      :is-open="openAddSupplierModal"
      @close="openAddSupplierModal = false"
      @saved="onSupplierSaved"
    />

    <!-- Inline Add Material Modal -->
    <AddMaterialModal
      :is-open="openAddMaterialModal"
      @close="openAddMaterialModal = false"
      @saved="onMaterialSaved"
    />
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { purchaseService, supplierService, materialService, chantierService, taskService } from '@/services'
import AddSupplierModal from './AddSupplierModal.vue'
import AddMaterialModal from './AddMaterialModal.vue'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  purchase: {
    type: Object,
    default: null,
  },
  defaultChantierId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const isEdit = ref(false)
const saving = ref(false)
const loadingTasks = ref(false)

const openAddSupplierModal = ref(false)
const openAddMaterialModal = ref(false)

const chantiers = ref([])
const tasks = ref([])
const suppliers = ref([])
const materials = ref([])

const form = reactive({
  reference: '',
  chantier_id: null,
  task_id: null,
  supplier_id: null,
  date: new Date().toISOString().split('T')[0],
  status: 'Commandé',
  payment_status: 'Non payé',
  payment_mode: 'Virement',
  subject: '',
  notes: '',
  lines: [
    { material_id: null, quantity: 1, unit_price: 0, total_price: 0 },
  ],
})

const computedTotalAmount = computed(() => {
  return form.lines.reduce((sum, l) => sum + (Number(l.total_price) || 0), 0)
})

const formatNumber = (val) => {
  return new Intl.NumberFormat('fr-FR').format(val || 0)
}

const loadChantiers = async () => {
  try {
    const data = await chantierService.getChantiers()
    chantiers.value = data.items || data || []
    if (!form.chantier_id && props.defaultChantierId) {
      form.chantier_id = props.defaultChantierId
      await loadTasksForChantier(form.chantier_id)
    } else if (!form.chantier_id && chantiers.value.length > 0) {
      form.chantier_id = chantiers.value[0].id
      await loadTasksForChantier(form.chantier_id)
    }
  } catch (err) {
    console.error('Erreur chargement chantiers:', err)
  }
}

const loadTasksForChantier = async (chantierId) => {
  if (!chantierId) {
    tasks.value = []
    return
  }
  loadingTasks.value = true
  try {
    const data = await taskService.getTasks(chantierId)
    tasks.value = data || []
  } catch (err) {
    console.error('Erreur chargement des tâches:', err)
    tasks.value = []
  } finally {
    loadingTasks.value = false
  }
}

const onChantierChange = async () => {
  form.task_id = null
  await loadTasksForChantier(form.chantier_id)
}

const loadSuppliers = async () => {
  try {
    suppliers.value = await supplierService.getSuppliers({ is_active: true })
  } catch (err) {
    console.error('Erreur fournisseurs:', err)
  }
}

const loadMaterials = async () => {
  try {
    materials.value = await materialService.getMaterials({ is_active: true })
  } catch (err) {
    console.error('Erreur matériaux:', err)
  }
}

onMounted(() => {
  loadChantiers()
  loadSuppliers()
  loadMaterials()
})

const addLine = () => {
  form.lines.push({ material_id: null, quantity: 1, unit_price: 0, total_price: 0 })
}

const removeLine = (index) => {
  if (form.lines.length > 1) {
    form.lines.splice(index, 1)
  }
}

const onMaterialSelected = (line) => {
  const mat = materials.value.find((m) => m.id === line.material_id)
  if (mat) {
    line.unit_price = Number(mat.indicative_price) || 0
    recalculateLine(line)
  }
}

const recalculateLine = (line) => {
  line.total_price = Math.round((Number(line.quantity) || 0) * (Number(line.unit_price) || 0))
}

const onSupplierSaved = async (newSup) => {
  await loadSuppliers()
  form.supplier_id = newSup.id
}

const onMaterialSaved = async (newMat) => {
  await loadMaterials()
  // assign to last line if empty
  const lastLine = form.lines[form.lines.length - 1]
  if (lastLine && !lastLine.material_id) {
    lastLine.material_id = newMat.id
    onMaterialSelected(lastLine)
  }
}

watch(
  () => props.purchase,
  async (val) => {
    if (val && val.id) {
      isEdit.value = true
      form.chantier_id = val.chantier_id
      await loadTasksForChantier(val.chantier_id)
      form.task_id = val.task_id || null
      form.supplier_id = val.supplier_id
      form.date = val.date
      form.status = val.status || 'Commandé'
      form.payment_status = val.payment_status || 'Non payé'
      form.payment_mode = val.payment_mode || 'Virement'
      form.subject = val.subject || ''
      form.notes = val.notes || ''
      if (val.lines && val.lines.length > 0) {
        form.lines = val.lines.map((l) => ({
          material_id: l.material_id,
          quantity: l.quantity,
          unit_price: Number(l.unit_price),
          total_price: Number(l.total_price),
        }))
      }
    } else {
      isEdit.value = false
      form.task_id = null
      form.subject = ''
      form.notes = ''
      form.lines = [{ material_id: null, quantity: 1, unit_price: 0, total_price: 0 }]
      if (props.defaultChantierId) {
        form.chantier_id = props.defaultChantierId
        loadTasksForChantier(form.chantier_id)
      }
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  // Validate lines
  for (const line of form.lines) {
    if (!line.material_id) {
      Swal.fire('Attention', 'Veuillez sélectionner un matériau pour chaque ligne', 'warning')
      return
    }
    if (!line.quantity || line.quantity <= 0) {
      Swal.fire('Attention', 'La quantité doit être supérieure à zéro', 'warning')
      return
    }
  }

  saving.value = true
  try {
    let result
    if (isEdit.value && props.purchase?.id) {
      result = await purchaseService.updatePurchase(props.purchase.id, form)
      Swal.fire({
        icon: 'success',
        title: 'Achat mis à jour',
        text: `La commande ${result.reference} a été enregistrée.`,
        timer: 1800,
        showConfirmButton: false,
      })
    } else {
      result = await purchaseService.createPurchase(form)
      Swal.fire({
        icon: 'success',
        title: 'Bon de commande créé',
        text: `Commande ${result.reference} générée avec succès.`,
        timer: 1800,
        showConfirmButton: false,
      })
    }
    emit('saved', result)
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
