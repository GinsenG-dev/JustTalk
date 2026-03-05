<script setup>
import { ref } from "vue";
import { apiFetch, setToken } from "../api";
import { useRouter } from "vue-router";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");

async function submit() {
  error.value = "";
  try {
    const data = await apiFetch("/auth/register", {
      method: "POST",
      body: { username: username.value, email: email.value, password: password.value },
    });
    setToken(data.access_token);
    router.push("/me");
  } catch (e) {
    error.value = e.message;
  }
}
</script>

<template>
  <div style="max-width:420px;margin:40px auto;">
    <h2>Register</h2>
    <div v-if="error" style="color:red">{{ error }}</div>
    <input v-model="username" placeholder="username" />
    <input v-model="email" placeholder="email" />
    <input v-model="password" placeholder="password" type="password" />
    <button @click="submit">Create account</button>
  </div>
</template>