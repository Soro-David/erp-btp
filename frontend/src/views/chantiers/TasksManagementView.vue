<template>
  <div class="space-y-6">
    <!-- En-tête Page & Sélecteur de Chantier -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="list-check" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-black text-slate-900">Planification & Gestion des Tâches</h1>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-800">BTP Ops</span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Organisation par phases, ordonnancement des tâches, dépendances Fin → Début et jalons
          </p>
        </div>
      </div>

      <!-- Sélecteur de chantier actif -->
      <div class="flex items-center gap-3">
        <div class="text-right hidden sm:block">
          <span class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider">Chantier Actif</span>
          <span class="text-xs font-bold text-slate-700">{{ activeChantier?.name || 'Sélectionner un chantier' }}</span>
        </div>
        <select
          v-model="selectedChantierId"
          class="px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold text-slate-800 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all shadow-xs"
          @change="loadChantierPlanning"
        >
          <option v-for="c in chantiersList" :key="c.id" :value="c.id">
            {{ c.code }} - {{ c.name }}
          </option>
        </select>

        <button
          type="button"
          @click="recalculateProgress"
          class="px-3 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-xs flex items-center gap-1.5 transition-colors"
          title="Recalculer l'avancement physique global"
          :disabled="loading"
        >
          <fas-icon icon="arrows-rotate" :class="{ 'animate-spin': recalculating }" />
          <span class="hidden lg:inline">Recalculer</span>
        </button>
      </div>
    </div>

    <!-- KPI CARDS SUMMARY -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
      <!-- 1. Avancement Global -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Avancement Global</span>
          <fas-icon icon="gauge-high" class="text-blue-600" />
        </div>
        <div>
          <div class="text-2xl font-black text-slate-900 font-mono">
            {{ Math.round(planningData.physical_progress || 0) }}%
          </div>
          <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden mt-2">
            <div
              class="h-full bg-[#1d4ed8] rounded-full transition-all duration-500"
              :style="{ width: (planningData.physical_progress || 0) + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 2. Tâches Totales -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Total Tâches</span>
          <fas-icon icon="tasks" class="text-slate-600" />
        </div>
        <div>
          <div class="text-2xl font-black text-slate-900 font-mono">{{ planningData.total_tasks || 0 }}</div>
          <span class="text-[11px] text-slate-400">réparties en {{ planningData.total_phases || 0 }} phases</span>
        </div>
      </div>

      <!-- 3. Terminées -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Tâches Terminées</span>
          <fas-icon icon="circle-check" class="text-emerald-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-emerald-600 font-mono">{{ planningData.completed_tasks || 0 }}</div>
          <span class="text-[11px] text-emerald-600 font-semibold">
            {{ planningData.total_tasks ? Math.round((planningData.completed_tasks / planningData.total_tasks) * 100) : 0 }}% achevé
          </span>
        </div>
      </div>

      <!-- 4. Retards Détectés -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between" :class="{ 'border-rose-300 bg-rose-50/20': planningData.delayed_tasks > 0 }">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">En Retard</span>
          <fas-icon icon="clock" class="text-rose-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-rose-600 font-mono">{{ planningData.delayed_tasks || 0 }}</div>
          <span class="text-[11px] font-semibold" :class="planningData.delayed_tasks > 0 ? 'text-rose-600' : 'text-slate-400'">
            {{ planningData.delayed_tasks > 0 ? 'Actions correctives requises' : 'Aucun retard actif' }}
          </span>
        </div>
      </div>

      <!-- 5. Tâches Bloquées -->
      <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between" :class="{ 'border-amber-300 bg-amber-50/20': planningData.blocked_tasks > 0 }">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span class="font-bold text-slate-600">Tâches Bloquées</span>
          <fas-icon icon="triangle-exclamation" class="text-amber-500" />
        </div>
        <div>
          <div class="text-2xl font-black text-amber-600 font-mono">{{ planningData.blocked_tasks || 0 }}</div>
          <span class="text-[11px] font-semibold" :class="planningData.blocked_tasks > 0 ? 'text-amber-600' : 'text-slate-400'">
            {{ planningData.blocked_tasks > 0 ? 'Goulots signalés sur site' : 'Fluide' }}
          </span>
        </div>
      </div>
    </div>

    <!-- BARRE D'ACTIONS ET ONGLETS DE VISUALISATION -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-white p-3 rounded-2xl border border-slate-200 shadow-xs">
      <!-- Onglets -->
      <div class="flex items-center gap-1 overflow-x-auto pb-1 md:pb-0">
        <button
          type="button"
          @click="activeView = 'tree'"
          class="px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all whitespace-nowrap"
          :class="activeView === 'tree' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'"
        >
          <fas-icon icon="list" />
          <span>Tableau Hiérarchique</span>
        </button>

        <button
          type="button"
          @click="activeView = 'gantt'"
          class="px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all whitespace-nowrap"
          :class="activeView === 'gantt' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'"
        >
          <fas-icon icon="chart-gantt" />
          <span>Diagramme de Gantt</span>
        </button>

        <button
          type="button"
          @click="activeView = 'calendar'"
          class="px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all whitespace-nowrap"
          :class="activeView === 'calendar' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'"
        >
          <fas-icon icon="calendar-days" />
          <span>Calendrier</span>
        </button>

        <button
          type="button"
          @click="activeView = 'milestones'"
          class="px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all whitespace-nowrap"
          :class="activeView === 'milestones' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'"
        >
          <fas-icon icon="flag" />
          <span>Jalons Clés ({{ planningData.milestones ? planningData.milestones.length : 0 }})</span>
        </button>
      </div>

      <!-- Boutons d'ajout rapides -->
      <div class="flex items-center gap-2 flex-wrap">
        <button
          type="button"
          @click="openAddPhaseModal"
          class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold shadow-xs flex items-center gap-1.5 transition-colors"
        >
          <fas-icon icon="folder-plus" class="text-blue-600" />
          <span>Ajouter phase</span>
        </button>

        <button
          type="button"
          @click="openAddMilestoneModal"
          class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold shadow-xs flex items-center gap-1.5 transition-colors"
        >
          <fas-icon icon="flag" class="text-amber-500" />
          <span>Ajouter jalon</span>
        </button>

        <button
          type="button"
          @click="openAddTaskModal()"
          class="px-3.5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 transition-all"
        >
          <fas-icon icon="plus" />
          <span>Nouvelle tâche</span>
        </button>
      </div>
    </div>

    <!-- FILTRES RECHERCHE (Visible dans le tableau hiérarchique) -->
    <div v-if="activeView === 'tree'" class="flex flex-col sm:flex-row items-center gap-3 bg-white p-3 rounded-2xl border border-slate-200 shadow-xs">
      <div class="relative flex-1 w-full">
        <fas-icon icon="magnifying-glass" class="absolute left-3.5 top-3 text-slate-400 text-xs" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Rechercher par code, intitulé, responsable..."
          class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
        />
      </div>

      <div class="flex items-center gap-2 w-full sm:w-auto">
        <select
          v-model="filterStatus"
          class="px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 focus:outline-none focus:border-blue-600"
        >
          <option value="">Tous les statuts</option>
          <option value="À faire">À faire</option>
          <option value="En cours">En cours</option>
          <option value="En attente">En attente</option>
          <option value="Bloquée">Bloquée</option>
          <option value="Terminée">Terminée</option>
        </select>

        <select
          v-model="filterPriority"
          class="px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 focus:outline-none focus:border-blue-600"
        >
          <option value="">Toutes priorités</option>
          <option value="Faible">Faible</option>
          <option value="Normale">Normale</option>
          <option value="Importante">Importante</option>
          <option value="Critique">Critique</option>
        </select>
      </div>
    </div>

    <!-- CONTENU PRINCIPAL SELON ONGLET ACTIF -->
    <div>
      <!-- 1. VUE TABLEAU HIÉRARCHIQUE -->
      <div v-if="activeView === 'tree'" class="space-y-4">
        <div
          v-for="phase in filteredPhases"
          :key="phase.id"
          class="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden"
        >
          <!-- En-tête Phase dépliable -->
          <div
            class="px-4 py-3.5 bg-slate-50/80 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2 cursor-pointer hover:bg-slate-100/70 transition-colors"
            @click="togglePhaseCollapse(phase.id)"
          >
            <div class="flex items-center gap-3">
              <button type="button" class="text-slate-400 hover:text-slate-700 p-1">
                <fas-icon :icon="isPhaseCollapsed(phase.id) ? 'chevron-right' : 'chevron-down'" />
              </button>
              <div class="w-8 h-8 rounded-lg bg-blue-100 text-[#1d4ed8] flex items-center justify-center font-bold text-xs">
                <fas-icon icon="folder-open" />
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span class="font-mono text-xs font-bold text-slate-500">{{ phase.code }}</span>
                  <h3 class="text-sm font-bold text-slate-900">{{ phase.name }}</h3>
                </div>
                <p class="text-[11px] text-slate-400">
                  Responsable : {{ phase.responsible?.first_name ? `${phase.responsible.first_name} ${phase.responsible.last_name}` : 'Non assigné' }}
                </p>
              </div>
            </div>

            <!-- Avancement phase & actions -->
            <div class="flex items-center gap-4 self-end sm:self-center">
              <div class="flex items-center gap-2 w-32">
                <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                  <div class="bg-[#1d4ed8] h-full rounded-full" :style="{ width: phase.progress + '%' }"></div>
                </div>
                <span class="text-xs font-mono font-bold text-slate-700">{{ Math.round(phase.progress) }}%</span>
              </div>

              <button
                type="button"
                @click.stop="openAddTaskModal(phase.id)"
                class="px-2.5 py-1 rounded-lg bg-white border border-slate-200 hover:bg-blue-50 hover:text-[#1d4ed8] text-slate-700 text-xs font-semibold flex items-center gap-1 shadow-2xs"
                title="Ajouter une tâche dans cette phase"
              >
                <fas-icon icon="plus" class="text-[10px]" />
                <span class="hidden sm:inline">Tâche</span>
              </button>
            </div>
          </div>

          <!-- Liste des tâches de cette phase -->
          <div v-show="!isPhaseCollapsed(phase.id)">
            <div v-if="getTasksForPhase(phase.id).length > 0" class="overflow-x-auto">
              <table class="w-full text-left text-xs whitespace-nowrap">
                <thead>
                  <tr class="bg-slate-50 text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100">
                    <th class="py-2.5 px-4">Code / Intitulé</th>
                    <th class="py-2.5 px-3">Responsable</th>
                    <th class="py-2.5 px-3">Priorité</th>
                    <th class="py-2.5 px-3">Statut</th>
                    <th class="py-2.5 px-3">Dates prévues</th>
                    <th class="py-2.5 px-3">Avancement</th>
                    <th class="py-2.5 px-3">Retard</th>
                    <th class="py-2.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <template v-for="task in getTasksForPhase(phase.id)" :key="task.id">
                    <!-- Tâche mère -->
                    <tr class="hover:bg-slate-50/70 transition-colors cursor-pointer group" @click="openTaskDetail(task)">
                      <td class="py-2.5 px-4">
                        <div class="flex items-center gap-2">
                          <span class="font-mono text-xs font-bold text-slate-500">{{ task.code }}</span>
                          <span class="font-semibold text-slate-900">{{ task.name }}</span>
                          <span v-if="task.subtasks && task.subtasks.length > 0" class="px-1.5 py-0.2 rounded text-[10px] bg-slate-100 text-slate-600 font-bold">
                            {{ task.subtasks.length }} sous-tâches
                          </span>
                        </div>
                      </td>
                      <td class="py-2.5 px-3 text-slate-600">
                        {{ task.responsible_name || '-' }}
                      </td>
                      <td class="py-2.5 px-3">
                        <span
                          class="px-2 py-0.5 rounded text-[10px] font-bold"
                          :class="{
                            'bg-slate-100 text-slate-600': task.priority === 'Faible',
                            'bg-blue-100 text-blue-700': task.priority === 'Normale',
                            'bg-amber-100 text-amber-800': task.priority === 'Importante',
                            'bg-rose-100 text-rose-800': task.priority === 'Critique',
                          }"
                        >
                          {{ task.priority }}
                        </span>
                      </td>
                      <td class="py-2.5 px-3">
                        <span
                          class="px-2 py-0.5 rounded text-[10px] font-bold"
                          :class="{
                            'bg-emerald-100 text-emerald-800': task.status === 'Terminée',
                            'bg-blue-100 text-blue-800': task.status === 'En cours',
                            'bg-amber-100 text-amber-800': task.status === 'En attente' || task.status === 'À faire',
                            'bg-rose-100 text-rose-800': task.status === 'Bloquée',
                            'bg-slate-100 text-slate-600': task.status === 'Annulée',
                          }"
                        >
                          {{ task.status }}
                        </span>
                      </td>
                      <td class="py-2.5 px-3 text-slate-600 font-mono text-[11px]">
                        {{ formatDate(task.planned_start_date) }} → {{ formatDate(task.planned_end_date) }}
                      </td>
                      <td class="py-2.5 px-3">
                        <div class="flex items-center gap-2 w-24">
                          <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                            <div
                              class="h-full rounded-full"
                              :class="task.progress >= 100 ? 'bg-emerald-500' : 'bg-[#1d4ed8]'"
                              :style="{ width: task.progress + '%' }"
                            ></div>
                          </div>
                          <span class="text-xs font-mono font-bold text-slate-700">{{ Math.round(task.progress) }}%</span>
                        </div>
                      </td>
                      <td class="py-2.5 px-3">
                        <span v-if="task.delay_days > 0" class="text-rose-600 font-bold flex items-center gap-1 text-[11px]">
                          <fas-icon icon="triangle-exclamation" />
                          +{{ task.delay_days }} j
                        </span>
                        <span v-else class="text-slate-400 text-[11px]">-</span>
                      </td>
                      <td class="py-2.5 px-4 text-right">
                        <div class="flex items-center justify-end gap-1.5" @click.stop>
                          <button
                            type="button"
                            @click="openAddSubtaskModal(task)"
                            class="p-1 rounded text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                            title="Ajouter une sous-tâche"
                          >
                            <fas-icon icon="turn-down" class="rotate-90 text-xs" />
                          </button>
                          <button
                            type="button"
                            @click="openTaskDetail(task)"
                            class="p-1 rounded text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                            title="Détails / Éditer"
                          >
                            <fas-icon icon="pen-to-square" class="text-xs" />
                          </button>
                        </div>
                      </td>
                    </tr>

                    <!-- Sous-tâches imbriquées -->
                    <template v-if="task.subtasks && task.subtasks.length > 0">
                      <tr
                        v-for="sub in task.subtasks"
                        :key="'sub-' + sub.id"
                        class="bg-slate-50/40 hover:bg-blue-50/30 transition-colors cursor-pointer text-slate-700"
                        @click="openTaskDetail(sub)"
                      >
                        <td class="py-2 px-4 pl-10">
                          <div class="flex items-center gap-2">
                            <fas-icon icon="turn-down" class="text-slate-300 text-[10px] rotate-90" />
                            <span class="font-mono text-[11px] text-slate-400">{{ sub.code }}</span>
                            <span class="font-medium text-slate-800 text-xs">{{ sub.name }}</span>
                          </div>
                        </td>
                        <td class="py-2 px-3 text-slate-500 text-[11px]">{{ sub.responsible_name || '-' }}</td>
                        <td class="py-2 px-3">
                          <span class="text-[10px] font-semibold text-slate-600">{{ sub.priority }}</span>
                        </td>
                        <td class="py-2 px-3">
                          <span
                            class="px-1.5 py-0.2 rounded text-[10px] font-bold"
                            :class="sub.status === 'Terminée' ? 'bg-emerald-50 text-emerald-700' : 'bg-blue-50 text-blue-700'"
                          >
                            {{ sub.status }}
                          </span>
                        </td>
                        <td class="py-2 px-3 font-mono text-[10px] text-slate-500">
                          {{ formatDate(sub.planned_start_date) }} → {{ formatDate(sub.planned_end_date) }}
                        </td>
                        <td class="py-2 px-3">
                          <div class="flex items-center gap-1.5 w-20">
                            <div class="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                              <div
                                class="h-full rounded-full"
                                :class="sub.progress >= 100 ? 'bg-emerald-500' : 'bg-[#1d4ed8]'"
                                :style="{ width: sub.progress + '%' }"
                              ></div>
                            </div>
                            <span class="text-[10px] font-mono text-slate-600">{{ Math.round(sub.progress) }}%</span>
                          </div>
                        </td>
                        <td class="py-2 px-3 text-[10px]">
                          <span v-if="sub.delay_days > 0" class="text-rose-600 font-bold">+{{ sub.delay_days }} j</span>
                          <span v-else class="text-slate-400">-</span>
                        </td>
                        <td class="py-2 px-4 text-right">
                          <button
                            type="button"
                            @click.stop="openTaskDetail(sub)"
                            class="p-1 text-slate-400 hover:text-blue-600"
                          >
                            <fas-icon icon="pen-to-square" class="text-xs" />
                          </button>
                        </td>
                      </tr>
                    </template>
                  </template>
                </tbody>
              </table>
            </div>
            <div v-else class="py-8 text-center text-slate-400 text-xs italic">
              Aucune tâche créée dans cette phase.
              <button
                type="button"
                @click="openAddTaskModal(phase.id)"
                class="text-[#1d4ed8] font-bold hover:underline ml-1"
              >
                Créer la première tâche
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. VUE DIAGRAMME DE GANTT -->
      <div v-else-if="activeView === 'gantt'">
        <GanttChart
          :phases="planningData.phases || []"
          :tasks-tree="planningData.tasks_tree || []"
          :milestones="planningData.milestones || []"
          @select-task="openTaskDetail"
          @select-milestone="handleMilestoneClick"
        />
      </div>

      <!-- 3. VUE CALENDRIER -->
      <div v-else-if="activeView === 'calendar'">
        <CalendarView
          :tasks="allFlatTasks"
          :milestones="planningData.milestones || []"
          @select-task="openTaskDetail"
          @select-milestone="handleMilestoneClick"
        />
      </div>

      <!-- 4. VUE JALONS CONTRACTUELS -->
      <div v-else-if="activeView === 'milestones'" class="space-y-4">
        <div class="flex items-center justify-between bg-white p-4 rounded-2xl border border-slate-200">
          <div>
            <h3 class="text-sm font-bold text-slate-900">Jalons Stratégiques & Contractuels</h3>
            <p class="text-xs text-slate-500">Points de contrôle majeurs validant le respect des engagements contractuels</p>
          </div>
          <button
            type="button"
            @click="openAddMilestoneModal"
            class="px-3 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5"
          >
            <fas-icon icon="flag" />
            <span>Nouveau Jalon</span>
          </button>
        </div>

        <div v-if="planningData.milestones && planningData.milestones.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="m in planningData.milestones"
            :key="m.id"
            class="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs hover:border-amber-400 transition-all space-y-3"
          >
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200">
                {{ m.code }}
              </span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold"
                :class="{
                  'bg-emerald-100 text-emerald-800': m.status === 'Atteint',
                  'bg-amber-100 text-amber-800': m.status === 'À venir',
                  'bg-rose-100 text-rose-800': m.status === 'En retard',
                }"
              >
                {{ m.status }}
              </span>
            </div>

            <div>
              <h4 class="font-bold text-slate-900 text-sm">{{ m.name }}</h4>
              <p class="text-xs text-slate-500 mt-1 line-clamp-2">{{ m.description || 'Aucune description' }}</p>
            </div>

            <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
              <div class="flex items-center gap-1.5">
                <fas-icon icon="calendar" class="text-slate-400 text-xs" />
                <span>{{ formatDate(m.planned_date) }}</span>
              </div>
              <div v-if="m.responsible_name" class="text-slate-500 font-medium">
                {{ m.responsible_name }}
              </div>
            </div>
          </div>
        </div>
        <div v-else class="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400 text-xs">
          Aucun jalon défini pour ce chantier.
        </div>
      </div>
    </div>

    <!-- MODALS ATTACHÉES -->
    <AddTaskModal
      v-model="showAddTaskModal"
      :chantier-id="selectedChantierId"
      :phases="planningData.phases || []"
      :tasks="allFlatTasks"
      :responsables="responsablesList"
      :default-phase-id="modalDefaultPhaseId"
      :default-parent-task-id="modalDefaultParentTaskId"
      @created="onTaskCreated"
      @request-add-phase="openAddPhaseModal"
      @request-add-responsable="openAddResponsableModal"
    />

    <AddPhaseModal
      v-model="showAddPhaseModal"
      :chantier-id="selectedChantierId"
      :responsables="responsablesList"
      @created="onPhaseCreated"
      @request-add-responsable="openAddResponsableModal"
    />

    <AddMilestoneModal
      v-model="showAddMilestoneModal"
      :chantier-id="selectedChantierId"
      :responsables="responsablesList"
      @created="onMilestoneCreated"
    />

    <TaskDetailModal
      v-model="showTaskDetailModal"
      :task="selectedTask"
      :responsables="responsablesList"
      @updated="onTaskUpdated"
      @deleted="onTaskDeleted"
      @request-add-subtask="openAddSubtaskFromDetail"
    />

    <AddResponsableModal
      v-model="showAddResponsableModal"
      @created="onResponsableCreated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { chantierService, taskService } from '@/services'
