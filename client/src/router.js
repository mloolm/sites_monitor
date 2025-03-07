import { createRouter as createVueRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';

export function createRouter() {
  return createVueRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: HomeView },
    ],
  });
}