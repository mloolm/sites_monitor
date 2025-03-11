// main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router'; // Импортируем готовый объект router
import vuetify from './plugins/vuetify';
import App from './App.vue';
import 'vuetify/dist/vuetify.min.css';


const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(vuetify);

app.mount('#app');