import { toast } from '@/utils/alert'

import GanttChart from './components/GanttChart.vue'
import CalendarView from './components/CalendarView.vue'
import AddTaskModal from './components/AddTaskModal.vue'
import AddPhaseModal from './components/AddPhaseModal.vue'
import AddMilestoneModal from './components/AddMilestoneModal.vue'
import TaskDetailModal from './components/TaskDetailModal.vue'
import AddResponsableModal from './components/AddResponsableModal.vue'

const route = useRoute()

// États principaux
const chantiersList = ref([])
const selectedChantierId = ref(null)
const activeView = ref('tree') // 'tree', 'gantt', 'calendar', 'milestones'
const loading = ref(false)
const recalculating = ref(false)

const planningData = reactive({
  chantier_id: null,
  chantier_code: '',
  chantier_name: '',
  physical_progress: 0,
  total_phases: 0,
  total_tasks: 0,
  completed_tasks: 0,
  delayed_tasks: 0,
  blocked_tasks: 0,
  phases: [],
  tasks_tree: [],
  milestones: [],
})

const responsablesList = ref([])
const collapsedPhases = ref({})

// Filtres
const searchQuery = ref('')
const filterStatus = ref('')
const filterPriority = ref('')

// États des Modals
const showAddTaskModal = ref(false)
const showAddPhaseModal = ref(false)
const showAddMilestoneModal = ref(false)
const showTaskDetailModal = ref(false)
const showAddResponsableModal = ref(false)

