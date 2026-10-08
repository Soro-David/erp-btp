<template>
  <div class="space-y-6">
    <!-- En-tête Page & Bouton d'ajout -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="cubes" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Catalogue des Matériaux</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">BTP Catalogue</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Nomenclature des fournitures, conditionnements, seuils d'alerte et valorisation du stock
          </p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="openAddMaterialModal(null)"
          class="px-4 py-2.5 rounded-2xl bg-[#1d4ed8] hover:bg-blue-700 text-white text-xs font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 transition-all transform active:scale-95"
        >
          <fas-icon icon="plus" />
          <span>+ Nouveau Matériau</span>
        </button>
      </div>
    </div>

    <!-- KPIs Matériaux & Stocks -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Total Références</span>
          <fas-icon icon="list" class="text-blue-600" />
        </div>
        <div>
          <div class="text-2xl font-black text-slate-900 font-mono">{{ materials.length }}</div>
          <div class="text-[10px] text-slate-400 mt-0.5">Articles au catalogue</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Ruptures de Stock</span>
          <fas-icon icon="triangle-exclamation" class="text-red-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-red-600 font-mono">
            {{ materials.filter((m) => m.stock_status === 'Rupture').length }}
          </div>
          <div class="text-[10px] text-red-400 mt-0.5">Niveau de stock nul</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Stock Faible / Alerte</span>
          <fas-icon icon="bell" class="text-amber-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-amber-600 font-mono">
            {{ materials.filter((m) => m.stock_status === 'Stock faible').length }}
          </div>
          <div class="text-[10px] text-amber-500 mt-0.5">Sous le seuil minimum</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Valeur Totale Stock</span>
          <fas-icon icon="vault" class="text-emerald-600" />
        </div>
        <div>
          <div class="text-xl font-black text-emerald-700 font-mono">
            {{ formatNumber(computedTotalStockValue) }} <span class="text-xs font-normal">FCFA</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">Valorisation indicative</div>
        </div>
      </div>
    </div>

    <!-- Catégories Pills & Filtres -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs space-y-3">
      <!-- Filtres catégories en pilules -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs scrollbar-thin">
        <button
          type="button"
          @click="selectedCategoryId = null; loadMaterials()"
          class="px-3 py-1.5 rounded-xl font-bold whitespace-nowrap transition-all"
          :class="selectedCategoryId === null ? 'bg-slate-900 text-white shadow-xs' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
        >
          Toutes catégories
        </button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          type="button"
          @click="selectedCategoryId = cat.id; loadMaterials()"
          class="px-3 py-1.5 rounded-xl font-bold whitespace-nowrap transition-all"
          :class="selectedCategoryId === cat.id ? 'bg-[#1d4ed8] text-white shadow-xs' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
        >
          {{ cat.name }}
        </button>
      </div>

      <!-- Recherche et filtre état de stock -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs pt-1 border-t border-slate-100">
        <div class="relative sm:col-span-2">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <fas-icon icon="magnifying-glass" />
          </span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher désignation, code, référence fabricant..."
            class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
            @input="debounceSearch"
          />
        </div>

        <div>
          <select
            v-model="stockStatusFilter"
            @change="loadMaterials"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
          >
            <option :value="null">Tous les états de stock</option>
            <option value="Normal">Stock Normal</option>
            <option value="Stock faible">Stock faible</option>
            <option value="Rupture">Rupture de stock</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tableau des Matériaux -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="loading" class="py-16 text-center text-slate-400 space-y-2">
        <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
        <p class="text-xs font-semibold">Chargement des matériaux...</p>
      </div>

      <div v-else-if="materials.length === 0" class="py-16 text-center text-slate-400 space-y-3">
        <div class="w-14 h-14 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-300 text-2xl">
          <fas-icon icon="cubes" />
        </div>
        <div class="text-sm font-bold text-slate-700">Aucun matériau trouvé</div>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">
          Aucune référence ne correspond à vos filtres.
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <th class="py-3 px-4">Code</th>
              <th class="py-3 px-4">Désignation du Matériau</th>
              <th class="py-3 px-4">Catégorie</th>
              <th class="py-3 px-4 text-center">Unité</th>
              <th class="py-3 px-4 text-right">Prix Indicatif</th>
              <th class="py-3 px-4 text-right">Stock Physique</th>
              <th class="py-3 px-4 text-center">État</th>
              <th class="py-3 px-4 text-right">Valeur Stock</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="m in materials" :key="m.id" class="hover:bg-slate-50/70 transition-colors">
              <!-- Code -->
              <td class="py-3 px-4 font-mono font-bold text-slate-600">
                {{ m.code }}
              </td>

              <!-- Désignation -->
              <td class="py-3 px-4">
                <div class="font-bold text-slate-800 text-sm">{{ m.name }}</div>
                <div v-if="m.reference" class="text-[10px] text-slate-400">
                  Réf: {{ m.reference }}
                </div>
              </td>

              <!-- Catégorie -->
              <td class="py-3 px-4 text-slate-600">
                <span class="px-2 py-0.5 rounded-lg text-[11px] bg-slate-100 font-semibold text-slate-700">
                  {{ m.category?.name || '-' }}
                </span>
              </td>

              <!-- Unité -->
              <td class="py-3 px-4 text-center font-bold text-slate-700 font-mono">
                {{ m.unit?.code || 'U' }}
              </td>

              <!-- Prix Indicatif -->
              <td class="py-3 px-4 text-right font-mono font-bold text-slate-700">
                {{ formatNumber(m.indicative_price) }} FCFA
              </td>

              <!-- Stock Physique -->
              <td class="py-3 px-4 text-right font-mono font-black text-sm text-slate-900">
                {{ m.current_stock }}
              </td>

              <!-- État Stock -->
              <td class="py-3 px-4 text-center">
                <span
                  class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold"
                  :class="getStockStatusClass(m.stock_status)"
                >
                  {{ m.stock_status }}
                </span>
              </td>

              <!-- Valeur du stock -->
              <td class="py-3 px-4 text-right font-mono font-black text-slate-900">
                {{ formatNumber(m.stock_value) }} FCFA
              </td>

              <!-- Actions -->
              <td class="py-3 px-4 text-right whitespace-nowrap">
                <div class="flex items-center justify-end gap-1.5">
                  <!-- Sortie rapide vers chantier -->
                  <button
                    type="button"
                    @click="openIssueModal(m)"
                    :disabled="m.current_stock <= 0"
                    class="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    title="Sortie de stock vers un chantier"
                  >
                    <fas-icon icon="arrow-right-from-bracket" class="text-xs" />
                  </button>

                  <!-- Modifier -->
                  <button
                    type="button"
                    @click="openAddMaterialModal(m)"
                    class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
                    title="Modifier"
                  >
                    <fas-icon icon="pen-to-square" class="text-xs" />
                  </button>

                  <!-- Supprimer -->
                  <button
                    type="button"
                    @click="confirmDelete(m)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                    title="Supprimer / Archiver"
                  >
                    <fas-icon icon="trash-can" class="text-xs" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modals -->
    <AddMaterialModal
      :is-open="showMaterialModal"
      :material="editingMaterial"
      @close="showMaterialModal = false"
      @saved="loadMaterials"
    />

    <StockIssueModal
      :is-open="showIssueModal"
      :preselected-material-id="issuingMaterialId"
      @close="showIssueModal = false"
      @saved="loadMaterials"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { materialService } from '@/services'
