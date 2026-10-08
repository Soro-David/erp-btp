<template>
  <div class="space-y-6">
    <!-- En-tête Page & Actions Principales -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="cart-shopping" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Achats & Approvisionnements</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-800">BTP Achats</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Commandes matériaux, achats rapides sur site, réceptions et règlements fournisseurs
          </p>
        </div>
      </div>

      <!-- Boutons d'action -->
      <div class="flex flex-wrap items-center gap-2.5">
        <!-- Bouton Achat Rapide Terrain -->
        <button
          type="button"
          @click="openQuickPurchaseModal = true"
          class="px-4 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white text-xs font-black shadow-md shadow-orange-500/20 flex items-center gap-2 transition-all transform active:scale-95"
        >
          <fas-icon icon="bolt" class="text-amber-200" />
          <span>+ Achat rapide (Terrain)</span>
        </button>

        <!-- Bouton Nouvel Achat Standard -->
        <button
          type="button"
          @click="openPurchaseFormModal(null)"
          class="px-4 py-2.5 rounded-2xl bg-[#1d4ed8] hover:bg-blue-700 text-white text-xs font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 transition-all transform active:scale-95"
        >
          <fas-icon icon="plus" />
          <span>+ Nouvel Achat</span>
        </button>
      </div>
    </div>

    <!-- KPI DASHBOARD SUMMARY -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
      <!-- 1. Total Engagé -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Total Engagé</span>
          <fas-icon icon="coins" class="text-blue-600" />
        </div>
        <div>
          <div class="text-xl font-black text-slate-900 font-mono">
            {{ formatNumber(stats.total_committed_amount) }} <span class="text-xs font-bold text-slate-400">FCFA</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-1">{{ stats.total_purchases }} commandes au total</div>
        </div>
      </div>

      <!-- 2. Montant Payé -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Montant Payé</span>
          <fas-icon icon="circle-check" class="text-emerald-600" />
        </div>
        <div>
          <div class="text-xl font-black text-emerald-600 font-mono">
            {{ formatNumber(stats.total_paid_amount) }} <span class="text-xs font-bold text-slate-400">FCFA</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-1">Règlements honorés</div>
        </div>
      </div>

      <!-- 3. Reste à Payer -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Reste à Régler</span>
          <fas-icon icon="clock" class="text-amber-500" />
        </div>
        <div>
          <div class="text-xl font-black text-amber-600 font-mono">
            {{ formatNumber(stats.remaining_to_pay) }} <span class="text-xs font-bold text-slate-400">FCFA</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-1">Encours fournisseurs</div>
        </div>
      </div>

      <!-- 4. Commandes en Attente -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">En cours / Commande</span>
          <fas-icon icon="truck" class="text-sky-600" />
        </div>
        <div>
          <div class="text-xl font-black text-sky-700 font-mono">
            {{ stats.ordered_purchases + stats.partially_received_purchases }}
          </div>
          <div class="text-[10px] text-slate-400 mt-1">En attente de réception</div>
        </div>
      </div>

      <!-- 5. Commandes Reçues -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between col-span-2 lg:col-span-1">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Reçus Intégralement</span>
          <fas-icon icon="boxes-stacked" class="text-indigo-600" />
        </div>
        <div>
          <div class="text-xl font-black text-indigo-700 font-mono">
            {{ stats.received_purchases }}
          </div>
          <div class="text-[10px] text-slate-400 mt-1">Stock entré en magasin</div>
        </div>
      </div>
    </div>

    <!-- Barre de filtres et recherche -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs space-y-3">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <!-- Recherche textuelle -->
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <fas-icon icon="magnifying-glass" />
          </span>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Rechercher réf, fournisseur, objet..."
            class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
            @input="debounceSearch"
          />
        </div>

        <!-- Filtre Chantier -->
        <div>
          <select
            v-model="filters.chantier_id"
            @change="loadPurchases"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
          >
            <option :value="null">Tous les chantiers</option>
            <option v-for="c in chantiers" :key="c.id" :value="c.id">
              {{ c.code }} - {{ c.name }}
            </option>
          </select>
        </div>

        <!-- Filtre Statut Commande -->
        <div>
          <select
            v-model="filters.status"
            @change="loadPurchases"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
          >
            <option :value="null">Tous les statuts de réception</option>
            <option value="Brouillon">Brouillon</option>
            <option value="Commandé">Commandé</option>
            <option value="Partiellement reçu">Partiellement reçu</option>
            <option value="Reçu">Reçu intégralement</option>
            <option value="Annulé">Annulé</option>
          </select>
        </div>

        <!-- Filtre Statut Paiement -->
        <div>
          <select
            v-model="filters.payment_status"
            @change="loadPurchases"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:bg-white focus:border-blue-600"
          >
            <option :value="null">Tous les statuts de paiement</option>
            <option value="Payé">Payé</option>
            <option value="Partiellement payé">Partiellement payé</option>
            <option value="Non payé">Non payé</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tableau des achats -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="loading" class="py-16 text-center text-slate-400 space-y-2">
        <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
        <p class="text-xs font-semibold">Chargement des commandes d'achat...</p>
      </div>

      <div v-else-if="purchases.length === 0" class="py-16 text-center text-slate-400 space-y-3">
        <div class="w-14 h-14 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-300 text-2xl">
          <fas-icon icon="cart-shopping" />
        </div>
        <div class="text-sm font-bold text-slate-700">Aucun achat trouvé</div>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">
          Aucun bon de commande ne correspond à vos filtres actuels.
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <th class="py-3 px-4">Référence</th>
              <th class="py-3 px-4">Date</th>
              <th class="py-3 px-4">Chantier / Tâche</th>
              <th class="py-3 px-4">Fournisseur</th>
              <th class="py-3 px-4 text-right">Montant (FCFA)</th>
              <th class="py-3 px-4 text-center">Réception</th>
              <th class="py-3 px-4 text-center">Paiement</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="p in purchases"
              :key="p.id"
              class="hover:bg-slate-50/70 transition-colors group cursor-pointer"
              @click="goToDetail(p.id)"
            >
              <!-- Référence -->
              <td class="py-3 px-4">
                <div class="flex items-center gap-1.5">
                  <span class="font-black text-slate-900 font-mono">{{ p.reference }}</span>
                  <span
                    v-if="p.is_quick_purchase"
                    class="px-1.5 py-0.5 rounded-md text-[9px] font-black bg-orange-100 text-orange-800 uppercase flex items-center gap-0.5"
                    title="Achat direct terrain"
                  >
                    <fas-icon icon="bolt" class="text-[8px]" />
                    <span>Terrain</span>
                  </span>
                </div>
                <div v-if="p.subject" class="text-[11px] text-slate-500 truncate max-w-xs mt-0.5">
                  {{ p.subject }}
                </div>
              </td>

              <!-- Date -->
              <td class="py-3 px-4 text-slate-600 font-medium whitespace-nowrap">
                {{ formatDate(p.date) }}
              </td>

              <!-- Chantier / Tâche -->
              <td class="py-3 px-4">
                <div class="font-bold text-slate-800">{{ p.chantier?.name || 'Chantier #' + p.chantier_id }}</div>
                <div v-if="p.task" class="text-[10px] text-blue-600 font-semibold flex items-center gap-1 mt-0.5">
                  <fas-icon icon="list-check" class="text-[9px]" />
                  <span>{{ p.task.name }}</span>
                </div>
              </td>

              <!-- Fournisseur -->
              <td class="py-3 px-4">
                <div class="font-bold text-slate-800">{{ p.supplier?.name || '-' }}</div>
                <div class="text-[10px] text-slate-400">{{ p.supplier?.phone || '' }}</div>
              </td>

              <!-- Montant Total -->
              <td class="py-3 px-4 text-right whitespace-nowrap">
                <span class="font-black text-slate-900 font-mono text-sm">
                  {{ formatNumber(p.total_amount) }}
                </span>
                <span class="text-[10px] text-slate-400 font-bold ml-1">FCFA</span>
              </td>

              <!-- Statut Réception -->
              <td class="py-3 px-4 text-center whitespace-nowrap">
                <span
                  class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold"
                  :class="getReceptionBadgeClass(p.status)"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="getReceptionDotClass(p.status)"></span>
                  <span>{{ p.status }}</span>
                </span>
              </td>

              <!-- Statut Paiement -->
              <td class="py-3 px-4 text-center whitespace-nowrap">
                <span
                  class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold"
                  :class="getPaymentBadgeClass(p.payment_status)"
                >
                  <span>{{ p.payment_status }}</span>
                </span>
              </td>

              <!-- Actions -->
              <td class="py-3 px-4 text-right whitespace-nowrap" @click.stop>
                <div class="flex items-center justify-end gap-1.5">
                  <!-- Réceptionner si non complètement reçu -->
                  <button
                    v-if="p.status !== 'Reçu' && p.status !== 'Annulé'"
                    type="button"
                    @click="openReceiveModal(p)"
                    class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 transition-colors"
                    title="Enregistrer une réception"
                  >
                    <fas-icon icon="dolly" class="text-xs" />
                  </button>

                  <!-- Voir Détail -->
                  <button
                    type="button"
                    @click="goToDetail(p.id)"
                    class="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 transition-colors"
                    title="Voir la commande"
                  >
                    <fas-icon icon="eye" class="text-xs" />
                  </button>

                  <!-- Modifier si brouillon ou commandé -->
                  <button
                    v-if="p.status === 'Brouillon' || p.status === 'Commandé'"
                    type="button"
                    @click="openPurchaseFormModal(p)"
                    class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
                    title="Modifier"
                  >
                    <fas-icon icon="pen-to-square" class="text-xs" />
                  </button>

                  <!-- Supprimer -->
                  <button
                    v-if="p.status === 'Brouillon' || p.status === 'Commandé'"
                    type="button"
                    @click="confirmDelete(p)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                    title="Supprimer"
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
    <PurchaseFormModal
      :is-open="showPurchaseForm"
      :purchase="editingPurchase"
      @close="showPurchaseForm = false"
      @saved="onPurchaseSaved"
    />

    <QuickPurchaseModal
      :is-open="openQuickPurchaseModal"
      @close="openQuickPurchaseModal = false"
      @saved="onPurchaseSaved"
    />

    <PurchaseReceiveModal
      :is-open="showReceiveModal"
      :purchase="receivingPurchase"
      @close="showReceiveModal = false"
      @saved="onReceiptSaved"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { purchaseService, chantierService } from '@/services'
