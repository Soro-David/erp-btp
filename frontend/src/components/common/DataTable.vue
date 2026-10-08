<template>
  <div 
    class="bg-white rounded-2xl transition-all shadow-sm"
    :class="[
      bordered ? 'border border-slate-200' : '',
      wrapperClass
    ]"
  >
    <!-- 1. En-tête / Barre d'outils du Tableau -->
    <div 
      v-if="showHeader" 
      class="p-4 sm:p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
    >
      <!-- Titre / Sous-titre ou slot titre -->
      <div v-if="title || subtitle || $slots.title" class="min-w-0">
        <slot name="title">
          <div class="flex items-center gap-2">
            <h3 v-if="title" class="text-base sm:text-lg font-bold text-slate-900 tracking-tight truncate">
              {{ title }}
            </h3>
            <span v-if="badgeText" class="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
              {{ badgeText }}
            </span>
          </div>
          <p v-if="subtitle" class="text-xs text-slate-500 mt-0.5 truncate">
            {{ subtitle }}
          </p>
        </slot>
      </div>

      <!-- Barre d'actions & Recherche -->
      <div class="flex items-center gap-2.5 flex-wrap sm:ml-auto w-full sm:w-auto">
        <!-- Champ de recherche intégrée -->
        <div v-if="searchable" class="relative flex-1 sm:w-64">
          <fas-icon 
            icon="magnifying-glass" 
            class="text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 text-xs pointer-events-none" 
          />
          <input
            v-model="searchTerm"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full pl-8 pr-7 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-xl placeholder-slate-400 text-slate-900 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition-all"
          />
          <button 
            v-if="searchTerm" 
            type="button" 
            @click="searchTerm = ''" 
            class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-0.5"
            title="Effacer la recherche"
          >
            <fas-icon icon="xmark" class="text-xs" />
          </button>
        </div>

        <!-- Slot d'actions d'en-tête (Boutons + Ajouter, Exporter, Filtres, etc.) -->
        <slot name="header-actions"></slot>
      </div>
    </div>

    <!-- 2. Zone du Tableau avec scroll horizontal fluide -->
    <div class="overflow-x-auto relative">
      <table class="w-full text-left text-xs sm:text-sm whitespace-nowrap">
        <!-- En-têtes de colonnes -->
        <thead class="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider select-none">
          <tr>
            <th
              v-for="col in normalizedColumns"
              :key="col.key"
              scope="col"
              :style="{ width: col.width || 'auto' }"
              class="px-4 py-3.5"
              :class="[
                col.headerClass || '',
                getAlignmentClass(col.align),
                col.sortable ? 'cursor-pointer hover:bg-slate-100 hover:text-slate-800 transition-colors' : ''
              ]"
              @click="col.sortable ? handleSort(col.key) : null"
            >
              <div 
                class="inline-flex items-center gap-1.5"
                :class="col.align === 'right' ? 'flex-row-reverse' : col.align === 'center' ? 'justify-center w-full' : ''"
              >
                <span>{{ col.label }}</span>
                <!-- Indicateur de tri -->
                <span v-if="col.sortable" class="text-[10px] text-slate-400">
                  <fas-icon 
                    v-if="sortKey === col.key && sortOrder === 'asc'" 
                    icon="arrow-up-long" 
                    class="text-blue-600 font-bold" 
                  />
                  <fas-icon 
                    v-else-if="sortKey === col.key && sortOrder === 'desc'" 
                    icon="arrow-down-long" 
                    class="text-blue-600 font-bold" 
                  />
                  <fas-icon 
                    v-else 
                    icon="sort" 
                    class="text-slate-300 hover:text-slate-500" 
                  />
                </span>
              </div>
            </th>

            <!-- Colonne Actions supplémentaire si prop `actions` est activée -->
            <th 
              v-if="actions || $slots.actions" 
              scope="col"
              class="px-4 py-3.5"
              :class="[getAlignmentClass(actionsAlign), 'font-bold text-slate-500']"
            >
              {{ actionsHeader }}
            </th>
          </tr>
        </thead>

        <!-- Corps du tableau -->
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <!-- État de chargement (Spinner / Skeleton) -->
          <tr v-if="loading">
            <td 
              :colspan="totalColumnsCount" 
              class="px-4 text-center"
              :style="{ height: tableBodyMinHeight }"
            >
              <slot name="loading">
                <div class="flex flex-col items-center justify-center gap-2.5 text-slate-500 text-xs py-12">
                  <fas-icon icon="spinner" class="animate-spin text-2xl text-blue-600" />
                  <span class="font-medium">{{ loadingText }}</span>
                </div>
              </slot>
            </td>
          </tr>

          <!-- État vide (Aucun enregistrement) -->
          <tr v-else-if="paginatedItems.length === 0">
            <td 
              :colspan="totalColumnsCount" 
              class="px-4 text-center"
              :style="{ height: tableBodyMinHeight }"
            >
              <slot name="empty">
                <div class="flex flex-col items-center justify-center gap-2 max-w-sm mx-auto text-slate-400 py-12">
                  <div class="w-12 h-12 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-xl text-slate-400 mb-1">
                    <fas-icon :icon="emptyIcon" />
                  </div>
                  <div class="font-bold text-slate-700 text-sm">{{ emptyTitle }}</div>
                  <div class="text-xs text-slate-500">{{ emptySubtitle }}</div>
                  <button 
                    v-if="searchTerm" 
                    type="button" 
                    @click="searchTerm = ''" 
                    class="mt-2 text-xs font-semibold text-blue-600 hover:underline"
                  >
                    Effacer le filtre de recherche
                  </button>
                </div>
              </slot>
            </td>
          </tr>

          <!-- Lignes de données réelles -->
          <tr
            v-for="(item, index) in paginatedItems"
            :key="getItemKey(item, index)"
            class="data-table-row h-[52px] transition-colors"
            :class="[
              striped && index % 2 === 1 ? 'bg-slate-50/50' : 'bg-white',
              hoverable ? 'hover:bg-blue-50/40 cursor-default' : '',
              rowClickable ? 'cursor-pointer' : '',
              rowClass ? rowClass(item, index) : ''
            ]"
            @click="handleRowClick(item, index)"
          >
            <!-- Cellules des colonnes -->
            <td
              v-for="col in normalizedColumns"
              :key="col.key"
              class="px-4 py-3.5 text-xs sm:text-sm"
              :class="[
                col.class || '',
                getAlignmentClass(col.align)
              ]"
            >
              <!-- Slot dynamique personnalisé pour chaque colonne : #cell(nomColonne) -->
              <slot 
                :name="`cell(${col.key})`" 
                :item="item" 
                :value="getNestedValue(item, col.key)" 
                :index="index"
                :column="col"
              >
                <!-- Rendu par défaut avec formatage optionnel -->
                <span v-if="col.format">
                  {{ col.format(getNestedValue(item, col.key), item) }}
                </span>
                <span v-else>
                  {{ formatDefaultValue(getNestedValue(item, col.key)) }}
                </span>
              </slot>
            </td>

            <!-- Cellule des Actions par ligne -->
            <td 
              v-if="actions || $slots.actions" 
              class="px-4 py-3.5 text-xs sm:text-sm"
              :class="getAlignmentClass(actionsAlign)"
              @click.stop
            >
              <slot name="actions" :item="item" :index="index">
                <span class="text-slate-400 text-xs">—</span>
              </slot>
            </td>
          </tr>

          <!-- Lignes vides de remplissage pour garantir 10 lignes fixes -->
          <tr
            v-for="emptyIdx in emptyRowsCount"
            :key="`empty-row-${emptyIdx}`"
            class="data-table-row h-[52px] select-none pointer-events-none"
            :class="[
              striped && (paginatedItems.length + emptyIdx - 1) % 2 === 1 ? 'bg-slate-50/30' : 'bg-white',
            ]"
            aria-hidden="true"
          >
            <!-- Cellules vides pour chaque colonne -->
            <td
              v-for="col in normalizedColumns"
              :key="`empty-col-${col.key}-${emptyIdx}`"
              class="px-4 py-3.5 text-xs sm:text-sm text-transparent"
              :class="[
                col.class || '',
                getAlignmentClass(col.align)
              ]"
            >
              <span class="inline-block opacity-0">&nbsp;</span>
            </td>

            <!-- Cellule vide pour Actions si prop active -->
            <td 
              v-if="actions || $slots.actions" 
              class="px-4 py-3.5 text-xs sm:text-sm text-transparent"
              :class="getAlignmentClass(actionsAlign)"
            >
              <span class="inline-block opacity-0">&nbsp;</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 3. Pied de page & Pagination (Fixe à 10 lignes, pagination alignée à droite) -->
    <div 
      v-if="paginated && totalItemsCount > 0" 
      class="p-4 sm:px-5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500"
    >
      <!-- Informations sur le nombre de résultats affichés -->
      <div class="flex items-center gap-3">
        <span>
          Affichage de <strong class="text-slate-800">{{ rangeStart }}</strong> à 
          <strong class="text-slate-800">{{ rangeEnd }}</strong> sur 
          <strong class="text-slate-800">{{ totalItemsCount }}</strong> résultat{{ totalItemsCount > 1 ? 's' : '' }}
        </span>
      </div>

      <!-- Commandes de Pagination strictly alignées à droite -->
      <div class="flex items-center justify-end gap-1 sm:ml-auto w-full sm:w-auto">
        <!-- Bouton Précédent -->
        <button
          type="button"
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
          class="p-1.5 sm:px-2.5 sm:py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-xs font-medium flex items-center gap-1"
          title="Page précédente"
        >
          <fas-icon icon="chevron-left" class="text-[10px]" />
          <span class="hidden sm:inline">Précédent</span>
        </button>

        <!-- Numéros de pages -->
        <div class="flex items-center gap-1">
          <button
            v-for="page in (totalPages > 1 ? visiblePages : [1])"
            :key="page"
            type="button"
            @click="typeof page === 'number' ? goToPage(page) : null"
            class="min-w-[28px] h-7 px-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center"
            :class="[
              page === currentPage
                ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/30'
                : typeof page === 'number'
                  ? 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  : 'text-slate-400 cursor-default'
            ]"
            :disabled="typeof page !== 'number'"
          >
            {{ page }}
          </button>
        </div>

        <!-- Bouton Suivant -->
        <button
          type="button"
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
          class="p-1.5 sm:px-2.5 sm:py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-xs font-medium flex items-center gap-1"
          title="Page suivante"
        >
          <span class="hidden sm:inline">Suivant</span>
          <fas-icon icon="chevron-right" class="text-[10px]" />
        </button>
      </div>
    </div>

    <!-- Slot additionnel optionnel sous le tableau -->
    <slot name="footer"></slot>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // Colonnes du tableau : [{ key, label, sortable, align, width, class, headerClass, format }]
  columns: {
    type: Array,
    required: true,
    default: () => []
  },
  // Données brutes des lignes
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  // État de chargement
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: 'Chargement des données en cours...'
  },
  // Recherche intégrée
  searchable: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: 'Rechercher...'
  },
  // Titre & Sous-titre de la carte
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  badgeText: {
    type: String,
    default: ''
  },
  // Pagination
  paginated: {
    type: Boolean,
    default: true
  },
  pageSize: {
    type: Number,
    default: 10
  },
  pageSizeOptions: {
    type: Array,
    default: () => []
  },
  // Fixer les lignes affichées (complète avec des lignes vides jusqu'à 10 pour stabiliser la hauteur)
  fixedRows: {
    type: Boolean,
    default: true
  },
  fixedRowCount: {
    type: Number,
    default: 10
  },
  // Colonne Actions
  actions: {
    type: Boolean,
    default: false
  },
  actionsHeader: {
    type: String,
    default: 'Actions'
  },
  actionsAlign: {
    type: String,
    default: 'right'
  },
  // Style & Présentation
  bordered: {
    type: Boolean,
    default: true
  },
  striped: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: true
  },
  rowClickable: {
    type: Boolean,
    default: false
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  rowClass: {
    type: Function,
    default: null
  },
  wrapperClass: {
    type: String,
    default: ''
  },
  // État vide
  emptyTitle: {
    type: String,
    default: 'Aucune donnée disponible'
  },
  emptySubtitle: {
    type: String,
    default: 'Aucun enregistrement ne correspond aux filtres.'
  },
  emptyIcon: {
    type: String,
    default: 'folder-open'
  }
})

