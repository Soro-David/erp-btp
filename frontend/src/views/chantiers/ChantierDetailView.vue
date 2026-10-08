<template>
  <div class="space-y-6">
    <!-- 1. En-tête & Fil d'Ariane -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <nav class="flex items-center gap-2 text-xs font-medium text-slate-500">
        <router-link to="/dashboard" class="hover:text-blue-600 transition-colors">ERP BTP</router-link>
        <span>/</span>
        <router-link to="/chantiers" class="hover:text-blue-600 transition-colors">Chantiers</router-link>
        <span>/</span>
        <span class="text-slate-900 font-semibold truncate">{{ chantier.name }}</span>
      </nav>
      <div class="flex items-center gap-2">
        <router-link
          to="/chantiers"
          class="px-3.5 py-2 rounded-xl bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
        >
          <fas-icon icon="arrow-left" class="text-slate-500" />
          <span>Retour à la liste</span>
        </router-link>
        <button
          @click="exportChantierPdf"
          class="px-3.5 py-2 rounded-xl bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
        >
          <fas-icon icon="file-pdf" class="text-rose-500" />
          <span>Rapport PDF</span>
        </button>
        <button
          @click="openNewSituationModal"
          class="px-4 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-2 transition-all shadow-sm"
        >
          <fas-icon icon="file-invoice-dollar" />
          <span>+ Nouvelle situation</span>
        </button>
      </div>
    </div>

    <!-- 2. Fiche Synthétique Chantier (Carte Blanche Premium) -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-5">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div class="flex items-start gap-4">
          <div class="w-14 h-14 rounded-2xl bg-blue-50 border border-blue-100 text-[#1d4ed8] flex items-center justify-center text-2xl flex-shrink-0">
            <fas-icon icon="building" />
          </div>
          <div>
            <div class="flex flex-wrap items-center gap-2.5 mb-1">
              <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
                {{ chantier.name }}
              </h1>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-700 border border-blue-200">
                {{ chantier.status }}
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-600">
                Réf : {{ chantier.reference }}
              </span>
            </div>
            <p class="text-xs sm:text-sm text-slate-500 flex items-center gap-4 flex-wrap">
              <span class="flex items-center gap-1.5">
                <fas-icon icon="location-dot" class="text-slate-400" />
                {{ chantier.location }}
              </span>
              <span class="flex items-center gap-1.5">
                <fas-icon icon="user-tie" class="text-slate-400" />
                Maître d'ouvrage : <strong class="text-slate-700">{{ chantier.client }}</strong>
              </span>
              <span class="flex items-center gap-1.5">
                <fas-icon icon="hard-hat" class="text-slate-400" />
                Chef de chantier : <strong class="text-slate-700">{{ chantier.manager }}</strong>
              </span>
            </p>
          </div>
        </div>

        <!-- Dates clés & badge délai -->
        <div class="flex items-center gap-3 bg-slate-50 border border-slate-200/80 rounded-xl px-4 py-3 text-xs self-start lg:self-center">
          <div>
            <div class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Période d'exécution</div>
            <div class="font-semibold text-slate-800 mt-0.5 flex items-center gap-2">
              <span>{{ chantier.startDate }}</span>
              <fas-icon icon="arrow-right" class="text-slate-400 text-[10px]" />
              <span>{{ chantier.endDate }}</span>
            </div>
          </div>
          <span class="ml-2 px-2 py-1 rounded-lg text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
            Dans les délais
          </span>
        </div>
      </div>

      <!-- Métriques financières & Barre d'avancement -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-slate-100">
        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Budget Contractuel</div>
          <div class="text-lg sm:text-xl font-black text-slate-900 mt-1">{{ formatFcfa(chantier.budget) }}</div>
          <div class="text-[10px] text-slate-500 mt-0.5">TTC selon marché signé</div>
        </div>

        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Dépenses Réelles</div>
          <div class="text-lg sm:text-xl font-black text-[#1d4ed8] mt-1">{{ formatFcfa(chantier.expenses) }}</div>
          <div class="text-[10px] text-slate-500 mt-0.5">{{ Math.round((chantier.expenses / chantier.budget) * 100) }}% du budget alloué</div>
        </div>

        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Solde Restant</div>
          <div class="text-lg sm:text-xl font-black text-emerald-600 mt-1">{{ formatFcfa(chantier.budget - chantier.expenses) }}</div>
          <div class="text-[10px] text-emerald-700 mt-0.5">Marge opérationnelle saine</div>
        </div>

        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100 flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Avancement Global</span>
            <span class="text-sm font-black text-[#1d4ed8]">{{ chantier.progress }}%</span>
          </div>
          <div class="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden mt-2">
            <div
              class="h-full rounded-full bg-[#1d4ed8] transition-all duration-500"
              :style="{ width: chantier.progress + '%' }"
            ></div>
          </div>
          <div class="text-[10px] text-slate-500 mt-1">Lot Gros Œuvre achevé</div>
        </div>
      </div>
    </div>

    <!-- 3. Barre des 9 Onglets Spécifiques BTP MANAGER -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="flex items-center border-b border-slate-200 overflow-x-auto scrollbar-none px-2 bg-slate-50/40">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="currentTab = tab.id"
          class="flex items-center gap-2 px-4 py-3.5 text-xs font-semibold whitespace-nowrap transition-all border-b-2 relative"
          :class="[
            currentTab === tab.id
              ? 'border-[#1d4ed8] text-[#1d4ed8] bg-white font-bold'
              : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100/60'
          ]"
        >
          <fas-icon :icon="tab.icon" class="text-xs" :class="currentTab === tab.id ? 'text-[#1d4ed8]' : 'text-slate-400'" />
          <span>{{ tab.name }}</span>
          <span 
            v-if="tab.badge" 
            class="px-1.5 py-0.2 rounded-full text-[10px] font-bold"
            :class="currentTab === tab.id ? 'bg-blue-100 text-blue-800' : 'bg-slate-200 text-slate-700'"
          >
            {{ tab.badge }}
          </span>
        </button>
      </div>

      <!-- Contenu des Onglets -->
      <div class="p-6">
        <!-- ONGLET 1 : VUE GÉNÉRALE -->
        <div v-if="currentTab === 'general'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Colonne gauche : Descriptif & Spécifications -->
            <div class="lg:col-span-2 space-y-6">
              <div class="border border-slate-200 rounded-xl p-5 space-y-3 bg-white">
                <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <fas-icon icon="circle-info" class="text-[#1d4ed8]" />
                  <span>Présentation du Projet & Périmètre</span>
                </h3>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                  Construction d'un groupe scolaire de 6 classes, comprenant un bâtiment administratif, des sanitaires autonomes, une aire de jeux et une clôture sécurisée en maçonnerie de 220 mètres linéaires à Yopougon Andokoi. Structure R+1 en béton armé, toiture bac alu avec charpente métallique traitée anti-corrosion.
                </p>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[11px]">Surface bâtie</span>
                    <strong class="text-slate-800 font-bold">1 420 m²</strong>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[11px]">Type de marché</span>
                    <strong class="text-slate-800 font-bold">Appel d'Offres Public (AOP)</strong>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[11px]">Bureau de contrôle</span>
                    <strong class="text-slate-800 font-bold">SOCOTEC Côte d'Ivoire</strong>
                  </div>
                </div>
              </div>

              <!-- Évolution de l'avancement par corps d'état -->
              <div class="border border-slate-200 rounded-xl p-5 space-y-4 bg-white">
                <h3 class="text-sm font-bold text-slate-900 flex items-center justify-between">
                  <span class="flex items-center gap-2">
                    <fas-icon icon="chart-simple" class="text-emerald-600" />
                    <span>Progression par Corps d'État</span>
                  </span>
                  <span class="text-xs font-semibold text-slate-500">Moyenne pondérée : 68%</span>
                </h3>
                <div class="space-y-3">
                  <div v-for="lot in corpsDetat" :key="lot.name" class="space-y-1">
                    <div class="flex items-center justify-between text-xs">
                      <span class="font-medium text-slate-700">{{ lot.name }}</span>
                      <span class="font-bold text-slate-900">{{ lot.progress }}%</span>
                    </div>
                    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-500" :class="lot.color" :style="{ width: lot.progress + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Colonne droite : Coordonnées, Contacts & Alertes -->
            <div class="space-y-6">
              <div class="border border-slate-200 rounded-xl p-5 space-y-4 bg-white">
                <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <fas-icon icon="users" class="text-[#1d4ed8]" />
                  <span>Intervenants Clés</span>
                </h3>
                <div class="space-y-3 text-xs">
                  <div class="flex items-center justify-between p-2.5 rounded-lg bg-slate-50">
                    <div>
                      <div class="font-bold text-slate-800">Konan Kouassi</div>
                      <div class="text-[11px] text-slate-500">Conducteur de Travaux Principal</div>
                    </div>
                    <a href="tel:+22507000000" class="p-2 rounded-lg bg-white text-[#1d4ed8] border border-slate-200 hover:bg-blue-50">
                      <fas-icon icon="phone" />
                    </a>
                  </div>
                  <div class="flex items-center justify-between p-2.5 rounded-lg bg-slate-50">
                    <div>
                      <div class="font-bold text-slate-800">Mairie de Yopougon</div>
                      <div class="text-[11px] text-slate-500">Maître d'Ouvrage Délégué</div>
                    </div>
                    <button class="p-2 rounded-lg bg-white text-slate-600 border border-slate-200 hover:bg-slate-100">
                      <fas-icon icon="envelope" />
                    </button>
                  </div>
                  <div class="flex items-center justify-between p-2.5 rounded-lg bg-slate-50">
                    <div>
                      <div class="font-bold text-slate-800">BIA Architecture</div>
                      <div class="text-[11px] text-slate-500">Maîtrise d'Œuvre / Architecte</div>
                    </div>
                    <button class="p-2 rounded-lg bg-white text-slate-600 border border-slate-200 hover:bg-slate-100">
                      <fas-icon icon="file-signature" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- Alertes chantier -->
              <div class="border border-amber-200 bg-amber-50/50 rounded-xl p-4 space-y-2 text-xs">
                <div class="font-bold text-amber-900 flex items-center gap-2">
                  <fas-icon icon="triangle-exclamation" class="text-amber-600" />
                  <span>Points de vigilance (QSE)</span>
                </div>
                <p class="text-amber-800 text-[11px]">
                  Prévision de fortes pluies ce jeudi. Renforcer le bâchage des palettes de ciment et sécuriser les tranchées du réseau EU/EP.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- ONGLET 2 : TÂCHES DU CHANTIER -->
        <div v-if="currentTab === 'tasks'" class="space-y-4">
          <!-- Lien vers le module de planification -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 bg-blue-50/70 border border-blue-200 rounded-2xl">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-[#1d4ed8] text-white flex items-center justify-center text-base">
                <fas-icon icon="list-check" />
              </div>
              <div>
                <h4 class="text-xs font-bold text-blue-900">Module Avancé de Planification des Tâches</h4>
                <p class="text-[11px] text-blue-700">Arborescence, dépendances Fin → Début, priorités et alertes de blocage</p>
              </div>
            </div>
            <router-link
              :to="{ path: '/chantiers/taches', query: { chantier_id: chantier.id } }"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 self-start sm:self-auto transition-all"
            >
              <fas-icon icon="arrow-up-right-from-square" class="text-xs" />
              <span>Gérer dans le module dédié</span>
            </router-link>
          </div>

          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Lots & Tâches Opérationnelles</h3>
              <p class="text-xs text-slate-500">Suivi précis du calendrier des travaux et de l'affectation des équipes</p>
            </div>
            <button
              @click="openAddTaskModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="plus" />
              <span>Ajouter une tâche</span>
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <th class="pb-3 px-3">Réf</th>
                  <th class="pb-3 px-3">Désignation de la tâche</th>
                  <th class="pb-3 px-3">Corps d'état</th>
                  <th class="pb-3 px-3">Responsable</th>
                  <th class="pb-3 px-3">Échéance</th>
                  <th class="pb-3 px-3">Avancement</th>
                  <th class="pb-3 px-3">Statut</th>
                  <th class="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="task in tasksList" :key="task.id" class="hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-3 font-mono font-bold text-blue-700">{{ task.code }}</td>
                  <td class="py-3 px-3 font-semibold text-slate-900">{{ task.name }}</td>
                  <td class="py-3 px-3 text-slate-500">{{ task.lot }}</td>
                  <td class="py-3 px-3">{{ task.assignee }}</td>
                  <td class="py-3 px-3">{{ task.dueDate }}</td>
                  <td class="py-3 px-3">
                    <div class="flex items-center gap-2">
                      <div class="w-20 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div class="h-full bg-[#1d4ed8] rounded-full" :style="{ width: task.progress + '%' }"></div>
                      </div>
                      <span class="font-bold text-slate-800">{{ task.progress }}%</span>
                    </div>
                  </td>
                  <td class="py-3 px-3">
                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase" :class="getTaskStatusClass(task.status)">
                      {{ task.status }}
                    </span>
                  </td>
                  <td class="py-3 px-3 text-right">
                    <button @click="markTaskCompleted(task)" class="p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors" title="Marquer terminée">
                      <fas-icon icon="check" />
                    </button>
                    <button @click="editTask(task)" class="p-1.5 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors ml-1" title="Modifier">
                      <fas-icon icon="pen-to-square" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ONGLET 3 : PLANNING GANTT / JALONS -->
        <div v-if="currentTab === 'planning'" class="space-y-5">
          <!-- Lien vers Gantt complet -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-2xl">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-emerald-700 text-white flex items-center justify-center text-base">
                <fas-icon icon="chart-gantt" />
              </div>
              <div>
                <h4 class="text-xs font-bold text-emerald-950">Diagramme de Gantt & Jalons Contractuels Interactif</h4>
                <p class="text-[11px] text-emerald-700">Zoom jour/semaine/mois, tracé des chemins critiques et suivi des retards</p>
              </div>
            </div>
            <router-link
              :to="{ path: '/chantiers/planning', query: { chantier_id: chantier.id } }"
              class="px-3.5 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 self-start sm:self-auto transition-all"
            >
              <fas-icon icon="arrow-up-right-from-square" class="text-xs" />
              <span>Ouvrir le Gantt Interactif</span>
            </router-link>
          </div>

          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Planning Directeur & Jalons Contractuels</h3>
              <p class="text-xs text-slate-500">Vue chronologique des phases d'exécution du chantier</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-500">Durée totale : <strong>10.5 mois</strong></span>
            </div>
          </div>

          <!-- Chronologie visuelle -->
          <div class="space-y-4">
            <div v-for="(phase, idx) in planningPhases" :key="idx" class="border border-slate-200 rounded-xl p-4 bg-white hover:border-blue-300 transition-colors">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs" :class="phase.completed ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-50 text-[#1d4ed8]'">
                    <fas-icon :icon="phase.completed ? 'check' : 'hourglass-half'" />
                  </div>
                  <div>
                    <h4 class="font-bold text-slate-900 text-xs sm:text-sm">{{ phase.name }}</h4>
                    <span class="text-[11px] text-slate-400">{{ phase.dates }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <span class="text-xs font-bold" :class="phase.completed ? 'text-emerald-600' : 'text-[#1d4ed8]'">
                    {{ phase.progress }}% réalisé
                  </span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="phase.completed ? 'bg-emerald-50 text-emerald-700' : 'bg-blue-50 text-blue-700'">
                    {{ phase.status }}
                  </span>
                </div>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-500" :class="phase.completed ? 'bg-emerald-500' : 'bg-[#1d4ed8]'" :style="{ width: phase.progress + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- ONGLET 4 : MATÉRIAUX & STOCKS DU SITE -->
        <div v-if="currentTab === 'materials'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Gestion des Matériaux & Réceptions sur Site</h3>
              <p class="text-xs text-slate-500">Contrôle des bons de livraison, consommations et stocks de sécurité</p>
            </div>
            <button
              @click="openAddMaterialModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="plus" />
              <span>Enregistrer réception</span>
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <th class="pb-3 px-3">Matériau</th>
                  <th class="pb-3 px-3">Fournisseur</th>
                  <th class="pb-3 px-3">Qté Commandée</th>
                  <th class="pb-3 px-3">Qté Livrée</th>
                  <th class="pb-3 px-3">Stock Site</th>
                  <th class="pb-3 px-3">Coût Total</th>
                  <th class="pb-3 px-3">Statut Stock</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="mat in materialsList" :key="mat.id" class="hover:bg-slate-50">
                  <td class="py-3 px-3 font-semibold text-slate-900">{{ mat.name }}</td>
                  <td class="py-3 px-3 text-slate-500">{{ mat.supplier }}</td>
                  <td class="py-3 px-3">{{ mat.qtyOrdered }} {{ mat.unit }}</td>
                  <td class="py-3 px-3 font-bold text-emerald-600">{{ mat.qtyDelivered }} {{ mat.unit }}</td>
                  <td class="py-3 px-3 font-mono font-semibold">{{ mat.stockSite }} {{ mat.unit }}</td>
                  <td class="py-3 px-3 font-bold text-slate-900">{{ formatFcfa(mat.totalCost) }}</td>
                  <td class="py-3 px-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold" :class="mat.stockSite > 20 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'">
                      {{ mat.stockSite > 20 ? 'Stock Conforme' : 'Réappro requis' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ONGLET 5 : ÉQUIPEMENTS & ENGINS -->
        <div v-if="currentTab === 'equipment'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Parc Engins Mobilisés sur Chantier</h3>
              <p class="text-xs text-slate-500">Heures machine, consommations de carburant et visites techniques</p>
            </div>
            <button
              @click="openAddEquipmentModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="plus" />
              <span>Affecter un engin</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="eng in equipmentList" :key="eng.id" class="border border-slate-200 rounded-xl p-4 bg-white flex items-start gap-4">
              <div class="w-12 h-12 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center text-xl flex-shrink-0">
                <fas-icon :icon="eng.icon" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <h4 class="font-bold text-slate-900 text-sm">{{ eng.name }}</h4>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="eng.status === 'Opérationnel' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'">
                    {{ eng.status }}
                  </span>
                </div>
                <div class="text-xs text-slate-500 mt-1">Immat : <span class="font-mono text-slate-700 font-semibold">{{ eng.immat }}</span> • Conducteur : {{ eng.driver }}</div>
                <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-100 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[10px]">Heures compteur</span>
                    <strong class="text-slate-800 font-bold">{{ eng.hours }} h</strong>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[10px]">Coût journalier</span>
                    <strong class="text-slate-800 font-bold">{{ formatFcfa(eng.dailyRate) }}/j</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ONGLET 6 : MAIN-D'ŒUVRE -->
        <div v-if="currentTab === 'workforce'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Pointage Journalier & Effectifs</h3>
              <p class="text-xs text-slate-500">Présences relevées sur chantier aujourd'hui (38 compagnons au poste)</p>
            </div>
            <button
              @click="openPointageModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="clipboard-user" />
              <span>Pointer l'équipe</span>
            </button>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
            <div class="bg-slate-50 rounded-xl p-3 border border-slate-200">
              <span class="text-xs text-slate-500">Total Ouvriers</span>
              <div class="text-xl font-black text-slate-900">38</div>
            </div>
            <div class="bg-slate-50 rounded-xl p-3 border border-slate-200">
              <span class="text-xs text-slate-500">Maçons & Coffreurs</span>
              <div class="text-xl font-black text-[#1d4ed8]">18</div>
            </div>
            <div class="bg-slate-50 rounded-xl p-3 border border-slate-200">
              <span class="text-xs text-slate-500">Ferrailleurs</span>
              <div class="text-xl font-black text-slate-900">10</div>
            </div>
            <div class="bg-slate-50 rounded-xl p-3 border border-slate-200">
              <span class="text-xs text-slate-500">Électriciens / Plombiers</span>
              <div class="text-xl font-black text-slate-900">10</div>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <th class="pb-3 px-3">Équipe</th>
                  <th class="pb-3 px-3">Chef d'équipe</th>
                  <th class="pb-3 px-3">Effectif</th>
                  <th class="pb-3 px-3">Tâche du jour</th>
                  <th class="pb-3 px-3">Heures totales</th>
                  <th class="pb-3 px-3">Masse salariale / jour</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="team in teamsList" :key="team.name" class="hover:bg-slate-50">
                  <td class="py-3 px-3 font-semibold text-slate-900">{{ team.name }}</td>
                  <td class="py-3 px-3">{{ team.lead }}</td>
                  <td class="py-3 px-3 font-bold">{{ team.count }} ouvriers</td>
                  <td class="py-3 px-3 text-slate-500">{{ team.activity }}</td>
                  <td class="py-3 px-3">{{ team.hours }} h</td>
                  <td class="py-3 px-3 font-bold text-slate-900">{{ formatFcfa(team.cost) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ONGLET 7 : DÉPENSES DU CHANTIER -->
        <div v-if="currentTab === 'expenses'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Comptabilité Analytique & Engagements</h3>
              <p class="text-xs text-slate-500">Ventilation des coûts réels engagés sur le chantier</p>
            </div>
            <button
              @click="openAddExpenseModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="plus" />
              <span>Déclarer une dépense</span>
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <th class="pb-3 px-3">N° Pièce</th>
                  <th class="pb-3 px-3">Date</th>
                  <th class="pb-3 px-3">Poste de dépense</th>
                  <th class="pb-3 px-3">Bénéficiaire / Fournisseur</th>
                  <th class="pb-3 px-3">Montant FCFA</th>
                  <th class="pb-3 px-3">Moyen de paiement</th>
                  <th class="pb-3 px-3">Statut</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="exp in expensesList" :key="exp.id" class="hover:bg-slate-50">
                  <td class="py-3 px-3 font-mono font-bold text-slate-900">{{ exp.code }}</td>
                  <td class="py-3 px-3 text-slate-500">{{ exp.date }}</td>
                  <td class="py-3 px-3 font-semibold">{{ exp.category }}</td>
                  <td class="py-3 px-3">{{ exp.vendor }}</td>
                  <td class="py-3 px-3 font-bold text-[#1d4ed8]">{{ formatFcfa(exp.amount) }}</td>
                  <td class="py-3 px-3 text-slate-500">{{ exp.method }}</td>
                  <td class="py-3 px-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {{ exp.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ONGLET 8 : DOCUMENTS TECHNIQUES & PLANS -->
        <div v-if="currentTab === 'documents'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Gestion Documentaire & GED Chantier</h3>
              <p class="text-xs text-slate-500">Plans architecturaux, permis de construire, procès-verbaux et rapports SOCOTEC</p>
            </div>
            <button
              @click="uploadDocument"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="cloud-arrow-up" />
              <span>Téléverser un document</span>
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="doc in documentsList" :key="doc.id" class="border border-slate-200 rounded-xl p-4 bg-white hover:shadow-md transition-shadow">
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center text-lg flex-shrink-0">
                  <fas-icon icon="file-pdf" />
                </div>
                <div class="flex-1 overflow-hidden">
                  <h4 class="font-bold text-slate-900 text-xs truncate">{{ doc.title }}</h4>
                  <div class="text-[11px] text-slate-400 mt-0.5">{{ doc.category }} • {{ doc.size }}</div>
                  <div class="text-[10px] text-slate-500 mt-0.5">Modifié le {{ doc.updatedAt }}</div>
                </div>
              </div>
              <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100">
                <span class="text-[11px] text-slate-500 font-mono">{{ doc.version }}</span>
                <div class="flex items-center gap-1.5">
                  <button @click="viewDocument(doc)" class="px-2 py-1 rounded-lg text-xs font-semibold text-blue-700 hover:bg-blue-50">
                    Ouvrir
                  </button>
                  <button @click="downloadDoc(doc)" class="px-2 py-1 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100">
                    Télécharger
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ONGLET 9 : SITUATIONS DE TRAVAUX (FACTURATION CLIENT) -->
        <div v-if="currentTab === 'situations'" class="space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-bold text-slate-900">Situations de Travaux Mensuelles & Décomptes</h3>
              <p class="text-xs text-slate-500">États d'avancement financiers validés par la maîtrise d'œuvre et la mairie</p>
            </div>
            <button
              @click="openNewSituationModal"
              class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold flex items-center gap-1.5 self-start shadow-sm"
            >
              <fas-icon icon="plus" />
              <span>Créer Situation N°05</span>
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <th class="pb-3 px-3">Situation</th>
                  <th class="pb-3 px-3">Mois / Période</th>
                  <th class="pb-3 px-3">Avancement Cumulé</th>
                  <th class="pb-3 px-3">Montant Brut HT</th>
                  <th class="pb-3 px-3">Retenue Garantie (5%)</th>
                  <th class="pb-3 px-3">Net à Payer (FCFA)</th>
                  <th class="pb-3 px-3">Statut Paiement</th>
                  <th class="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="sit in situationsList" :key="sit.id" class="hover:bg-slate-50">
                  <td class="py-3 px-3 font-bold text-blue-700 font-mono">{{ sit.ref }}</td>
                  <td class="py-3 px-3">{{ sit.period }}</td>
                  <td class="py-3 px-3 font-bold">{{ sit.cumulativeProgress }}%</td>
                  <td class="py-3 px-3">{{ formatFcfa(sit.grossAmount) }}</td>
                  <td class="py-3 px-3 text-rose-600">-{{ formatFcfa(sit.guarantee) }}</td>
                  <td class="py-3 px-3 font-black text-slate-900">{{ formatFcfa(sit.netAmount) }}</td>
                  <td class="py-3 px-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold" :class="sit.paid ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'">
                      {{ sit.status }}
                    </span>
                  </td>
                  <td class="py-3 px-3 text-right">
                    <button @click="printSituation(sit)" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-900 hover:bg-slate-100" title="Imprimer Décompte">
                      <fas-icon icon="print" />
                    </button>
                    <button @click="downloadSituation(sit)" class="p-1.5 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-blue-50 ml-1" title="Télécharger PDF">
                      <fas-icon icon="download" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { chantierService } from '@/services'
import { alertSuccess, toast, confirmDialog } from '@/utils/alert'

const route = useRoute()
const router = useRouter()

// Données du chantier modélisé (avec fallback par défaut)
const chantier = ref({
  id: 1,
  reference: 'CH-2026-001',
  name: 'École primaire à Yopougon',
  location: 'Yopougon Andokoi, Abidjan (Côte d\'Ivoire)',
  client: 'Mairie de Yopougon / Ministère Éducation Nationale',
  manager: 'Konan Kouassi',
  status: 'En cours',
  progress: 68,
  budget: 250000000,
  expenses: 170000000,
  startDate: '15 Jan 2026',
  endDate: '30 Nov 2026',
})

onMounted(async () => {
  const chantierId = route.params.id
  if (chantierId) {
    try {
      const data = await chantierService.getChantier(chantierId)
      if (data) {
        chantier.value = {
          id: data.id,
          reference: data.code,
          name: data.name,
          location: `${data.city}${data.commune ? ', ' + data.commune : ''} (${data.country})`,
          client: data.client_name || (data.client ? data.client.name : 'Client non renseigné'),
          manager: data.project_manager ? data.project_manager.full_name : (data.site_manager ? data.site_manager.full_name : 'Non assigné'),
          status: data.status,
          progress: data.physical_progress || 0,
          budget: data.budget_estimated || data.contract_amount || 0,
          expenses: data.cost_estimated || 0,
          startDate: data.start_date_planned,
          endDate: data.end_date_planned,
        }
      }
    } catch (err) {
      // Fallback gracieux sur le chantier démo si non trouvé en BD
      console.log('Chantier démo chargé pour id:', chantierId)
    }
  }
})

// Définition des 9 onglets exigés par la charte
const tabs = [
  { id: 'general', name: 'Vue générale', icon: 'chart-pie' },
  { id: 'tasks', name: 'Tâches', icon: 'list-check', badge: '14' },
  { id: 'planning', name: 'Planning', icon: 'calendar-days' },
  { id: 'materials', name: 'Matériaux', icon: 'boxes-stacked', badge: '8' },
  { id: 'equipment', name: 'Équipements', icon: 'truck-pickup', badge: '4' },
  { id: 'workforce', name: 'Main-d\'œuvre', icon: 'users-gear', badge: '38' },
  { id: 'expenses', name: 'Dépenses', icon: 'wallet' },
  { id: 'documents', name: 'Documents', icon: 'file-contract', badge: '12' },
  { id: 'situations', name: 'Situations', icon: 'file-invoice-dollar', badge: '4' },
]

const currentTab = ref('general')

// Corps d'état
const corpsDetat = [
  { name: 'Terrassement & Fondations profondes', progress: 100, color: 'bg-emerald-500' },
  { name: 'Gros Œuvre & Maçonnerie R+1', progress: 92, color: 'bg-emerald-500' },
  { name: 'Charpente Métallique & Couverture', progress: 75, color: 'bg-[#1d4ed8]' },
  { name: 'Électricité & Câblage Réseau', progress: 45, color: 'bg-amber-500' },
  { name: 'Plomberie & Sanitaires autonomes', progress: 40, color: 'bg-amber-500' },
  { name: 'Revêtements carrelage & Peinture', progress: 15, color: 'bg-slate-300' },
]

// Tâches
const tasksList = ref([
  { id: 1, code: 'TSK-101', name: 'Coulage plancher haut niveau R+1', lot: 'Gros Œuvre', assignee: 'Équipe Maçonnerie 1', dueDate: '18 Mars 2026', progress: 100, status: 'Terminé' },
  { id: 2, code: 'TSK-102', name: 'Pose pannes et bac alu classe 4', lot: 'Charpente', assignee: 'Équipe Métallerie', dueDate: '25 Mars 2026', progress: 75, status: 'En cours' },
  { id: 3, code: 'TSK-103', name: 'Tirage de câbles cuivre bâtiment A', lot: 'Électricité', assignee: 'Koffi & Frères', dueDate: '02 Avril 2026', progress: 45, status: 'En cours' },
  { id: 4, code: 'TSK-104', name: 'Pose des dallettes fosse septique', lot: 'Plomberie', assignee: 'Sous-traitant SANIT', dueDate: '10 Avril 2026', progress: 30, status: 'En cours' },
  { id: 5, code: 'TSK-105', name: 'Application sous-couche hydrofuge', lot: 'Peinture', assignee: 'En attente affectation', dueDate: '20 Avril 2026', progress: 0, status: 'En attente' },
])

// Planning
const planningPhases = [
  { name: 'Phase 1 : Études géotechniques & Terrassement', dates: '15 Jan 2026 → 15 Fév 2026', progress: 100, completed: true, status: 'Validée' },
  { name: 'Phase 2 : Fondations spéciales & Gros œuvre', dates: '16 Fév 2026 → 20 Mars 2026', progress: 95, completed: false, status: 'En cours' },
  { name: 'Phase 3 : Toiture, menuiseries aluminium & étanchéité', dates: '21 Mars 2026 → 30 Mai 2026', progress: 35, completed: false, status: 'En cours' },
  { name: 'Phase 4 : Lots techniques (Élec, Plomb, VRD)', dates: '01 Juin 2026 → 31 Août 2026', progress: 10, completed: false, status: 'Programmé' },
  { name: 'Phase 5 : Finitions, clôture, peinture & OPR / Réception', dates: '01 Sept 2026 → 30 Nov 2026', progress: 0, completed: false, status: 'À venir' },
]

// Matériaux
const materialsList = [
  { id: 1, name: 'Ciment CPJ 42.5 (Sacs 50kg)', supplier: 'CIMAF Côte d\'Ivoire', qtyOrdered: 1200, qtyDelivered: 950, stockSite: 85, unit: 'Sacs', totalCost: 4750000 },
  { id: 2, name: 'Fer à béton haute adhérence HA12', supplier: 'SOTACI Abidjan', qtyOrdered: 35, qtyDelivered: 35, stockSite: 4, unit: 'Tonnes', totalCost: 19250000 },
  { id: 3, name: 'Gravier concassé 15/25', supplier: 'Carrière d\'Akoupé', qtyOrdered: 240, qtyDelivered: 180, stockSite: 35, unit: 'm³', totalCost: 3600000 },
  { id: 4, name: 'Sable de lagune lavé', supplier: 'Sables de Grand-Bassam', qtyOrdered: 300, qtyDelivered: 260, stockSite: 50, unit: 'm³', totalCost: 2340000 },
  { id: 5, name: 'Bacs alu thermo-laqués 75/100', supplier: 'Alu Ivoire Industrie', qtyOrdered: 450, qtyDelivered: 450, stockSite: 110, unit: 'm²', totalCost: 5850000 },
]

// Équipements
const equipmentList = [
  { id: 1, name: 'Pelle Hydraulique CAT 320', immat: 'ENG-2024-09', driver: 'Mamadou Touré', status: 'Opérationnel', hours: 412, dailyRate: 180000, icon: 'truck-pickup' },
  { id: 2, name: 'Bétonnière thermique tractée 500L', immat: 'BET-500-02', driver: 'Équipe Béton 1', status: 'Opérationnel', hours: 680, dailyRate: 35000, icon: 'gear' },
  { id: 3, name: 'Camion benne Mercedes 20m³', immat: 'CAM-6712-CI', driver: 'Seydou Diarra', status: 'Opérationnel', hours: 320, dailyRate: 120000, icon: 'truck' },
  { id: 4, name: 'Groupe Électrogène 45 kVA', immat: 'GRP-45-A', driver: 'Responsable Matériel', status: 'En révision', hours: 915, dailyRate: 40000, icon: 'bolt' },
]

// Main-d'œuvre
const teamsList = [
  { name: 'Équipe Maçonnerie & Coffrage', lead: 'Bakary Fofana', count: 18, activity: 'Élévation murs briques salle de classe 4', hours: 144, cost: 144000 },
  { name: 'Équipe Ferraillage & Armatures', lead: 'Jean-Marc N\'Dri', count: 10, activity: 'Préparation cage d\'armatures poutres toiture', hours: 80, cost: 80000 },
  { name: 'Équipe Électricité & Tirage', lead: 'Amadou Cissé', count: 6, activity: 'Passage fourreaux gaines ICTA dalles', hours: 48, cost: 60000 },
  { name: 'Manœuvres & Approvisionnement', lead: 'Yao Kouassi', count: 4, activity: 'Déchargement palettes ciment et nettoyage', hours: 32, cost: 24000 },
]

// Dépenses
const expensesList = [
  { id: 1, code: 'DEP-2026-312', date: '14 Mars 2026', category: 'Matériaux & Ciment', vendor: 'CIMAF Côte d\'Ivoire', amount: 4750000, method: 'Virement bancaire', status: 'Payée' },
  { id: 2, code: 'DEP-2026-308', date: '10 Mars 2026', category: 'Acompte Sous-traitance', vendor: 'Koffi Électricité SARL', amount: 3500000, method: 'Chèque certifié', status: 'Payée' },
  { id: 3, code: 'DEP-2026-299', date: '05 Mars 2026', category: 'Carburant engins chantier', vendor: 'Station Total Yopougon', amount: 850000, method: 'Carte carburant', status: 'Payée' },
  { id: 4, code: 'DEP-2026-285', date: '28 Fév 2026', category: 'Ferraillage & Acier HA', vendor: 'SOTACI Abidjan', amount: 19250000, method: 'Virement bancaire', status: 'Payée' },
]

// Documents
const documentsList = [
  { id: 1, title: 'Plan d\'exécution structure R+1 (Béton armé)', category: 'Plans techniques', size: '14.2 Mo', updatedAt: '02 Fév 2026', version: 'v2.4 Final' },
  { id: 2, title: 'Arrêté de Permis de Construire N°2025/112', category: 'Autorisations légales', size: '2.1 Mo', updatedAt: '12 Jan 2026', version: 'Validé' },
  { id: 3, title: 'Rapport de Contrôle Qualité Sols & Fondations', category: 'Bureau de Contrôle', size: '4.8 Mo', updatedAt: '18 Fév 2026', version: 'SOCOTEC CI' },
  { id: 4, title: 'PV de Réunion de Chantier N°08', category: 'Comptes-rendus', size: '1.4 Mo', updatedAt: '12 Mars 2026', version: 'Signé par tous' },
  { id: 5, title: 'Contrat d\'Assurance Tous Risques Chantier (TRC)', category: 'Assurances', size: '3.3 Mo', updatedAt: '10 Jan 2026', version: 'Police Active' },
]

// Situations de travaux
const situationsList = [
  { id: 1, ref: 'SIT-N°01', period: 'Janvier 2026', cumulativeProgress: 20, grossAmount: 50000000, guarantee: 2500000, netAmount: 47500000, paid: true, status: 'Payée par virement' },
  { id: 2, ref: 'SIT-N°02', period: 'Février 2026', cumulativeProgress: 40, grossAmount: 50000000, guarantee: 2500000, netAmount: 47500000, paid: true, status: 'Payée par virement' },
  { id: 3, ref: 'SIT-N°03', period: 'Mars 2026', cumulativeProgress: 55, grossAmount: 37500000, guarantee: 1875000, netAmount: 35625000, paid: true, status: 'Payée par virement' },
  { id: 4, ref: 'SIT-N°04', period: 'Avril 2026', cumulativeProgress: 68, grossAmount: 32500000, guarantee: 1625000, netAmount: 30875000, paid: false, status: 'En cours de validation Mairie' },
]

function formatFcfa(val) {
  if (val === undefined || val === null) return '0 FCFA'
  return new Intl.NumberFormat('fr-FR').format(val) + ' FCFA'
}

function getTaskStatusClass(status) {
  if (status === 'Terminé') return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
  if (status === 'En cours') return 'bg-blue-50 text-blue-700 border border-blue-200'
  return 'bg-amber-50 text-amber-700 border border-amber-200'
}

// Actions interactives avec SweetAlert2
function exportChantierPdf() {
  toast('Génération du rapport complet du chantier en cours...', 'info')
  setTimeout(() => {
    alertSuccess('Rapport Chantier Téléchargé', 'Le dossier technique au format PDF pour l\'École primaire à Yopougon est prêt.')
  }, 1000)
}

async function openNewSituationModal() {
  const confirmed = await confirmDialog(
    'Créer la Situation N°05 ?',
    'Voulez-vous générer le décompte financier provisoire N°05 basé sur un avancement prévisionnel de 75% ?',
    'Générer la situation'
  )
  if (confirmed) {
    alertSuccess('Situation N°05 Générée', 'Le projet de situation a été créé et soumis pour visa de la maîtrise d\'œuvre.')
  }
}

function openAddTaskModal() {
  router.push({ path: '/chantiers/taches', query: { chantier_id: chantier.value.id } })
}

async function openAddMaterialModal() {
  alertSuccess('Réception Fournisseur', 'Enregistrement du bon de livraison et rapprochement du bon de commande.')
}

async function openAddEquipmentModal() {
  alertSuccess('Affectation Engin', 'Mobilisation d\'un engin du parc ou location externe.')
}

async function openPointageModal() {
  toast('Feuille de pointage journalier enregistrée avec succès', 'success')
}

async function openAddExpenseModal() {
  alertSuccess('Déclaration de Dépense', 'Formulaire de saisie des factures et bons de commande analytiques.')
}

function uploadDocument() {
  toast('Zone de téléversement GED active', 'info')
}

function viewDocument(doc) {
  toast(`Ouverture du document : ${doc.title}`, 'info')
}

function downloadDoc(doc) {
  toast(`Téléchargement en cours : ${doc.title}`, 'success')
}

function printSituation(sit) {
  toast(`Impression de la ${sit.ref}`, 'info')
}

function downloadSituation(sit) {
  toast(`Téléchargement du décompte ${sit.ref} (PDF)`, 'success')
}

async function markTaskCompleted(task) {
  const ok = await confirmDialog('Clôturer la tâche ?', `Marquer la tâche "${task.name}" comme terminée à 100% ?`)
  if (ok) {
    task.progress = 100
    task.status = 'Terminé'
    toast('Tâche mise à jour avec succès', 'success')
  }
}

function editTask(task) {
  toast(`Édition de la tâche ${task.code}`, 'info')
}
</script>