const modalDefaultPhaseId = ref(null)
const modalDefaultParentTaskId = ref(null)
const selectedTask = ref(null)

const activeChantier = computed(() => {
  return chantiersList.value.find((c) => c.id === selectedChantierId.value)
})

// Liste plate de toutes les tâches pour les filtres et dépendances
const allFlatTasks = computed(() => {
  const result = []
  function flatten(tasks) {
    tasks.forEach((t) => {
      result.push(t)
      if (t.subtasks && t.subtasks.length > 0) {
        flatten(t.subtasks)
      }
    })
  }
  flatten(planningData.tasks_tree || [])
  return result
})

// Phases filtrées
const filteredPhases = computed(() => {
  return planningData.phases || []
})

function getTasksForPhase(phaseId) {
  let list = (planningData.tasks_tree || []).filter((t) => t.phase_id === phaseId)

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter((t) =>
      t.name.toLowerCase().includes(q) ||
      t.code.toLowerCase().includes(q) ||
      (t.responsible_name && t.responsible_name.toLowerCase().includes(q))
    )
  }

  if (filterStatus.value) {
    list = list.filter((t) => t.status === filterStatus.value)
  }

  if (filterPriority.value) {
    list = list.filter((t) => t.priority === filterPriority.value)
  }

  return list
}

