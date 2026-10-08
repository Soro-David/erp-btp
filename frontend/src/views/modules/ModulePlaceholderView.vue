<template>
  <div class="space-y-6">
    <!-- En-tête du module avec fil d'Ariane (Carte Blanche Premium) -->
    <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <!-- Fil d'Ariane -->
        <nav class="flex items-center gap-2 text-xs font-medium text-slate-500 mb-2">
          <router-link to="/dashboard" class="hover:text-blue-600 transition-colors">ERP BTP</router-link>
          <span>/</span>
          <span class="text-slate-400">{{ moduleConfig.parent }}</span>
          <span>/</span>
          <span class="text-blue-700 font-semibold">{{ moduleConfig.title }}</span>
        </nav>

        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-xl bg-blue-50 border border-blue-100 text-[#1d4ed8] flex items-center justify-center text-xl flex-shrink-0">
            <fas-icon :icon="moduleConfig.icon" />
          </div>
          <div>
            <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              {{ moduleConfig.title }}
            </h1>
            <p class="text-xs sm:text-sm text-slate-500 mt-0.5">
              {{ moduleConfig.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- Actions d'en-tête (Charte : Bouton Secondaire GRIS, Bouton Principal BLEU) -->
      <div class="flex items-center gap-2.5 flex-wrap">
        <button 
          @click="handleExport"
          class="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-2 border border-slate-300 transition-colors shadow-sm"
        >
          <fas-icon icon="file-arrow-down" class="text-slate-500" />
          <span>Exporter (Excel/PDF)</span>
        </button>
        <button 
          @click="handleCreate"
          class="px-4 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all"
        >
          <fas-icon icon="plus" />
          <span>{{ moduleConfig.actionLabel || 'Nouveau' }}</span>
        </button>
      </div>
    </div>

    <!-- Mini KPI du module (Cartes Blanches avec Devise FCFA) -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
      <div 
        v-for="(kpi, idx) in moduleConfig.kpis" 
        :key="idx"
        class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:border-blue-200 transition-colors"
      >
        <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">{{ kpi.label }}</div>
        <div class="text-xl sm:text-2xl font-black text-slate-900" :class="kpi.color">{{ kpi.value }}</div>
        <div class="text-[10px] text-slate-400 mt-1 font-medium">{{ kpi.sub }}</div>
      </div>
    </div>

    <!-- Tableau & Filtres du module Partagé (DataTable) -->
    <DataTable
      :columns="tableColumns"
      :items="tableItems"
      searchable
      search-placeholder="Filtrer les enregistrements..."
      actions
      actions-header="Actions"
      actions-align="right"
      row-clickable
      @row-click="({ item }) => handleRowAction(item._raw)"
    >
      <!-- Barre d'onglets de filtrage rapide dans le header du tableau -->
      <template #header-actions>
        <div class="flex items-center gap-1.5 overflow-x-auto text-xs scrollbar-none">
          <button 
            v-for="tab in ['Tous', 'En cours', 'Validés', 'En attente']" 
            :key="tab"
            type="button"
            @click="activeTab = tab"
            class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
            :class="activeTab === tab ? 'bg-blue-50 text-blue-700 font-bold border border-blue-200' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'"
          >
            {{ tab }}
          </button>
        </div>
      </template>

      <!-- Colonne Statut avec badge dynamique -->
      <template #cell(statut)="{ value }">
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider" :class="getStatusBadgeClass(value)">
          {{ value }}
        </span>
      </template>

      <!-- Colonne Référence en gras bleu monospace -->
      <template #cell(reference)="{ value }">
        <span class="font-mono text-blue-700 font-bold">{{ value }}</span>
      </template>

      <!-- Actions de ligne -->
      <template #actions="{ item }">
        <div class="flex items-center justify-end gap-1">
          <button 
            type="button"
            @click.stop="handleRowAction(item._raw)"
            class="p-1.5 rounded-lg text-slate-500 hover:text-blue-700 hover:bg-blue-50 transition-colors"
            title="Voir les détails"
          >
            <fas-icon icon="eye" class="text-xs" />
          </button>
          <button 
            type="button"
            @click.stop="handleEditRow(item._raw)"
            class="p-1.5 rounded-lg text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 transition-colors"
            title="Modifier"
          >
            <fas-icon icon="pen-to-square" class="text-xs" />
          </button>
          <button 
            type="button"
            @click.stop="handleDeleteRow(item._raw)"
            class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
            title="Supprimer"
          >
            <fas-icon icon="trash-can" class="text-xs" />
          </button>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast, alertSuccess, confirmDialog } from '@/utils/alert'

const route = useRoute()
const router = useRouter()
const searchTerm = ref('')
const activeTab = ref('Tous')

// Définitions thématiques selon la route
const moduleConfigs = {
  // Projets & Chantiers
  '/chantiers': {
    parent: 'Projets & Chantiers',
    title: 'Gestion des Chantiers',
    description: 'Cartographie, états d\'avancement, budgets et maîtres d\'ouvrage.',
    icon: 'building',
    actionLabel: 'Nouveau Chantier',
    kpis: [
      { label: 'Chantiers actifs', value: '8', sub: 'Tous secteurs confondus', color: 'text-blue-700' },
      { label: 'En préparation', value: '3', sub: 'Dossiers techniques en cours', color: 'text-amber-600' },
      { label: 'Réceptionnés', value: '14', sub: 'Sur l\'année 2026', color: 'text-emerald-600' },
      { label: 'Taux respect planning', value: '94 %', sub: 'Objectif : 90%', color: 'text-slate-900' },
    ],
    columns: ['Référence', 'Nom du Chantier', 'Maître d\'Ouvrage', 'Budget Prévisionnel', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'CHT-2026-084', nom: 'École primaire à Yopougon', mo: 'Mairie de Yopougon', budget: '250 000 000 FCFA', statut: 'En cours' } },
      { id: 2, data: { reference: 'CH-2026-01', nom: 'Tour Azur R+14', mo: 'SCI Laguna', budget: '1 200 000 000 FCFA', statut: 'En cours' } },
      { id: 3, data: { reference: 'CH-2026-02', nom: 'Pont Grand-Bassam', mo: 'Ministère Équipement', budget: '850 000 000 FCFA', statut: 'En cours' } },
      { id: 4, data: { reference: 'CH-2026-03', nom: 'Voie Express Tronçon B', mo: 'AGEROUTE', budget: '420 000 000 FCFA', statut: 'Validés' } },
      { id: 5, data: { reference: 'CH-2026-04', nom: 'Villas Résidentielles Songon', mo: 'Privé Promotion', budget: '680 000 000 FCFA', statut: 'En attente' } },
    ],
  },
  '/chantiers/taches': {
    parent: 'Projets & Chantiers',
    title: 'Tâches & Jalons',
    description: 'Organisation quotidienne des équipes, suivi des livrables et contrôles qualité.',
    icon: 'list-check',
    actionLabel: 'Nouvelle Tâche',
    kpis: [
      { label: 'Tâches ouvertes', value: '42', sub: 'Sur l\'ensemble des sites', color: 'text-blue-700' },
      { label: 'Critiques / Jalons', value: '5', sub: 'À valider sous 48h', color: 'text-rose-600' },
      { label: 'Achevées cette semaine', value: '28', sub: 'Cadence respectée', color: 'text-emerald-600' },
      { label: 'Taux de conformité', value: '98%', sub: 'Contrôles bureau Veritas', color: 'text-slate-900' },
    ],
    columns: ['Réf. Tâche', 'Désignation', 'Chantier Lié', 'Équipe Affectée', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'TK-840', designation: 'Ferraillage poutres voile R+7', chantier: 'Tour Azur', equipe: 'Équipe Ferrailleurs 1', statut: 'En cours' } },
      { id: 2, data: { reference: 'TK-841', designation: 'Essai de compression éprouvettes béton', chantier: 'Pont Grand-Bassam', equipe: 'Laboratoire Qualité', statut: 'Validés' } },
      { id: 3, data: { reference: 'TK-842', designation: 'Pose caniveaux latéraux PK 12+400', chantier: 'Voie Express', equipe: 'Équipe VRD Nord', statut: 'En cours' } },
      { id: 4, data: { reference: 'TK-843', designation: 'Terrassement plate-forme îlot 3', chantier: 'Songon', equipe: 'Conducteurs Engins', statut: 'En attente' } },
    ],
  },
  '/chantiers/planning': {
    parent: 'Projets & Chantiers',
    title: 'Planning & GANTT',
    description: 'Planification temporelle des phases de construction et chemin critique.',
    icon: 'calendar-days',
    actionLabel: 'Ajuster Planning',
    kpis: [
      { label: 'Jalons franchis', value: '18 / 24', sub: 'Phase en cours', color: 'text-emerald-600' },
      { label: 'Décalage moyen', value: '+1.5 j', sub: 'Marge de sécurité disponible', color: 'text-amber-600' },
      { label: 'Ressources allouées', value: '92 %', sub: 'Optimisation matériels', color: 'text-blue-700' },
      { label: 'Date fin prévisionnelle', value: 'Nov 2026', sub: 'Conforme marché', color: 'text-slate-900' },
    ],
    columns: ['Phase GANTT', 'Chantier', 'Date Début', 'Échéance', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'PH-01', designation: 'Fondations spéciales & Pieux', date_deb: '01/02/2026', date_fin: '30/04/2026', statut: 'Validés' } },
      { id: 2, data: { reference: 'PH-02', designation: 'Élévation structure RDC à R+14', date_deb: '05/05/2026', date_fin: '15/10/2026', statut: 'En cours' } },
      { id: 3, data: { reference: 'PH-03', designation: 'Lots secondaires & Électricité', date_deb: '01/09/2026', date_fin: '15/12/2026', statut: 'En attente' } },
    ],
  },
  // Marchés
  '/marches/appels-offres': {
    parent: 'Marchés',
    title: 'Appels d\'Offres & Soumissions',
    description: 'Prospection, constitution des dossiers de réponse et suivi des adjudications.',
    icon: 'file-contract',
    actionLabel: 'Nouvelle Soumission',
    kpis: [
      { label: 'AO en veille', value: '12', sub: 'Côte d\'Ivoire & Sous-région', color: 'text-blue-700' },
      { label: 'Dossiers déposés', value: '4', sub: 'Montant : 4,1 Mrd FCFA', color: 'text-amber-600' },
      { label: 'Taux de succès', value: '38 %', sub: 'Moyenne sectorielle 25%', color: 'text-emerald-600' },
      { label: 'Prochain dépôt', value: 'J-5', sub: 'Projet CHU Abobo', color: 'text-rose-600' },
    ],
    columns: ['Numéro AO', 'Intitulé Marché', 'Autorité Contractante', 'Cautionnement', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'AO-2026-91', intitule: 'Aménagement voirie urbaine Yopougon', autorite: 'Mairie de Yopougon', caution: '15 000 000 FCFA', statut: 'En cours' } },
      { id: 2, data: { reference: 'AO-2026-88', intitule: 'Construction Hôpital Général 100 Lits', autorite: 'Ministère Santé', caution: '40 000 000 FCFA', statut: 'En attente' } },
      { id: 3, data: { reference: 'AO-2026-75', intitule: 'Élargissement Boulevard VGE', autorite: 'AGEROUTE', caution: '65 000 000 FCFA', statut: 'Validés' } },
    ],
  },
  '/marches/contrats': {
    parent: 'Marchés',
    title: 'Contrats & Avenants',
    description: 'Engagements contractuels, pénalités, révisions de prix et garanties bancaires.',
    icon: 'scroll',
    actionLabel: 'Enregistrer Contrat',
    kpis: [
      { label: 'Contrats actifs', value: '9', sub: 'Portefeuille 3,8 Mrd', color: 'text-emerald-600' },
      { label: 'Avenants validés', value: '3', sub: 'Plus-values : 180 M', color: 'text-amber-600' },
      { label: 'Retenues de garantie', value: '5 %', sub: 'Conforme CCAG', color: 'text-blue-700' },
      { label: 'Garanties actives', value: '8', sub: 'Banques partenaires', color: 'text-slate-900' },
    ],
    columns: ['Réf. Contrat', 'Objet du Contrat', 'Client / Partenaire', 'Montant TTC', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'CT-2026-01', objet: 'Contrat d\'Entreprise Générale Tour Azur', client: 'SCI Laguna', montant: '1 416 000 000 FCFA', statut: 'Validés' } },
      { id: 2, data: { reference: 'CT-2026-02', objet: 'Sous-traitance Pieux Forés', client: 'Fondations Pro CI', montant: '210 000 000 FCFA', statut: 'En cours' } },
    ],
  },
  '/marches/situations': {
    parent: 'Marchés',
    title: 'Situations de Travaux & Décomptes',
    description: 'Décomptes Généraux et Définitifs (DGD), attachements mensuels et validation MOE.',
    icon: 'file-invoice-dollar',
    actionLabel: 'Créer Situation',
    kpis: [
      { label: 'Situations émises', value: '24', sub: 'Sur exercice 2026', color: 'text-blue-700' },
      { label: 'Montant en attente', value: '345 M', sub: 'En cours de visa MOE', color: 'text-amber-600' },
      { label: 'Encaissées ce mois', value: '180 M', sub: 'Délai moyen : 35 jours', color: 'text-emerald-600' },
      { label: 'Taux contestation', value: '0 %', sub: 'Aucun litige métreur', color: 'text-slate-900' },
    ],
    columns: ['N° Situation', 'Chantier', 'Période d\'Avancement', 'Montant HT', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'SIT-AZ-04', chantier: 'Tour Azur', periode: 'Juillet 2026', montant: '125 000 000 FCFA', statut: 'Validés' } },
      { id: 2, data: { reference: 'SIT-AZ-05', chantier: 'Tour Azur', periode: 'Août 2026', montant: '142 000 000 FCFA', statut: 'En attente' } },
      { id: 3, data: { reference: 'SIT-PB-02', chantier: 'Pont Grand-Bassam', periode: 'Août 2026', montant: '98 000 000 FCFA', statut: 'En cours' } },
    ],
  },
  // Achats & Stocks
  '/achats-stocks/achats': {
    parent: 'Achats & Stocks',
    title: 'Bons de Commande & Achats',
    description: 'Approvisionnements chantiers, commandes de matériaux et négociations centrales.',
    icon: 'cart-shopping',
    actionLabel: 'Nouvelle Commande',
    kpis: [
      { label: 'Commandes du mois', value: '54', sub: 'Matériaux et outillage', color: 'text-slate-900' },
      { label: 'En attente livraison', value: '8', sub: 'Livraisons prévues 48h', color: 'text-amber-600' },
      { label: 'Volume d\'achats', value: '240 M', sub: 'Sous contrôle budgétaire', color: 'text-emerald-600' },
      { label: 'Fournisseurs actifs', value: '32', sub: 'Agréés BTP', color: 'text-blue-700' },
    ],
    columns: ['N° Bon Commande', 'Fournisseur', 'Destination Chantier', 'Montant TTC', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'BC-2026-112', fournisseur: 'Ciment LafargeHolcim', chantier: 'Tour Azur', montant: '45 000 000 FCFA', statut: 'Validés' } },
      { id: 2, data: { reference: 'BC-2026-113', fournisseur: 'SOTACI Aciers', chantier: 'Pont Bassam', montant: '62 000 000 FCFA', statut: 'En cours' } },
      { id: 3, data: { reference: 'BC-2026-114', fournisseur: 'Carrière d\'Akoupé', chantier: 'Voie Express', montant: '18 500 000 FCFA', statut: 'En attente' } },
    ],
  },
  '/achats-stocks/fournisseurs': {
    parent: 'Achats & Stocks',
    title: 'Répertoire Fournisseurs & Sous-traitants',
    description: 'Évaluation qualité, délais de paiement et homologation des prestataires.',
    icon: 'handshake',
    actionLabel: 'Ajouter Fournisseur',
    kpis: [
      { label: 'Fournisseurs homologués', value: '48', sub: 'Grands comptes et régionaux', color: 'text-emerald-600' },
      { label: 'Note moyenne', value: '4.7 / 5', sub: 'Évaluation chantiers', color: 'text-amber-600' },
      { label: 'Sous-traitants clés', value: '16', sub: 'Fluides, Élec, Peinture', color: 'text-blue-700' },
      { label: 'Délai moyen règlement', value: '30 jours', sub: 'Respect des accords', color: 'text-slate-900' },
    ],
    columns: ['Code Tiers', 'Raison Sociale', 'Spécialité Matériau', 'Téléphone', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'FR-001', nom: 'LafargeHolcim Côte d\'Ivoire', spec: 'Ciments & Béton prêt à l\'emploi', tel: '+225 27 21 00 00', statut: 'Validés' } },
      { id: 2, data: { reference: 'FR-002', nom: 'SOTACI', spec: 'Fers à béton, Treillis soudés', tel: '+225 27 23 00 00', statut: 'Validés' } },
      { id: 3, data: { reference: 'FR-003', nom: 'Carrière Roches Noires', spec: 'Agrégats, Ballast, Gravillons', tel: '+225 07 08 00 00', statut: 'Validés' } },
    ],
  },
  '/achats-stocks/materiaux': {
    parent: 'Achats & Stocks',
    title: 'Catalogue Matériaux & Mercuriale',
    description: 'Nomenclature des articles BTP, fiches techniques et coûts unitaires.',
    icon: 'trowel-bricks',
    actionLabel: 'Ajouter Article',
    kpis: [
      { label: 'Références cataloguées', value: '340', sub: 'Nomenclature interne', color: 'text-slate-900' },
      { label: 'Prix négociés', value: '100 %', sub: 'Mercuriale 2026', color: 'text-emerald-600' },
      { label: 'Normes CE / NI', value: 'Conformes', sub: 'Certificats de traçabilité', color: 'text-blue-700' },
      { label: 'Variation coûts', value: '+2.1 %', sub: 'Indice BT01 national', color: 'text-amber-600' },
    ],
    columns: ['Code Article', 'Désignation Matériau', 'Unité', 'Prix Unitaire Réf.', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'MAT-01', nom: 'Ciment CPJ 42.5 (Sac 50kg)', unit: 'Sac', pu: '4 800 FCFA', statut: 'Validés' } },
      { id: 2, data: { reference: 'MAT-02', nom: 'Fer à béton HA 12 (Barre 12m)', unit: 'Tonne', pu: '620 000 FCFA', statut: 'Validés' } },
      { id: 3, data: { reference: 'MAT-03', nom: 'Sable lagunaire lavé 0/4', unit: 'm³', pu: '12 500 FCFA', statut: 'Validés' } },
    ],
  },
  '/achats-stocks/stocks': {
    parent: 'Achats & Stocks',
    title: 'Inventaires & Stocks Dépôts',
    description: 'Suivi des réceptions, sorties chantiers, alertes de réapprovisionnement et valorisation.',
    icon: 'boxes-stacked',
    actionLabel: 'Mouvement Stock',
    kpis: [
      { label: 'Valeur globale stock', value: '185 M FCFA', sub: '3 dépôts centraux', color: 'text-emerald-600' },
      { label: 'Alertes stock bas', value: '3', sub: 'Ciment et carburant', color: 'text-rose-600' },
      { label: 'Taux de rotation', value: '18 jours', sub: 'Flux tendu chantiers', color: 'text-blue-700' },
      { label: 'Dernier inventaire', value: '31/08/2026', sub: 'Écart : 0.4%', color: 'text-slate-900' },
    ],
    columns: ['Réf. Dépôt', 'Article', 'Quantité Disponible', 'Seuil Alerte', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'DEP-VRD', nom: 'Tuyaux PEHD D200 PN16', qte: '180 barres', seuil: '50 barres', statut: 'Validés' } },
      { id: 2, data: { reference: 'DEP-CIM', nom: 'Ciment Cujas 42.5', qte: '450 sacs', seuil: '600 sacs', statut: 'En attente' } },
      { id: 3, data: { reference: 'DEP-GO', nom: 'Treillis anti-fissuration PAF', qte: '120 panneaux', seuil: '30 panneaux', statut: 'Validés' } },
    ],
  },
  // Engins & Équipements
  '/engins': {
    parent: 'Engins & Équipements',
    title: 'Parc Engins & Véhicules BTP',
    description: 'Affectation des pelles, grues, camions et suivi des compteurs horaires.',
    icon: 'truck-pickup',
    actionLabel: 'Ajouter Engin',
    kpis: [
      { label: 'Engins opérationnels', value: '28 / 32', sub: 'Taux de dispo : 87.5%', color: 'text-emerald-600' },
      { label: 'Sur chantiers', value: '24', sub: 'Actifs aujourd\'hui', color: 'text-blue-700' },
      { label: 'En révision', value: '4', sub: 'Atelier mécanique central', color: 'text-amber-600' },
      { label: 'Consommation gasoil', value: '1 240 L/j', sub: 'Contrôlé par sonde GPS', color: 'text-slate-900' },
    ],
    columns: ['Code Engin', 'Modèle / Marque', 'Chantier Affecté', 'Compteur Heures', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'ENG-P01', modele: 'Pelle CAT 336 GC', chantier: 'Tour Azur', heures: '3 450 h', statut: 'En cours' } },
      { id: 2, data: { reference: 'ENG-G01', modele: 'Grue à Tour Potain MDT 219', chantier: 'Tour Azur', heures: '1 820 h', statut: 'Validés' } },
      { id: 3, data: { reference: 'ENG-C04', modele: 'Camion Benne 8x4 Mercedes', chantier: 'Voie Express', heures: '78 000 km', statut: 'En cours' } },
      { id: 4, data: { reference: 'ENG-B02', modele: 'Bulldozer Komatsu D65', chantier: 'Atelier', heures: '4 120 h', statut: 'En attente' } },
    ],
  },
  '/engins/maintenance': {
    parent: 'Engins & Équipements',
    title: 'Maintenance Préventive & Curative',
    description: 'Planning des vidanges, remplacements hydrauliques et carnets d\'entretien.',
    icon: 'wrench',
    actionLabel: 'Ordre de Travail',
    kpis: [
      { label: 'Entretiens prévus J+7', value: '6', sub: 'Vidanges et filtres', color: 'text-amber-600' },
      { label: 'Temps d\'arrêt moyen', value: '4.2 h', sub: 'Objectif < 6h', color: 'text-emerald-600' },
      { label: 'Coût pièces ce mois', value: '8.4 M FCFA', sub: 'Sous budget', color: 'text-blue-700' },
      { label: 'Contrôles périodiques', value: '100 %', sub: 'Conformité ministérielle', color: 'text-slate-900' },
    ],
    columns: ['N° Fiche OT', 'Engin Concerné', 'Nature Intervention', 'Technicien Responsable', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'OT-491', engin: 'Pelle CAT 336 GC', nature: 'Vidange moteur 500h + Filtres', tech: 'M. Touré (Chef Atelier)', statut: 'Validés' } },
      { id: 2, data: { reference: 'OT-492', engin: 'Grue Potain MDT 219', nature: 'Graissage câbles & contrôle fins de course', tech: 'Apave Inspection', statut: 'Validés' } },
      { id: 3, data: { reference: 'OT-493', engin: 'Bulldozer Komatsu D65', nature: 'Réfection vérin de lame', tech: 'Atelier Central', statut: 'En cours' } },
    ],
  },
  // Ressources Humaines
  '/rh/employes': {
    parent: 'Ressources Humaines',
    title: 'Gestion du Personnel & Pointage',
    description: 'Fiches salariés, habilitations sécurité BTP, visites médicales et pointages terrain.',
    icon: 'users-gear',
    actionLabel: 'Nouveau Salarié',
    kpis: [
      { label: 'Effectif total BTP', value: '156', sub: 'CDI, CDD et Intérim', color: 'text-slate-900' },
      { label: 'Présents sur sites', value: '142', sub: 'Taux présence 96.2%', color: 'text-emerald-600' },
      { label: 'Habilitations à jour', value: '98 %', sub: 'Travail en hauteur, CACES', color: 'text-blue-700' },
      { label: 'Visites médicales', value: '3 à planifier', sub: 'Médecine du travail', color: 'text-amber-600' },
    ],
    columns: ['Matricule', 'Nom & Prénom', 'Poste / Qualification', 'Affectation Principale', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'EMP-014', nom: 'Kouassi Konan', poste: 'Conducteur de Travaux Principal', affectation: 'Tour Azur', statut: 'Validés' } },
      { id: 2, data: { reference: 'EMP-089', nom: 'Diallo Mamadou', poste: 'Grutier CACES R487', affectation: 'Tour Azur', statut: 'Validés' } },
      { id: 3, data: { reference: 'EMP-112', nom: 'Yao N\'Dri', poste: 'Chef d\'Équipe VRD', affectation: 'Pont Grand-Bassam', statut: 'Validés' } },
      { id: 4, data: { reference: 'EMP-145', nom: 'Traoré Bakary', poste: 'Mécanicien Engins Lourds', affectation: 'Atelier Central', statut: 'Validés' } },
    ],
  },
  '/rh/equipes': {
    parent: 'Ressources Humaines',
    title: 'Équipes & Brigades Chantiers',
    description: 'Constitution des équipes spécialisées, chefs d\'équipes et rotations de quarts.',
    icon: 'people-group',
    actionLabel: 'Créer Brigade',
    kpis: [
      { label: 'Brigades actives', value: '14', sub: 'Réparties sur 8 sites', color: 'text-emerald-600' },
      { label: 'Taille moyenne équipe', value: '10 ouvriers', sub: 'Ratio encadrement optimal', color: 'text-slate-900' },
      { label: 'Heures sup. contrôlées', value: '4.2 %', sub: 'Respect convention BTP', color: 'text-amber-600' },
      { label: 'Taux sécurité', value: '0 accident', sub: '180 jours sans AT', color: 'text-blue-700' },
    ],
    columns: ['Code Brigade', 'Spécialité Travaux', 'Chef de Brigade', 'Membres', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'EQ-01', spec: 'Coffrage & Béton Armé', chef: 'A. Koffi', membres: '14 ouvriers', statut: 'Validés' } },
      { id: 2, data: { reference: 'EQ-02', spec: 'Ferraillage Voiles & Radier', chef: 'I. Diop', membres: '12 ouvriers', statut: 'Validés' } },
      { id: 3, data: { reference: 'EQ-03', spec: 'Terrassement & Compactage', chef: 'O. Coulibaly', membres: '8 conducteurs', statut: 'Validés' } },
    ],
  },
  // Finance
  '/finance': {
    parent: 'Finance',
    title: 'Gestion Financière & Trésorerie BTP',
    description: 'Flux de trésorerie, facturation clients, encaissements et suivi des marges chantiers.',
    icon: 'wallet',
    actionLabel: 'Saisie Opération',
    kpis: [
      { label: 'Chiffre d\'Affaires YTD', value: '2,45 Mrd FCFA', sub: '+18.4% vs N-1', color: 'text-emerald-600' },
      { label: 'Facturation Encaissée', value: '1,82 Mrd FCFA', sub: 'Reste à recouvrer : 630 M', color: 'text-slate-900' },
      { label: 'Marge Opérationnelle', value: '24.5 %', sub: 'Objectif société 22%', color: 'text-amber-600' },
      { label: 'Trésorerie Disponible', value: '412 M FCFA', sub: 'Positions bancaires saines', color: 'text-blue-700' },
    ],
    columns: ['Réf. Flux', 'Libellé de l\'Opération', 'Compte / Chantier', 'Montant FCFA', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'ENC-2026-89', libelle: 'Règlement Acompte Situation N°3 SCI Laguna', chantier: 'Tour Azur', montant: '+142 000 000 FCFA', statut: 'Validés' } },
      { id: 2, data: { reference: 'DEC-2026-44', libelle: 'Paiement Facture Ciment LafargeHolcim', chantier: 'Fournisseurs', montant: '-45 000 000 FCFA', statut: 'Validés' } },
      { id: 3, data: { reference: 'DEC-2026-45', libelle: 'Virement Paie Salariés & Ouvriers Août', chantier: 'RH & Personnel', montant: '-38 400 000 FCFA', statut: 'Validés' } },
    ],
  },
  // Rapports
  '/rapports': {
    parent: 'Pilotage',
    title: 'Rapports d\'Activité & Métriques',
    description: 'Génération automatique des synthèses hebdomadaires, mensuelles et audits HSE.',
    icon: 'chart-pie',
    actionLabel: 'Générer Synthèse',
    kpis: [
      { label: 'Rapports générés', value: '38', sub: 'Ce trimestre', color: 'text-slate-900' },
      { label: 'Conformité planning', value: '96.2 %', sub: 'Moyenne consolidée', color: 'text-emerald-600' },
      { label: 'Rapports HSE / Sécurité', value: '100 %', sub: 'Zéro non-conformité grave', color: 'text-blue-700' },
      { label: 'Indice de performance', value: '1.08', sub: 'Avance sur coût & délais', color: 'text-amber-600' },
    ],
    columns: ['ID Rapport', 'Type de Document', 'Période Couverte', 'Auteur / Rôle', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'RAP-HEB-36', type: 'Synthèse Hebdomadaire Chantiers', periode: 'Semaine 36 (Sept 2026)', auteur: 'Direction Technique', statut: 'Validés' } },
      { id: 2, data: { reference: 'RAP-FIN-08', type: 'Bilan Mensuel Trésorerie & Marges', periode: 'Août 2026', auteur: 'Direction Financière', statut: 'Validés' } },
      { id: 3, data: { reference: 'AUD-HSE-04', type: 'Audit Sécurité & Environnement', periode: 'T3 2026', auteur: 'Responsable QHSE', statut: 'Validés' } },
    ],
  },
  // Paramètres & Préférences
  '/parametres': {
    parent: 'Configuration',
    title: 'Paramètres Généraux de l\'Entreprise',
    description: 'TVA, devises (FCFA), numérotation automatique des devis et gestion des dépôts.',
    icon: 'gear',
    actionLabel: 'Modifier Paramètres',
    kpis: [
      { label: 'Devise de référence', value: 'FCFA (XOF)', sub: 'Fixe zone UEMOA', color: 'text-blue-700' },
      { label: 'Taux TVA standard', value: '18.0 %', sub: 'Régime réel BTP', color: 'text-slate-900' },
      { label: 'Retenue de garantie', value: '5.0 %', sub: 'Délai légal 12 mois', color: 'text-emerald-600' },
      { label: 'API Backend', value: 'FastAPI v0.109', sub: 'PostgreSQL Connecté', color: 'text-blue-700' },
    ],
    columns: ['Code Paramètre', 'Clé de Configuration', 'Valeur Actuelle', 'Description', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'CONF-CURR', cle: 'DEFAULT_CURRENCY', val: 'FCFA', desc: 'Devise par défaut de tous les chantiers', statut: 'Validés' } },
      { id: 2, data: { reference: 'CONF-TVA', cle: 'DEFAULT_TVA_RATE', val: '18%', desc: 'Taux TVA par défaut marchés publics', statut: 'Validés' } },
      { id: 3, data: { reference: 'CONF-RET', cle: 'DEFAULT_WARRANTY_HOLD', val: '5%', desc: 'Retenue de garantie sur situations', statut: 'Validés' } },
    ],
  },
  '/preferences': {
    parent: 'Configuration',
    title: 'Préférences & Notifications',
    description: 'Alertes e-mail chantiers, alertes stocks bas et seuils de validation budgétaires.',
    icon: 'bell',
    actionLabel: 'Enregistrer Choix',
    kpis: [
      { label: 'Canaux actifs', value: 'Email + In-App', sub: 'Notifications instantanées', color: 'text-blue-700' },
      { label: 'Alerte stock seuil', value: '< 20%', sub: 'Déclenchement réappro', color: 'text-amber-600' },
      { label: 'Validation requise', value: '> 5 M FCFA', sub: 'Double signature Owner', color: 'text-emerald-600' },
      { label: 'Sauvegarde auto', value: 'Temps réel', sub: 'PostgreSQL Cloud Sync', color: 'text-slate-900' },
    ],
    columns: ['Type Alerte', 'Canal Notif', 'Condition Déclencheur', 'Destinataires', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'NOTIF-01', canal: 'Email + Cloche', condition: 'Dépassement budget chantier > 5%', dest: 'Owner, Directeur', statut: 'Validés' } },
      { id: 2, data: { reference: 'NOTIF-02', canal: 'In-App', condition: 'Stock ciment < 100 sacs', dest: 'Conducteur de travaux', statut: 'Validés' } },
    ],
  },
}

