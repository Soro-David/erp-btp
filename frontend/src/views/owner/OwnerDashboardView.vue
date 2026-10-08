<template>
  <div class="space-y-6">
    <!-- En-tête Espace Owner (Carte Blanche) -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-1">
          <fas-icon icon="building" />
          <span>ESPACE PROPRIÉTAIRE (FASTAPI)</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Tableau de Bord Stratégique BTP</h1>
        <p class="text-slate-500 text-xs sm:text-sm mt-0.5">
          {{ ownerData?.message || 'Supervision macro-économique, rentabilité chantiers et trésorerie' }}
        </p>
      </div>
      <div class="flex items-center gap-3">
        <div class="text-xs text-slate-600 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200 font-medium">
          Devise : <strong class="text-blue-700">FCFA (XOF)</strong>
        </div>
        <button 
          @click="loadData" 
          :disabled="loading"
          class="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 transition-colors border border-slate-300 text-xs font-semibold flex items-center gap-1.5 shadow-sm"
          title="Actualiser via API FastAPI"
        >
          <fas-icon icon="arrows-rotate" :class="loading ? 'animate-spin' : ''" />
          <span class="hidden sm:inline">{{ loading ? 'Chargement...' : 'Actualiser' }}</span>
        </button>
      </div>
    </div>

    <!-- Message de l'API FastAPI si reçu -->
    <div v-if="ownerData" class="p-4 rounded-2xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <fas-icon icon="bolt" class="text-blue-700" />
        <span>Connecté à l'endpoint FastAPI <strong>/api/v1/owner/dashboard-summary</strong> pour : <strong>{{ ownerData.user }}</strong></span>
      </div>
      <span class="font-mono text-[10px] bg-blue-100 text-blue-800 px-2 py-0.5 rounded uppercase font-bold">{{ ownerData.role }}</span>
    </div>

    <!-- Grille KPI Stratégique Responsive (Cartes Blanches) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Portefeuille Chantiers</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">12 Projets</div>
        <div class="text-xs text-slate-500 mt-2 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>8 actifs • 4 en préparation</span>
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Volume Contrats</div>
        <div class="text-xl sm:text-2xl font-black text-blue-700">2,45 Mrd FCFA</div>
        <div class="text-xs text-emerald-600 mt-2 font-medium">
          ↗ +18% vs N-1
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Marge Moyenne Estimée</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-600">24.5 %</div>
        <div class="text-xs text-slate-500 mt-2">
          Objectif annuel : 22.0 %
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Facturation Encaissée</div>
        <div class="text-xl sm:text-2xl font-black text-slate-900">1,82 Mrd FCFA</div>
        <div class="text-xs text-amber-600 mt-2 font-medium">
          Solde à recouvrer : 630 M FCFA
        </div>
      </div>
    </div>

    <!-- Modules Stratégiques retournés par FastAPI -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <fas-icon icon="rocket" class="text-blue-700" />
        <span>Modules Stratégiques Propriétaire (FastAPI)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(mod, idx) in (ownerData?.modules || defaultModules)" 
          :key="idx" 
          class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3 hover:bg-blue-50/50 transition-colors"
        >
          <span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-sm">
            {{ idx + 1 }}
          </span>
          <span class="text-sm font-semibold text-slate-800">{{ mod }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardService } from '@/services'

const ownerData = ref(null)
const loading = ref(false)

const defaultModules = [
  'Vue globale rentabilité',
  'Portefeuille chantiers',
  'Approbation budgets',
  'Alertes trésorerie',
]

async function loadData() {
  loading.value = true
  try {
    const data = await dashboardService.getOwnerSummary()
    ownerData.value = data
  } catch (err) {
    console.error('Erreur API Owner via Axios:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