const emit = defineEmits(['row-click', 'sort', 'search', 'page-change'])

// État local
const searchTerm = ref('')
const sortKey = ref('')
const sortOrder = ref('asc') // 'asc' | 'desc'
const currentPage = ref(1)
const perPage = ref(props.pageSize)

// Normalisation des colonnes (supporte chaîne simple ou objet `{ key, label }`)
const normalizedColumns = computed(() => {
  return props.columns.map(col => {
    if (typeof col === 'string') {
      return {
        key: col,
        label: col.charAt(0).toUpperCase() + col.slice(1),
        sortable: false,
        align: 'left'
      }
    }
    return {
      key: col.key || col.id,
      label: col.label || col.title || col.key,
      sortable: col.sortable ?? false,
      align: col.align || 'left',
      width: col.width || null,
      class: col.class || '',
      headerClass: col.headerClass || '',
      format: col.format || null
    }
  })
})

const totalColumnsCount = computed(() => {
  return normalizedColumns.value.length + (props.actions ? 1 : 0)
})

const showHeader = computed(() => {
  return !!(props.title || props.subtitle || props.searchable)
})

// Filtrage des éléments par recherche
const filteredItems = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  if (!query) {
    return props.items
  }

  return props.items.filter(item => {
    return normalizedColumns.value.some(col => {
      const val = getNestedValue(item, col.key)
      if (val === null || val === undefined) return false
      return String(val).toLowerCase().includes(query)
    })
  })
})

