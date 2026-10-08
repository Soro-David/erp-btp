<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
    @click.self="close"
  >
    <div
      class="bg-white border border-slate-200 rounded-2xl w-full max-w-lg p-6 sm:p-7 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150"
    >
      <!-- En-tête Modal -->
      <div class="flex items-center justify-between pb-3.5 mb-4 border-b border-slate-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-[#047857] flex items-center justify-center text-lg">
            <fas-icon icon="user-plus" />
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900">Ajouter un responsable / intervenant</h3>
            <p class="text-xs text-slate-500">Ajout immédiat au répertoire des équipes et intervenants BTP</p>
          </div>
        </div>
        <button
          type="button"
          @click="close"
          class="text-slate-400 hover:text-slate-700 p-1 transition-colors"
          title="Fermer"
        >
          <fas-icon icon="xmark" class="text-lg" />
        </button>
      </div>

      <!-- Formulaire -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Rôle / Fonction (sélectionnable ou personnalisé) -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">
            Fonction / Rôle assigné <span class="text-rose-500">*</span>
          </label>
          <div class="relative">
            <select
              v-model="form.role_name"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 appearance-none pr-9 cursor-pointer"
            >
              <option value="Chef de projet">Chef de projet</option>
              <option value="Conducteur des travaux">Conducteur des travaux</option>
              <option value="Chef de chantier">Chef de chantier</option>
              <option value="Responsable HSE">Responsable HSE</option>
              <option value="Bureau d'études">Bureau d'études</option>
              <option value="Entreprise exécutante">Entreprise exécutante</option>
              <option value="Autre intervenant">Autre intervenant</option>
            </select>
            <fas-icon
              icon="chevron-down"
              class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs"
            />
          </div>
        </div>

        <!-- Nom & Prénom en 2 colonnes -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Nom de famille <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.last_name"
              type="text"
              required
              placeholder="Ex: Kouassi"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Prénom(s) <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.first_name"
              type="text"
              required
              placeholder="Ex: Jean-Luc"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>
        </div>

        <!-- Téléphone & Email -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Téléphone <span class="text-slate-400 font-normal">(optionnel)</span>
            </label>
            <input
              v-model="form.phone"
              type="tel"
              placeholder="+225 07 00 00 00"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Email professionnel <span class="text-slate-400 font-normal">(optionnel)</span>
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="contact@intervenant.ci"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>
        </div>

        <!-- Entreprise / Cabinet -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">
            Entreprise ou Cabinet associé <span class="text-slate-400 font-normal">(optionnel)</span>
          </label>
          <input
            v-model="form.company"
            type="text"
            placeholder="Ex: BTP Solutions SARL, Cabinet Structure..."
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
          />
        </div>

        <!-- Erreur globale si présente -->
        <p v-if="errorMessage" class="text-xs text-rose-500 bg-rose-50 p-2.5 rounded-xl border border-rose-200">
          {{ errorMessage }}
        </p>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
            :disabled="loading"
          >
            Annuler
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-4 py-2 rounded-xl bg-[#047857] hover:bg-[#065f46] text-white font-bold text-xs shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <fas-icon v-if="loading" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="user-plus" />
            <span>{{ loading ? 'Enregistrement...' : 'Ajouter le responsable' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { chantierService } from '@/services'
import { toast } from '@/utils/alert'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  defaultRole: {
    type: String,
    default: 'Conducteur des travaux',
  },
  targetKey: {
    type: String,
    default: 'site_manager_id',
  },
})

const emit = defineEmits(['update:modelValue', 'created'])

const form = reactive({
  first_name: '',
  last_name: '',
  role_name: 'Conducteur des travaux',
  phone: '',
  email: '',
  company: '',
})

const errorMessage = ref('')
const loading = ref(false)

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.first_name = ''
      form.last_name = ''
      form.role_name = props.defaultRole || 'Conducteur des travaux'
      form.phone = ''
      form.email = ''
      form.company = ''
      errorMessage.value = ''
    }
  }
)

function close() {
  emit('update:modelValue', false)
}

async function handleSubmit() {
  errorMessage.value = ''
  if (!form.last_name.trim() || !form.first_name.trim()) {
    errorMessage.value = 'Le nom et le prénom sont obligatoires.'
    return
  }

  loading.value = true
  try {
    const created = await chantierService.createResponsable({
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
      role_name: form.role_name.trim(),
      phone: form.phone.trim() || null,
      email: form.email.trim() || null,
      company: form.company.trim() || null,
    })
    toast(`Responsable « ${created.full_name} » ajouté avec succès`, 'success')
    emit('created', { responsable: created, targetKey: props.targetKey })
    close()
  } catch (err) {
    const detail = err.response?.data?.detail || 'Erreur lors de la création du responsable'
    errorMessage.value = typeof detail === 'string' ? detail : 'Veuillez vérifier les informations saisies.'
  } finally {
    loading.value = false
  }
}
</script>
