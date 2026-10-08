<template>
  <div class="space-y-6">
    <!-- En-tête du Dashboard -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <div>
        <div class="flex items-center gap-2 text-xs font-bold text-[#047857] uppercase tracking-wider mb-1">
          <fas-icon icon="gauge-high" />
          <span>Tableau de bord</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Bonjour {{ authStore.userName ? authStore.userName.split(' ')[0] : '' }} 👋
        </h1>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          Vue d'ensemble opérationnelle, performance financière et suivi des chantiers en cours.
        </p>
      </div>

      <!-- Actions Principale (BLEU) & Secondaire (GRIS) -->
      <div class="flex items-center gap-3">
        <button 
          @click="handleExport"
          class="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs sm:text-sm border border-slate-200 transition-colors flex items-center gap-2"
        >
          <fas-icon icon="file-export" />
          <span>Exporter rapport</span>
        </button>

        <router-link 
          to="/chantiers/nouveau" 
          class="px-4 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-[#1e40af] text-white font-bold text-xs sm:text-sm shadow-sm transition-all flex items-center gap-2"
        >
          <fas-icon icon="plus" />
          <span>+ Nouveau chantier</span>
        </router-link>
      </div>
    </div>

    <!-- Grille des 6 KPIs Clés (Cartes blanches, bordures légères) -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
      <!-- 1. Projets Actifs -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Projets actifs</span>
          <fas-icon icon="folder-open" class="text-blue-500 text-sm" />
        </div>
        <div class="text-2xl font-black text-slate-900">12</div>
        <div class="text-[11px] text-emerald-600 font-medium mt-1">8 actifs • 4 études</div>
      </div>

      <!-- 2. Chantiers en cours -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Chantiers</span>
          <fas-icon icon="building" class="text-[#047857] text-sm" />
        </div>
        <div class="text-2xl font-black text-slate-900">8</div>
        <div class="text-[11px] text-slate-500 mt-1">Sur 4 villes</div>
      </div>

      <!-- 3. Appels d'offres -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Appels d'offres</span>
          <fas-icon icon="file-lines" class="text-purple-500 text-sm" />
        </div>
        <div class="text-2xl font-black text-slate-900">5</div>
        <div class="text-[11px] text-purple-600 font-medium mt-1">3 en cours d'étude</div>
      </div>

      <!-- 4. Budget Total -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Budget total</span>
          <fas-icon icon="wallet" class="text-blue-600 text-sm" />
        </div>
        <div class="text-lg sm:text-xl font-black text-blue-700 font-mono">2,45 Mrd</div>
        <div class="text-[11px] text-slate-500 mt-1">FCFA engagés</div>
      </div>

      <!-- 5. Dépenses -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Dépenses</span>
          <fas-icon icon="receipt" class="text-amber-600 text-sm" />
        </div>
        <div class="text-lg sm:text-xl font-black text-slate-900 font-mono">1,78 Mrd</div>
        <div class="text-[11px] text-slate-500 mt-1">FCFA décaissés</div>
      </div>

      <!-- 6. Avancement Moyen -->
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider">Avancement</span>
          <fas-icon icon="chart-line" class="text-emerald-600 text-sm" />
        </div>
        <div class="text-2xl font-black text-emerald-600">72.8 %</div>
        <div class="text-[11px] text-emerald-600 font-medium mt-1">↗ +3.4% ce mois</div>
      </div>
    </div>

    <!-- Section Graphiques : Avancement des Projets & Budget vs Dépenses -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Graphique 1 : Avancement des projets -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <fas-icon icon="chart-simple" class="text-[#1d4ed8]" />
              <span>Avancement des projets</span>
            </h2>
            <p class="text-xs text-slate-500">Taux d'exécution physique par chantier</p>
          </div>
          <span class="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-lg">
            Temps réel
          </span>
        </div>

        <div class="space-y-4 pt-2">
          <div v-for="p in projectProgress" :key="p.nom" class="space-y-1.5">
            <div class="flex justify-between text-xs font-medium">
              <span class="text-slate-800 font-semibold">{{ p.nom }}</span>
              <span class="font-bold text-slate-700">{{ p.progression }} %</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div 
                class="h-2.5 rounded-full transition-all duration-500" 
                :class="p.progression >= 80 ? 'bg-[#047857]' : p.progression >= 50 ? 'bg-[#1d4ed8]' : 'bg-amber-500'"
                :style="{ width: `${p.progression}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Graphique 2 : Budget vs Dépenses -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <fas-icon icon="scale-balanced" class="text-[#047857]" />
              <span>Budget prévu vs Dépenses réelles</span>
            </h2>
            <p class="text-xs text-slate-500">Comparaison financière ventilée par chantier (FCFA)</p>
          </div>
          <div class="flex items-center gap-3 text-[11px]">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 bg-[#1d4ed8] rounded-sm"></span> Budget</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 bg-slate-400 rounded-sm"></span> Dépenses</span>
          </div>
        </div>

        <div class="space-y-4 pt-2">
          <div v-for="b in budgetComparison" :key="b.nom" class="space-y-1">
            <div class="flex justify-between text-xs">
              <span class="font-semibold text-slate-800">{{ b.nom }}</span>
              <span class="text-slate-500 font-mono text-[11px]">{{ b.depenses }} / {{ b.budget }}</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="flex-1 bg-slate-100 rounded-full h-2 overflow-hidden flex">
                <div class="bg-[#1d4ed8] h-2" :style="{ width: `${b.ratio}%` }"></div>
              </div>
              <span class="text-[11px] font-bold text-slate-600 w-10 text-right">{{ b.ratio }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section Deux Colonnes : Projets Récents (Tableau) & Alertes -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Tableau Partagé : Projets Récents (DataTable) -->
      <DataTable
        :columns="recentProjectsColumns"
        :items="recentProjects"
        title="Projets récents"
        subtitle="Supervision directe des opérations en cours"
        :paginated="false"
        :searchable="false"
        class="lg:col-span-2"
      >
        <template #header-actions>
          <router-link 
            to="/chantiers" 
            class="text-xs font-semibold text-[#1d4ed8] hover:underline flex items-center gap-1"
          >
            <span>Voir tous les chantiers</span>
            <fas-icon icon="arrow-right" />
          </router-link>
        </template>

        <template #cell(projet)="{ item, value }">
          <router-link :to="`/chantiers/${item.id}`" class="hover:text-[#1d4ed8] transition-colors flex items-center gap-1.5 group font-semibold text-slate-900">
            <span>{{ value }}</span>
            <fas-icon icon="arrow-up-right-from-square" class="text-[10px] text-slate-400 group-hover:text-blue-600 transition-colors" />
          </router-link>
        </template>

        <template #cell(client)="{ value }">
          <span class="text-slate-600">{{ value }}</span>
        </template>

        <template #cell(responsable)="{ value }">
          <span class="font-medium text-slate-800">{{ value }}</span>
        </template>

        <template #cell(avancement)="{ value }">
          <div class="flex items-center gap-2">
            <div class="w-16 bg-slate-100 rounded-full h-1.5 overflow-hidden">
              <div class="h-1.5 rounded-full bg-[#047857]" :style="{ width: `${value}%` }"></div>
            </div>
            <span class="font-bold text-[11px] text-slate-700">{{ value }}%</span>
          </div>
        </template>

        <template #cell(budget)="{ value }">
          <span class="font-mono font-medium text-slate-900">{{ value }}</span>
        </template>

        <template #cell(statut)="{ item, value }">
          <span 
            class="px-2.5 py-1 rounded-full text-[10px] font-bold"
            :class="item.statusClass"
          >
            {{ value }}
          </span>
        </template>
      </DataTable>

      <!-- Section Alertes (1 colonne) -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
            <fas-icon icon="triangle-exclamation" class="text-amber-500" />
            <span>Alertes opérationnelles</span>
          </h2>
          <span class="text-[10px] bg-red-50 text-red-700 font-bold px-2 py-0.5 rounded-full border border-red-200">
            4 alertes
          </span>
        </div>

        <div class="space-y-3">
          <!-- 1. Stock Faible -->
          <div class="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-xs space-y-1">
            <div class="flex items-center gap-2 font-bold text-amber-900">
              <fas-icon icon="box-open" class="text-amber-600" />
              <span>Stock faible : Ciment CPJ 42.5</span>
            </div>
            <p class="text-amber-800 text-[11px]">350 sacs restants au dépôt (seuil minimum : 500 sacs).</p>
            <router-link to="/achats-stocks/stocks" class="inline-block text-[11px] font-bold text-[#1d4ed8] hover:underline pt-1">
              Commander du ciment ➔
            </router-link>
          </div>

          <!-- 2. Maintenance à prévoir -->
          <div class="p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-xs space-y-1">
            <div class="flex items-center gap-2 font-bold text-blue-900">
              <fas-icon icon="wrench" class="text-blue-600" />
              <span>Maintenance à prévoir : Grue Potain</span>
            </div>
            <p class="text-blue-800 text-[11px]">Contrôle périodique des câbles sous 48h requis (Tour Azur).</p>
            <router-link to="/engins/maintenance" class="inline-block text-[11px] font-bold text-[#1d4ed8] hover:underline pt-1">
              Consulter l'OT ➔
            </router-link>
          </div>

          <!-- 3. Contrat proche échéance -->
          <div class="p-3.5 rounded-xl bg-purple-50 border border-purple-200 text-xs space-y-1">
            <div class="flex items-center gap-2 font-bold text-purple-900">
              <fas-icon icon="file-contract" class="text-purple-600" />
              <span>Contrat proche de l'échéance</span>
            </div>
            <p class="text-purple-800 text-[11px]">Sous-traitance Pieux Forés arrive à échéance le 30/09.</p>
            <router-link to="/marches/contrats" class="inline-block text-[11px] font-bold text-[#1d4ed8] hover:underline pt-1">
              Voir l'avenant ➔
            </router-link>
          </div>

          <!-- 4. Situation de travaux à valider -->
          <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs space-y-1">
            <div class="flex items-center gap-2 font-bold text-emerald-900">
              <fas-icon icon="receipt" class="text-emerald-600" />
              <span>Situation de travaux à valider</span>
            </div>
            <p class="text-emerald-800 text-[11px]">Décompte N°4 Pont Bassam (98 000 000 FCFA en attente visa MOE).</p>
            <router-link to="/marches/situations" class="inline-block text-[11px] font-bold text-[#1d4ed8] hover:underline pt-1">
              Valider la situation ➔
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/alert'

const authStore = useAuthStore()

const projectProgress = [
  { nom: 'Construction école primaire à Yopougon', progression: 68 },
  { nom: 'Tour Azur R+14 (Plateau)', progression: 84 },
  { nom: 'Pont de Franchissement Grand-Bassam', progression: 62 },
  { nom: 'Voie Express Tronçon B', progression: 95 },
  { nom: 'Villas Résidentielles Songon', progression: 35 },
]

const budgetComparison = [
  { nom: 'École primaire Yopougon', budget: '250 M', depenses: '170 M', ratio: 68 },
  { nom: 'Tour Azur R+14', budget: '1 200 M', depenses: '1 008 M', ratio: 84 },
  { nom: 'Pont Grand-Bassam', budget: '850 M', depenses: '527 M', ratio: 62 },
  { nom: 'Voie Express Bassam', budget: '420 M', depenses: '399 M', ratio: 95 },
  { nom: 'Villas Songon', budget: '680 M', depenses: '238 M', ratio: 35 },
]

const recentProjectsColumns = [
  { key: 'projet', label: 'Projet', sortable: true },
  { key: 'client', label: 'Client' },
  { key: 'responsable', label: 'Responsable' },
  { key: 'avancement', label: 'Avancement', sortable: true },
  { key: 'budget', label: 'Budget (FCFA)' },
  { key: 'statut', label: 'Statut', align: 'right' }
]

const recentProjects = [
  {
    id: 1,
    projet: 'Construction école primaire à Yopougon',
    client: 'Ministère de la Construction',
    responsable: 'Ing. K. Kouassi',
    avancement: 68,
    budget: '250 000 000 FCFA',
    statut: 'En cours',
    statusClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  },
  {
    id: 2,
    projet: 'Tour Azur — Immeuble R+14',
    client: 'SCI Laguna',
    responsable: 'M. Yao',
    avancement: 84,
    budget: '1 200 000 000 FCFA',
    statut: 'En cours',
    statusClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  },
  {
    id: 3,
    projet: 'Pont de Franchissement Bassam',
    client: 'Ministère de l\'Équipement',
    responsable: 'A. Traoré',
    avancement: 62,
    budget: '850 000 000 FCFA',
    statut: 'En cours',
    statusClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  },
  {
    id: 4,
    projet: 'Voie Express Grand-Bassam',
    client: 'AGEROUTE',
    responsable: 'D. Koffi',
    avancement: 95,
    budget: '420 000 000 FCFA',
    statut: 'Finitions',
    statusClass: 'bg-blue-50 text-blue-700 border border-blue-200',
  },
]

function handleExport() {
  toast.fire({
    icon: 'success',
    title: 'Rapport Dashboard exporté en PDF.',
  })
}
</script>
