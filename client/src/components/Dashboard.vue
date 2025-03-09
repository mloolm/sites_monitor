<template>
  <div>
    <h2>Панель управления</h2>
    <p>{{ message }}</p>
    <button @click="logout">Выйти</button>
  </div>
   <div>
    <AddSiteForm />
    <SiteList />
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import api from "../api";
import { useRouter } from "vue-router";
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
    router.push("/login");
  }
});

function logout() {
  localStorage.removeItem("token");
  router.push("/login");
}
</script>
