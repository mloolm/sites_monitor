<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>Настройки уведомлений</v-card-title>

      <!-- Раздел подключения Telegram -->
      <v-card-subtitle>Подключение Telegram</v-card-subtitle>
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="telegramToken"
              label="Токен Telegram"
              readonly
              outlined
              dense
              :loading="isLoading"
              :error-messages="errorMessage"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-btn
              color="primary"
              @click="fetchTelegramToken"
              :disabled="isLoading"
            >
              Получить токен
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useSiteStore } from '../stores/siteStore';
import api from '../api';

const token = localStorage.getItem("token");

</script>

<style scoped>
.v-card {
  margin-top: 20px;
}
</style>