function isPhaseCollapsed(phaseId) {
  return !!collapsedPhases.value[phaseId]
}

function togglePhaseCollapse(phaseId) {
  collapsedPhases.value[phaseId] = !collapsedPhases.value[phaseId]
}

// Chargement des données
async function loadChantiers() {
  try {
    const data = await chantierService.getChantiers()
    const list = data.items || data || []
    chantiersList.value = list

    if (list.length > 0) {
      const paramId = route.query.chantier_id
      if (paramId && list.some((c) => c.id === Number(paramId))) {
        selectedChantierId.value = Number(paramId)
      } else {
        selectedChantierId.value = list[0].id
      }
      await loadChantierPlanning()
    }
  } catch (err) {
    toast('Erreur lors du chargement des chantiers', 'error')
  }
}

async function loadResponsables() {
  try {
    responsablesList.value = await chantierService.getResponsables()
  } catch (err) {
    console.error(err)
  }
}

async function loadChantierPlanning() {
  if (!selectedChantierId.value) return
  loading.value = true
  try {
    const plan = await taskService.getPlanning(selectedChantierId.value)
    Object.assign(planningData, plan)
  } catch (err) {
    toast('Erreur lors du chargement du planning', 'error')
  } finally {
    loading.value = false
  }
}

async function recalculateProgress() {
  if (!selectedChantierId.value) return
  recalculating.value = true
  try {
    const res = await taskService.recalculatePlanning(selectedChantierId.value)
    planningData.physical_progress = res.physical_progress
    toast(`Avancement global actualisé : ${res.physical_progress}%`, 'success')
    await loadChantierPlanning()
  } catch (err) {
    toast('Erreur lors du recalcul de la progression', 'error')
  } finally {
    recalculating.value = false
  }
}

