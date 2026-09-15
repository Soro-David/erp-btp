<template>
  <div class="space-y-6">
    <!-- En-tête Espace Worker (Mobile-first) -->
    <div class="bg-dark-800/80 p-5 rounded-2xl border border-dark-600 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold mb-1">
          <span>👷</span>
          <span>CHEF DE CHANTIER / TERRAIN</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Saisie & Suivi Quotidien</h2>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Pointage ouvriers, avancement métré et bons de sortie matériaux</p>
      </div>
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>Chantier Cocody R+2 Actif</span>
      </div>
    </div>

    <!-- Grille KPI Chantier Responsive -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Effectif sur Site</div>
        <div class="text-2xl sm:text-3xl font-black text-white">28 Ouvriers</div>
        <div class="text-xs text-emerald-400 mt-2 flex items-center gap-1">
          <span>✓</span>
          <span>Pointage matinal validé</span>
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Béton Coulé (Jour)</div>
        <div class="text-2xl sm:text-3xl font-black text-white">45 m³</div>
        <div class="text-xs text-slate-400 mt-2">
          Dalle supérieure niveau 2
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Ciment Consommé</div>
        <div class="text-2xl sm:text-3xl font-black text-btp-400">120 Sacs</div>
        <div class="text-xs text-slate-400 mt-2">
          CPJ 42.5 • Stock : 350 sacs
        </div>
      </div>

      <div class="bg-dark-800 border border-dark-600 rounded-2xl p-5 shadow-lg">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Ferraillage Posé</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-400">3.8 Tonnes</div>
        <div class="text-xs text-slate-400 mt-2">
          Aciers HA FeE500
        </div>
      </div>
    </div>

    <!-- Actions Rapides Terrain (Touch-friendly pour smartphone) -->
    <div class="bg-dark-800 border border-dark-600 rounded-2xl p-6 shadow-xl">
      <h3 class="text-base sm:text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span>📱</span>
        <span>Actions Rapides de Terrain</span>
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <button class="p-4 rounded-xl bg-dark-900 border border-dark-600 hover:border-emerald-500/50 hover:bg-dark-700 text-left transition-all group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">⏱️</div>
          <div class="font-bold text-white text-sm">Pointage Équipe</div>
          <div class="text-xs text-slate-400 mt-1">Présences, retards & heures sup</div>
        </button>

        <button class="p-4 rounded-xl bg-dark-900 border border-dark-600 hover:border-amber-500/50 hover:bg-dark-700 text-left transition-all group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">🧱</div>
          <div class="font-bold text-white text-sm">Sortie Matériaux</div>
          <div class="text-xs text-slate-400 mt-1">Ciment, fer, sable, gravier</div>
        </button>

        <button class="p-4 rounded-xl bg-dark-900 border border-dark-600 hover:border-blue-500/50 hover:bg-dark-700 text-left transition-all group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">📏</div>
          <div class="font-bold text-white text-sm">Saisie Métrés</div>
          <div class="text-xs text-slate-400 mt-1">Volumes et surfaces exécutés</div>
        </button>

        <button class="p-4 rounded-xl bg-dark-900 border border-dark-600 hover:border-purple-500/50 hover:bg-dark-700 text-left transition-all group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">📸</div>
          <div class="font-bold text-white text-sm">Journal & Photos</div>
          <div class="text-xs text-slate-400 mt-1">Rapport météo et constats</div>
        </button>
      </div>
    </div>
  </div>
</template>
