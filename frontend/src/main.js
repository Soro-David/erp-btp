import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

// Import FontAwesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import FasIcon from '@/components/common/FasIcon.vue'

// Import des composants partagés
import { DataTable, BaseTable, AppSidebar, AppNavbar, AppFooter } from '@/components'

// Import SweetAlert2
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

// Ajout de toutes les icônes Solid à la bibliothèque
library.add(fas)

const app = createApp(App)

// Enregistrement global des composants partagés
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('fas-icon', FasIcon)
app.component('DataTable', DataTable)
app.component('BaseTable', BaseTable)
app.component('AppSidebar', AppSidebar)
app.component('AppNavbar', AppNavbar)
app.component('AppFooter', AppFooter)

// Rendre SweetAlert accessible globalement (this.$swal)
app.config.globalProperties.$swal = Swal
app.provide('$swal', Swal)

app.use(createPinia())
app.use(router)
app.mount('#app')
