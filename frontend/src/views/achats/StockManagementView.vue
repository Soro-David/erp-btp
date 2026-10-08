<template>
  <div class="space-y-6">
    <!-- En-tête Page & Actions Principales -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-700 flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="warehouse" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Gestion des Stocks & Dépôts</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-100 text-indigo-800">Inventaire BTP</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Suivi multi-dépôts, mouvements d'entrées/sorties vers chantiers, transferts et inventaires
          </p>
        </div>
      </div>

      <!-- Boutons d'action rapides -->
      <div class="flex flex-wrap items-center gap-2">
        <button
          type="button"
          @click="showIssueModal = true"
          class="px-3.5 py-2.5 rounded-2xl bg-[#1d4ed8] hover:bg-blue-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all transform active:scale-95"
        >
          <fas-icon icon="arrow-right-from-bracket" />
          <span>Sortie Chantier</span>
        </button>

        <button
          type="button"
          @click="showTransferModal = true"
          class="px-3.5 py-2.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all transform active:scale-95"
        >
          <fas-icon icon="right-left" />
          <span>Transfert</span>
        </button>

        <button
          type="button"
          @click="showReturnModal = true"
          class="px-3.5 py-2.5 rounded-2xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all transform active:scale-95"
        >
          <fas-icon icon="rotate-left" />
          <span>Retour Chantier</span>
        </button>

        <button
          type="button"
          @click="showInventoryModal = true"
          class="px-3.5 py-2.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all transform active:scale-95"
        >
          <fas-icon icon="clipboard-check" />
          <span>Inventaire</span>
        </button>
      </div>
    </div>

    <!-- KPIs Stock -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Valeur Totale Stock</span>
          <fas-icon icon="vault" class="text-emerald-600" />
        </div>
        <div>
          <div class="text-xl font-black text-slate-900 font-mono">
            {{ formatNumber(stockDashboard.total_stock_value) }} <span class="text-xs font-normal">FCFA</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">Tous dépôts confondus</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Dépôts & Magasins</span>
          <fas-icon icon="warehouse" class="text-blue-600" />
        </div>
        <div>
          <div class="text-2xl font-black text-blue-600 font-mono">
            {{ locations.length }}
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">Lieux de stockage actifs</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Mouvements Enregistrés</span>
          <fas-icon icon="arrow-trend-up" class="text-indigo-600" />
        </div>
        <div>
          <div class="text-2xl font-black text-indigo-700 font-mono">
            {{ totalMovementsCount }}
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">Entrées / Sorties tracées</div>
        </div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Alertes Stock</span>
          <fas-icon icon="bell" class="text-amber-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-amber-600 font-mono">
            {{ (stockDashboard.out_of_stock_count || 0) + (stockDashboard.low_stock_count || 0) }}
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">
            {{ stockDashboard.out_of_stock_count || 0 }} rupture(s), {{ stockDashboard.low_stock_count || 0 }} faible(s)
          </div>
        </div>
      </div>
    </div>

    <!-- Onglets de gestion du Stock -->
    <div class="flex items-center gap-1 bg-slate-100 p-1.5 rounded-2xl border border-slate-200 text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'stock_overview'"
        class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
        :class="activeTab === 'stock_overview' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
      >
        <fas-icon icon="cubes" />
        <span>État des stocks par dépôt</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'movements'"
        class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
        :class="activeTab === 'movements' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
      >
        <fas-icon icon="receipt" />
        <span>Journal des mouvements</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'locations'"
        class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
        :class="activeTab === 'locations' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
      >
        <fas-icon icon="warehouse" />
        <span>Dépôts & Magasins</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'inventories'"
        class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
        :class="activeTab === 'inventories' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
      >
        <fas-icon icon="clipboard-check" />
        <span>Inventaires physiques</span>
      </button>
    </div>

    <!-- Onglet 1 : État des stocks par dépôt -->
    <div v-if="activeTab === 'stock_overview'" class="space-y-4">
      <!-- Filtre par Dépôt -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2 w-full sm:w-auto">
          <span class="font-bold text-slate-600">Filtrer par Dépôt :</span>
          <select
            v-model="selectedLocationFilter"
            @change="loadStockOverview"
            class="px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:border-blue-600"
          >
            <option :value="null">Tous les dépôts & magasins</option>
            <option v-for="loc in locations" :key="loc.id" :value="loc.id">
              {{ loc.name }}
            </option>
          </select>
        </div>

        <div class="text-xs text-slate-500">
          Affichage de <span class="font-bold text-slate-900">{{ stockOverview.length }}</span> référence(s) en stock
        </div>
      </div>

      <!-- Tableau Stock par Dépôt -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div v-if="loadingOverview" class="py-16 text-center text-slate-400 space-y-2">
          <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
          <p class="text-xs font-semibold">Calcul des niveaux de stock physique...</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <th class="py-3 px-4">Dépôt / Magasin</th>
                <th class="py-3 px-4">Matériau</th>
                <th class="py-3 px-4">Catégorie</th>
                <th class="py-3 px-4 text-center">Unité</th>
                <th class="py-3 px-4 text-right">Quantité Disponible</th>
                <th class="py-3 px-4 text-center">Statut</th>
                <th class="py-3 px-4 text-right">Prix Indicatif</th>
                <th class="py-3 px-4 text-right">Valeur Stock</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="item in stockOverview" :key="item.location_id + '-' + item.material_id" class="hover:bg-slate-50/50">
                <td class="py-3 px-4 font-bold text-slate-800">
                  <div class="flex items-center gap-1.5">
                    <fas-icon icon="warehouse" class="text-slate-400 text-xs" />
                    <span>{{ item.location_name }}</span>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <div class="font-bold text-slate-900">{{ item.material_name }}</div>
                  <div class="text-[10px] text-slate-400 font-mono">{{ item.material_code }}</div>
                </td>
                <td class="py-3 px-4 text-slate-600">{{ item.category_name }}</td>
                <td class="py-3 px-4 text-center font-bold text-slate-700 font-mono">{{ item.unit_code }}</td>
                <td class="py-3 px-4 text-right font-black font-mono text-slate-900 text-sm">
                  {{ item.quantity }}
                </td>
                <td class="py-3 px-4 text-center">
                  <span
                    class="px-2 py-0.5 rounded-full text-[10px] font-bold"
                    :class="item.stock_status === 'Normal' ? 'bg-emerald-100 text-emerald-800' : item.stock_status === 'Stock faible' ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'"
                  >
                    {{ item.stock_status }}
                  </span>
                </td>
                <td class="py-3 px-4 text-right font-mono text-slate-700">
                  {{ formatNumber(item.indicative_price) }} FCFA
                </td>
                <td class="py-3 px-4 text-right font-mono font-black text-slate-900">
                  {{ formatNumber(item.stock_value) }} FCFA
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Onglet 2 : Journal des mouvements -->
    <div v-if="activeTab === 'movements'" class="space-y-4">
      <!-- Filtres du Journal -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-wrap items-center gap-3 text-xs">
        <div>
          <select
            v-model="movementFilterType"
            @change="loadMovements"
            class="px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:border-blue-600"
          >
            <option :value="null">Tous types de mouvements</option>
            <option value="Entrée">Entrées (Réceptions / Achats)</option>
            <option value="Sortie">Sorties (Affectations chantier)</option>
            <option value="Transfert">Transferts inter-dépôts</option>
            <option value="Retour">Retours de chantier</option>
            <option value="Ajustement">Ajustements d'inventaire</option>
          </select>
        </div>
      </div>

      <!-- Tableau du Journal -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div v-if="loadingMovements" class="py-16 text-center text-slate-400 space-y-2">
          <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
          <p class="text-xs font-semibold">Chargement du journal des mouvements...</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <th class="py-3 px-4">Réf Mouvement</th>
                <th class="py-3 px-4">Date & Heure</th>
                <th class="py-3 px-4">Type</th>
                <th class="py-3 px-4">Matériau</th>
                <th class="py-3 px-4 text-right">Quantité</th>
                <th class="py-3 px-4">Dépôt</th>
                <th class="py-3 px-4">Chantier / Destination</th>
                <th class="py-3 px-4">Motif / Notes</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="m in movements" :key="m.id" class="hover:bg-slate-50/50">
                <td class="py-3 px-4 font-mono font-bold text-slate-800">{{ m.reference }}</td>
                <td class="py-3 px-4 text-slate-600 whitespace-nowrap">{{ formatDateTime(m.date) }}</td>
                <td class="py-3 px-4 whitespace-nowrap">
                  <span
                    class="px-2.5 py-0.5 rounded-full text-[10px] font-bold"
                    :class="getMovementTypeBadge(m.movement_type)"
                  >
                    {{ m.movement_type }}
                  </span>
                </td>
                <td class="py-3 px-4 font-bold text-slate-800">
                  {{ m.material?.name || 'Matériau #' + m.material_id }}
                </td>
                <td class="py-3 px-4 text-right font-mono font-black text-sm whitespace-nowrap" :class="m.movement_type === 'Sortie' ? 'text-red-600' : 'text-emerald-600'">
                  {{ m.movement_type === 'Sortie' ? '-' : '+' }}{{ Math.abs(m.quantity) }} {{ m.material?.unit?.code || 'U' }}
                </td>
                <td class="py-3 px-4 text-slate-700">{{ m.location?.name || '-' }}</td>
                <td class="py-3 px-4 text-slate-700">
                  <div v-if="m.chantier" class="font-bold text-blue-700">{{ m.chantier.name }}</div>
                  <div v-if="m.task" class="text-[10px] text-slate-400">{{ m.task.name }}</div>
                  <span v-if="!m.chantier && !m.task" class="text-slate-400">-</span>
                </td>
                <td class="py-3 px-4 text-slate-500 text-[11px] truncate max-w-xs">
                  {{ m.reason || m.notes || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Onglet 3 : Dépôts & Magasins -->
    <div v-if="activeTab === 'locations'" class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="font-bold text-slate-800 text-sm">Emplacements de Stockage</h2>
        <button
          type="button"
          @click="showAddLocationPrompt"
          class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5"
        >
          <fas-icon icon="plus" />
          <span>Nouveau Dépôt / Magasin</span>
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="loc in locations"
          :key="loc.id"
          class="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs space-y-3"
        >
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-700 flex items-center justify-center text-lg">
                <fas-icon icon="warehouse" />
              </div>
              <div>
                <h3 class="font-bold text-slate-800 text-sm">{{ loc.name }}</h3>
                <span class="text-[10px] font-mono text-slate-400">{{ loc.code }}</span>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700">
              {{ loc.type }}
            </span>
          </div>

          <div class="text-xs text-slate-600 space-y-1.5">
            <div v-if="loc.location" class="flex items-center gap-2">
              <fas-icon icon="location-dot" class="text-slate-400" />
              <span>{{ loc.location }}</span>
            </div>
            <div class="flex items-center gap-2">
              <fas-icon icon="check" class="text-emerald-500" />
              <span class="text-emerald-700 font-bold">Actif et opérationnel</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Onglet 4 : Inventaires physiques -->
    <div v-if="activeTab === 'inventories'" class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="font-bold text-slate-800 text-sm">Sessions d'Inventaires Physiques</h2>
        <button
          type="button"
          @click="showInventoryModal = true"
          class="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5"
        >
          <fas-icon icon="plus" />
          <span>Nouvelle Session d'Inventaire</span>
        </button>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div v-if="inventories.length === 0" class="py-12 text-center text-slate-400 text-xs">
          Aucun inventaire enregistré pour le moment.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase border-b border-slate-200">
                <th class="py-3 px-4">Référence</th>
                <th class="py-3 px-4">Date</th>
                <th class="py-3 px-4">Dépôt</th>
                <th class="py-3 px-4 text-center">Statut</th>
                <th class="py-3 px-4">Notes</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="inv in inventories" :key="inv.id" class="hover:bg-slate-50/50">
                <td class="py-3 px-4 font-mono font-bold text-slate-800">{{ inv.reference }}</td>
                <td class="py-3 px-4 text-slate-600">{{ formatDate(inv.inventory_date) }}</td>
                <td class="py-3 px-4 font-bold text-slate-800">{{ inv.location?.name }}</td>
                <td class="py-3 px-4 text-center">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    {{ inv.status }}
                  </span>
                </td>
                <td class="py-3 px-4 text-slate-500">{{ inv.notes || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <StockIssueModal
      :is-open="showIssueModal"
      @close="showIssueModal = false"
      @saved="refreshAllData"
    />

    <StockTransferModal
      :is-open="showTransferModal"
      @close="showTransferModal = false"
      @saved="refreshAllData"
    />

    <StockReturnModal
      :is-open="showReturnModal"
      @close="showReturnModal = false"
      @saved="refreshAllData"
    />

    <StockInventoryModal
      :is-open="showInventoryModal"
      @close="showInventoryModal = false"
      @saved="refreshAllData"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { stockService } from '@/services'
import StockIssueModal from './components/StockIssueModal.vue'
import StockTransferModal from './components/StockTransferModal.vue'
import StockReturnModal from './components/StockReturnModal.vue'
import StockInventoryModal from './components/StockInventoryModal.vue'
import Swal from 'sweetalert2'

const activeTab = ref('stock_overview')
const loadingOverview = ref(false)
const loadingMovements = ref(false)

const locations = ref([])
const stockOverview = ref([])
const movements = ref([])
const inventories = ref([])
const totalMovementsCount = ref(0)

const selectedLocationFilter = ref(null)
const movementFilterType = ref(null)

const stockDashboard = reactive({
  total_materials_count: 0,
  active_materials_count: 0,
  out_of_stock_count: 0,
  low_stock_count: 0,
  total_stock_value: 0,
  total_locations_count: 0,
})

const showIssueModal = ref(false)
const showTransferModal = ref(false)
const showReturnModal = ref(false)
const showInventoryModal = ref(false)

const formatNumber = (val) => {
  return new Intl.NumberFormat('fr-FR').format(val || 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (dtStr) => {
  if (!dtStr) return '-'
  return new Date(dtStr).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getMovementTypeBadge = (type) => {
  switch (type) {
    case 'Entrée':
      return 'bg-emerald-100 text-emerald-800'
    case 'Sortie':
      return 'bg-red-100 text-red-800'
    case 'Transfert':
      return 'bg-indigo-100 text-indigo-800'
    case 'Retour':
      return 'bg-teal-100 text-teal-800'
    case 'Ajustement':
      return 'bg-amber-100 text-amber-800'
    default:
      return 'bg-slate-100 text-slate-700'
  }
}

const loadDashboardStats = async () => {
  try {
    const data = await stockService.getDashboardStats()
    Object.assign(stockDashboard, data)
  } catch (err) {
    console.error('Erreur stats stock:', err)
  }
}

const loadLocations = async () => {
  try {
    locations.value = await stockService.getLocations()
  } catch (err) {
    console.error('Erreur locations:', err)
  }
}

const loadStockOverview = async () => {
  loadingOverview.value = true
  try {
    stockOverview.value = await stockService.getStockOverview(selectedLocationFilter.value)
  } catch (err) {
    console.error('Erreur vue stock:', err)
  } finally {
    loadingOverview.value = false
  }
}

const loadMovements = async () => {
  loadingMovements.value = true
  try {
    movements.value = await stockService.getMovements({
      movement_type: movementFilterType.value || undefined,
    })
    totalMovementsCount.value = movements.value.length
  } catch (err) {
    console.error('Erreur mouvements:', err)
  } finally {
    loadingMovements.value = false
  }
}

const loadInventories = async () => {
  try {
    inventories.value = await stockService.getInventories()
  } catch (err) {
    console.error('Erreur inventaires:', err)
  }
}

const refreshAllData = () => {
  loadDashboardStats()
  loadLocations()
  loadStockOverview()
  loadMovements()
  loadInventories()
}

onMounted(() => {
  refreshAllData()
})

const showAddLocationPrompt = async () => {
  const { value: formValues } = await Swal.fire({
    title: 'Nouveau Dépôt / Magasin',
    html:
      '<input id="swal-loc-code" class="swal2-input" placeholder="Code (ex: DEP-04)">' +
      '<input id="swal-loc-name" class="swal2-input" placeholder="Nom (ex: Magasin Chantier Riviera)">' +
      '<input id="swal-loc-addr" class="swal2-input" placeholder="Emplacement géographique">',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Créer le Dépôt',
    cancelButtonText: 'Annuler',
    preConfirm: () => {
      const code = document.getElementById('swal-loc-code').value
      const name = document.getElementById('swal-loc-name').value
      const location = document.getElementById('swal-loc-addr').value
      if (!name) {
        Swal.showValidationMessage('Veuillez au moins renseigner le nom du dépôt')
        return false
      }
      return { code, name, location, type: 'Magasin' }
    },
  })

  if (formValues) {
    try {
      await stockService.createLocation(formValues)
      Swal.fire({
        icon: 'success',
        title: 'Dépôt créé',
        timer: 1500,
        showConfirmButton: false,
      })
      await loadLocations()
    } catch (err) {
      Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
    }
  }
}
</script>
