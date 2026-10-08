<template>
  <div class="space-y-4">
    <!-- Zone de téléversement (Drag & Drop + Caméra Mobile) -->
    <div
      class="border-2 border-dashed rounded-2xl p-5 text-center transition-all cursor-pointer relative"
      :class="isDragging ? 'border-blue-500 bg-blue-50/50' : 'border-slate-300 hover:border-blue-400 bg-slate-50/50 hover:bg-white'"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInputRef"
        type="file"
        class="hidden"
        :accept="acceptedMimeTypes"
        @change="handleFileSelect"
      />

      <!-- Hidden camera input for mobile direct capture -->
      <input
        ref="cameraInputRef"
        type="file"
        class="hidden"
        accept="image/*"
        capture="environment"
        @change="handleFileSelect"
      />

      <div class="flex flex-col items-center justify-center gap-2">
        <div class="w-12 h-12 rounded-2xl bg-blue-100 text-blue-700 flex items-center justify-center text-xl shadow-xs">
          <fas-icon icon="cloud-arrow-up" />
        </div>
        <div>
          <span class="text-xs font-bold text-slate-800">
            Cliquez pour téléverser ou glissez-déposez
          </span>
          <p class="text-[11px] text-slate-400 mt-0.5">
            PDF, JPG, PNG, WEBP jusqu'à 15 Mo (Factures, Bons de livraison, Devis, Reçus)
          </p>
        </div>

        <!-- Bouton raccourci Caméra Mobile / Tablette -->
        <button
          type="button"
          @click.stop="triggerCameraInput"
          class="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-orange-50 text-orange-700 hover:bg-orange-100 text-xs font-bold border border-orange-200 transition-colors"
        >
          <fas-icon icon="camera" />
          <span>Prendre en photo un ticket / facture</span>
        </button>
      </div>
    </div>

    <!-- Modal ou formulaire d'envoi si fichier sélectionné -->
    <div
      v-if="selectedFile"
      class="p-4 rounded-2xl bg-white border border-blue-200 shadow-md space-y-3 animate-in fade-in duration-150"
    >
      <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-sm flex-shrink-0">
            <fas-icon :icon="getFileIcon(selectedFile.name)" />
          </div>
          <div class="min-w-0">
            <div class="text-xs font-bold text-slate-800 truncate">{{ selectedFile.name }}</div>
            <div class="text-[10px] text-slate-400">{{ formatFileSize(selectedFile.size) }}</div>
          </div>
        </div>
        <button
          type="button"
          @click="clearSelectedFile"
          class="text-slate-400 hover:text-red-500 p-1 rounded-lg"
          title="Annuler"
        >
          <fas-icon icon="xmark" class="text-sm" />
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div>
          <label class="block font-bold text-slate-700 mb-1">Type de document *</label>
          <select
            v-model="uploadForm.document_type"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-500"
          >
            <option value="Facture">Facture fournisseur</option>
            <option value="Bon de livraison">Bon de livraison (BL)</option>
            <option value="Bon de commande">Bon de commande (BC)</option>
            <option value="Devis">Devis / Proforma</option>
            <option value="Reçu">Reçu de caisse / Ticket</option>
            <option value="Justificatif de paiement">Justificatif de paiement</option>
            <option value="Photo de livraison">Photo livraison chantier</option>
            <option value="Autre">Autre pièce justificative</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-slate-700 mb-1">N° de pièce (optionnel)</label>
          <input
            v-model="uploadForm.document_number"
            type="text"
            placeholder="Ex: FAC-2026-981"
            class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold focus:outline-none focus:bg-white focus:border-blue-500"
          />
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <button
          type="button"
          @click="clearSelectedFile"
          class="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-100"
        >
          Annuler
        </button>
        <button
          type="button"
          @click="submitUpload"
          :disabled="isUploading"
          class="px-4 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 disabled:opacity-50"
        >
          <fas-icon v-if="isUploading" icon="spinner" class="animate-spin" />
          <fas-icon v-else icon="upload" />
          <span>{{ isUploading ? 'Téléversement...' : 'Confirmer et Joindre' }}</span>
        </button>
      </div>
    </div>

    <!-- Liste des documents déjà attachés -->
    <div v-if="documents && documents.length > 0" class="space-y-2">
      <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
        Pièces jointes ({{ documents.length }})
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <div
          v-for="doc in documents"
          :key="doc.id"
          class="flex items-center justify-between p-3 rounded-xl bg-white border border-slate-200 shadow-2xs hover:border-blue-300 transition-colors"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <div class="w-8 h-8 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center text-sm flex-shrink-0">
              <fas-icon :icon="getFileIcon(doc.original_filename)" />
            </div>
            <div class="min-w-0">
              <div class="text-xs font-bold text-slate-800 truncate" :title="doc.original_filename">
                {{ doc.original_filename }}
              </div>
              <div class="flex items-center gap-2 text-[10px] text-slate-400">
                <span class="font-bold text-blue-600">{{ doc.document_type }}</span>
                <span>•</span>
                <span>{{ formatFileSize(doc.file_size) }}</span>
                <span v-if="doc.document_number">• N° {{ doc.document_number }}</span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-1 flex-shrink-0 ml-2">
            <!-- Bouton Aperçu / Téléchargement -->
            <a
              :href="getDocumentUrl(doc)"
              target="_blank"
              class="p-1.5 rounded-lg text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              title="Visualiser le document"
            >
              <fas-icon icon="eye" class="text-xs" />
            </a>
            <!-- Bouton Supprimer -->
            <button
              v-if="allowDelete"
              type="button"
              @click="$emit('delete', doc.id)"
              class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
              title="Supprimer"
            >
              <fas-icon icon="trash-can" class="text-xs" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-2 text-xs text-slate-400 italic">
      Aucun document joint pour le moment.
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  documents: {
    type: Array,
    default: () => [],
  },
  allowDelete: {
    type: Boolean,
    default: true,
  },
  acceptedMimeTypes: {
    type: String,
    default: '.pdf,image/jpeg,image/png,image/webp',
  },
})

