<template>
  <div class="role-view">
    <div class="role-header">
      <div class="badge-role">🏢 ESPACE OWNER — PROPRIÉTAIRE & DIRECTION</div>
      <h2>Tableau de Bord Stratégique BTP</h2>
      <p>Supervision générale des chantiers, indicateurs de rentabilité, marge et trésorerie</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">Portefeuille Chantiers</span>
        <span class="kpi-value">12 Projets</span>
        <span class="kpi-sub">8 en cours • 4 en préparation</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Montant Global Contrats</span>
        <span class="kpi-value">2 450 000 000 FCFA</span>
        <span class="kpi-sub highlight">Objectif annuel en hausse</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Marge Réalisée Estimée</span>
        <span class="kpi-value">24.5 %</span>
        <span class="kpi-sub success">Conforme aux prévisions</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Facturation & Règlements</span>
        <span class="kpi-value">1 820 000 000 FCFA</span>
        <span class="kpi-sub">Solde à recouvrer : 630 M</span>
      </div>
    </div>

    <div class="info-box">
      <h3>🚀 Modules Stratégiques de l'Espace Propriétaire</h3>
      <ul>
        <li>📊 <strong>Rentabilité Globale</strong> : Analyse comparative Budget Prévu vs Dépenses Réelles par chantier.</li>
        <li>📑 <strong>Validation des Contrats</strong> : Validation des montants, avances et retenues de garantie.</li>
        <li>💰 <strong>Suivi de Trésorerie</strong> : Règlements clients et échéanciers fournisseurs / sous-traitants.</li>
        <li>🏗️ <strong>Cartographie des Projets</strong> : Localisation des chantiers sur l'étendue du territoire.</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.role-view { display: flex; flex-direction: column; gap: 2rem; }
.role-header h2 { font-size: 1.8rem; color: #fff; margin: 0.4rem 0; }
.role-header p { color: var(--text-secondary); }
.badge-role { display: inline-block; padding: 0.3rem 0.8rem; background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.kpi-title { font-size: 0.85rem; color: var(--text-secondary); }
.kpi-value { font-size: 1.5rem; font-weight: 800; color: #fff; }
.kpi-sub { font-size: 0.8rem; color: var(--text-muted); }
.kpi-sub.highlight { color: var(--accent-btp); }
.kpi-sub.success { color: var(--status-success); }
.info-box { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 2rem; }
.info-box h3 { color: #fff; margin-bottom: 1.2rem; font-size: 1.1rem; }
.info-box ul { display: flex; flex-direction: column; gap: 0.9rem; list-style: none; color: var(--text-secondary); }
.info-box li strong { color: #fff; }
</style>
