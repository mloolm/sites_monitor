<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>Notification Settings</v-card-title>

      <!-- Telegram -->
      <v-card-subtitle>Telegram</v-card-subtitle>
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="telegramToken"
              label="Code for Telegram"
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
              Get code
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>

  <v-container>
    <v-row align="center">
      <v-col cols="12">
         <v-btn
        color="primary"
        @click="subscribeToPush"
        :disabled="isLoading"
        >
          Subscribe to Push
        </v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container>
    <v-row align="center">
      <v-col cols="12">
        <v-btn
        color="primary"
        @click="sendTestMessage"
        :disabled="isLoading"
        >
          Send test message
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import {useRouter} from "vue-router";
const router = useRouter();
const message = ref("");
const telegramToken = ref(""); // Переменная для хранения кода Telegram
const isLoading = ref(false); // Для отображения состояния загрузки
const errorMessage = ref(""); // Для отображения ошибок

const token = localStorage.getItem("token");

function sendTestMessage(){
  const message = 'Test message from site monitor!'
  api.sendNotyMessage(token, message)
}

async function subscribeToPush() {
    if(!token) return;

    if (!('serviceWorker' in navigator))
    {
      console.error('Service worker not loaded')
      return;
    }


    let vapid_pub = await api.getVapidKey(token);

    if(typeof vapid_pub.data == 'undefined')
    {
        console.error('Error retrieving public key');
        return
    }

    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: vapid_pub.data
    });

    console.log("Push подписка:", JSON.stringify(subscription));
    api.subscribePWA(token, JSON.stringify(subscription))
}



// Функция для получения кода Telegram
function fetchTelegramToken() {
  isLoading.value = true; // Начинаем загрузку
  errorMessage.value = ""; // Очищаем сообщения об ошибках

  try {
    api.getTelegramAuthCode(token).then((res) => {
      console.log(res.data);
      telegramToken.value = '/auth ' + res.data; // Обновляем значение telegramToken
    }).catch((err) => {
      console.error("Error getting auth code:", err);
      errorMessage.value = "Failed to fetch the code. Please try again.";
    }).finally(() => {
      isLoading.value = false; // Завершаем загрузку
    });
  } catch (err) {
    console.error("Error getting auth code:", err);
    errorMessage.value = "An unexpected error occurred.";
    isLoading.value = false; // Завершаем загрузку
  }
}



 onMounted(async () => {

  if (!token) {
    router.push("/login");
    return;
  }


  try {
    const response = await api.getUserData(token);
  } catch (err) {
    console.error("Ошибка при получении данных пользователя:", err);
    router.push("/login");
  }

  try {
    const providers = await api.getNotificationData(token);
    console.log(providers)


  } catch (err) {
    console.error("Ошибка при получении данных о провайдерах уведомлений:", err);
  }
});

</script>

<style scoped>
.v-card {
  margin-top: 20px;
}
</style>