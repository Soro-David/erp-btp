<template>
  <div class="space-y-6">
    <!-- En-tête Espace Manager -->
    <div class="bg-dark-800/80 p-5 rounded-2xl border border-dark-600 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-bold mb-1">
          <span>📋</span>
          <span>CONDUITE DE TRAVAUX</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Pilotage Opérationnel des Chantiers</h2>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Suivi des plannings, commandes de matériaux, contrôle des tâches et attachements</p>
      </div>
    </div>

    <!-- Grille KPI Manager Responsive -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Chantiers Assignés</div>
        <div class="text-2xl sm:text-3xl font-black text-white">3 Projets</div>
        <div class="text-xs text-blue-300 mt-2 truncate" title="École Bingerville, Immeuble Cocody, Voie Yopougon">
          Bingerville • Cocody • Yopougon
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Tâches en Cours</div>
        <div class="text-2xl sm:text-3xl font-black text-white">24 Tâches</div>
        <div class="text-xs text-amber-400 mt-2">
          3 avec alerte de délai
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Demandes d'Achat</div>
        <div class="text-2xl sm:text-3xl font-black text-btp-400">6 En Attente</div>
        <div class="text-xs text-slate-400 mt-2">
          Ciment CPJ, fers HA, gravier
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Échéance Situation</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-400">Situation N° 4</div>
        <div class="text-xs text-slate-400 mt-2">
          Fin de période dans 4 jours
        </div>
      </div>
    </div>

    <!-- Outils Conduite de Travaux -->
    <div class="bg-dark-800 border border-dark-600 rounded-2xl p-6 shadow-xl">
      <h3 class="text-base sm:text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span>🛠️</span>
        <span>Outils de Gestion de Projet BTP</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📐 Découpage WBS (Phases & Tâches)</div>
          <p class="text-xs text-slate-400">Suivi structuré : Terrassement, Fondations, Gros Œuvre, Cloisonnement, Réseaux et Finitions.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📦 Approvisionnements & Réceptions</div>
          <p class="text-xs text-slate-400">Bons de commande fournisseurs, contrôle quantitatif à la livraison et vérification de conformité.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📈 Calcul d'Avancement Pondéré</div>
          <p class="text-xs text-slate-400">Consolidation automatique de l'avancement physique basée sur les quantités réalisées sur le terrain.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📑 Projet de Situation de Travaux</div>
          <p class="text-xs text-slate-400">Compilation des attachements pour transmission à la direction et au bureau de contrôle (BCT).</p>
        </div>
      </div>
    </div>
  </div>
</template>
