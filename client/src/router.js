// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import NotificationSettings from "./components/NotificationSettings.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/dashboard", component: Dashboard },
  { path: "/noty", component: NotificationSettings },
  { path: "/", redirect: "/login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;