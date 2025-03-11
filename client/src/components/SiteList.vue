<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card>
          <v-card-title>Список сайтов</v-card-title>
          <v-list>
            <v-list-item v-for="site in siteStore.sites" :key="site.id">
              <v-list-item-content class="d-flex align-center justify-space-between">
                <v-list-item-title class="text-body-1">{{ site.url }}</v-list-item-title>
                <v-btn icon color="error" @click="openDeleteDialog(site)" class="ml-2">
                  <span class="material-icons">delete</span>
                </v-btn>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-container>
    </v-main>


    <!-- Диалоговое окно подтверждения -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text>
          Вы действительно хотите удалить сайт <strong>{{ siteToDelete?.url }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDeleteDialog">Отмена</v-btn>
          <v-btn color="error" @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useSiteStore } from '../stores/siteStore';
import api from '../api';

const siteStore = useSiteStore(); // Получаем доступ к хранилищу
const token = localStorage.getItem("token");

// Состояния для диалога удаления
const deleteDialog = ref(false);
const siteToDelete = ref(null);

onMounted(async () => {
  await siteStore.fetchSites(token); // Загружаем список сайтов при монтировании
});

// Открытие диалога удаления
function openDeleteDialog(site) {
  siteToDelete.value = site; // Сохраняем сайт, который хотим удалить
  deleteDialog.value = true; // Открываем диалог
}

// Закрытие диалога удаления
function closeDeleteDialog() {
  siteToDelete.value = null; // Очищаем выбранный сайт
  deleteDialog.value = false; // Закрываем диалог
}

// Подтверждение удаления
async function confirmDelete() {
  try {
    if (siteToDelete.value) {
      await api.deleteSite(token, siteToDelete.value.id); // Удаляем сайт через API
      await siteStore.fetchSites(token); // Обновляем список сайтов
      closeDeleteDialog(); // Закрываем диалог
      alert('Сайт успешно удален!');
    }
  } catch (error) {
    console.error('Ошибка при удалении сайта:', error);
    alert('Не удалось удалить сайт.');
  }
}
</script>

<style scoped>
.site-list {
  padding: 20px;
}
</style>