// Tri des éléments
const sortedItems = computed(() => {
  if (!sortKey.value) {
    return filteredItems.value
  }

  const itemsCopy = [...filteredItems.value]
  itemsCopy.sort((a, b) => {
    const valA = getNestedValue(a, sortKey.value)
    const valB = getNestedValue(b, sortKey.value)

    if (valA === valB) return 0
    if (valA === null || valA === undefined) return 1
    if (valB === null || valB === undefined) return -1

    let comparison = 0
    if (typeof valA === 'number' && typeof valB === 'number') {
      comparison = valA - valB
    } else {
      comparison = String(valA).localeCompare(String(valB), undefined, { numeric: true, sensitivity: 'base' })
    }

    return sortOrder.value === 'asc' ? comparison : -comparison
  })

  return itemsCopy
})

// Pagination
const totalItemsCount = computed(() => sortedItems.value.length)

const totalPages = computed(() => {
  if (!props.paginated || perPage.value <= 0) return 1
  return Math.ceil(totalItemsCount.value / perPage.value) || 1
})

const paginatedItems = computed(() => {
  if (!props.paginated) {
    return sortedItems.value
  }
  const start = (currentPage.value - 1) * perPage.value
  return sortedItems.value.slice(start, start + perPage.value)
})

// Calcul du nombre de lignes vides pour atteindre exactement le nombre cible fixe (par défaut 10)
const emptyRowsCount = computed(() => {
  if (!props.fixedRows) return 0
  if (props.loading || paginatedItems.value.length === 0) return 0
  const target = props.fixedRowCount || perPage.value || 10
  return Math.max(0, target - paginatedItems.value.length)
})

