<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Логин:</label>
        <input v-model="username" type="text" id="username" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input v-model="password" type="password" id="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../api";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

async function handleLogin() {
  try {
    const response = await api.login(username.value, password.value);
    const token = response.data.access_token;
    localStorage.setItem("token", token); // Сохраняем токен
    router.push("/dashboard"); // Переходим на защищенную страницу
  } catch (err) {
    error.value = "Неверный логин или пароль";
  }
}
</script>