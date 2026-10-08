<template>
  <div class="space-y-6">
    <!-- Breadcrumbs -->
    <div class="flex items-center gap-2 text-xs text-slate-500">
      <router-link to="/achats/fournisseurs" class="hover:text-blue-600 flex items-center gap-1 font-bold">
        <fas-icon icon="arrow-left" />
        <span>Fournisseurs</span>
      </router-link>
      <span>/</span>
      <span class="text-slate-800 font-extrabold">{{ supplier?.name || 'Fiche fournisseur' }}</span>
    </div>

    <!-- En-tête -->
    <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <div class="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-2xl shadow-xs">
          <fas-icon icon="handshake" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">{{ supplier?.name }}</h1>
            <span class="px-2 py-0.5 rounded-full text-xs font-bold font-mono bg-slate-100 text-slate-700">
              {{ supplier?.code }}
            </span>
            <span
              class="px-2.5 py-0.5 rounded-full text-xs font-bold"
              :class="supplier?.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'"
            >
              {{ supplier?.is_active ? 'Actif' : 'Inactif' }}
            </span>
          </div>
          <p v-if="supplier?.trade_name" class="text-xs text-slate-500 italic mt-0.5">
            {{ supplier.trade_name }}
          </p>
          <div class="flex flex-wrap items-center gap-4 text-xs text-slate-600 mt-2">
            <span v-if="supplier?.contact_name" class="flex items-center gap-1.5">
              <fas-icon icon="user" class="text-slate-400" />
              <span>{{ supplier.contact_name }}</span>
            </span>
            <span class="flex items-center gap-1.5 font-mono">
              <fas-icon icon="phone" class="text-slate-400" />
              <span>{{ supplier?.phone }}</span>
            </span>
            <span v-if="supplier?.email" class="flex items-center gap-1.5">
              <fas-icon icon="envelope" class="text-slate-400" />
              <span>{{ supplier.email }}</span>
            </span>
            <span class="flex items-center gap-1.5">
              <fas-icon icon="location-dot" class="text-slate-400" />
              <span>{{ supplier?.city || 'Abidjan' }} ({{ supplier?.address || '-' }})</span>
            </span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="showEditModal = true"
          class="px-4 py-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-colors flex items-center gap-1.5"
        >
          <fas-icon icon="pen-to-square" />
          <span>Modifier</span>
        </button>
      </div>
    </div>

    <!-- KPIs Financiers Fournisseur -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Commandes Réalisées</div>
        <div class="text-2xl font-black text-slate-900 font-mono">{{ stats.total_orders || 0 }}</div>
        <div class="text-[10px] text-slate-400 mt-0.5">Bons émis</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Montant Cumulé Engagé</div>
        <div class="text-xl font-black text-slate-900 font-mono">
          {{ formatNumber(stats.total_amount) }} <span class="text-xs font-normal">FCFA</span>
        </div>
        <div class="text-[10px] text-slate-400 mt-0.5">Volume d'affaires</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Montant Réglé</div>
        <div class="text-xl font-black text-emerald-600 font-mono">
          {{ formatNumber(stats.amount_paid) }} <span class="text-xs font-normal">FCFA</span>
        </div>
        <div class="text-[10px] text-slate-400 mt-0.5">Paiements validés</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Solde Restant Dû</div>
        <div class="text-xl font-black text-amber-600 font-mono">
          {{ formatNumber(stats.balance) }} <span class="text-xs font-normal">FCFA</span>
        </div>
        <div class="text-[10px] text-slate-400 mt-0.5">À régler</div>
      </div>
    </div>

    <!-- Historique des commandes de ce fournisseur -->
    <div class="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
      <div class="p-5 border-b border-slate-100 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <fas-icon icon="receipt" class="text-blue-600" />
          <h2 class="font-bold text-slate-800 text-sm">Historique des Commandes Fournisseur</h2>
        </div>
        <span class="text-xs text-slate-400">{{ purchases.length }} commande(s)</span>
      </div>

      <div v-if="purchases.length === 0" class="py-12 text-center text-slate-400 text-xs">
        Aucune commande passée auprès de ce fournisseur pour l'instant.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase border-b border-slate-200">
              <th class="py-3 px-4">Réf Commande</th>
              <th class="py-3 px-4">Date</th>
              <th class="py-3 px-4">Chantier</th>
              <th class="py-3 px-4">Objet</th>
              <th class="py-3 px-4 text-right">Montant (FCFA)</th>
              <th class="py-3 px-4 text-center">Réception</th>
              <th class="py-3 px-4 text-center">Paiement</th>
              <th class="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="p in purchases" :key="p.id" class="hover:bg-slate-50/50">
              <td class="py-3 px-4 font-mono font-bold text-slate-900">{{ p.reference }}</td>
              <td class="py-3 px-4 text-slate-600">{{ formatDate(p.date) }}</td>
              <td class="py-3 px-4 font-bold text-slate-800">{{ p.chantier?.name || '-' }}</td>
              <td class="py-3 px-4 text-slate-600 truncate max-w-xs">{{ p.subject || '-' }}</td>
              <td class="py-3 px-4 text-right font-mono font-bold text-slate-900">
                {{ formatNumber(p.total_amount) }}
              </td>
              <td class="py-3 px-4 text-center">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700">
                  {{ p.status }}
                </span>
              </td>
              <td class="py-3 px-4 text-center">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold" :class="p.payment_status === 'Payé' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'">
                  {{ p.payment_status }}
                </span>
              </td>
              <td class="py-3 px-4 text-right">
                <router-link
                  :to="`/achats/${p.id}`"
                  class="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 transition-colors inline-block"
                  title="Voir la commande"
                >
                  <fas-icon icon="eye" class="text-xs" />
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal d'édition -->
    <AddSupplierModal
      :is-open="showEditModal"
      :supplier="supplier"
      @close="showEditModal = false"
      @saved="loadSupplierDetail"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { supplierService, purchaseService } from '@/services'
import AddSupplierModal from './components/AddSupplierModal.vue'

const route = useRoute()
const supplierId = Number(route.params.id)

const supplier = ref(null)
const purchases = ref([])
const stats = reactive({
  total_orders: 0,
  total_amount: 0,
  amount_paid: 0,
  balance: 0,
})

const showEditModal = ref(false)

const formatNumber = (val) => {
  return new Intl.NumberFormat('fr-FR').format(val || 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

const loadSupplierDetail = async () => {
  try {
    supplier.value = await supplierService.getSupplierById(supplierId)
    const statsData = await supplierService.getSupplierStats(supplierId)
    Object.assign(stats, statsData)
    purchases.value = await purchaseService.getPurchases({ supplier_id: supplierId })
  } catch (err) {
    console.error('Erreur chargement détail fournisseur:', err)
  }
}

onMounted(() => {
  loadSupplierDetail()
})
</script>
