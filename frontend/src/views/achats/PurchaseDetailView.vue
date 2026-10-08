<template>
  <div class="space-y-6">
    <!-- Bouton Retour & Fil d'Ariane -->
    <div class="flex items-center gap-2 text-xs text-slate-500">
      <router-link to="/achats" class="hover:text-blue-600 flex items-center gap-1 font-bold">
        <fas-icon icon="arrow-left" />
        <span>Achats</span>
      </router-link>
      <span>/</span>
      <span class="text-slate-800 font-extrabold font-mono">{{ purchase?.reference || 'Détail commande' }}</span>
    </div>

    <!-- En-tête Principal de la Commande -->
    <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <div class="w-14 h-14 rounded-2xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-2xl shadow-xs">
          <fas-icon icon="file-invoice" />
        </div>
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <h1 class="text-xl font-black text-slate-900 font-mono">{{ purchase?.reference }}</h1>
            <span
              v-if="purchase?.is_quick_purchase"
              class="px-2 py-0.5 rounded-full text-[10px] font-black bg-orange-100 text-orange-800 uppercase flex items-center gap-1"
            >
              <fas-icon icon="bolt" class="text-[9px]" />
              <span>Achat Rapide Terrain</span>
            </span>
            <span
              class="px-2.5 py-0.5 rounded-full text-xs font-bold"
              :class="getReceptionBadgeClass(purchase?.status)"
            >
              {{ purchase?.status }}
            </span>
            <span
              class="px-2.5 py-0.5 rounded-full text-xs font-bold"
              :class="getPaymentBadgeClass(purchase?.payment_status)"
            >
              {{ purchase?.payment_status }}
            </span>
          </div>
          <p v-if="purchase?.subject" class="text-xs text-slate-600 font-medium mt-1">
            {{ purchase?.subject }}
          </p>
          <div class="flex items-center gap-3 text-[11px] text-slate-400 mt-1">
            <span>Émis le {{ formatDate(purchase?.date) }}</span>
            <span>•</span>
            <span>Mode : {{ purchase?.payment_mode || 'Virement' }}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          v-if="purchase?.status !== 'Reçu' && purchase?.status !== 'Annulé'"
          type="button"
          @click="showReceiveModal = true"
          class="px-4 py-2 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-700/20 flex items-center gap-2 transition-all"
        >
          <fas-icon icon="dolly" />
          <span>Réceptionner</span>
        </button>

        <button
          type="button"
          @click="printPurchaseOrder"
          class="px-4 py-2 rounded-2xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-2xs flex items-center gap-1.5 transition-colors"
        >
          <fas-icon icon="print" />
          <span>Imprimer BC</span>
        </button>

        <button
          v-if="purchase?.status === 'Brouillon' || purchase?.status === 'Commandé'"
          type="button"
          @click="showEditModal = true"
          class="px-3.5 py-2 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-colors"
        >
          <fas-icon icon="pen-to-square" />
          <span>Modifier</span>
        </button>
      </div>
    </div>

    <!-- Contenu en 2 colonnes : Détail principal + Sidebar infos -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Colonne Principale (Onglets) -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Onglets -->
        <div class="flex items-center gap-1 bg-slate-100 p-1.5 rounded-2xl border border-slate-200 text-xs font-bold">
          <button
            type="button"
            @click="activeTab = 'articles'"
            class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
            :class="activeTab === 'articles' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
          >
            <fas-icon icon="boxes-stacked" />
            <span>Articles commandés ({{ purchase?.lines?.length || 0 }})</span>
          </button>

          <button
            type="button"
            @click="activeTab = 'receipts'"
            class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
            :class="activeTab === 'receipts' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
          >
            <fas-icon icon="dolly" />
            <span>Bons de Réception ({{ purchase?.receipts?.length || 0 }})</span>
          </button>

          <button
            type="button"
            @click="activeTab = 'documents'"
            class="flex-1 py-2 px-3 rounded-xl transition-all flex items-center justify-center gap-2"
            :class="activeTab === 'documents' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
          >
            <fas-icon icon="paperclip" />
            <span>Pièces jointes ({{ purchase?.documents?.length || 0 }})</span>
          </button>
        </div>

        <!-- Onglet 1 : Articles & Lignes -->
        <div v-if="activeTab === 'articles'" class="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex items-center justify-between">
            <h2 class="font-bold text-slate-800 text-sm">Détail des Matériaux Commandés</h2>
            <span class="text-xs text-slate-400">Total : {{ formatNumber(purchase?.total_amount) }} FCFA</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                  <th class="py-3 px-4">Désignation</th>
                  <th class="py-3 px-4 text-right">Qté Commandée</th>
                  <th class="py-3 px-4 text-right">Qté Reçue</th>
                  <th class="py-3 px-4 text-right">Prix Unitaire</th>
                  <th class="py-3 px-4 text-right">Total HT</th>
                  <th class="py-3 px-4 text-center">Avancement</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="line in purchase?.lines" :key="line.id" class="hover:bg-slate-50/50">
                  <td class="py-3 px-4">
                    <div class="font-bold text-slate-800">{{ line.material?.name || 'Matériau #' + line.material_id }}</div>
                    <div class="text-[10px] text-slate-400 font-mono">
                      {{ line.material?.code }} • Unité : {{ line.material?.unit?.code || 'U' }}
                    </div>
                  </td>
                  <td class="py-3 px-4 text-right font-mono font-bold text-slate-700">
                    {{ line.quantity }}
                  </td>
                  <td class="py-3 px-4 text-right font-mono font-bold text-emerald-600">
                    {{ line.quantity_received || 0 }}
                  </td>
                  <td class="py-3 px-4 text-right font-mono text-slate-700">
                    {{ formatNumber(line.unit_price) }} FCFA
                  </td>
                  <td class="py-3 px-4 text-right font-mono font-black text-slate-900">
                    {{ formatNumber(line.total_price) }} FCFA
                  </td>
                  <td class="py-3 px-4 text-center">
                    <div class="w-24 mx-auto">
                      <div class="flex items-center justify-between text-[10px] font-bold text-slate-500 mb-1">
                        <span>{{ Math.round(((line.quantity_received || 0) / line.quantity) * 100) }}%</span>
                      </div>
                      <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div
                          class="h-full rounded-full transition-all"
                          :class="(line.quantity_received || 0) >= line.quantity ? 'bg-emerald-500' : 'bg-blue-600'"
                          :style="{ width: `${Math.min(100, Math.round(((line.quantity_received || 0) / line.quantity) * 100))}%` }"
                        ></div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Total Footer -->
          <div class="p-4 bg-slate-50 border-t border-slate-100 flex justify-end items-center gap-6">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Montant Total TTC :</span>
            <span class="text-xl font-black text-slate-900 font-mono">
              {{ formatNumber(purchase?.total_amount) }} FCFA
            </span>
          </div>
        </div>

        <!-- Onglet 2 : Bons de Réception -->
        <div v-if="activeTab === 'receipts'" class="space-y-4">
          <div v-if="!purchase?.receipts || purchase.receipts.length === 0" class="bg-white p-12 text-center rounded-3xl border border-slate-200">
            <fas-icon icon="dolly" class="text-3xl text-slate-300 mb-2" />
            <div class="text-sm font-bold text-slate-700">Aucune réception enregistrée</div>
            <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
              Lorsque les matériaux sont livrés sur le chantier ou au dépôt, enregistrez le bon de réception.
            </p>
            <button
              v-if="purchase?.status !== 'Reçu'"
              type="button"
              @click="showReceiveModal = true"
              class="mt-4 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-xs inline-flex items-center gap-1.5"
            >
              <fas-icon icon="plus" />
              <span>Enregistrer la première livraison</span>
            </button>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="rec in purchase.receipts"
              :key="rec.id"
              class="bg-white rounded-3xl border border-slate-200 shadow-xs p-5 space-y-3"
            >
              <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold text-sm">
                    <fas-icon icon="dolly" />
                  </div>
                  <div>
                    <span class="font-black text-slate-900 font-mono text-xs">{{ rec.receipt_number }}</span>
                    <div class="text-[10px] text-slate-400">
                      Livré le {{ formatDate(rec.date) }} • Dépôt : {{ rec.location?.name || 'Dépôt #' + rec.location_id }}
                    </div>
                  </div>
                </div>
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  Entrée en stock effectuée
                </span>
              </div>

              <!-- Lignes réceptionnées -->
              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                  <thead>
                    <tr class="text-[10px] font-bold text-slate-400 uppercase">
                      <th class="py-1 px-2">Article</th>
                      <th class="py-1 px-2 text-right">Reçu conforme</th>
                      <th class="py-1 px-2 text-right">Rejeté / Avarié</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-50">
                    <tr v-for="item in rec.items" :key="item.id">
                      <td class="py-1.5 px-2 font-medium text-slate-800">
                        {{ item.material?.name || 'Matériau #' + item.material_id }}
                      </td>
                      <td class="py-1.5 px-2 text-right font-mono font-bold text-emerald-600">
                        {{ item.quantity_received }}
                      </td>
                      <td class="py-1.5 px-2 text-right font-mono font-bold" :class="item.quantity_rejected > 0 ? 'text-red-600' : 'text-slate-400'">
                        {{ item.quantity_rejected }}
                        <span v-if="item.rejection_reason" class="block text-[10px] text-red-500 font-normal">
                          ({{ item.rejection_reason }})
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div v-if="rec.notes" class="text-[11px] text-slate-500 bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                <span class="font-bold">Observations :</span> {{ rec.notes }}
              </div>
            </div>
          </div>
        </div>

        <!-- Onglet 3 : Pièces Jointes & Justificatifs -->
        <div v-if="activeTab === 'documents'" class="bg-white rounded-3xl border border-slate-200 shadow-xs p-6 space-y-4">
          <div>
            <h2 class="font-bold text-slate-800 text-sm">Pièces Jointes & Justificatifs de Paiement</h2>
            <p class="text-xs text-slate-400 mt-0.5">
              Téléversez vos factures scannées, bons de livraison signés ou photos des matériaux
            </p>
          </div>

          <DocumentUploader
            :documents="purchase?.documents || []"
            @upload="handleDocumentUpload"
            @delete="handleDocumentDelete"
          />
        </div>
      </div>

      <!-- Colonne Latérale : Informations Chantier & Fournisseur -->
      <div class="space-y-6">
        <!-- Carte Chantier -->
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs space-y-3.5">
          <div class="flex items-center gap-2.5 text-slate-800 font-bold text-sm border-b border-slate-100 pb-3">
            <fas-icon icon="building" class="text-blue-600" />
            <span>Chantier d'Affectation</span>
          </div>

          <div class="space-y-2 text-xs">
            <div>
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Projet / Chantier</span>
              <router-link
                :to="`/chantiers/${purchase?.chantier_id}`"
                class="font-bold text-blue-700 hover:underline flex items-center gap-1 mt-0.5"
              >
                <span>{{ purchase?.chantier?.name || 'Chantier #' + purchase?.chantier_id }}</span>
                <fas-icon icon="arrow-up-right-from-square" class="text-[10px]" />
              </router-link>
            </div>

            <div v-if="purchase?.task">
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Tâche rattachée</span>
              <div class="font-bold text-slate-800 flex items-center gap-1.5 mt-0.5">
                <fas-icon icon="list-check" class="text-slate-400 text-xs" />
                <span>{{ purchase.task.code }} - {{ purchase.task.name }}</span>
              </div>
            </div>

            <div>
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Code Chantier</span>
              <span class="font-mono font-bold text-slate-700">{{ purchase?.chantier?.code }}</span>
            </div>
          </div>
        </div>

        <!-- Carte Fournisseur -->
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs space-y-3.5">
          <div class="flex items-center gap-2.5 text-slate-800 font-bold text-sm border-b border-slate-100 pb-3">
            <fas-icon icon="handshake" class="text-amber-600" />
            <span>Fournisseur</span>
          </div>

          <div class="space-y-2 text-xs">
            <div>
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Raison Sociale</span>
              <router-link
                :to="`/achats/fournisseurs/${purchase?.supplier_id}`"
                class="font-bold text-blue-700 hover:underline flex items-center gap-1 mt-0.5"
              >
                <span>{{ purchase?.supplier?.name }}</span>
                <fas-icon icon="arrow-up-right-from-square" class="text-[10px]" />
              </router-link>
            </div>

            <div>
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Téléphone</span>
              <span class="font-bold text-slate-800 font-mono">{{ purchase?.supplier?.phone }}</span>
            </div>

            <div v-if="purchase?.supplier?.email">
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Email</span>
              <span class="text-slate-600">{{ purchase.supplier.email }}</span>
            </div>

            <div v-if="purchase?.supplier?.payment_terms">
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Conditions de règlement</span>
              <span class="text-slate-600">{{ purchase.supplier.payment_terms }}</span>
            </div>
          </div>
        </div>

        <!-- Carte Conditions Financières -->
        <div class="bg-gradient-to-br from-blue-900 to-indigo-950 p-5 rounded-3xl text-white shadow-md space-y-4">
          <div class="text-xs font-bold text-blue-200 uppercase tracking-wider">
            Synthèse Financière
          </div>

          <div>
            <span class="text-[11px] text-blue-300 block">Total de la commande</span>
            <div class="text-2xl font-black font-mono text-white mt-0.5">
              {{ formatNumber(purchase?.total_amount) }} <span class="text-xs font-normal">FCFA</span>
            </div>
          </div>

          <div class="pt-3 border-t border-white/10 space-y-2 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-blue-200">Statut Règlement :</span>
              <span class="font-bold text-white">{{ purchase?.payment_status }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-blue-200">Moyen utilisé :</span>
              <span class="font-bold text-white">{{ purchase?.payment_mode }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <PurchaseReceiveModal
      :is-open="showReceiveModal"
      :purchase="purchase"
      @close="showReceiveModal = false"
      @saved="loadPurchaseDetail"
    />

    <PurchaseFormModal
      :is-open="showEditModal"
      :purchase="purchase"
      @close="showEditModal = false"
      @saved="loadPurchaseDetail"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { purchaseService } from '@/services'
import DocumentUploader from '@/components/common/DocumentUploader.vue'
import PurchaseReceiveModal from './components/PurchaseReceiveModal.vue'
import PurchaseFormModal from './components/PurchaseFormModal.vue'
import Swal from 'sweetalert2'

const route = useRoute()
const purchaseId = Number(route.params.id)

const loading = ref(false)
const purchase = ref(null)
const activeTab = ref('articles')

const showReceiveModal = ref(false)
const showEditModal = ref(false)

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
    default:
      return 'bg-slate-100 text-slate-700'
  }
}

