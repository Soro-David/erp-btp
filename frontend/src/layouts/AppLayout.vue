<template>
  <div class="h-screen w-screen flex bg-[#f8fafc] text-slate-900 font-sans antialiased overflow-hidden">
    <!-- 1. ZONE ARRIÈRE-PLAN ORANGE POUR LA SIDEBAR -->
    <div class="bg-transparent lg:bg-orange-500 flex-shrink-0 flex items-stretch relative">
      <AppSidebar 
        :is-collapsed="isSidebarCollapsed"
        :is-mobile-open="isMobileSidebarOpen"
        @close-mobile="isMobileSidebarOpen = false"
        @toggle-collapse="toggleCollapseDesktop"
      />
    </div>

    <!-- 2. SECTION DROITE : NAVBAR VERTE EN HAUT + CONTENU + FOOTER EN BAS -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      <!-- Navbar globale VERTE (Prend sa place en haut du contenu) -->
      <AppNavbar 
        @toggle-sidebar="handleToggleSidebar" 
      />

      <!-- Zone de contenu principal scrollable avec Footer intégré en bas -->
      <main class="flex-1 overflow-y-auto bg-[#f8fafc] flex flex-col">
        <!-- Contenu des pages -->
        <div class="flex-1 p-4 sm:p-6 lg:p-8">
          <div class="max-w-7xl mx-auto space-y-6">
            <slot>
              <router-view />
            </slot>
          </div>
        </div>

        <!-- Footer professionnel BTP Manager -->
        <AppFooter />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const isSidebarCollapsed = ref(false)
const isMobileSidebarOpen = ref(false)

onMounted(() => {
  const savedState = localStorage.getItem('btp_sidebar_collapsed')
  if (savedState !== null) {
    isSidebarCollapsed.value = savedState === 'true'
  }
})

function handleToggleSidebar() {
  if (window.innerWidth < 1024) {
    isMobileSidebarOpen.value = !isMobileSidebarOpen.value
  } else {
    toggleCollapseDesktop()
  }
}

function toggleCollapseDesktop() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  localStorage.setItem('btp_sidebar_collapsed', isSidebarCollapsed.value.toString())
}
</script>
