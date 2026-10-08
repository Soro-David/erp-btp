<template>
  <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
    <!-- Barre de Contrôles & Filtres Gantt -->
    <div class="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/60">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-base">
          <fas-icon icon="chart-gantt" />
        </div>
        <div>
          <h3 class="text-sm font-bold text-slate-900">Diagramme de Gantt Opérationnel</h3>
          <p class="text-xs text-slate-500">Planification dynamique, chemins critiques et jalons</p>
        </div>
      </div>

      <!-- Sélecteur de Zoom & Actions -->
      <div class="flex items-center gap-2 flex-wrap">
        <div class="flex items-center bg-white border border-slate-200 rounded-xl p-0.5 shadow-xs">
          <button
            type="button"
            @click="setZoom('day')"
            class="px-2.5 py-1 rounded-lg text-xs font-bold transition-colors"
            :class="zoomLevel === 'day' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-50'"
          >
            Jour
          </button>
          <button
            type="button"
            @click="setZoom('week')"
            class="px-2.5 py-1 rounded-lg text-xs font-bold transition-colors"
            :class="zoomLevel === 'week' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-50'"
          >
            Semaine
          </button>
          <button
            type="button"
            @click="setZoom('month')"
            class="px-2.5 py-1 rounded-lg text-xs font-bold transition-colors"
            :class="zoomLevel === 'month' ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-50'"
          >
            Mois
          </button>
        </div>

        <button
          type="button"
          @click="scrollToToday"
          class="px-3 py-1.5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-xs flex items-center gap-1.5"
          title="Centrer la vue sur aujourd'hui"
        >
          <fas-icon icon="crosshairs" class="text-blue-600" />
          <span>Aujourd'hui</span>
        </button>

        <button
          type="button"
          @click="toggleDependencies"
          class="px-3 py-1.5 rounded-xl border text-xs font-bold shadow-xs flex items-center gap-1.5 transition-colors"
          :class="showDependencies ? 'bg-blue-50 border-blue-200 text-[#1d4ed8]' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'"
        >
          <fas-icon icon="network-wired" />
          <span>Liaisons</span>
        </button>
      </div>
    </div>

    <!-- Légende Rapide -->
    <div class="px-4 py-2 border-b border-slate-100 bg-white flex items-center gap-4 flex-wrap text-[11px] text-slate-600">
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded bg-emerald-500 inline-block"></span>
        <span>Terminée</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded bg-[#1d4ed8] inline-block"></span>
        <span>En cours</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded bg-rose-500 inline-block"></span>
        <span>Bloquée / Retard</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded bg-slate-400 inline-block"></span>
        <span>À faire / En attente</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 bg-amber-500 rotate-45 inline-block"></span>
        <span>Jalon contractuel</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-0.5 bg-rose-500 border-t-2 border-dashed border-rose-500 inline-block"></span>
        <span>Ligne Aujourd'hui</span>
      </div>
    </div>

    <!-- Zone Principale Gantt Split (Colonnes fixes + Timeline Scrollable) -->
    <div class="flex flex-1 overflow-hidden min-h-[500px]">
      <!-- COLONNE GAUCHE : ARBRE DES PHASES ET TÂCHES (Fixe) -->
      <div class="w-72 sm:w-80 border-r border-slate-200 flex flex-col flex-shrink-0 bg-white select-none">
        <!-- En-tête gauche -->
        <div class="h-14 px-4 bg-slate-100/70 border-b border-slate-200 flex items-center justify-between text-xs font-bold text-slate-700">
          <span>Tâches & Phases</span>
          <span>Avancement</span>
        </div>

        <!-- Lignes gauche synchronisées -->
        <div class="overflow-y-auto divide-y divide-slate-100 flex-1" ref="leftPaneRef" @scroll="syncScrollY">
          <div
            v-for="(row, idx) in flatRows"
            :key="idx"
            class="h-10 px-3 flex items-center justify-between text-xs transition-colors hover:bg-slate-50 cursor-pointer"
            :class="{
              'bg-slate-100/60 font-bold text-slate-900': row.type === 'phase',
              'font-semibold text-amber-900 bg-amber-50/40': row.type === 'milestone',
              'hover:bg-blue-50/50': row.type === 'task' || row.type === 'subtask',
            }"
            @click="handleRowClick(row)"
          >
            <div class="flex items-center gap-1.5 min-w-0" :style="{ paddingLeft: (row.level * 16) + 'px' }">
              <fas-icon
                v-if="row.type === 'phase'"
                icon="folder"
                class="text-blue-600 text-xs flex-shrink-0"
              />
              <span
                v-else-if="row.type === 'milestone'"
                class="w-2.5 h-2.5 bg-amber-500 rotate-45 flex-shrink-0"
              ></span>
              <fas-icon
                v-else-if="row.type === 'subtask'"
                icon="turn-down"
                class="text-slate-400 text-[10px] rotate-90 flex-shrink-0"
              />
              <span
                v-else
                class="w-2 h-2 rounded-full flex-shrink-0"
                :class="row.data.status === 'Terminée' ? 'bg-emerald-500' : (row.data.is_blocked || row.data.delay_days > 0 ? 'bg-rose-500' : 'bg-blue-600')"
              ></span>

              <span class="truncate font-medium text-slate-800" :title="row.title">
                {{ row.title }}
              </span>
            </div>

            <div class="flex items-center gap-1 flex-shrink-0 ml-2">
              <span
                v-if="row.type === 'task' || row.type === 'subtask' || row.type === 'phase'"
                class="font-mono text-[11px] font-bold text-slate-600"
              >
                {{ Math.round(row.data.progress || 0) }}%
              </span>
              <span
                v-else-if="row.type === 'milestone'"
                class="text-[10px] px-1.5 py-0.5 rounded font-bold"
                :class="row.data.status === 'Atteint' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-800'"
              >
                {{ row.data.status }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- COLONNE DROITE : TIMELINE HORIZONTALE INTERACTIVE -->
      <div
        class="flex-1 overflow-x-auto overflow-y-auto relative bg-slate-50/30"
        ref="timelineContainerRef"
        @scroll="syncScrollX"
      >
        <div :style="{ width: totalTimelineWidth + 'px' }" class="relative min-h-full">
          <!-- EN-TÊTE TEMPORELLE (Sticky top) -->
          <div class="sticky top-0 z-20 bg-white border-b border-slate-200 select-none shadow-xs h-14 flex flex-col">
            <!-- Ligne des Mois -->
            <div class="h-7 flex border-b border-slate-100 text-xs font-bold text-slate-700 bg-slate-50">
              <div
                v-for="(m, mIdx) in monthHeaders"
                :key="mIdx"
                class="border-r border-slate-200 px-2 flex items-center justify-center truncate uppercase tracking-wider text-[11px]"
                :style="{ width: m.width + 'px' }"
              >
                {{ m.label }}
              </div>
            </div>

            <!-- Ligne des Unités (Jours ou Semaines) -->
            <div class="h-7 flex text-[10px] font-medium text-slate-500">
              <div
                v-for="(col, cIdx) in timeColumns"
                :key="cIdx"
                class="border-r border-slate-100 flex items-center justify-center font-mono flex-shrink-0"
                :class="{
                  'bg-blue-50/50 font-bold text-[#1d4ed8]': col.isToday,
                  'bg-slate-100/40 text-slate-400': col.isWeekend,
                }"
                :style="{ width: columnWidth + 'px' }"
              >
                {{ col.label }}
              </div>
            </div>
          </div>

          <!-- GRILLE DES COLONNES (Fond) -->
          <div class="absolute inset-0 top-14 pointer-events-none flex z-0">
            <div
              v-for="(col, cIdx) in timeColumns"
              :key="cIdx"
              class="border-r border-slate-100/80 h-full flex-shrink-0"
              :class="{
                'bg-blue-50/20': col.isToday,
                'bg-slate-100/20': col.isWeekend,
              }"
              :style="{ width: columnWidth + 'px' }"
            ></div>
          </div>

          <!-- LIGNE AUJOURD'HUI VERTICALE -->
          <div
            v-if="todayXPosition >= 0"
            class="absolute top-0 bottom-0 z-10 pointer-events-none"
            :style="{ left: todayXPosition + 'px' }"
          >
            <div class="w-0.5 h-full bg-rose-500 border-l border-dashed border-rose-500 relative">
              <div class="sticky top-14 -left-12 px-1.5 py-0.5 rounded bg-rose-600 text-white font-bold text-[9px] shadow-sm whitespace-nowrap">
                Aujourd'hui
              </div>
            </div>
          </div>

          <!-- BARRES GANTT & REPRÉSENTATION GRAPHIQUE -->
          <div class="relative z-10 pt-0">
            <!-- LIAISONS SVG ENTRE TÂCHES -->
            <svg
              v-if="showDependencies"
              class="absolute inset-0 pointer-events-none z-10"
              :width="totalTimelineWidth"
              :height="flatRows.length * 40"
            >
              <defs>
                <marker
                  id="gantt-arrow"
                  viewBox="0 0 10 10"
                  refX="6"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#3b82f6" />
                </marker>
              </defs>
              <path
                v-for="(dep, dIdx) in svgDependencyCurves"
                :key="dIdx"
                :d="dep.path"
                stroke="#3b82f6"
                stroke-width="1.8"
                fill="none"
                stroke-dasharray="3,3"
                marker-end="url(#gantt-arrow)"
              />
            </svg>

            <!-- LIGNES ET BARRES INDIVIDUELLES -->
            <div
              v-for="(row, idx) in flatRows"
              :key="idx"
              class="h-10 relative flex items-center border-b border-slate-100/60 hover:bg-blue-50/20 transition-colors"
            >
              <!-- 1. BARRE DE PHASE -->
              <div
                v-if="row.type === 'phase' && row.bar"
                class="absolute h-6 rounded-md bg-[#0f294a] text-white flex items-center px-2 shadow-xs text-[10px] font-bold overflow-hidden cursor-pointer hover:opacity-90"
                :style="{ left: row.bar.left + 'px', width: row.bar.width + 'px' }"
                :title="row.title + ' (' + row.bar.startDate + ' au ' + row.bar.endDate + ')'"
              >
                <!-- Avancement phase interne -->
                <div
                  class="absolute left-0 top-0 bottom-0 bg-blue-500/40"
                  :style="{ width: (row.data.progress || 0) + '%' }"
                ></div>
                <span class="relative z-10 truncate">{{ row.title }} ({{ Math.round(row.data.progress) }}%)</span>
              </div>

              <!-- 2. JALON DIAMANT -->
              <div
                v-else-if="row.type === 'milestone' && row.bar"
                class="absolute flex items-center gap-2 cursor-pointer group"
                :style="{ left: row.bar.left + 'px' }"
                :title="row.title + ' - Prévu le ' + row.bar.date"
              >
                <div
                  class="w-5 h-5 rotate-45 border-2 border-white shadow-md flex items-center justify-center transition-transform group-hover:scale-125"
                  :class="row.data.status === 'Atteint' ? 'bg-emerald-500' : 'bg-amber-500'"
                ></div>
                <span class="text-[11px] font-bold text-slate-800 whitespace-nowrap bg-white/90 px-1.5 py-0.5 rounded shadow-xs border border-slate-100">
                  {{ row.title }}
                </span>
              </div>

              <!-- 3. BARRE DE TÂCHE / SOUS-TÂCHE -->
              <div
                v-else-if="(row.type === 'task' || row.type === 'subtask') && row.bar"
                class="absolute h-7 rounded-lg shadow-sm flex items-center px-2 cursor-pointer transition-all hover:ring-2 hover:ring-blue-400 group overflow-hidden select-none"
                :class="getTaskBarClass(row.data)"
                :style="{ left: row.bar.left + 'px', width: row.bar.width + 'px' }"
                @click.stop="handleRowClick(row)"
              >
                <!-- Remplissage interne d'avancement -->
                <div
                  class="absolute left-0 top-0 bottom-0 bg-white/20"
                  :style="{ width: (row.data.progress || 0) + '%' }"
                ></div>

                <!-- Contenu de la barre -->
                <div class="relative z-10 flex items-center justify-between w-full text-white text-[10px] font-bold overflow-hidden">
                  <span class="truncate mr-1">{{ row.title }}</span>
                  <span class="font-mono flex-shrink-0">{{ Math.round(row.data.progress) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'

const props = defineProps({
  phases: {
    type: Array,
    default: () => [],
  },
  tasksTree: {
    type: Array,
    default: () => [],
  },
  milestones: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['selectTask', 'selectMilestone', 'selectPhase'])

const zoomLevel = ref('week') // 'day', 'week', 'month'
const showDependencies = ref(true)

const leftPaneRef = ref(null)
const timelineContainerRef = ref(null)

// Paramètres de mise à l'échelle
const columnWidth = computed(() => {
  if (zoomLevel.value === 'day') return 36
  if (zoomLevel.value === 'week') return 120
  return 160 // month
})

function setZoom(lvl) {
  zoomLevel.value = lvl
}

function toggleDependencies() {
  showDependencies.value = !showDependencies.value
}

// 1. Calcul des bornes temporelles globales
const timelineBounds = computed(() => {
  const dates = []

  // Collecter dates des phases
  props.phases.forEach((p) => {
    if (p.start_date_planned) dates.push(new Date(p.start_date_planned).getTime())
    if (p.end_date_planned) dates.push(new Date(p.end_date_planned).getTime())
  })

  // Collecter dates des tâches
  function collectTaskDates(tasks) {
    tasks.forEach((t) => {
      if (t.planned_start_date) dates.push(new Date(t.planned_start_date).getTime())
      if (t.planned_end_date) dates.push(new Date(t.planned_end_date).getTime())
      if (t.subtasks && t.subtasks.length > 0) {
        collectTaskDates(t.subtasks)
      }
    })
  }
  collectTaskDates(props.tasksTree)

  // Collecter jalons
  props.milestones.forEach((m) => {
    if (m.planned_date) dates.push(new Date(m.planned_date).getTime())
  })

  // Aujourd'hui
  dates.push(new Date().getTime())

  if (dates.length === 0) {
    const now = new Date()
    return {
      start: new Date(now.getFullYear(), now.getMonth(), 1),
      end: new Date(now.getFullYear(), now.getMonth() + 2, 1),
    }
  }

  const minTime = Math.min(...dates)
  const maxTime = Math.max(...dates)

  // Marges
  const startDate = new Date(minTime)
  startDate.setDate(startDate.getDate() - 10)

  const endDate = new Date(maxTime)
  endDate.setDate(endDate.getDate() + 20)

  return { start: startDate, end: endDate }
})

// 2. Génération des colonnes temporelles
const timeColumns = computed(() => {
  const cols = []
  const { start, end } = timelineBounds.value
  const todayStr = new Date().toISOString().split('T')[0]

  if (zoomLevel.value === 'day') {
    const curr = new Date(start)
    while (curr <= end) {
      const dateStr = curr.toISOString().split('T')[0]
      const dayNum = curr.getDate()
      const dayOfWeek = curr.getDay()
      cols.push({
        date: new Date(curr),
        dateStr,
        label: `${dayNum}`,
        isToday: dateStr === todayStr,
        isWeekend: dayOfWeek === 0 || dayOfWeek === 6,
      })
      curr.setDate(curr.getDate() + 1)
    }
  } else if (zoomLevel.value === 'week') {
    const curr = new Date(start)
    // Align to Monday
    const day = curr.getDay()
    const diff = curr.getDate() - day + (day === 0 ? -6 : 1)
    curr.setDate(diff)

    while (curr <= end) {
      const weekDate = new Date(curr)
      const weekLabel = `S${getWeekNumber(weekDate)} (${weekDate.getDate()}/${weekDate.getMonth() + 1})`
      cols.push({
        date: weekDate,
        dateStr: weekDate.toISOString().split('T')[0],
        label: weekLabel,
        isToday: isDateInCurrentWeek(weekDate),
        isWeekend: false,
      })
      curr.setDate(curr.getDate() + 7)
    }
  } else {
    // Month
    const curr = new Date(start.getFullYear(), start.getMonth(), 1)
    while (curr <= end) {
      const monthDate = new Date(curr)
      const monthNames = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
      cols.push({
        date: monthDate,
        dateStr: monthDate.toISOString().split('T')[0],
        label: `${monthNames[monthDate.getMonth()]} ${monthDate.getFullYear()}`,
        isToday: isSameMonthYear(monthDate, new Date()),
        isWeekend: false,
      })
      curr.setMonth(curr.getMonth() + 1)
    }
  }

  return cols
})

const totalTimelineWidth = computed(() => {
  return timeColumns.value.length * columnWidth.value
})

// En-têtes mensuels supérieurs
const monthHeaders = computed(() => {
  const headers = []
  if (timeColumns.value.length === 0) return headers

  let currentMonthYear = ''
  let currentCount = 0
  const monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
  ]

  timeColumns.value.forEach((col) => {
    const d = col.date
    const key = `${monthNames[d.getMonth()]} ${d.getFullYear()}`
    if (key !== currentMonthYear) {
      if (currentMonthYear !== '') {
        headers.push({
          label: currentMonthYear,
          width: currentCount * columnWidth.value,
        })
      }
      currentMonthYear = key
      currentCount = 1
    } else {
      currentCount++
    }
  })

  if (currentCount > 0) {
    headers.push({
      label: currentMonthYear,
      width: currentCount * columnWidth.value,
    })
  }

  return headers
})

// Conversion d'une date en position X en pixels
function getXFromDate(dateInput) {
  if (!dateInput) return 0
  const target = new Date(dateInput).getTime()
  const { start, end } = timelineBounds.value
  const startTime = start.getTime()
  const endTime = end.getTime()

  if (endTime <= startTime) return 0
  const ratio = (target - startTime) / (endTime - startTime)
  return Math.round(ratio * totalTimelineWidth.value)
}

// Position X d'Aujourd'hui
const todayXPosition = computed(() => {
  return getXFromDate(new Date())
})

// 3. Transformation des données hiérarchiques en lignes plates pour le rendu
const flatRows = computed(() => {
  const rows = []

  // Phases
  props.phases.forEach((phase) => {
    let phaseStart = phase.start_date_planned
    let phaseEnd = phase.end_date_planned

    // Si la phase n'a pas de dates directes, calculer à partir des tâches
    const phaseTasks = props.tasksTree.filter((t) => t.phase_id === phase.id)
    if (!phaseStart && phaseTasks.length > 0) {
      const dates = phaseTasks.map((t) => t.planned_start_date).filter(Boolean)
      if (dates.length > 0) phaseStart = dates.sort()[0]
    }
    if (!phaseEnd && phaseTasks.length > 0) {
      const dates = phaseTasks.map((t) => t.planned_end_date).filter(Boolean)
      if (dates.length > 0) phaseEnd = dates.sort().reverse()[0]
    }

    let bar = null
    if (phaseStart && phaseEnd) {
      const left = getXFromDate(phaseStart)
      const right = getXFromDate(phaseEnd)
      bar = {
        left,
        width: Math.max(16, right - left),
        startDate: phaseStart,
        endDate: phaseEnd,
      }
    }

    rows.push({
      type: 'phase',
      level: 0,
      id: `phase-${phase.id}`,
      title: `${phase.code} - ${phase.name}`,
      data: phase,
      bar,
    })

    // Tâches de cette phase
    phaseTasks.forEach((t) => {
      pushTaskRow(t, 1)
    })
  })

  // Fonction récursive pour tâches et sous-tâches
  function pushTaskRow(task, level) {
    let bar = null
    if (task.planned_start_date && task.planned_end_date) {
      const left = getXFromDate(task.planned_start_date)
      const right = getXFromDate(task.planned_end_date)
      bar = {
        left,
        width: Math.max(20, right - left),
        startDate: task.planned_start_date,
        endDate: task.planned_end_date,
      }
    }

    rows.push({
      type: level > 1 ? 'subtask' : 'task',
      level,
      id: `task-${task.id}`,
      title: `${task.code} - ${task.name}`,
      data: task,
      bar,
    })

    if (task.subtasks && task.subtasks.length > 0) {
      task.subtasks.forEach((sub) => {
        pushTaskRow(sub, level + 1)
      })
    }
  }

  // Jalons (Milestones)
  if (props.milestones && props.milestones.length > 0) {
    props.milestones.forEach((m) => {
      let bar = null
      if (m.planned_date) {
        bar = {
          left: getXFromDate(m.planned_date),
          date: m.planned_date,
        }
      }
      rows.push({
        type: 'milestone',
        level: 0,
        id: `milestone-${m.id}`,
        title: `Jalon : ${m.code} - ${m.name}`,
        data: m,
        bar,
      })
    })
  }

  return rows
})

// 4. Calcul des courbes de liaisons SVG entre tâches
const svgDependencyCurves = computed(() => {
  if (!showDependencies.value) return []
  const curves = []

  // Dictionnaire de position Y et barre X de chaque tâche
  const taskPositions = {}
  flatRows.value.forEach((row, idx) => {
    if (row.type === 'task' || row.type === 'subtask') {
      taskPositions[row.data.id] = {
        y: (idx * 40) + 20, // centre de la ligne 40px
        bar: row.bar,
      }
    }
  })

  // Trouver toutes les dépendances
  flatRows.value.forEach((row) => {
    if ((row.type === 'task' || row.type === 'subtask') && row.data.dependencies) {
      const succPos = taskPositions[row.data.id]
      if (!succPos || !succPos.bar) return

      row.data.dependencies.forEach((dep) => {
        const predPos = taskPositions[dep.predecessor_id]
        if (!predPos || !predPos.bar) return

        const startX = predPos.bar.left + predPos.bar.width
        const startY = predPos.y
        const endX = succPos.bar.left
        const endY = succPos.y

        // Courbe Bézier
        const midX = startX + Math.max(15, (endX - startX) / 2)
        const path = `M ${startX} ${startY} C ${midX} ${startY}, ${midX} ${endY}, ${endX - 3} ${endY}`

        curves.push({
          id: `${dep.predecessor_id}-${row.data.id}`,
          path,
        })
      })
    }
  })

  return curves
})

function getTaskBarClass(task) {
  if (task.status === 'Terminée') {
    return 'bg-emerald-600 hover:bg-emerald-700'
  }
  if (task.is_blocked || task.delay_days > 0) {
    return 'bg-rose-600 hover:bg-rose-700'
  }
  if (task.status === 'En cours') {
    return 'bg-[#1d4ed8] hover:bg-blue-800'
  }
  return 'bg-slate-500 hover:bg-slate-600'
}

function handleRowClick(row) {
  if (row.type === 'task' || row.type === 'subtask') {
    emit('selectTask', row.data)
  } else if (row.type === 'milestone') {
    emit('selectMilestone', row.data)
  } else if (row.type === 'phase') {
    emit('selectPhase', row.data)
  }
}

function syncScrollY(e) {
  if (timelineContainerRef.value && e.target === leftPaneRef.value) {
    timelineContainerRef.value.scrollTop = leftPaneRef.value.scrollTop
  }
}

function syncScrollX(e) {
  if (leftPaneRef.value && e.target === timelineContainerRef.value) {
    leftPaneRef.value.scrollTop = timelineContainerRef.value.scrollTop
  }
}

function scrollToToday() {
  if (timelineContainerRef.value && todayXPosition.value >= 0) {
    const containerWidth = timelineContainerRef.value.clientWidth
    timelineContainerRef.value.scrollLeft = Math.max(0, todayXPosition.value - (containerWidth / 2))
  }
}

onMounted(() => {
  nextTick(() => {
    scrollToToday()
  })
})

// Utilitaires de dates
function getWeekNumber(d) {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  const dayNum = date.getUTCDay() || 7
  date.setUTCDate(date.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1))
  return Math.ceil(((date - yearStart) / 86400000 + 1) / 7)
}

function isDateInCurrentWeek(date) {
  const now = new Date()
  return getWeekNumber(date) === getWeekNumber(now) && date.getFullYear() === now.getFullYear()
}

function isSameMonthYear(d1, d2) {
  return d1.getMonth() === d2.getMonth() && d1.getFullYear() === d2.getFullYear()
}
</script>
