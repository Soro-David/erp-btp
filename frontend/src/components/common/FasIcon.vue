<template>
  <font-awesome-icon :icon="resolvedIcon" v-bind="$attrs" />
</template>

<script setup>
import { computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const props = defineProps({
  icon: {
    type: [String, Array, Object],
    default: null,
  },
  name: {
    type: String,
    default: null,
  },
})

const resolvedIcon = computed(() => {
  const val = props.name || props.icon
  if (!val) return ['fas', 'question']
  if (Array.isArray(val) || typeof val === 'object') return val

  // Nettoyage si la chaîne contient 'fa-solid fa-user', 'fas fa-user' ou 'fa-user'
  const cleaned = String(val)
    .replace(/^fa-solid\s+/, '')
    .replace(/^fas\s+/, '')
    .replace(/^fa-/, '')
    .trim()

  return ['fas', cleaned]
})
</script>
