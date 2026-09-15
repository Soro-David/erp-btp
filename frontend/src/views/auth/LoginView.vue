<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="brand-badge">🏗️ BTP MANAGER</div>
        <h2>Connexion ERP</h2>
        <p>Accédez à votre espace selon votre rôle et vos habilitations</p>
      </div>

      <div v-if="authStore.error" class="alert-error">
        ⚠️ {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Adresse Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            required 
            placeholder="ex: admin@gmail.com"
          />
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            required 
            placeholder="••••••••"
          />
        </div>

        <button type="submit" class="btn-submit" :disabled="authStore.loading">
          <span>{{ authStore.loading ? 'Vérification...' : 'Se connecter' }}</span>
          <span v-if="!authStore.loading">➔</span>
        </button>
      </form>

      <!-- Raccourcis de test pour la démo -->
      <div class="quick-credentials">
        <div class="quick-title">Comptes de test pré-configurés :</div>
        <div class="chips-container">
          <button 
            type="button" 
            class="chip chip-admin" 
            @click="fillCreds('admin@gmail.com', 'Password@1234')"
          >
            👑 SuperAdmin
          </button>
          <button 
            type="button" 
            class="chip chip-owner" 
            @click="fillCreds('owner@btp.ci', 'Password@1234')"
          >
            🏢 Owner
          </button>
          <button 
            type="button" 
            class="chip chip-director" 
            @click="fillCreds('director@btp.ci', 'Password@1234')"
          >
            📐 Director
          </button>
          <button 
            type="button" 
            class="chip chip-manager" 
            @click="fillCreds('manager@btp.ci', 'Password@1234')"
          >
            📋 Manager
          </button>
          <button 
            type="button" 
            class="chip chip-worker" 
            @click="fillCreds('worker@btp.ci', 'Password@1234')"
          >
            👷 Worker
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('admin@gmail.com')
const password = ref('Password@1234')

function fillCreds(e, p) {
  email.value = e
  password.value = p
}

async function handleLogin() {
  try {
    await authStore.login(email.value, password.value)
    // Redirection selon le rôle
    const role = authStore.userRole
    if (role === 'SUPER_ADMIN') router.push('/superadmin/users')
    else if (role === 'OWNER') router.push('/owner')
    else if (role === 'DIRECTOR') router.push('/director')
    else if (role === 'MANAGER') router.push('/manager')
    else if (role === 'WORKER') router.push('/worker')
    else router.push('/')
  } catch (err) {
    // Erreur gérée dans le store
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 160px);
  padding: 2rem;
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 18px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-badge {
  display: inline-block;
  padding: 0.35rem 0.85rem;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid var(--accent-btp-glow);
  color: var(--accent-btp);
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
}

.login-header h2 {
  font-size: 1.8rem;
  color: #fff;
  margin-bottom: 0.4rem;
}

.login-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.alert-error {
  background: var(--status-error-bg);
  border: 1px solid var(--status-error);
  color: #fca5a5;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.88rem;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.form-group input {
  background: rgba(11, 15, 23, 0.8);
  border: 1px solid var(--border-color);
  color: #fff;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: var(--accent-btp);
  box-shadow: 0 0 0 3px var(--accent-btp-glow);
}

.btn-submit {
  background: linear-gradient(135deg, var(--accent-btp) 0%, #d97706 100%);
  color: #0f172a;
  border: none;
  padding: 0.95rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  margin-top: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--accent-btp-glow);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quick-credentials {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.quick-title {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.chip {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.chip:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: var(--border-highlight);
}
</style>