// Handlers Modals
function openAddTaskModal(phaseId = null) {
  modalDefaultPhaseId.value = phaseId
  modalDefaultParentTaskId.value = null
  showAddTaskModal.value = true
}

function openAddSubtaskModal(parentTask) {
  modalDefaultPhaseId.value = parentTask.phase_id
  modalDefaultParentTaskId.value = parentTask.id
  showAddTaskModal.value = true
}

function openAddSubtaskFromDetail(parentTask) {
  showTaskDetailModal.value = false
  openAddSubtaskModal(parentTask)
}

function openAddPhaseModal() {
  showAddPhaseModal.value = true
}

function openAddMilestoneModal() {
  showAddMilestoneModal.value = true
}

function openAddResponsableModal() {
  showAddResponsableModal.value = true
}

function openTaskDetail(task) {
  selectedTask.value = task
  showTaskDetailModal.value = true
}

function handleMilestoneClick(milestone) {
  activeView.value = 'milestones'
}

function onTaskCreated() {
  loadChantierPlanning()
}

function onTaskUpdated() {
  loadChantierPlanning()
}

function onTaskDeleted() {
  loadChantierPlanning()
}

function onPhaseCreated() {
  loadChantierPlanning()
}

function onMilestoneCreated() {
  loadChantierPlanning()
}

async function onResponsableCreated() {
  await loadResponsables()
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
  })
}

onMounted(async () => {
  await loadResponsables()
  await loadChantiers()
})
</script>