const emit = defineEmits(['upload', 'delete'])

const fileInputRef = ref(null)
const cameraInputRef = ref(null)
const isDragging = ref(false)
const selectedFile = ref(null)
const isUploading = ref(false)

const uploadForm = reactive({
  document_type: 'Facture',
  document_number: '',
})

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const triggerCameraInput = () => {
  cameraInputRef.value?.click()
}

const handleFileSelect = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const clearSelectedFile = () => {
  selectedFile.value = null
  uploadForm.document_number = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
  if (cameraInputRef.value) cameraInputRef.value.value = ''
}

const submitUpload = async () => {
  if (!selectedFile.value) return
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('document_type', uploadForm.document_type)
    if (uploadForm.document_number) {
      formData.append('document_number', uploadForm.document_number)
    }

    emit('upload', formData)
    clearSelectedFile()
  } finally {
    isUploading.value = false
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 o'
  if (bytes < 1024) return bytes + ' o'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' Ko'
  return (bytes / (1024 * 1024)).toFixed(1) + ' Mo'
}

const getFileIcon = (filename) => {
  if (!filename) return 'file'
  const ext = filename.split('.').pop()?.toLowerCase()
  if (['jpg', 'jpeg', 'png', 'webp', 'gif'].includes(ext)) return 'file-image'
  if (ext === 'pdf') return 'file-pdf'
  if (['xls', 'xlsx', 'csv'].includes(ext)) return 'file-excel'
  return 'file-lines'
}

const getDocumentUrl = (doc) => {
  if (!doc) return '#'
  // FastAPI static uploads mount is at /uploads/...
  if (doc.file_path && doc.file_path.startsWith('uploads/')) {
    return `http://localhost:8000/${doc.file_path}`
  }
  return doc.file_url || `http://localhost:8000/uploads/purchases/${doc.purchase_id}/${doc.original_filename}`
}
</script>
