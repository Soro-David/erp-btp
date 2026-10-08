<template>
  <div class="space-y-6">
    <!-- En-tête Espace Director (Carte Blanche) -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-purple-50 border border-purple-200 text-purple-800 text-xs font-bold mb-1">
          <fas-icon icon="compass-drafting" />
          <span>DIRECTION TECHNIQUE (FASTAPI)</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Supervision Technique & Projets</h1>
        <p class="text-slate-500 text-xs sm:text-sm mt-0.5">
          {{ directorData?.message || 'Appels d\'offres, validation des situations et allocation des ressources' }}
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
    <div v-if="directorData" class="p-4 rounded-2xl bg-purple-50 border border-purple-200 text-xs text-purple-900 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <fas-icon icon="bolt" class="text-purple-700" />
        <span>Connecté à l'endpoint FastAPI <strong>/api/v1/director/projects-overview</strong> pour : <strong>{{ directorData.user }}</strong></span>
      </div>
      <span class="font-mono text-[10px] bg-purple-100 text-purple-800 px-2 py-0.5 rounded uppercase font-bold">{{ directorData.role }}</span>
    </div>

    <!-- Grille KPI Director Responsive (Cartes Blanches) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Appels d'Offres</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">5 Dossiers</div>
        <div class="text-xs text-purple-700 mt-2 font-medium">
          3 en analyse • 2 soumis
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Situations à Valider</div>
        <div class="text-2xl sm:text-3xl font-black text-amber-600">4 En Attente</div>
        <div class="text-xs text-slate-500 mt-2">
          Montant : 142 000 000 FCFA
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Avancement Moyen</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-600">68.2 %</div>
        <div class="text-xs text-emerald-600 mt-2 font-medium">
          ↗ +4.5% sur la quinzaine
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Parc Engins Mobilisé</div>
        <div class="text-2xl sm:text-3xl font-black text-slate-900">18 / 22</div>
        <div class="text-xs text-slate-500 mt-2">
          4 en révision préventive
        </div>
      </div>
    </div>

    <!-- Modules Direction Technique retournés par FastAPI -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <fas-icon icon="clipboard-list" class="text-purple-700" />
        <span>Responsabilités & Outils Direction Technique (FastAPI)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(mod, idx) in (directorData?.modules || defaultModules)" 
          :key="idx" 
          class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3 hover:bg-purple-50/50 transition-colors"
        >
          <span class="w-8 h-8 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center font-bold text-sm">
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

const directorData = ref(null)
const loading = ref(false)

const defaultModules = [
  'Validation technique des projets',
  'Supervision des conducteurs de travaux',
  'Validation situations de travaux',
  'Rapports d\'avancement consolidés',
]

async function loadData() {
  loading.value = true
  try {
    const data = await dashboardService.getDirectorOverview()
    directorData.value = data
  } catch (err) {
    console.error('Erreur API Director via Axios:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
