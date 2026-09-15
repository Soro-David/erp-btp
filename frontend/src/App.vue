<template>
  <div class="app-wrapper">
    <!-- En-tête de l'ERP -->
    <header class="header">
      <div class="brand">
        <div class="brand-icon">🏗️</div>
        <div>
          <h1 class="brand-title">BTP MANAGER</h1>
          <p class="brand-subtitle">ERP Spécialisé BTP & Génie Civil — Côte d'Ivoire & Afrique Francophone</p>
        </div>
      </div>
      <div class="env-badge">
        <span class="status-dot"></span>
        <span>Environnement Local (Phase 1)</span>
      </div>
    </header>

    <!-- Contenu Principal -->
    <main class="main-container">
      <!-- Bannière de phase -->
      <section class="banner">
        <div class="banner-content">
          <div class="banner-tag">PHASE 1 — INFRASTRUCTURE & SOCLE TECHNIQUE</div>
          <h2>Validation de la chaîne technique complète</h2>
          <p>
            Vérification en temps réel de la communication bidirectionnelle entre le client web 
            <strong>Vue.js 3</strong>, l'API REST <strong>FastAPI (Python)</strong> et la base de données relationnelle <strong>PostgreSQL 16</strong>.
          </p>
        </div>
        <div class="banner-action">
          <button 
            class="btn-refresh" 
            :disabled="loading" 
            @click="checkHealth"
          >
            <span :class="{ 'spin': loading }">🔄</span>
            <span>{{ loading ? 'Test en cours...' : 'Tester la connexion' }}</span>
          </button>
        </div>
      </section>

      <!-- Schéma de liaison en direct -->
      <section class="pipeline-container">
        <div class="pipeline-node node-frontend">
          <div class="node-icon">💻</div>
          <div class="node-title">Frontend</div>
          <div class="node-detail">Vue 3 + Vite</div>
          <span class="badge badge-success">Actif</span>
        </div>

        <div class="pipeline-connector" :class="{ 'connected': backendOnline }">
          <div class="connector-line"></div>
          <div class="connector-arrow">➔</div>
          <span class="connector-label">HTTP / CORS</span>
        </div>

        <div class="pipeline-node node-backend">
          <div class="node-icon">⚡</div>
          <div class="node-title">Backend API</div>
          <div class="node-detail">FastAPI (Python)</div>
          <span 
            class="badge" 
            :class="backendOnline ? 'badge-success' : 'badge-error'"
          >
            {{ backendOnline ? 'Connecté' : 'Hors ligne' }}
          </span>
        </div>

        <div class="pipeline-connector" :class="{ 'connected': dbOnline }">
          <div class="connector-line"></div>
          <div class="connector-arrow">➔</div>
          <span class="connector-label">SQLAlchemy / TCP</span>
        </div>

        <div class="pipeline-node node-db">
          <div class="node-icon">🗄️</div>
          <div class="node-title">Base de Données</div>
          <div class="node-detail">PostgreSQL 16</div>
          <span 
            class="badge" 
            :class="dbOnline ? 'badge-success' : 'badge-error'"
          >
            {{ dbOnline ? 'Opérationnel' : 'Inaccessible' }}
          </span>
        </div>
      </section>

      <!-- Cartes de Diagnostic -->
      <section class="cards-grid">
        <!-- Carte Frontend -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span class="card-emoji">🎨</span>
              <h3>1. Frontend Client</h3>
            </div>
            <span class="badge badge-success">OK</span>
          </div>
          <div class="card-body">
            <div class="detail-row">
              <span class="label">Framework :</span>
              <span class="val">Vue.js 3.4 (Composition API)</span>
            </div>
            <div class="detail-row">
              <span class="label">Bundler :</span>
              <span class="val">Vite 5 (Hot Reload)</span>
            </div>
            <div class="detail-row">
              <span class="label">Gestion d'état :</span>
              <span class="val">Pinia Store</span>
            </div>
            <div class="detail-row">
              <span class="label">Client HTTP :</span>
              <span class="val">Axios</span>
            </div>
            <div class="detail-row">
              <span class="label">Port Hôte :</span>
              <span class="val highlight">5173</span>
            </div>
          </div>
        </div>

        <!-- Carte Backend -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span class="card-emoji">⚙️</span>
              <h3>2. API REST Backend</h3>
            </div>
            <span 
              class="badge" 
              :class="backendOnline ? 'badge-success' : 'badge-error'"
            >
              {{ backendOnline ? 'En ligne' : 'Injoignable' }}
            </span>
          </div>
          <div class="card-body">
            <div class="detail-row">
              <span class="label">Moteur :</span>
              <span class="val">FastAPI (Python 3.12)</span>
            </div>
            <div class="detail-row">
              <span class="label">Endpoint testé :</span>
              <span class="val code">/api/v1/health</span>
            </div>
            <div class="detail-row">
              <span class="label">Documentation :</span>
              <a href="http://localhost:8000/docs" target="_blank" class="val link">Swagger UI (/docs) ↗</a>
            </div>
            <div class="detail-row">
              <span class="label">Latence API :</span>
              <span class="val" :class="{ 'highlight': backendLatency }">
                {{ backendLatency ? backendLatency + ' ms' : '—' }}
              </span>
            </div>
            <div class="detail-row">
              <span class="label">Port Hôte :</span>
              <span class="val highlight">8000</span>
            </div>
          </div>
        </div>

        <!-- Carte Base de Données -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span class="card-emoji">🐘</span>
              <h3>3. PostgreSQL</h3>
            </div>
            <span 
              class="badge" 
              :class="dbOnline ? 'badge-success' : 'badge-error'"
            >
              {{ dbOnline ? 'Connecté' : 'Non détecté' }}
            </span>
          </div>
          <div class="card-body">
            <div class="detail-row">
              <span class="label">SGBD :</span>
              <span class="val">PostgreSQL 16 Alpine</span>
            </div>
            <div class="detail-row">
              <span class="label">Nom de la base :</span>
              <span class="val code">{{ healthData?.database?.version ? 'btp_manager' : '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">ORM :</span>
              <span class="val">SQLAlchemy 2.0</span>
            </div>
            <div class="detail-row">
              <span class="label">Latence DB :</span>
              <span class="val" :class="{ 'highlight': healthData?.database?.latency_ms }">
                {{ healthData?.database?.latency_ms ? healthData.database.latency_ms + ' ms' : '—' }}
              </span>
            </div>
            <div class="detail-row">
              <span class="label">Version distante :</span>
              <span class="val truncate" :title="healthData?.database?.version">
                {{ healthData?.database?.version || 'En attente...' }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Vue détaillée JSON de réponse de l'API -->
      <section class="json-inspector">
        <div class="inspector-header">
          <h4>Réponse brute renvoyée par le Backend (`/api/v1/health`)</h4>
          <span class="timestamp">Dernière vérification : {{ lastChecked || 'Jamais' }}</span>
        </div>
        <pre class="json-box"><code>{{ healthDataFormatted }}</code></pre>
      </section>
    </main>

    <!-- Pied de page -->
    <footer class="footer">
      <p>Projet BTP Manager © 2026 — Architecture Clean & Modulaire prête pour la Phase 2</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const backendOnline = ref(false)
const dbOnline = ref(false)
const backendLatency = ref(null)
const healthData = ref(null)
const lastChecked = ref('')

const healthDataFormatted = computed(() => {
  if (!healthData.value) return '// Cliquez sur "Tester la connexion" pour interroger l\'API'
  return JSON.stringify(healthData.value, null, 2)
})

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

async function checkHealth() {
  loading.value = true
  const startTime = performance.now()
  try {
    const response = await axios.get(`${apiBaseUrl}/health`, { timeout: 5000 })
    backendLatency.value = Math.round(performance.now() - startTime)
    healthData.value = response.data
    backendOnline.value = true
    dbOnline.value = response.data?.database?.status === 'connected'
    lastChecked.value = new Date().toLocaleTimeString('fr-FR')
  } catch (error) {
    backendLatency.value = null
    backendOnline.value = false
    dbOnline.value = false
    healthData.value = {
      error: error.message,
      status: 'unreachable',
      suggestion: 'Vérifiez que le backend FastAPI est démarré sur http://localhost:8000'
    }
    lastChecked.value = new Date().toLocaleTimeString('fr-FR')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkHealth()
})
</script>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2.5rem;
  background: rgba(19, 27, 46, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-icon {
  font-size: 2.2rem;
  padding: 0.5rem;
  background: rgba(245, 158, 11, 0.12);
  border-radius: 12px;
  border: 1px solid var(--accent-btp-glow);
}

.brand-title {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-subtitle {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.env-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.9rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
  font-size: 0.85rem;
  color: #34d399;
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: #34d399;
  border-radius: 50%;
  box-shadow: 0 0 8px #34d399;
}

.main-container {
  flex: 1;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  padding: 2.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.banner {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(19, 27, 46, 0.9) 100%);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 2rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.banner-tag {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--accent-btp);
  margin-bottom: 0.5rem;
}

.banner h2 {
  font-size: 1.6rem;
  margin-bottom: 0.6rem;
  color: #fff;
}

.banner p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 780px;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: linear-gradient(135deg, var(--accent-btp) 0%, #d97706 100%);
  color: #0f172a;
  font-weight: 700;
  font-size: 0.95rem;
  border: none;
  padding: 0.85rem 1.6rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 4px 14px var(--accent-btp-glow);
}

.btn-refresh:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}

.btn-refresh:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spin {
  display: inline-block;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pipeline-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.8rem 2.5rem;
}

.pipeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  min-width: 140px;
}

.node-icon {
  font-size: 2.2rem;
}

.node-title {
  font-weight: 700;
  font-size: 1rem;
}

.node-detail {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.pipeline-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  flex: 1;
  padding: 0 1.5rem;
  opacity: 0.4;
  transition: opacity 0.3s ease;
}

.pipeline-connector.connected {
  opacity: 1;
}

.connector-line {
  width: 100%;
  height: 2px;
  background: dashed var(--border-highlight);
}

.connected .connector-line {
  background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}

.connector-arrow {
  font-size: 1.1rem;
  color: #3b82f6;
}

.connector-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 1.5rem;
  transition: border-color 0.2s, transform 0.2s;
}

.card:hover {
  border-color: var(--border-highlight);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.card-title-group h3 {
  font-size: 1.1rem;
  font-weight: 600;
}

.card-emoji {
  font-size: 1.3rem;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.88rem;
}

.detail-row .label {
  color: var(--text-secondary);
}

.detail-row .val {
  color: var(--text-primary);
  font-weight: 500;
}

.val.highlight {
  color: var(--accent-btp);
  font-weight: 700;
}

.val.code {
  font-family: monospace;
  background: rgba(255, 255, 255, 0.06);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.val.link {
  color: #38bdf8;
  text-decoration: none;
}

.val.link:hover {
  text-decoration: underline;
}

.val.truncate {
  max-width: 180px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge {
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-success {
  background: var(--status-success-bg);
  color: var(--status-success);
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.badge-error {
  background: var(--status-error-bg);
  color: var(--status-error);
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.json-inspector {
  background: #080c14;
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 1.5rem;
}

.inspector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.inspector-header h4 {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.timestamp {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.json-box {
  background: #04070d;
  padding: 1.2rem;
  border-radius: 8px;
  border: 1px solid #141f33;
  overflow-x: auto;
  font-family: 'Fira Code', monospace;
  font-size: 0.85rem;
  color: #38bdf8;
  line-height: 1.5;
}

.footer {
  text-align: center;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  .banner {
    flex-direction: column;
    align-items: flex-start;
  }
  .pipeline-container {
    flex-direction: column;
    gap: 1.5rem;
  }
  .pipeline-connector {
    transform: rotate(90deg);
    padding: 1rem 0;
  }
}
</style>
