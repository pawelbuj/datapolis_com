import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import legacy CSS globally (as-is, no refactoring)
import '../assets/css/main.min.css'
import '../assets/css/async.min.css'
import '../assets/css/dark-theme.css'
import '../assets/css/new-homepage.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
