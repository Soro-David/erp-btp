<template>
  <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
    <!-- Barre de Navigation Calendrier -->
    <div class="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/60">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-base">
          <fas-icon icon="calendar-days" />
        </div>
        <div>
          <h3 class="text-sm font-bold text-slate-900 capitalize">{{ currentMonthLabel }}</h3>
          <p class="text-xs text-slate-500">Vue opérationnelle mensuelle des interventions sur site</p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="prevMonth"
          class="p-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs shadow-xs"
          title="Mois précédent"
        >
          <fas-icon icon="chevron-left" />
        </button>
        <button
          type="button"
          @click="goToToday"
          class="px-3 py-1.5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-xs"
        >
          Aujourd'hui
        </button>
        <button
          type="button"
          @click="nextMonth"
          class="p-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs shadow-xs"
          title="Mois suivant"
        >
          <fas-icon icon="chevron-right" />
        </button>
      </div>
    </div>

    <!-- Grille des Jours de la Semaine -->
    <div class="grid grid-cols-7 border-b border-slate-200 bg-slate-100 text-center py-2 text-xs font-bold text-slate-600">
      <div>Lun</div>
      <div>Mar</div>
      <div>Mer</div>
      <div>Jeu</div>
      <div>Ven</div>
      <div class="text-slate-400">Sam</div>
      <div class="text-slate-400">Dim</div>
    </div>

    <!-- Grille des Cases du Calendrier -->
    <div class="grid grid-cols-7 auto-rows-fr divide-x divide-y divide-slate-100 bg-slate-50/20 flex-1 min-h-[500px]">
      <div
        v-for="(day, idx) in calendarDays"
        :key="idx"
        class="min-h-[100px] p-1.5 flex flex-col transition-colors relative"
        :class="{
          'bg-slate-100/50 opacity-50': !day.isCurrentMonth,
          'bg-blue-50/40 font-bold': day.isToday,
          'bg-white': day.isCurrentMonth && !day.isToday,
        }"
      >
        <!-- Numéro du Jour -->
        <div class="flex items-center justify-between mb-1">
          <span
            class="text-xs font-mono font-bold w-6 h-6 rounded-full flex items-center justify-center"
            :class="day.isToday ? 'bg-[#1d4ed8] text-white shadow-xs' : 'text-slate-700'"
          >
            {{ day.dayNumber }}
          </span>
          <span v-if="day.milestones.length > 0" class="text-amber-500 text-xs" title="Jalon contractuel">
            <fas-icon icon="flag" />
          </span>
        </div>

        <!-- Jalons de la journée -->
        <div v-for="m in day.milestones" :key="'m-' + m.id" class="mb-1">
          <div
            @click="$emit('selectMilestone', m)"
            class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-200 truncate cursor-pointer hover:bg-amber-200"
            :title="'Jalon : ' + m.name"
          >
            ◆ {{ m.name }}
          </div>
        </div>

        <!-- Tâches de la journée -->
        <div class="space-y-1 overflow-y-auto max-h-24">
          <div
            v-for="task in day.tasks"
            :key="'t-' + task.id"
            @click="$emit('selectTask', task)"
            class="px-1.5 py-0.5 rounded text-[10px] font-medium truncate cursor-pointer transition-all hover:scale-102 shadow-2xs"
            :class="{
              'bg-emerald-100 text-emerald-800 border-l-2 border-emerald-500': task.status === 'Terminée',
              'bg-blue-100 text-blue-900 border-l-2 border-[#1d4ed8]': task.status === 'En cours',
              'bg-rose-100 text-rose-800 border-l-2 border-rose-500': task.status === 'Bloquée' || task.delay_days > 0,
              'bg-slate-200 text-slate-700 border-l-2 border-slate-400': task.status === 'À faire' || task.status === 'En attente',
            }"
            :title="task.name + ' (' + task.progress + '%)'"
          >
            {{ task.code }}: {{ task.name }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => [],
  },
  milestones: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['selectTask', 'selectMilestone'])

const currentDate = ref(new Date())

const currentMonthLabel = computed(() => {
  return currentDate.value.toLocaleDateString('fr-FR', {
    month: 'long',
    year: 'numeric',
  })
})

function prevMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() - 1)
  currentDate.value = d
}

function nextMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + 1)
  currentDate.value = d
}

function goToToday() {
  currentDate.value = new Date()
}

// Génération de la matrice des 35/42 jours du mois
const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()

  const firstDayOfMonth = new Date(year, month, 1)
  const lastDayOfMonth = new Date(year, month + 1, 0)

  // Jour début (1=Lundi, ..., 7=Dimanche)
  let startDayOfWeek = firstDayOfMonth.getDay()
  if (startDayOfWeek === 0) startDayOfWeek = 7 // Dimanche = 7

  const days = []
  const todayStr = new Date().toISOString().split('T')[0]

  // Jours du mois précédent
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = startDayOfWeek - 1; i > 0; i--) {
    const d = new Date(year, month - 1, prevMonthLastDay - i + 1)
    const dateStr = d.toISOString().split('T')[0]
    days.push({
      date: d,
      dateStr,
      dayNumber: d.getDate(),
      isCurrentMonth: false,
      isToday: dateStr === todayStr,
      tasks: getTasksForDate(dateStr),
      milestones: getMilestonesForDate(dateStr),
    })
  }

  // Jours du mois en cours
  for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
    const d = new Date(year, month, day)
    const dateStr = d.toISOString().split('T')[0]
    days.push({
      date: d,
      dateStr,
      dayNumber: day,
      isCurrentMonth: true,
      isToday: dateStr === todayStr,
      tasks: getTasksForDate(dateStr),
      milestones: getMilestonesForDate(dateStr),
    })
  }

  // Jours du mois suivant pour compléter à un multiple de 7
  const remaining = 7 - (days.length % 7)
  if (remaining < 7) {
    for (let day = 1; day <= remaining; day++) {
      const d = new Date(year, month + 1, day)
      const dateStr = d.toISOString().split('T')[0]
      days.push({
        date: d,
        dateStr,
        dayNumber: day,
        isCurrentMonth: false,
        isToday: dateStr === todayStr,
        tasks: getTasksForDate(dateStr),
        milestones: getMilestonesForDate(dateStr),
      })
    }
  }

  return days
})

function getTasksForDate(dateStr) {
  return props.tasks.filter((t) => {
    if (!t.planned_start_date || !t.planned_end_date) return false
    return dateStr >= t.planned_start_date && dateStr <= t.planned_end_date
  })
}

function getMilestonesForDate(dateStr) {
  return props.milestones.filter((m) => m.planned_date === dateStr)
}
</script>
