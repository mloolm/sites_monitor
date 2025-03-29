<template>
  <v-app>
    <Menu v-if="showMenu" />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import Menu from './components/Menu.vue';

const route = useRoute();
const token = localStorage.getItem("token");

// Computed property to determine whether the menu should be displayed.
const showMenu = computed(() => {
  return route.path !== '/login';
});
</script>