const getPaymentBadgeClass = (paymentStatus) => {
  switch (paymentStatus) {
    case 'Payé':
      return 'bg-emerald-100 text-emerald-800'
    case 'Partiellement payé':
      return 'bg-amber-100 text-amber-800'
    default:
      return 'bg-slate-100 text-slate-700'
  }
}

const loadPurchaseDetail = async () => {
  loading.value = true
  try {
    purchase.value = await purchaseService.getPurchaseById(purchaseId)
  } catch (err) {
    console.error('Erreur chargement détail achat:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPurchaseDetail()
})

const handleDocumentUpload = async (formData) => {
  try {
    await purchaseService.uploadDocument(purchaseId, formData)
    Swal.fire({
      icon: 'success',
      title: 'Pièce jointe ajoutée',
      timer: 1500,
      showConfirmButton: false,
    })
    await loadPurchaseDetail()
  } catch (err) {
    Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
  }
}

const handleDocumentDelete = async (documentId) => {
  const result = await Swal.fire({
    title: 'Supprimer ce document ?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Oui, supprimer',
  })
  if (result.isConfirmed) {
    try {
      await purchaseService.deleteDocument(documentId)
      Swal.fire({
        icon: 'success',
        title: 'Document supprimé',
        timer: 1500,
        showConfirmButton: false,
      })
      await loadPurchaseDetail()
    } catch (err) {
      Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
    }
  }
}

const printPurchaseOrder = () => {
  window.print()
}
</script>