// Config actuelle basée sur la route active
const moduleConfig = computed(() => {
  return moduleConfigs[route.path] || {
    parent: 'Module ERP',
    title: 'Gestion Opérationnelle',
    description: 'Module en cours de déploiement dans le cadre de l\'ERP BTP.',
    icon: 'helmet-safety',
    actionLabel: 'Nouvelle Entrée',
    kpis: [
      { label: 'Statut Module', value: 'Actif', sub: 'Connecté FastAPI', color: 'text-emerald-600' },
      { label: 'Enregistrements', value: '18', sub: 'Base PostgreSQL', color: 'text-blue-700' },
      { label: 'Dernière Synchro', value: 'À l\'instant', sub: 'Temps réel', color: 'text-slate-900' },
      { label: 'Permissions', value: 'RBAC Validé', sub: 'Rôle autorisé', color: 'text-emerald-600' },
    ],
    columns: ['Identifiant', 'Libellé', 'Détails', 'Statut'],
    sampleData: [
      { id: 1, data: { reference: 'ENT-001', libelle: 'Enregistrement Standard 1', details: 'Données opérationnelles validées', statut: 'Validés' } },
      { id: 2, data: { reference: 'ENT-002', libelle: 'Enregistrement Standard 2', details: 'En attente de visa responsable', statut: 'En cours' } },
    ],
  }
})

