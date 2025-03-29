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

              <div class="mb-1">
                <v-chip
                    class="ml-0"
                    :class="getHealthClass(site.health)"
                    size="x-small"
                    text-color="black"
                >
                  {{ site.health }}%
                </v-chip>

                <v-chip
                    v-if="site.url.startsWith('https')"
                    class="ml-2"
                    :class="getSSLClass(site.ssl)"
                    text-color="black"
                    size="x-small"
                >
                  SSL valid to
                  {{ site.ssl ? new Date(site.ssl).toISOString().slice(0, 10).split('-').reverse().join('.') : '-' }}

                </v-chip>

              </div>

            </v-list-item-title>
            <v-btn
                icon="delete"
                size="x-small"
                color="error"
                flat
                @click.stop="openDeleteDialog(site)" class="ml-2">
              <span class="material-icons">delete</span>
            </v-btn>
          </v-list-item-content>
          <v-divider></v-divider>
        </v-list-item>

      </v-list>
    </v-card>
  </v-container>

  <!-- Confirmation dialog window -->
  <v-dialog v-model="deleteDialog" max-width="400">
    <v-card>
      <v-card-title>Confirm deletion</v-card-title>
      <v-card-text>
        Are you sure you want to delete the website? <strong>{{ siteToDelete?.url }}</strong>?
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
import {onMounted, ref} from 'vue';
import {useSiteStore} from '../stores/siteStore';
import api from '../api';
import {useRouter} from "vue-router";

const siteStore = useSiteStore(); // Получаем доступ к хранилищу
const token = localStorage.getItem("token");
const router = useRouter();
// States for the delete dialog
const deleteDialog = ref(false);
const siteToDelete = ref(null);

onMounted(async () => {
  await siteStore.fetchSites(token);
});

// Opening the delete dialog
function openDeleteDialog(site) {
  siteToDelete.value = site;
  deleteDialog.value = true;
}

// Closing the delete dialog
function closeDeleteDialog() {
  siteToDelete.value = null;
  deleteDialog.value = false;
}

// Confirming deletion
async function confirmDelete() {
  try {
    if (siteToDelete.value) {
      await api.deleteSite(token, siteToDelete.value.id); // Удаляем сайт через API
      await siteStore.fetchSites(token); // Обновляем список сайтов
      closeDeleteDialog(); // Закрываем диалог

    }
  } catch (error) {
    console.error('Error deleting the website:', error);
    alert('Failed to delete the website');
  }
}

const getSSLClass = (ssl) => {
  if (ssl == null) {
    return 'ssl-error';
  }

  // Converts SSL to a date if it is a string
  const sslDate = new Date(ssl);
  const currentDate = new Date();

  // Calculates the difference in days
  const diffTime = sslDate - currentDate;
  const diffDays = diffTime / (1000 * 3600 * 24);

  // If the remaining days are less than a week
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

// Function to navigate to the website's page
const goToSite = (siteId) => {
  router.push(`/site/${siteId}`);
};

</script>

<style scoped>
.ok, .ssl-ok {
  background-color: #d4edda; /* Зеленый цвет для статуса OK */
}

.warning, .ssl-warning {
  background-color: #fff3cd; /* Желтый цвет для статуса Warning */
}

.down, .ssl-error {
  background-color: #fbc7cc; /* Красный цвет для статуса Down */
}
</style>