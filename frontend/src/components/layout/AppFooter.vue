<template>
  <footer class="border-t border-slate-200/80 bg-white text-slate-500 mt-auto transition-colors select-none">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row items-center justify-between gap-3 text-xs">
      <!-- Section Gauche : Identité & Statut Système -->
      <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5 sm:gap-3 text-slate-600">
        <span class="text-[11px] text-slate-400">
          &copy; {{ currentYear }} Tous droits réservés.
        </span>
      </div>

      <!-- Section Droite : Récupération automatique du Nom Entreprise -->
      <div class="flex flex-wrap items-center justify-center sm:justify-end gap-3 sm:gap-4 text-xs">
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-orange-50 border border-orange-200 text-orange-800 font-semibold text-[11px] shadow-xs">
          <span class="w-2 h-2 rounded-full bg-orange-500"></span>
          <span>{{ authStore.companyName }}</span>
        </span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { alertInfo, alertSuccess } from '@/utils/alert'

const authStore = useAuthStore()
const currentYear = computed(() => new Date().getFullYear())

function openSupportModal() {
  alertInfo(
    'Support & Assistance BTP Manager',
    `Pour tout incident ou assistance technique sur vos chantiers :<br><br>
    📞 <strong>Ligne directe :</strong> +225 27 20 00 00 00<br>
    ✉️ <strong>Email d'astreinte :</strong> support@btp-manager.ci<br>
    ⏰ <strong>Disponibilité :</strong> 24h/24 et 7j/7 pour les urgences d'exploitation.`
  )
}

function openDocModal() {
  alertInfo(
    'Documentation Opérationnelle ERP BTP',
    `Modules et processus clés intégrés à la plateforme :<br><br>
    • <strong>Chantiers :</strong> Suivi des phases, métrés et validation d'avancement.<br>
    • <strong>Marchés :</strong> Gestion des contrats sous-traitants et situations mensuelles.<br>
    • <strong>Stocks & Achats :</strong> Bons de commande et alertes de seuils critiques.<br>
    • <strong>Engins :</strong> Carnet de bord et planification des entretiens périodiques.`
  )
}

function openSecurityModal() {
  alertSuccess(
    'Sécurité & Protection des Données',
    `Les données opérationnelles et financières sont protégées selon les normes de l'industrie :<br><br>
    🔒 Authentification forte par jetons JWT (HS256)<br>
    🛡️ Contrôle d'accès basé sur les rôles (RBAC SuperAdmin / Owner / Director / Manager / Worker)<br>
    💾 Sauvegardes automatiques et transactions isolées sous PostgreSQL.`
  )
}
</script>
