<template>
  <v-container>
    <p v-if="message" class="text-subtitle-1">{{ message }}</p>
  </v-container>
  <SiteList/>
  <AddSiteForm/>
</template>

<script setup>
import AddSiteForm from './AddSiteForm.vue';
import SiteList from './SiteList.vue';
import {ref} from "vue";
const message = ref("");
</script>

<style scoped>

</style>