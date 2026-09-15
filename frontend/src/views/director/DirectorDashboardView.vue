<template>
  <div class="space-y-6">
    <!-- En-tête Espace Director -->
    <div class="bg-dark-800/80 p-5 rounded-2xl border border-dark-600 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-bold mb-1">
          <span>📐</span>
          <span>DIRECTION TECHNIQUE</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Supervision Technique & Projets</h2>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Appels d'offres, validation des situations et allocation des ressources</p>
      </div>
    </div>

    <!-- Grille KPI Director Responsive -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Appels d'Offres</div>
        <div class="text-2xl sm:text-3xl font-black text-white">5 Dossiers</div>
        <div class="text-xs text-purple-300 mt-2">
          3 en analyse • 2 soumis
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Situations à Valider</div>
        <div class="text-2xl sm:text-3xl font-black text-btp-400">4 En Attente</div>
        <div class="text-xs text-slate-400 mt-2">
          Montant : 142 000 000 FCFA
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Avancement Moyen</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-400">68.2 %</div>
        <div class="text-xs text-emerald-400 mt-2 font-medium">
          ↗ +4.5% sur la quinzaine
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Parc Engins Mobilisé</div>
        <div class="text-2xl sm:text-3xl font-black text-white">18 / 22</div>
        <div class="text-xs text-slate-400 mt-2">
          4 en révision préventive
        </div>
      </div>
    </div>

    <!-- Modules Direction Technique -->
    <div class="bg-dark-800 border border-dark-600 rounded-2xl p-6 shadow-xl">
      <h3 class="text-base sm:text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span>📋</span>
        <span>Responsabilités & Outils de la Direction Technique</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">📑 Validation des Situations de Travaux</div>
          <p class="text-xs text-slate-400">Contrôle des attachements métrés, récapitulatif cumulé, calcul des acomptes et respect du plafond contractuel.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">⚖️ Réponses aux Appels d'Offres</div>
          <p class="text-xs text-slate-400">Étude des dossiers de consultation (DCE), décomposition des prix unitaires (BPU) et soumission dans les délais impartis.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">🚜 Plan de Charge des Équipements Lourds</div>
          <p class="text-xs text-slate-400">Affectation optimisée des grues, bulldozers, pelleteuses et camions bennes entre les différents chantiers.</p>
        </div>
        <div class="p-4 rounded-xl bg-dark-900/60 border border-dark-600">
          <div class="font-bold text-white text-sm mb-1">👷 Coordination de l'Encadrement</div>
          <p class="text-xs text-slate-400">Animation des revues d'avancement hebdomadaires avec les conducteurs de travaux et chefs de projets.</p>
        </div>
      </div>
    </div>
  </div>
</template>
