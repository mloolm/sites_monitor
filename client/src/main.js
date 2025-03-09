// main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router'; // Импортируем готовый объект router
import App from './App.vue';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router); // Используем готовый объект router
app.mount('#app');