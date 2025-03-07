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
import axios from 'axios';

const newSiteUrl = ref('');

async function addSite() {
  try {
    await axios.post('/api/add-site', { url: newSiteUrl.value });
    newSiteUrl.value = ''; // Очистить поле ввода
    alert('Сайт успешно добавлен!');
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