// Hauteur minimale du tableau pour garantir l'absence de sauts visuels en cas d'état vide ou chargement
const tableBodyMinHeight = computed(() => {
  if (!props.fixedRows) return 'auto'
  const count = props.fixedRowCount || perPage.value || 10
  return `${count * 52}px`
})

const rangeStart = computed(() => {
  if (totalItemsCount.value === 0) return 0
  return (currentPage.value - 1) * perPage.value + 1
})

const rangeEnd = computed(() => {
  return Math.min(currentPage.value * perPage.value, totalItemsCount.value)
})

// Pagination avec ellipses (ex: [1, 2, 3, '...', 10])
const visiblePages = computed(() => {
  const current = currentPage.value
  const total = totalPages.value

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  if (current <= 4) {
    return [1, 2, 3, 4, 5, '...', total]
  }

  if (current >= total - 3) {
    return [1, '...', total - 4, total - 3, total - 2, total - 1, total]
  }

  return [1, '...', current - 1, current, current + 1, '...', total]
})

// Handlers
function handleSort(key) {
  if (sortKey.value === key) {
    if (sortOrder.value === 'asc') {
      sortOrder.value = 'desc'
    } else {
      sortKey.value = ''
      sortOrder.value = 'asc'
    }
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key: sortKey.value, order: sortOrder.value })
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  emit('page-change', page)
}

function handleRowClick(item, index) {
  if (props.rowClickable) {
    emit('row-click', { item, index })
  }
}

function getItemKey(item, index) {
  return item[props.rowKey] !== undefined ? item[props.rowKey] : index
}

function getNestedValue(obj, path) {
  if (!obj || !path) return ''
  // Supporte les clés à points comme `user.profile.name`
  if (path.includes('.')) {
    return path.split('.').reduce((acc, part) => (acc && acc[part] !== undefined ? acc[part] : ''), obj)
  }
  return obj[path] !== undefined ? obj[path] : ''
}

function formatDefaultValue(val) {
  if (val === null || val === undefined || val === '') return '—'
  if (typeof val === 'boolean') return val ? 'Oui' : 'Non'
  return val
}

function getAlignmentClass(align) {
  switch (align) {
    case 'center':
      return 'text-center'
    case 'right':
      return 'text-right'
    case 'left':
    default:
      return 'text-left'
  }
}

// Réinitialisation de la page courante quand la recherche change
watch(searchTerm, (val) => {
  currentPage.value = 1
  emit('search', val)
})

watch(() => props.pageSize, (val) => {
  perPage.value = val
  currentPage.value = 1
})
</script>

<style scoped>
.data-table-row {
  height: 52px;
  min-height: 52px;
}
</style>
