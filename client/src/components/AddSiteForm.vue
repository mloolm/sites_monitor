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
import {ref, computed} from 'vue';
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

// Вычисляемое свойство для проверки валидности URL
const isUrlValid = computed(() => {
  return urlRules.required(newSiteUrl.value) === true && urlRules.isValidUrl(newSiteUrl.value) === true;
});

async function addSite() {
  try {
    await api.addSite(token, newSiteUrl.value); // Добавляем сайт через API
    newSiteUrl.value = ''; // Очистить поле ввода
    // Обновляем список сайтов в хранилище
    await siteStore.fetchSites(token);
  } catch (error) {
    if (error.status == 422) {
      alert('Некорректный URL сайта');
    } else {
      console.error('Ошибка при добавлении сайта:', error);
      alert('Не удалось добавить сайт.');
    }
  }
}
</script>

