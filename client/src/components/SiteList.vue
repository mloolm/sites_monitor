<template>
 <v-container>
    <v-card>
      <v-card-title>Sites list</v-card-title>
      <v-list>
        <v-list-item
          v-for="site in siteStore.sites"
          :key="site.id"

          @click="goToSite(site.id)"
        >
          <v-list-item-content class="d-flex align-center justify-space-between">
            <v-list-item-title class="text-body-1">
              {{ site.url }}
              <v-chip
                class="ml-2"
                :class="getHealthClass(site.health)"

                text-color="black"
              >
                {{ site.health }}%
              </v-chip>

             <v-chip
                v-if="site.url.startsWith('https')"
                class="ml-2"
                :class="getSSLClass(site.ssl)"
                text-color="black"
              >
                SSL valid to {{ site.ssl ? new Date(site.ssl).toISOString().slice(0, 10).split('-').reverse().join('.') : '-' }}

              </v-chip>

            </v-list-item-title>
            <v-btn icon color="error" @click.stop="openDeleteDialog(site)" class="ml-2">
              <span class="material-icons">delete</span>
            </v-btn>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>

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

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useSiteStore } from '../stores/siteStore';
import api from '../api';
import {useRouter} from "vue-router";
const siteStore = useSiteStore(); // Получаем доступ к хранилищу
const token = localStorage.getItem("token");
const router = useRouter();
// Состояния для диалога удаления
const deleteDialog = ref(false);
const siteToDelete = ref(null);

onMounted(async () => {
  await siteStore.fetchSites(token);
});

// Открытие диалога удаления
function openDeleteDialog(site) {
  siteToDelete.value = site;
  deleteDialog.value = true;
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

    }
  } catch (error) {
    console.error('Ошибка при удалении сайта:', error);
    alert('Не удалось удалить сайт.');
  }
}

const getSSLClass = (ssl) => {
  if (ssl == null) {
    return 'ssl-error';
  }

  // Преобразуем ssl в дату, если это строка
  const sslDate = new Date(ssl);
  const currentDate = new Date();

  // Рассчитываем разницу в днях
  const diffTime = sslDate - currentDate;
  const diffDays = diffTime / (1000 * 3600 * 24);

  // Если оставшиеся дни меньше недели
  if (diffDays <= 7) {
    return 'ssl-warning';
  }

  return 'ssl-ok';
};

const getHealthClass = (health) => {
  if (health >= 90) {
    return 'ok';
  } else if (health >= 80) {
    return 'warning';
  } else {
    return 'down';
  }
};

// Функция для перехода на страницу сайта
const goToSite = (siteId) => {
  router.push(`/site/${siteId}`);
};

</script>

<style scoped>
.ok, .ssl-ok {
  background-color: #d4edda; /* Зеленый цвет для статуса OK */
}

.warning, .ssl-warning  {
  background-color: #fff3cd; /* Желтый цвет для статуса Warning */
}

.down, .ssl-error {
  background-color: #fbc7cc; /* Красный цвет для статуса Down */
}
</style>