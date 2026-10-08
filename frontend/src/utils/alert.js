import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

// Configuration personnalisée SweetAlert adaptée au design system clair BTP Manager
export const BtpSwal = Swal.mixin({
  background: '#ffffff',
  color: '#0f172a',
  confirmButtonColor: '#1d4ed8', // Bleu principal
  cancelButtonColor: '#64748b',  // Gris secondaire
  customClass: {
    popup: 'rounded-2xl border border-slate-200 shadow-2xl font-sans',
    title: 'text-slate-900 font-extrabold text-base sm:text-lg',
    htmlContainer: 'text-slate-600 text-xs sm:text-sm',
    confirmButton: 'px-5 py-2.5 rounded-xl font-bold text-white text-xs sm:text-sm shadow-sm transition-all',
    cancelButton: 'px-4 py-2.5 rounded-xl font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 text-xs sm:text-sm transition-all',
  },
})

// Toast notification fluide en haut à droite
const toastInstance = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3500,
  timerProgressBar: true,
  background: '#ffffff',
  color: '#0f172a',
  customClass: {
    popup: 'rounded-xl border border-slate-200 shadow-lg text-xs font-sans text-slate-800',
  },
})

/**
 * Toast universel : appelable soit via toast('Message', 'success') soit via toast.fire(...)
 */
export const toast = (titleOrOptions, icon = 'success') => {
  if (typeof titleOrOptions === 'string') {
    return toastInstance.fire({
      icon,
      title: titleOrOptions,
    })
  }
  return toastInstance.fire(titleOrOptions)
}
toast.fire = (opts) => toastInstance.fire(opts)

/**
 * Affiche une alerte de succès
 */
export const alertSuccess = (title, text = '') => {
  return BtpSwal.fire({
    icon: 'success',
    title,
    html: text,
    iconColor: '#10b981',
  })
}

/**
 * Affiche une alerte d'erreur
 */
export const alertError = (title, text = '') => {
  return BtpSwal.fire({
    icon: 'error',
    title,
    html: text,
    iconColor: '#ef4444',
  })
}

/**
 * Affiche une alerte d'avertissement
 */
export const alertWarning = (title, text = '') => {
  return BtpSwal.fire({
    icon: 'warning',
    title,
    html: text,
    iconColor: '#f59e0b',
  })
}

/**
 * Affiche une alerte d'information
 */
export const alertInfo = (title, text = '') => {
  return BtpSwal.fire({
    icon: 'info',
    title,
    html: text,
    iconColor: '#1d4ed8',
  })
}

/**
 * Boîte de dialogue de confirmation avec Promesse
 * Supporte : confirmDialog('Titre', 'Texte', 'Confirmer')
 * OU confirmDialog({ title, text, confirmText, cancelText, icon })
 */
export const confirmDialog = async (arg1 = 'Êtes-vous sûr ?', arg2 = 'Cette action est irréversible.', arg3 = 'Confirmer') => {
  let title = 'Êtes-vous sûr ?'
  let text = 'Cette action est irréversible.'
  let confirmText = 'Confirmer'
  let cancelText = 'Annuler'
  let icon = 'warning'

  if (typeof arg1 === 'object' && arg1 !== null) {
    title = arg1.title || title
    text = arg1.text || text
    confirmText = arg1.confirmText || confirmText
    cancelText = arg1.cancelText || cancelText
    icon = arg1.icon || icon
  } else {
    title = arg1
    text = arg2
    confirmText = arg3
  }

  const result = await BtpSwal.fire({
    title,
    text,
    icon,
    showCancelButton: true,
    confirmButtonText: confirmText,
    cancelButtonText: cancelText,
    reverseButtons: true,
  })
  return result.isConfirmed
}

export const confirm = confirmDialog

export default Swal
