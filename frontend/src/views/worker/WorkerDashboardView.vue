<template>
  <div class="role-view">
    <div class="role-header">
      <div class="badge-role">👷 ESPACE WORKER — CHEF DE CHANTIER & TERRAIN</div>
      <h2>Saisie & Rapports de Chantier Quotidiens</h2>
      <p>Pointage ouvriers, saisie des quantités produites et consommation des matériaux</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">Mon Chantier Aujourd'hui</span>
        <span class="kpi-value">Chantier Cocody</span>
        <span class="kpi-sub">Phase : Gros Œuvre - R+2</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Effectif sur Site</span>
        <span class="kpi-value">28 Ouvriers</span>
        <span class="kpi-sub success">Pointage du matin validé</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Béton Coulé ce jour</span>
        <span class="kpi-value">45 m³</span>
        <span class="kpi-sub">Dalle supérieure</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Consommation Ciment</span>
        <span class="kpi-value">120 Sacs CPJ 42.5</span>
        <span class="kpi-sub">Stock restant : 350 sacs</span>
      </div>
    </div>

    <div class="info-box">
      <h3>📱 Outils de Saisie Mobile & Terrain</h3>
      <ul>
        <li>⏱️ <strong>Pointage d'Équipe</strong> : Enregistrement rapide des heures de présence, maçons, ferrailleurs, coffreurs.</li>
        <li>🧱 <strong>Bons de Sortie Matériaux</strong> : Sortie de fer à béton, sacs de ciment, sable et agrégats.</li>
        <li>📏 <strong>Saisie d'Avancement Réalisé</strong> : Renseignement des volumes et métrés exécutés sur chaque tâche.</li>
        <li>📷 <strong>Journal de Chantier & Photos</strong> : Remontée des constats météo, blocages et incidents en direct.</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.role-view { display: flex; flex-direction: column; gap: 2rem; }
.role-header h2 { font-size: 1.8rem; color: #fff; margin: 0.4rem 0; }
.role-header p { color: var(--text-secondary); }
.badge-role { display: inline-block; padding: 0.3rem 0.8rem; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.kpi-title { font-size: 0.85rem; color: var(--text-secondary); }
.kpi-value { font-size: 1.5rem; font-weight: 800; color: #fff; }
.kpi-sub { font-size: 0.8rem; color: var(--text-muted); }
.kpi-sub.success { color: var(--status-success); }
.info-box { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 2rem; }
.info-box h3 { color: #fff; margin-bottom: 1.2rem; font-size: 1.1rem; }
.info-box ul { display: flex; flex-direction: column; gap: 0.9rem; list-style: none; color: var(--text-secondary); }
.info-box li strong { color: #fff; }
</style>