import AddMaterialModal from './components/AddMaterialModal.vue'
import StockIssueModal from './components/StockIssueModal.vue'
import Swal from 'sweetalert2'

const loading = ref(false)
const materials = ref([])
const categories = ref([])
const searchQuery = ref('')
const selectedCategoryId = ref(null)
const stockStatusFilter = ref(null)

const showMaterialModal = ref(false)
const editingMaterial = ref(null)
const showIssueModal = ref(false)
const issuingMaterialId = ref(null)

let searchTimeout = null
const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadMaterials()
  }, 300)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('fr-FR').format(num || 0)
}

const computedTotalStockValue = computed(() => {
  return materials.value.reduce((sum, m) => sum + (Number(m.stock_value) || 0), 0)
})

const getStockStatusClass = (status) => {
  switch (status) {
    case 'Rupture':
      return 'bg-red-100 text-red-800'
    case 'Stock faible':
      return 'bg-amber-100 text-amber-800'
    case 'Surstock':
      return 'bg-indigo-100 text-indigo-800'
    default:
      return 'bg-emerald-100 text-emerald-800'
  }
}

const loadCategories = async () => {
  try {
    categories.value = await materialService.getCategories()
  } catch (err) {
    console.error('Erreur chargement catégories:', err)
  }
}

const loadMaterials = async () => {
  loading.value = true
  try {
    const params = {
      category_id: selectedCategoryId.value || undefined,
      search: searchQuery.value || undefined,
      stock_status: stockStatusFilter.value || undefined,
    }
    materials.value = await materialService.getMaterials(params)
  } catch (err) {
    console.error('Erreur chargement matériaux:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCategories()
  loadMaterials()
})

const openAddMaterialModal = (mat = null) => {
  editingMaterial.value = mat
  showMaterialModal.value = true
}

const openIssueModal = (mat) => {
  issuingMaterialId.value = mat.id
  showIssueModal.value = true
}

const confirmDelete = async (mat) => {
  const result = await Swal.fire({
    title: 'Supprimer ce matériau ?',
    text: `Voulez-vous supprimer ou désactiver la référence ${mat.name} (${mat.code}) ?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Oui, confirmer',
    cancelButtonText: 'Annuler',
  })

  if (result.isConfirmed) {
    try {
      await materialService.deleteMaterial(mat.id)
      Swal.fire({
        icon: 'success',
        title: 'Matériau supprimé / archivé',
        timer: 1500,
        showConfirmButton: false,
      })
      loadMaterials()
    } catch (err) {
      Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
    }
  }
}
</script>
