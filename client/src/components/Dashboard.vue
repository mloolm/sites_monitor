<template>
  <v-container class="dashboard">
    <v-row justify="space-between" align="center" class="mb-6">
      <v-col cols="auto">
        <h3 class="text-h5">Мониторинг</h3>
      </v-col>
      <v-col cols="auto">
        <v-btn color="error" @click="logout">Выйти</v-btn>
      </v-col>
    </v-row>

    <p v-if="message" class="text-subtitle-1">{{ message }}</p>

    <AddSiteForm/>
    <SiteList/>
  </v-container>
</template>

<script setup>
import {ref, onMounted} from "vue";
import api from "../api";
import {useRouter} from "vue-router";
import AddSiteForm from './AddSiteForm.vue';
import SiteList from './SiteList.vue';

const message = ref("");
const router = useRouter();

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    const response = await api.getUserData(token);
    message.value = response.data.message;
  } catch (err) {
    console.error("Ошибка при получении данных пользователя:", err);
    router.push("/login");
  }
});

function logout() {
  localStorage.removeItem("token");
  router.push("/login");
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.text-subtitle-1 {
  font-size: 1rem;
  color: #424242;
}
</style>