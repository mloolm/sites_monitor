<template>
  <v-app-bar app>
    <v-container>
      <div class="d-flex justify-space-between">
        <div><b>Sites Monitor</b></div>
        <div>
          <router-link
              v-for="item in menuItems"
              :key="item.text"
              :to="item.route"
              class="mr-3"
          >
            <span class="menu-link material-icons">{{ item.icon }}</span>
          </router-link>

          <router-link>
            <span class="menu-link material-icons" @click="logout">logout</span>
          </router-link>
        </div>
      </div>
    </v-container>
  </v-app-bar>
</template>

<script setup>
const router = useRouter();
import {onMounted, ref} from "vue";
import api from "../api";
import {useRouter} from "vue-router";

const message = ref("");

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
    console.error("Error retrieving user data:", err);
    router.push("/login");
  }
});

const menuItems = ref([
  {icon: 'home', route: '/dashboard'},
  {icon: 'settings', route: '/settings'},
  {icon: 'notifications', route: '/noty'},

]);

function logout() {
  localStorage.removeItem("token");
  router.push("/login");
}
</script>

<style scoped>
.menu-link {
  color: #3F51B5;
}
</style>