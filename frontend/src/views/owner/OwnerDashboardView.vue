<template>
  <div class="space-y-6">
    <!-- En-tête Espace Owner -->
    <div class="bg-dark-800/80 p-5 rounded-2xl border border-dark-600 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold mb-1">
          <span>🏢</span>
          <span>ESPACE PROPRIÉTAIRE</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Tableau de Bord Stratégique BTP</h2>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Supervision macro-économique, rentabilité chantiers et trésorerie</p>
      </div>
      <div class="text-xs text-slate-400 bg-dark-900/60 px-3 py-1.5 rounded-lg border border-dark-600">
        Devise : <strong class="text-amber-400">FCFA (XOF)</strong>
      </div>
    </div>

    <!-- Grille KPI Stratégique Responsive -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Portefeuille Chantiers</div>
        <div class="text-2xl sm:text-3xl font-black text-white">12 Projets</div>
        <div class="text-xs text-slate-400 mt-2 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>8 actifs • 4 en préparation</span>
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Volume Contrats</div>
        <div class="text-xl sm:text-2xl font-black text-btp-400">2,45 Mrd FCFA</div>
        <div class="text-xs text-emerald-400 mt-2 font-medium">
          ↗ +18% vs N-1
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Marge Moyenne Estimée</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-400">24.5 %</div>
        <div class="text-xs text-slate-400 mt-2">
          Objectif annuel : 22.0 %
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Facturation Encaissée</div>
        <div class="text-xl sm:text-2xl font-black text-white">1,82 Mrd FCFA</div>
        <div class="text-xs text-amber-400 mt-2">
          Solde à recouvrer : 630 M
        </div>
      </div>
    </div>

    <!-- Modules Stratégiques -->
    <div class="bg-dark-800 border border-dark-600 rounded-2xl p-6 shadow-xl">
      <h3 class="text-base sm:text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span>🚀</span>
        <span>Fonctionnalités Clés Espace Direction</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📊 Rentabilité Globale & Marge Réelle</div>
          <p class="text-xs text-slate-400">Analyse détaillée du budget prévisionnel comparé aux coûts réels engagés (matériaux, main-d'œuvre, engins, carburant, sous-traitance).</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📑 Approbation des Contrats & Avenants</div>
          <p class="text-xs text-slate-400">Validation des conditions contractuelles, avances de démarrage et clauses de retenue de garantie (5%).</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">💰 Tableau de Bord Trésorerie</div>
          <p class="text-xs text-slate-400">Suivi des situations de travaux validées, échéanciers de paiement clients et décaissements sous-traitants.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📍 Répartition Géographique des Projets</div>
          <p class="text-xs text-slate-400">Visibilité sur l'ensemble des sites de construction (Abidjan, Bouaké, San Pedro, Yamoussoukro).</p>
        </div>
      </div>
    </div>
  </div>
</template>
