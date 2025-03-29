import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import NotificationSettings from "./components/NotificationSettings.vue";
import SitePage from "./components/SitePage.vue";
import NotificationList from "./components/NotificationList.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/dashboard", component: Dashboard },
  { path: "/settings", component: NotificationSettings },
  { path: "/noty", component: NotificationList },
  { path: "/", redirect: "/login" },
  { path: "/site/:id", component: SitePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;