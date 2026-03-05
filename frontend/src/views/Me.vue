<script setup>
import { onMounted, ref } from "vue";
import { apiFetch, clearToken } from "../api";
import { useRouter } from "vue-router";

const router = useRouter();
const me = ref(null);
const error = ref("");

onMounted(async () => {
  try {
    me.value = await apiFetch("/users/me");
  } catch (e) {
    error.value = e.message;
  }
});

function logout() {
  clearToken();
  router.push("/login");
}
</script>

<template>
  <div style="max-width:640px;margin:40px auto;">
    <h2>Me</h2>
    <div v-if="error" style="color:red">{{ error }}</div>
    <pre v-if="me">{{ me }}</pre>
    <button @click="logout">Logout</button>
  </div>
</template>