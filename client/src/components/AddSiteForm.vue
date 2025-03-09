<template>
  <div class="add-site-form">
    <h2>Добавить сайт</h2>
    <form @submit.prevent="addSite">
      <input
        type="text"
        v-model="newSiteUrl"
        placeholder="Введите URL сайта"
        required
      />
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from "../api";
import { useSiteStore } from '../stores/siteStore'; // Импортируем хранилище

const newSiteUrl = ref('');
const token = localStorage.getItem("token");
const siteStore = useSiteStore(); // Получаем доступ к хранилищу

async function addSite() {
  try {
    await api.addSite(token, newSiteUrl.value); // Добавляем сайт через API
    newSiteUrl.value = ''; // Очистить поле ввода
    alert('Сайт успешно добавлен!');

    // Обновляем список сайтов в хранилище
    await siteStore.fetchSites(token);
  } catch (error) {
    console.error('Ошибка при добавлении сайта:', error);
    alert('Не удалось добавить сайт.');
  }
}
</script>

<style scoped>
.add-site-form {
  padding: 20px;
}

input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
}
</style>