import PurchaseFormModal from './components/PurchaseFormModal.vue'
import QuickPurchaseModal from './components/QuickPurchaseModal.vue'
import PurchaseReceiveModal from './components/PurchaseReceiveModal.vue'
import Swal from 'sweetalert2'

const router = useRouter()

const loading = ref(false)
const purchases = ref([])
const chantiers = ref([])

const stats = reactive({
  total_purchases: 0,
  pending_purchases: 0,
  ordered_purchases: 0,
  partially_received_purchases: 0,
  received_purchases: 0,
  total_committed_amount: 0,
  total_paid_amount: 0,
  remaining_to_pay: 0,
})

const filters = reactive({
  search: '',
  chantier_id: null,
  status: null,
  payment_status: null,
})

// Modals
const showPurchaseForm = ref(false)
const editingPurchase = ref(null)
const openQuickPurchaseModal = ref(false)
const showReceiveModal = ref(false)
const receivingPurchase = ref(null)

let searchTimeout = null
const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadPurchases()
  }, 350)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('fr-FR').format(num || 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

const getReceptionBadgeClass = (status) => {
  switch (status) {
    case 'Reçu':
      return 'bg-emerald-100 text-emerald-800'
    case 'Partiellement reçu':
      return 'bg-sky-100 text-sky-800'
    case 'Commandé':
      return 'bg-amber-100 text-amber-800'
    case 'Brouillon':
      return 'bg-slate-100 text-slate-700'
    case 'Annulé':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-slate-100 text-slate-700'
  }
}

const getReceptionDotClass = (status) => {
  switch (status) {
    case 'Reçu':
      return 'bg-emerald-500'
    case 'Partiellement reçu':
      return 'bg-sky-500'
    case 'Commandé':
      return 'bg-amber-500'
    default:
      return 'bg-slate-400'
  }
}

const getPaymentBadgeClass = (paymentStatus) => {
  switch (paymentStatus) {
    case 'Payé':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    case 'Partiellement payé':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
    default:
      return 'bg-slate-50 text-slate-600 border border-slate-200'
  }
}

const loadStats = async () => {
  try {
    const data = await purchaseService.getDashboardStats()
    Object.assign(stats, data)
  } catch (err) {
    console.error('Erreur stats achats:', err)
  }
}

const loadChantiers = async () => {
  try {
    const data = await chantierService.getChantiers()
    chantiers.value = data.items || data || []
  } catch (err) {
    console.error('Erreur chantiers:', err)
  }
}

const loadPurchases = async () => {
  loading.value = true
  try {
    const params = {
      search: filters.search || undefined,
      chantier_id: filters.chantier_id || undefined,
      status: filters.status || undefined,
      payment_status: filters.payment_status || undefined,
    }
    purchases.value = await purchaseService.getPurchases(params)
  } catch (err) {
    console.error('Erreur chargement achats:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
  loadChantiers()
  loadPurchases()
})

const goToDetail = (id) => {
  router.push(`/achats/${id}`)
}

const openPurchaseFormModal = (purchase = null) => {
  editingPurchase.value = purchase
  showPurchaseForm.value = true
}

const openReceiveModal = (purchase) => {
  receivingPurchase.value = purchase
  showReceiveModal.value = true
}

const onPurchaseSaved = () => {
  loadStats()
  loadPurchases()
}

const onReceiptSaved = () => {
  loadStats()
  loadPurchases()
}

const confirmDelete = async (purchase) => {
  const result = await Swal.fire({
    title: 'Supprimer cet achat ?',
    text: `Voulez-vous supprimer définitivement la commande ${purchase.reference} ?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Oui, supprimer',
    cancelButtonText: 'Annuler',
  })

  if (result.isConfirmed) {
    try {
      await purchaseService.deletePurchase(purchase.id)
      Swal.fire({
        icon: 'success',
        title: 'Achat supprimé',
        timer: 1500,
        showConfirmButton: false,
      })
      loadStats()
      loadPurchases()
    } catch (err) {
      Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
    }
  }
}
</script>
