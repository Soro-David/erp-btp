<template>
  <div class="role-view">
    <div class="role-header">
      <div class="badge-role">📐 ESPACE DIRECTOR — DIRECTION TECHNIQUE & GÉNÉRALE</div>
      <h2>Supervision Technique & Opérationnelle</h2>
      <p>Appels d'offres, validation des situations de travaux et gestion des ressources globales</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">Appels d'Offres en Cours</span>
        <span class="kpi-value">5 Dossiers</span>
        <span class="kpi-sub">3 en analyse • 2 soumis</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Situations à Valider</span>
        <span class="kpi-value highlight">4 Situations</span>
        <span class="kpi-sub">Montant cumulé : 142 000 000 FCFA</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Taux d'Avancement Moyen</span>
        <span class="kpi-value">68.2 %</span>
        <span class="kpi-sub success">+4.5% ce mois-ci</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Parc Engins Mobilisé</span>
        <span class="kpi-value">18 / 22</span>
        <span class="kpi-sub">4 en maintenance préventive</span>
      </div>
    </div>

    <div class="info-box">
      <h3>📋 Responsabilités de la Direction Technique</h3>
      <ul>
        <li>📑 <strong>Validation des Situations de Travaux</strong> : Contrôle des attachements et des retenues contractuelles.</li>
        <li>⚖️ <strong>Études de Prix & Devis</strong> : Supervision des réponses aux appels d'offres publics et privés.</li>
        <li>🚜 <strong>Parc d'Équipements Lourds</strong> : Affectation des pelleteuses, grues et compacteurs selon les plannings chantiers.</li>
        <li>👷 <strong>Supervision des Équipes</strong> : Coordination entre les conducteurs de travaux et chefs de projets.</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.role-view { display: flex; flex-direction: column; gap: 2rem; }
.role-header h2 { font-size: 1.8rem; color: #fff; margin: 0.4rem 0; }
.role-header p { color: var(--text-secondary); }
.badge-role { display: inline-block; padding: 0.3rem 0.8rem; background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.kpi-title { font-size: 0.85rem; color: var(--text-secondary); }
.kpi-value { font-size: 1.5rem; font-weight: 800; color: #fff; }
.kpi-value.highlight { color: #f59e0b; }
.kpi-sub { font-size: 0.8rem; color: var(--text-muted); }
.kpi-sub.success { color: var(--status-success); }
.info-box { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 2rem; }
.info-box h3 { color: #fff; margin-bottom: 1.2rem; font-size: 1.1rem; }
.info-box ul { display: flex; flex-direction: column; gap: 0.9rem; list-style: none; color: var(--text-secondary); }
.info-box li strong { color: #fff; }
</style>
