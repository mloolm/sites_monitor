import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createRouter } from './router';
import App from './App.vue';

const app = createApp(App);
const pinia = createPinia();
const router = createRouter();

app.use(pinia);
app.use(router);
app.mount('#app');