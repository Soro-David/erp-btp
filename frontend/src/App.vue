<template>
  <component :is="layoutComponent">
    <router-view />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const route = useRoute()

const layoutComponent = computed(() => {
  if (route.meta.layout === 'AuthLayout' || route.name === 'Login') {
    return AuthLayout
  }
  return AppLayout
})
</script>
