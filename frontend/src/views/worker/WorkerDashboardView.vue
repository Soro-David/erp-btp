<template>
  <div class="space-y-6">
    <!-- En-tête Espace Worker (Carte Blanche Mobile-first) -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold mb-1">
          <fas-icon icon="hard-hat" />
          <span>CHEF DE CHANTIER / TERRAIN (FASTAPI)</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Saisie & Suivi Quotidien</h1>
        <p class="text-slate-500 text-xs sm:text-sm mt-0.5">
          {{ workerData?.message || 'Pointage ouvriers, avancement métré et bons de sortie matériaux' }}
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Chantier Cocody R+2 Actif</span>
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

    <!-- Message de confirmation Axios FastAPI -->
    <div v-if="workerData" class="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <fas-icon icon="bolt" class="text-emerald-700" />
        <span>Connecté à l'endpoint FastAPI <strong>/api/v1/worker/daily-tasks</strong> pour : <strong>{{ workerData.user }}</strong></span>
      </div>
      <span class="font-mono text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded uppercase font-bold">{{ workerData.role }}</span>
    </div>

    <!-- Grille KPI Chantier Responsive (Cartes Blanches) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Effectif sur Site</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">28 Ouvriers</div>
        <div class="text-xs text-emerald-600 mt-2 flex items-center gap-1 font-medium">
          <fas-icon icon="check" />
          <span>Pointage matinal validé</span>
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Béton Coulé (Jour)</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">45 m³</div>
        <div class="text-xs text-slate-500 mt-2">
          Dalle supérieure niveau 2
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Engins en Activité</div>
        <div class="text-2xl sm:text-3xl font-black text-blue-700">3 Engins</div>
        <div class="text-xs text-slate-500 mt-2">
          Grue à tour • CAT 320 • Bétonnière
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Sécurité (QHSE)</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-600">0 Incident</div>
        <div class="text-xs text-slate-500 mt-2">
          Équipements EPI vérifiés 100%
        </div>
      </div>
    </div>

    <!-- Actions rapides de saisie terrain -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <fas-icon icon="person-digging" class="text-emerald-700" />
        <span>Saisie Rapide Terrain (Actions Chef de Chantier)</span>
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
        <button 
          v-for="(mod, idx) in (workerData?.modules || defaultModules)" 
          :key="idx" 
          @click="handleAction(mod)"
          class="p-4 rounded-xl bg-slate-50 border border-slate-200 hover:bg-emerald-50/50 hover:border-emerald-200 transition-all text-left flex flex-col justify-between h-28 group"
        >
          <span class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-xs group-hover:scale-105 transition-transform">
            {{ idx + 1 }}
          </span>
          <span class="text-xs font-bold text-slate-800 group-hover:text-emerald-800">{{ mod }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardService } from '@/services'
import { toast, alertSuccess } from '@/utils/alert'

const workerData = ref(null)
const loading = ref(false)

const defaultModules = [
  'Pointage journalier équipes',
  'Validation avancement des tâches',
  'Bons de sortie matériaux',
  'Signalement incident / anomalie',
]

async function loadData() {
  loading.value = true
  try {
    const data = await dashboardService.getWorkerTasks()
    workerData.value = data
  } catch (err) {
    console.error('Erreur API Worker via Axios:', err)
  } finally {
    loading.value = false
  }
}

function handleAction(mod) {
  alertSuccess(`Action Terrain : ${mod}`, 'Le formulaire de saisie rapide sur chantier est prêt.')
}

onMounted(() => {
  loadData()
})
</script>
