<template>
  <v-container class="login-form">
    <h2 class="text-h4 mb-6 text-center">Login</h2>
    <v-form @submit.prevent="handleLogin" ref="form">
      <v-text-field
          v-model="username"
          label="Login"
          placeholder="Enter login"
          required
          :rules="[rules.required]"
          variant="outlined"
          clearable
      ></v-text-field>

      <v-text-field
          v-model="password"
          label="Password"
          placeholder="Enter password"
          type="password"
          required
          :rules="[rules.required]"
          variant="outlined"
          clearable
      ></v-text-field>

      <v-btn
          type="submit"
          color="primary"
          block
          :loading="isLoading"
          :disabled="!isFormValid"
      >
        Login
      </v-btn>

      <p v-if="error" class="text-red mt-4">{{ error }}</p>
    </v-form>
  </v-container>
</template>

<script setup>
import {ref} from "vue";
import api from "../api";
import {useRouter} from "vue-router";

const username = ref("");
const password = ref("");
const error = ref("");
const isLoading = ref(false);
const router = useRouter();


// Link to the form for validation check
const form = ref(null);

// Validation
const rules = {
  required: (value) => !!value || "Required field",
};

// Form validity flag
const isFormValid = ref(true);

async function handleLogin() {
  // Checking the form's validity
  const valid = await form.value.validate();
  if (!valid) return;

  isLoading.value = true;
  try {
    const response = await api.login(username.value, password.value);
    const token = response.data.access_token;
    localStorage.setItem("token", token); // Save token
    router.push("/dashboard"); // go to the basic page
  } catch (err) {
    error.value = "Invalid login or password";
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
}

.text-red {
  color: red;
}
</style>