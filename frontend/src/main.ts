import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // <-- 1. 匯入我們剛剛建立的 router

const app = createApp(App)

app.use(router) // <-- 2. 告訴 Vue app 使用這個 router

app.mount('#app')