import { defineStore } from 'pinia';
import api from '../api';

export const useSiteStore = defineStore('site', {
  state: () => ({
    sites: [], // Sites list
  }),
  actions: {
    async fetchSites(token) {
      try {
        const response = await api.getSites(token);
        this.sites = response.data; // Updating the list of websites
      } catch (error) {
        console.error('Error loading websites', error);
      }
    },
  },
});