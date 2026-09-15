<template>
  <div class="role-view">
    <div class="role-header">
      <div class="badge-role">📋 ESPACE MANAGER — CONDUCTEUR DE TRAVAUX & CHEF DE PROJET</div>
      <h2>Pilotage Opérationnel des Chantiers</h2>
      <p>Suivi des plannings, commandes de matériaux, contrôle des tâches et attachements</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">Mes Chantiers Assignés</span>
        <span class="kpi-value">3 Projets</span>
        <span class="kpi-sub">École Bingerville • Immeuble Cocody • Voie Yopougon</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Tâches en Cours</span>
        <span class="kpi-value">24 Tâches</span>
        <span class="kpi-sub highlight">3 en retard de planning</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Demandes d'Achat</span>
        <span class="kpi-value">6 en Attente</span>
        <span class="kpi-sub">Ciment, fers à béton, gravier</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Prochaine Situation</span>
        <span class="kpi-value">Situation N° 4</span>
        <span class="kpi-sub success">Clôture fin de quinzaine</span>
      </div>
    </div>

    <div class="info-box">
      <h3>🛠️ Outils Conduite de Travaux</h3>
      <ul>
        <li>📐 <strong>Phases & Tâches</strong> : Découpage WBS du chantier (Fondations, Gros Œuvre, Second Œuvre, Finitions).</li>
        <li>📦 <strong>Approvisionnements & Stocks</strong> : Émission des bons de commande et réceptions sur site.</li>
        <li>📈 <strong>Avancement Pondéré</strong> : Calcul précis basé sur les métrés réels constatés par les chefs de chantier.</li>
        <li>📑 <strong>Préparation des Situations</strong> : Génération automatique des propositions de situations pour le client.</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.role-view { display: flex; flex-direction: column; gap: 2rem; }
.role-header h2 { font-size: 1.8rem; color: #fff; margin: 0.4rem 0; }
.role-header p { color: var(--text-secondary); }
.badge-role { display: inline-block; padding: 0.3rem 0.8rem; background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.kpi-title { font-size: 0.85rem; color: var(--text-secondary); }
.kpi-value { font-size: 1.5rem; font-weight: 800; color: #fff; }
.kpi-sub { font-size: 0.8rem; color: var(--text-muted); }
.kpi-sub.highlight { color: #f59e0b; }
.kpi-sub.success { color: var(--status-success); }
.info-box { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 2rem; }
.info-box h3 { color: #fff; margin-bottom: 1.2rem; font-size: 1.1rem; }
.info-box ul { display: flex; flex-direction: column; gap: 0.9rem; list-style: none; color: var(--text-secondary); }
.info-box li strong { color: #fff; }
</style>
