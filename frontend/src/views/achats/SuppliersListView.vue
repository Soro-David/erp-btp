<template>
  <div class="space-y-6">
    <!-- En-tête Page & Bouton d'ajout -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="handshake" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Fournisseurs & Sous-traitants</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Partenaires BTP</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Répertoire commercial, conditions de règlement et suivi des encours fournisseurs
          </p>
        </div>
      </div>

      <button
        type="button"
        @click="openAddModal(null)"
        class="px-4 py-2.5 rounded-2xl bg-[#1d4ed8] hover:bg-blue-700 text-white text-xs font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 transition-all transform active:scale-95"
      >
        <fas-icon icon="plus" />
        <span>+ Nouveau Fournisseur</span>
      </button>
    </div>

    <!-- KPI Summary -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Total Référencés</div>
        <div class="text-2xl font-black text-slate-900 font-mono">{{ suppliers.length }}</div>
        <div class="text-[10px] text-slate-400 mt-0.5">Partenaires agréés</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Fournisseurs Actifs</div>
        <div class="text-2xl font-black text-emerald-600 font-mono">
          {{ suppliers.filter((s) => s.is_active).length }}
        </div>
        <div class="text-[10px] text-slate-400 mt-0.5">En compte courant</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Localisation</div>
        <div class="text-2xl font-black text-blue-600 font-mono">Abidjan</div>
        <div class="text-[10px] text-slate-400 mt-0.5">& Villes de l'intérieur</div>
      </div>

      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div class="text-xs font-bold text-slate-500 mb-1">Paiements Préférés</div>
        <div class="text-2xl font-black text-amber-600 font-mono">Virement / 30j</div>
        <div class="text-[10px] text-slate-400 mt-0.5">Conditions moyennes</div>
      </div>
    </div>

    <!-- Barre de recherche -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between gap-4">
      <div class="relative flex-1 max-w-md">
        <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400 text-xs">
          <fas-icon icon="magnifying-glass" />
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Rechercher par raison sociale, code, téléphone..."
          class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs font-medium focus:outline-none focus:bg-white focus:border-blue-600"
          @input="debounceSearch"
        />
      </div>

      <div class="flex items-center gap-2">
        <label class="text-xs font-bold text-slate-600 flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            v-model="onlyActive"
            @change="loadSuppliers"
            class="rounded text-blue-600 focus:ring-blue-500"
          />
          <span>Actifs uniquement</span>
        </label>
      </div>
    </div>

    <!-- Liste des Fournisseurs -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="loading" class="py-16 text-center text-slate-400 space-y-2">
        <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
        <p class="text-xs font-semibold">Chargement des fournisseurs...</p>
      </div>

      <div v-else-if="filteredSuppliers.length === 0" class="py-16 text-center text-slate-400 space-y-3">
        <div class="w-14 h-14 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-300 text-2xl">
          <fas-icon icon="handshake" />
        </div>
        <div class="text-sm font-bold text-slate-700">Aucun fournisseur trouvé</div>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">
          Aucun partenaire ne correspond à vos critères de recherche.
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-50 text-[11px] font-extrabold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <th class="py-3 px-4">Code</th>
              <th class="py-3 px-4">Fournisseur / Raison Sociale</th>
              <th class="py-3 px-4">Contact</th>
              <th class="py-3 px-4">Coordonnées</th>
              <th class="py-3 px-4">Localisation</th>
              <th class="py-3 px-4">Règlement</th>
              <th class="py-3 px-4 text-center">Statut</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="s in filteredSuppliers"
              :key="s.id"
              class="hover:bg-slate-50/70 transition-colors group cursor-pointer"
              @click="goToDetail(s.id)"
            >
              <!-- Code -->
              <td class="py-3 px-4 font-mono font-bold text-slate-600">
                {{ s.code }}
              </td>

              <!-- Raison Sociale -->
              <td class="py-3 px-4">
                <div class="font-bold text-slate-800 text-sm group-hover:text-blue-600 transition-colors">
                  {{ s.name }}
                </div>
                <div v-if="s.trade_name" class="text-[11px] text-slate-400 italic">
                  {{ s.trade_name }}
                </div>
              </td>

              <!-- Contact -->
              <td class="py-3 px-4">
                <div class="font-medium text-slate-700">{{ s.contact_name || '-' }}</div>
              </td>

              <!-- Téléphone & Email -->
              <td class="py-3 px-4">
                <div class="font-bold text-slate-800 font-mono">{{ s.phone }}</div>
                <div v-if="s.email" class="text-[11px] text-slate-400 truncate max-w-xs">{{ s.email }}</div>
              </td>

              <!-- Localisation -->
              <td class="py-3 px-4 text-slate-600">
                <div>{{ s.city || 'Abidjan' }}</div>
                <div class="text-[10px] text-slate-400 truncate max-w-[160px]">{{ s.address || '' }}</div>
              </td>

              <!-- Conditions -->
              <td class="py-3 px-4 text-slate-600 text-[11px]">
                {{ s.payment_terms || 'Non spécifié' }}
              </td>

              <!-- Statut -->
              <td class="py-3 px-4 text-center">
                <span
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold"
                  :class="s.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'"
                >
                  {{ s.is_active ? 'Actif' : 'Inactif' }}
                </span>
              </td>

              <!-- Actions -->
              <td class="py-3 px-4 text-right whitespace-nowrap" @click.stop>
                <div class="flex items-center justify-end gap-1.5">
                  <button
                    type="button"
                    @click="goToDetail(s.id)"
                    class="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 transition-colors"
                    title="Voir la fiche"
                  >
                    <fas-icon icon="eye" class="text-xs" />
                  </button>
                  <button
                    type="button"
                    @click="openAddModal(s)"
                    class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
                    title="Modifier"
                  >
                    <fas-icon icon="pen-to-square" class="text-xs" />
                  </button>
                  <button
                    type="button"
                    @click="confirmDelete(s)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                    title="Désactiver / Supprimer"
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

    <!-- Modal d'ajout / modification -->
    <AddSupplierModal
      :is-open="showAddModal"
      :supplier="editingSupplier"
      @close="showAddModal = false"
      @saved="loadSuppliers"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supplierService } from '@/services'
