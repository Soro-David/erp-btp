<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">
      <!-- En-tête -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-lg">
            <fas-icon :icon="isEdit ? 'pen-to-square' : 'handshake'" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">
              {{ isEdit ? 'Modifier le Fournisseur' : 'Nouveau Fournisseur BTP' }}
            </h2>
            <p class="text-xs text-slate-500">
              Renseignez les coordonnées commerciales et administratives
            </p>
          </div>
        </div>
        <button
          type="button"
          @click="close"
          class="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100 transition-colors"
        >
          <fas-icon icon="xmark" class="text-base" />
        </button>
      </div>

      <!-- Corps du formulaire -->
      <form @submit.prevent="handleSubmit" class="p-6 overflow-y-auto space-y-4 text-xs flex-1">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Code -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Code Fournisseur</label>
            <input
              v-model="form.code"
              type="text"
              placeholder="Auto-généré (ex: FOUR-006)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600 uppercase"
            />
          </div>

          <!-- Raison Sociale -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Raison Sociale / Nom *</label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="Ex: CIMAF Côte d'Ivoire"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Nom commercial -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Nom commercial / Enseigne</label>
            <input
              v-model="form.trade_name"
              type="text"
              placeholder="Ex: Ciments de l'Afrique"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Contact principal -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Nom du Contact</label>
            <input
              v-model="form.contact_name"
              type="text"
              placeholder="Ex: M. Kouadio Jean"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Téléphone -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Téléphone Principal *</label>
            <input
              v-model="form.phone"
              type="text"
              required
              placeholder="Ex: +225 07 00 00 00 00"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Email -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Email Commercial</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="commandes@fournisseur.ci"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Ville & Pays -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">Ville</label>
            <input
              v-model="form.city"
              type="text"
              placeholder="Abidjan"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Pays</label>
            <input
              v-model="form.country"
              type="text"
              placeholder="Côte d'Ivoire"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Adresse -->
          <div class="md:col-span-2">
            <label class="block font-bold text-slate-700 mb-1">Adresse Géographique</label>
            <input
              v-model="form.address"
              type="text"
              placeholder="Ex: Zone Industrielle Yopougon, en face du dépôt SOTRA"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- RCCM & NCC -->
          <div>
            <label class="block font-bold text-slate-700 mb-1">N° RCCM</label>
            <input
              v-model="form.rccm"
              type="text"
              placeholder="CI-ABJ-2023-B-XXXX"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Numéro CC (NCC)</label>
            <input
              v-model="form.ncc"
              type="text"
              placeholder="1234567X"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Conditions de règlement -->
          <div class="md:col-span-2">
            <label class="block font-bold text-slate-700 mb-1">Conditions de règlement habituelles</label>
            <input
              v-model="form.payment_terms"
              type="text"
              placeholder="Ex: Virement 30j fin de mois, Acompte 30% commande..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Notes -->
          <div class="md:col-span-2">
            <label class="block font-bold text-slate-700 mb-1">Notes internes</label>
            <textarea
              v-model="form.notes"
              rows="2"
              placeholder="Catalogue principal, remises négociées..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-600"
            ></textarea>
          </div>
        </div>

        <!-- Pied de modal -->
        <div class="pt-4 border-t border-slate-100 flex items-center justify-end gap-2.5">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 font-bold transition-colors"
          >
            Annuler
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-5 py-2 rounded-xl bg-[#1d4ed8] hover:bg-blue-700 text-white font-bold shadow-md shadow-blue-900/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            <fas-icon v-if="saving" icon="spinner" class="animate-spin" />
            <fas-icon v-else :icon="isEdit ? 'check' : 'plus'" />
            <span>{{ isEdit ? 'Mettre à jour' : 'Enregistrer le Fournisseur' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { supplierService } from '@/services'
import Swal from 'sweetalert2'

const props = defineProps({
  isOpen: Boolean,
  supplier: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const isEdit = ref(false)
const saving = ref(false)

const form = reactive({
  code: '',
  name: '',
  trade_name: '',
  contact_name: '',
  phone: '',
  email: '',
  address: '',
  city: 'Abidjan',
  country: "Côte d'Ivoire",
  rccm: '',
  ncc: '',
  payment_terms: '',
  notes: '',
  is_active: true,
})

const resetForm = () => {
  form.code = ''
  form.name = ''
  form.trade_name = ''
  form.contact_name = ''
  form.phone = ''
  form.email = ''
  form.address = ''
  form.city = 'Abidjan'
  form.country = "Côte d'Ivoire"
  form.rccm = ''
  form.ncc = ''
  form.payment_terms = ''
  form.notes = ''
  form.is_active = true
}

watch(
  () => props.supplier,
  (val) => {
    if (val && val.id) {
      isEdit.value = true
      Object.assign(form, val)
    } else {
      isEdit.value = false
      resetForm()
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  saving.value = true
  try {
    let result
    if (isEdit.value && props.supplier?.id) {
      result = await supplierService.updateSupplier(props.supplier.id, form)
      Swal.fire({
        icon: 'success',
        title: 'Fournisseur mis à jour',
        text: `Les informations de ${result.name} ont été actualisées.`,
        timer: 1800,
        showConfirmButton: false,
      })
    } else {
      result = await supplierService.createSupplier(form)
      Swal.fire({
        icon: 'success',
        title: 'Fournisseur créé',
        text: `${result.name} a été enregistré avec le code ${result.code}.`,
        timer: 1800,
        showConfirmButton: false,
      })
    }
    emit('saved', result)
    close()
  } catch (error) {
    const detail = error.response?.data?.detail || error.message
    Swal.fire({
      icon: 'error',
      title: 'Erreur',
      text: detail,
    })
  } finally {
    saving.value = false
  }
}
</script>
