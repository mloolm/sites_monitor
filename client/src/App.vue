<template>
  <v-app>
    <!-- Условное отображение меню -->
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

// Вычисляемое свойство для определения, нужно ли показывать меню
const showMenu = computed(() => {
  return route.path !== '/login';
});
</script>

