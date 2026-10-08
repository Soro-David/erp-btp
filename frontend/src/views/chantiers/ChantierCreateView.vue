<template>
  <div class="space-y-6 max-w-7xl mx-auto pb-12">
    <!-- Fil d'Ariane & En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <nav class="flex items-center gap-2 text-xs font-medium text-slate-500 mb-1">
          <router-link to="/dashboard" class="hover:text-blue-600 transition-colors">ERP BTP</router-link>
          <span>/</span>
          <router-link to="/chantiers" class="hover:text-blue-600 transition-colors">Chantiers</router-link>
          <span>/</span>
          <span class="text-slate-900 font-semibold">Nouveau chantier</span>
        </nav>
        <div class="flex items-center gap-3">
          <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            Ajouter un chantier
          </h1>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200">
            Nouveau projet
          </span>
        </div>
        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">
          Renseignez les données techniques, administratives, financières et humaines du projet.
        </p>
      </div>

      <!-- Bouton de retour vers la liste -->
      <router-link
        to="/chantiers"
        class="self-start sm:self-auto px-4 py-2.5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs sm:text-sm font-semibold flex items-center gap-2 transition-colors shadow-sm"
      >
        <fas-icon icon="arrow-left" class="text-slate-500" />
        <span>Retour à la liste</span>
      </router-link>
    </div>

    <!-- Formulaire dynamique principal -->
    <ChantierForm />
  </div>
</template>

<script setup>
import ChantierForm from './components/ChantierForm.vue'
</script>