import AddSupplierModal from './components/AddSupplierModal.vue'
import Swal from 'sweetalert2'

const router = useRouter()

const loading = ref(false)
const suppliers = ref([])
const searchQuery = ref('')
const onlyActive = ref(true)

const showAddModal = ref(false)
const editingSupplier = ref(null)

let searchTimeout = null
const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadSuppliers()
  }, 300)
}

const loadSuppliers = async () => {
  loading.value = true
  try {
    const params = {
      search: searchQuery.value || undefined,
      is_active: onlyActive.value ? true : undefined,
    }
    suppliers.value = await supplierService.getSuppliers(params)
  } catch (err) {
    console.error('Erreur chargement fournisseurs:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSuppliers()
})

const filteredSuppliers = computed(() => {
  return suppliers.value
})

const goToDetail = (id) => {
  router.push(`/achats/fournisseurs/${id}`)
}

const openAddModal = (sup = null) => {
  editingSupplier.value = sup
  showAddModal.value = true
}

const confirmDelete = async (supplier) => {
  const result = await Swal.fire({
    title: 'Supprimer ce fournisseur ?',
    text: `Voulez-vous supprimer ou désactiver ${supplier.name} ?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Oui, confirmer',
    cancelButtonText: 'Annuler',
  })

  if (result.isConfirmed) {
    try {
      await supplierService.deleteSupplier(supplier.id)
      Swal.fire({
        icon: 'success',
        title: 'Fournisseur supprimé / archivé',
        timer: 1500,
        showConfirmButton: false,
      })
      loadSuppliers()
    } catch (err) {
      Swal.fire('Erreur', err.response?.data?.detail || err.message, 'error')
    }
  }
}
</script>
