<template>
  <div class="space-y-6">
    <!-- En-tête Espace Manager (Carte Blanche) -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold mb-1">
          <fas-icon icon="list-check" />
          <span>CONDUITE DE TRAVAUX (FASTAPI)</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Pilotage Opérationnel des Chantiers</h1>
        <p class="text-slate-500 text-xs sm:text-sm mt-0.5">
          {{ managerData?.message || 'Suivi des plannings, commandes de matériaux, contrôle des tâches et attachements' }}
        </p>
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

    <!-- Message de confirmation Axios FastAPI -->
    <div v-if="managerData" class="p-4 rounded-2xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <fas-icon icon="bolt" class="text-blue-700" />
        <span>Connecté à l'endpoint FastAPI <strong>/api/v1/manager/assigned-sites</strong> pour : <strong>{{ managerData.user }}</strong></span>
      </div>
      <span class="font-mono text-[10px] bg-blue-100 text-blue-800 px-2 py-0.5 rounded uppercase font-bold">{{ managerData.role }}</span>
    </div>

    <!-- Grille KPI Manager Responsive (Cartes Blanches) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Chantiers Assignés</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">3 Projets</div>
        <div class="text-xs text-blue-700 mt-2 truncate font-medium" title="École Bingerville, Immeuble Cocody, Voie Yopougon">
          Bingerville • Cocody • Yopougon
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Tâches en Cours</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">24 Tâches</div>
        <div class="text-xs text-amber-600 mt-2 font-medium">
          3 avec alerte de délai
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Demandes d'Achat</div>
        <div class="text-2xl sm:text-3xl font-black text-amber-600">6 En Attente</div>
        <div class="text-xs text-slate-500 mt-2">
          Ciment CPJ, fers HA, gravier
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Main-d'Œuvre Pointée</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-600">64 Ouvriers</div>
        <div class="text-xs text-slate-500 mt-2">
          Sur 3 sites actifs aujourd'hui
        </div>
      </div>
    </div>

    <!-- Modules Conducteur retournés par FastAPI -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <fas-icon icon="helmet-safety" class="text-blue-700" />
        <span>Outils Conduite de Travaux (FastAPI)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(mod, idx) in (managerData?.modules || defaultModules)" 
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

const managerData = ref(null)
const loading = ref(false)

const defaultModules = [
  'Mes chantiers assignés',
  'Gestion des tâches & planning GANTT',
  'Demandes d\'approvisionnement matériaux',
  'Rapports journaliers de chantier',
]

async function loadData() {
  loading.value = true
  try {
    const data = await dashboardService.getManagerSites()
    managerData.value = data
  } catch (err) {
    console.error('Erreur API Manager via Axios:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