// Configuration dynamique des colonnes pour le DataTable partagé
const tableColumns = computed(() => {
  if (!moduleConfig.value || !moduleConfig.value.columns) return []
  const sample = (moduleConfig.value.sampleData && moduleConfig.value.sampleData[0]) ? moduleConfig.value.sampleData[0].data : {}
  const dataKeys = Object.keys(sample)

  return moduleConfig.value.columns.map((colName, index) => {
    const key = dataKeys[index] || `col_${index}`
    return {
      key,
      label: colName,
      sortable: true
    }
  })
})

// Éléments du tableau avec onglets de statut
const tableItems = computed(() => {
  let rows = moduleConfig.value.sampleData || []
  if (activeTab.value !== 'Tous') {
    rows = rows.filter(r => r.data && r.data.statut === activeTab.value)
  }
  return rows.map(r => ({
    id: r.id,
    ...r.data,
    _raw: r
  }))
})

function getStatusBadgeClass(status) {
  switch (status) {
    case 'Validés':
    case 'Validé':
    case 'Terminé':
    case 'Actif':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    case 'En cours':
      return 'bg-blue-50 text-blue-700 border border-blue-200'
    case 'En attente':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'Retard':
    case 'Alerte':
      return 'bg-rose-50 text-rose-700 border border-rose-200'
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-200'
  }
}

