// src/stores/siteStore.js
import { defineStore } from 'pinia';
import api from '../api';

export const useSiteStore = defineStore('site', {
  state: () => ({
    sites: [], // Список сайтов
  }),
  actions: {
    async fetchSites(token) {
      try {
        const response = await api.getSites(token);
        this.sites = response.data; // Обновляем список сайтов
      } catch (error) {
        console.error('Ошибка при загрузке сайтов:', error);
      }
    },
  },
});