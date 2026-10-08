<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center text-lg">
            <fas-icon :icon="isEdit ? 'pen-to-square' : 'cubes'" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">
              {{ isEdit ? 'Modifier le Matériau' : 'Nouveau Matériau BTP' }}
            </h2>
            <p class="text-xs text-slate-500">
              Référence catalogue, conditionnement, prix indicatif et seuils d'alerte de stock
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
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Code Matériau -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Code Matériau</label>
            <input
              v-model="form.code"
              type="text"
              placeholder="Auto-généré (ex: MAT-2026-012)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 uppercase"
            />
          </div>

          <!-- Désignation -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Désignation du Matériau *</label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="Ex: Ciment CPJ 35 (Sac 50kg)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Catégorie avec bouton [+] création dynamique -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="font-bold text-slate-700">Catégorie *</label>
              <button
                type="button"
                @click="showAddCategoryPrompt"
                class="text-[11px] font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                title="Ajouter une nouvelle catégorie"
              >
                <fas-icon icon="plus" class="text-[10px]" />
                <span>Nouvelle</span>
              </button>
            </div>
            <select
              v-model="form.category_id"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option :value="null" disabled>Sélectionner une catégorie</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <!-- Unité de mesure avec bouton [+] création dynamique -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="font-bold text-slate-700">Unité de mesure *</label>
              <button
                type="button"
                @click="showAddUnitPrompt"
                class="text-[11px] font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                title="Ajouter une nouvelle unité"
              >
                <fas-icon icon="plus" class="text-[10px]" />
                <span>Nouvelle</span>
              </button>
            </div>
            <select
              v-model="form.unit_id"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            >
              <option :value="null" disabled>Sélectionner une unité</option>
              <option v-for="unit in units" :key="unit.id" :value="unit.id">
                {{ unit.code }} - {{ unit.name }}
              </option>
            </select>
          </div>

          <!-- Référence fabricant / catalogue -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Référence Fabricant / Marque</label>
            <input
              v-model="form.reference"
              type="text"
              placeholder="Ex: CIMAF-CPJ35"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Prix unitaire indicatif HT -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Prix Unitaire Indicatif (FCFA)</label>
            <input
              v-model.number="form.indicative_price"
              type="number"
              min="0"
              step="100"
              placeholder="Ex: 4800"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 font-mono"
            />
          </div>

          <!-- Seuil Stock Minimum (Alerte Rupture) -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Stock Minimum (Alerte réappro)</label>
            <input
              v-model.number="form.minimum_stock"
              type="number"
              min="0"
              placeholder="Ex: 50"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 font-mono"
            />
          </div>

          <!-- Seuil Stock Maximum (Capacité / Surstock) -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Stock Maximum (Capacité max)</label>
            <input
              v-model.number="form.maximum_stock"
              type="number"
              min="0"
              placeholder="Ex: 500"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 font-mono"
            />
          </div>

          <!-- Description / Spécifications techniques -->
          <div class="md:col-span-2">
            <label class="block font-bold text-slate-700 mb-1">Description / Spécifications</label>
            <textarea
              v-model="form.description"
              rows="2"
              placeholder="Normes, caractéristiques mécaniques, conseils de stockage..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            ></textarea>
          </div>
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
            class="px-5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-700 text-white font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else :icon="isEdit ? 'check' : 'plus'" />
            <span>{{ isEdit ? 'Mettre à jour' : 'Enregistrer le Matériau' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { materialService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  material: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const isEdit = ref(false)
const saving = ref(false)
const categories = ref([])
const units = ref([])

const form = reactive({
  code: '',
  name: '',
  description: '',
  category_id: null,
  unit_id: null,
  reference: '',
  indicative_price: 0,
  minimum_stock: 0,
  maximum_stock: 0,
  is_active: true,
})

const loadReferentials = async () => {
  try {
    const [cats, uns] = await Promise.all([
      materialService.getCategories(),
      materialService.getUnits(),
    ])
    categories.value = cats
    units.value = uns
  } catch (error) {
    console.error('Erreur chargement référentiels matériaux:', error)
  }
}

onMounted(() => {
  loadReferentials()
})

const resetForm = () => {
  form.code = ''
  form.name = ''
  form.description = ''
  form.category_id = categories.value[0]?.id || null
  form.unit_id = units.value[0]?.id || null
  form.reference = ''
  form.indicative_price = 0
  form.minimum_stock = 0
  form.maximum_stock = 0
  form.is_active = true
}

watch(
  () => props.material,
  (val) => {
    if (val && val.id) {
      isEdit.value = true
      Object.assign(form, {
        code: val.code,
        name: val.name,
        description: val.description || '',
        category_id: val.category_id,
        unit_id: val.unit_id,
        reference: val.reference || '',
        indicative_price: val.indicative_price || 0,
        minimum_stock: val.minimum_stock || 0,
        maximum_stock: val.maximum_stock || 0,
        is_active: val.is_active,
      })
    } else {
      isEdit.value = false
      resetForm()
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

// Inline prompt creation for category without leaving form
const showAddCategoryPrompt = async () => {
  const { value: catName } = await Swal.fire({
    title: 'Nouvelle catégorie',
    input: 'text',
    inputLabel: 'Nom de la catégorie (ex: Échafaudage & Étaiement)',
    inputPlaceholder: 'Entrez le nom...',
    showCancelButton: true,
    confirmButtonText: 'Ajouter',
    cancelButtonText: 'Annuler',
    inputValidator: (value) => {
      if (!value) return 'Veuillez saisir un nom'
    },
  })

  if (catName) {
    try {
      const newCat = await materialService.createCategory({ name: catName })
      await loadReferentials()
      form.category_id = newCat.id
    } catch (e) {
      Swal.fire('Erreur', e.response?.data?.detail || e.message, 'error')
    }
  }
}

// Inline prompt creation for unit without leaving form
const showAddUnitPrompt = async () => {
  const { value: formValues } = await Swal.fire({
    title: 'Nouvelle unité de mesure',
    html:
      '<input id="swal-unit-code" class="swal2-input" placeholder="Code (ex: M3, BARRE, SAC)">' +
      '<input id="swal-unit-name" class="swal2-input" placeholder="Libellé (ex: Mètre cube, Barre 12m)">',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Ajouter',
    cancelButtonText: 'Annuler',
    preConfirm: () => {
      const code = document.getElementById('swal-unit-code').value
      const name = document.getElementById('swal-unit-name').value
      if (!code || !name) {
        Swal.showValidationMessage('Veuillez renseigner le code et le libellé')
        return false
      }
      return { code, name }
    },
  })

  if (formValues) {
    try {
      const newUnit = await materialService.createUnit(formValues)
      await loadReferentials()
      form.unit_id = newUnit.id
    } catch (e) {
      Swal.fire('Erreur', e.response?.data?.detail || e.message, 'error')
    }
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    let result
    if (isEdit.value && props.material?.id) {
      result = await materialService.updateMaterial(props.material.id, form)
      Swal.fire({
        icon: 'success',
        title: 'Matériau mis à jour',
        text: `${result.name} a été actualisé.`,
        timer: 1800,
        showConfirmButton: false,
      })
    } else {
      result = await materialService.createMaterial(form)
      Swal.fire({
        icon: 'success',
        title: 'Matériau enregistré',
        text: `${result.name} ajouté au catalogue (${result.code}).`,
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
