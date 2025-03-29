<template>
  <v-container>
    <b class=" mb-4">Add site</b>
    <v-form @submit.prevent="addSite">
      <v-text-field
          v-model="newSiteUrl"
          label="Enter site URL"
          placeholder="https://example.com"
          required
          :rules="[urlRules.required, urlRules.isValidUrl]"
          variant="underlined"
          clearable
      ></v-text-field>
      <v-btn class="float-end" type="submit" color="primary" :disabled="!isUrlValid">Add site</v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import {computed, ref} from 'vue';
import api from "../api";
import {useSiteStore} from '../stores/siteStore'; // import store

const newSiteUrl = ref('');
const token = localStorage.getItem("token");
const siteStore = useSiteStore(); // Accessing the storage

// Валидация URL
const urlRules = {
  required: (value) => !!value || 'URL is required',
  isValidUrl: (value) => {
    const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/.*)*$/;
    return urlPattern.test(value) || 'Invalid URL';
  },
};

// Computed property to check the validity of the URL
const isUrlValid = computed(() => {
  return urlRules.required(newSiteUrl.value) === true && urlRules.isValidUrl(newSiteUrl.value) === true;
});

async function addSite() {
  try {
    await api.addSite(token, newSiteUrl.value); // add site via API
    newSiteUrl.value = '';
    // Update site list in the store
    await siteStore.fetchSites(token);
  } catch (error) {
    if (error.status == 422) {
      alert('Invalid site URL');
    } else {
      console.error('Error adding the website:', error);
      alert('Failed to add the website');
    }
  }
}
</script>