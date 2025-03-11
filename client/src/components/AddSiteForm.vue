<template>
  <v-container class="add-site-form">
    <h2 class="text-h4 mb-4">Добавить сайт</h2>
    <v-form @submit.prevent="addSite">
      <v-text-field
        v-model="newSiteUrl"
        label="Введите URL сайта"
        placeholder="https://example.com"
        required
        :rules="[urlRules.required, urlRules.isValidUrl]"
        variant="outlined"
        clearable
      ></v-text-field>

      <v-btn type="submit" color="primary" :disabled="!newSiteUrl">Добавить</v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import {ref} from 'vue';
import api from "../api";
import {useSiteStore} from '../stores/siteStore'; // Импортируем хранилище

const newSiteUrl = ref('');
const token = localStorage.getItem("token");
const siteStore = useSiteStore(); // Получаем доступ к хранилищу

// Валидация URL
const urlRules = {
  required: (value) => !!value || 'URL обязателен',
  isValidUrl: (value) => {
    const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/.*)*$/;
    return urlPattern.test(value) || 'Некорректный URL';
  },
};

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
  max-width: 500px;
  margin: 0 auto;
}
</style>