// Interaction et navigation
function handleRowAction(row) {
  if (route.path === '/chantiers') {
    // Naviguer vers la vue détaillée du chantier avec les 9 onglets
    router.push(`/chantiers/${row.id}`)
  } else {
    // Afficher les détails via SweetAlert2
    const detailsHtml = Object.entries(row.data)
      .map(([k, v]) => `<div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13px; text-align:left;"><strong>${k.toUpperCase()} :</strong> <span>${v}</span></div>`)
      .join('')
    alertSuccess(`Fiche : ${row.data.reference || 'Élément'}`, detailsHtml)
  }
}

async function handleEditRow(row) {
  toast(`Édition de l'enregistrement ${row.data.reference || row.id}`, 'info')
}

async function handleDeleteRow(row) {
  const ok = await confirmDialog(
    'Confirmer la suppression ?',
    `Êtes-vous sûr de vouloir supprimer ${row.data.reference || 'cet élément'} définitivement de la base ?`,
    'Supprimer'
  )
  if (ok) {
    toast(`Élément ${row.data.reference || ''} supprimé avec succès`, 'success')
  }
}

function handleExport() {
  toast(`Export Excel / PDF du module ${moduleConfig.value.title} en cours...`, 'info')
  setTimeout(() => {
    alertSuccess('Exportation Terminée', `Le fichier Excel et le bordereau PDF de "${moduleConfig.value.title}" ont été générés avec succès.`)
  }, 900)
}

function handleCreate() {
  if (route.path === '/chantiers') {
    router.push('/chantiers/nouveau')
  } else {
    alertSuccess(`Création - ${moduleConfig.value.title}`, `Ouverture du formulaire de création pour : ${moduleConfig.value.actionLabel}`)
  }
}
</script>
