<template>
  <v-container>
    <h4>Notification Settings</h4>
    <v-card class="pa-4">

      <!-- Telegram -->
      <v-card-text align="center" v-if="tlgAvailable"><b>Auth code for Telegram</b></v-card-text>
      <v-card-text v-if="tlgAvailable">
        <v-row align="center">
          <v-col cols="12" sm="8">
            <v-text-field
                variant="underlined"
                v-model="telegramToken"
                label="Press 'Get code' to generate code"
                readonly
                outlined
                dense
                :loading="isLoading"
                :error-messages="errorMessage"
            ></v-text-field>
            <p class="mt-3">
              To authorize and receive notifications in the Telegram bot, enter the command above. The code is valid for
              10 minutes. You can always generate a new one.
            </p>
          </v-col>
          <v-col cols="12" sm="4" class="text-center">
            <v-btn
                color="primary"
                @click="fetchTelegramToken"
                :disabled="isLoading"
                size="small"
            >
              Get code
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>

      <!-- Block with explanation if Telegram is unavailable -->
      <v-card-text v-else>
        <v-alert type="info" variant="outlined">
          Telegram notifications are not available. To enable notifications, you need to add the
          Telegram bot API key to the settings (.env file), where the notifications will be sent.
        </v-alert>
      </v-card-text>
    </v-card>

    <!-- Push -->
    <v-card v-if="pushAvailable" class="pa-4">
      <v-row>
        <v-col cols="12" align="center">
          <v-card-text align="center"><b>Subscribe (or update your subscription) to push notifications</b></v-card-text>

          <v-btn
              color="warning"
              @click="subscribeToPush"
              :disabled="isLoading"
          >
            Subscribe to Push
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else>
      <v-row>
        <v-col cols="12">
          <v-alert type="info" variant="outline">
            Service worker is not loaded or is malfunctioning. Push notifications are not available. Please contact
            support
          </v-alert>
        </v-col>
      </v-row>
    </v-card>

    <v-card v-if="pushAvailable || tlgAvailable" class="pa-4">
      <v-row>
        <v-col cols="12" align="center">
          <v-btn
              color="success"
              @click="sendTestMessage"
              :disabled="isLoading"
          >
            Send test message
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import api from '../api';
import {useRouter} from 'vue-router';

const router = useRouter();
const message = ref("");
const telegramToken = ref(""); // Variable to store the Telegram code.
const isLoading = ref(false); // For displaying the loading state.
const errorMessage = ref(""); // For displaying errors.
const tlgAvailable = ref(false); // Telegram availability.
const pushAvailable = ref(true);
const token = localStorage.getItem("token");

function sendTestMessage() {
  const message = 'Test message from site monitor!';
  api.sendNotyMessage(token, message);
}

async function subscribeToPush() {
  if (!token) return;

  if (!('serviceWorker' in navigator)) {
    pushAvailable.value = false;
    console.error('Service worker not loaded');
    return;
  } else {
    pushAvailable.value = true;
  }

  let vapid_pub = await api.getVapidKey(token);

  if (typeof vapid_pub.data == 'undefined') {
    pushAvailable.value = false;
    console.error('Error retrieving public key');
    return;
  }

  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: vapid_pub.data,
  });

  console.log("Push подписка:", JSON.stringify(subscription));
  api.subscribePWA(token, JSON.stringify(subscription));
}

// Function to get the Telegram code.
function fetchTelegramToken() {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    api.getTelegramAuthCode(token).then((res) => {
      console.log(res.data);
      telegramToken.value = '/auth ' + res.data; // Updating the value of telegramToken.
    }).catch((err) => {
      console.error("Error getting auth code:", err);
      errorMessage.value = "Failed to fetch the code. Please try again.";
    }).finally(() => {
      isLoading.value = false;
    });
  } catch (err) {
    console.error("Error getting auth code:", err);
    errorMessage.value = "An unexpected error occurred.";
    isLoading.value = false;
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
    console.error("Error retrieving user data:", err);
    router.push("/login");
  }

  try {
    const providers = await api.getNotificationData(token);
    if (typeof providers.data != 'undefined') {
      if (typeof providers.data.providers_available != 'undefined') {
        for (let i in providers.data.providers_available) {
          if ((i == 'telegram') && providers.data.providers_available[i]) {
            tlgAvailable.value = true;
          } else if (i == 'telegram') {
            tlgAvailable.value = false;
          }
        }
      }
      console.log('Providers.data', providers.data);
    } else {
      console.log('Providers', providers);
    }
  } catch (err) {
    console.error("Error retrieving notification provider data:", err);
  }
});
</script>

<style scoped>
.v-card {
  margin-top: 20px;
}
</style>