<script setup>
import { onMounted, ref } from "vue";
import { apiFetch, clearToken } from "../api";
import { useRouter } from "vue-router";

const router = useRouter();
const me = ref(null);
const loadError = ref("");
const saveError = ref("");
const saved = ref(false);
const saving = ref(false);

const displayName = ref("");
const bio = ref("");
const avatarUrl = ref("");

function applyMe(data) {
  me.value = data;
  displayName.value = data.display_name ?? "";
  bio.value = data.bio ?? "";
  avatarUrl.value = data.avatar_url ?? "";
}

onMounted(async () => {
  loadError.value = "";
  try {
    applyMe(await apiFetch("/users/me"));
  } catch (e) {
    loadError.value = e.message;
  }
});

async function saveProfile() {
  saveError.value = "";
  saved.value = false;
  saving.value = true;
  try {
    const body = {
      display_name: displayName.value.trim() || null,
      bio: bio.value.trim() || null,
      avatar_url: avatarUrl.value.trim() || null,
    };
    applyMe(await apiFetch("/users/me", { method: "PATCH", body }));
    saved.value = true;
  } catch (e) {
    saveError.value = e.message;
  } finally {
    saving.value = false;
  }
}

function logout() {
  clearToken();
  router.push("/login");
}
</script>

<template>
  <main class="me-page">
    <section class="me-panel">
      <p class="me-kicker">Профиль</p>
      <h1>Твой аккаунт</h1>
      <p class="me-lead">Имя для отображения, коротко о себе и ссылка на аватар (картинка в интернете).</p>

      <div v-if="loadError" class="form-error">{{ loadError }}</div>

      <template v-else-if="me">
        <div v-if="saveError" class="form-error">{{ saveError }}</div>
        <p v-if="saved" class="me-saved">Сохранено</p>

        <dl class="me-readonly">
          <div>
            <dt>Логин</dt>
            <dd>{{ me.username }}</dd>
          </div>
          <div>
            <dt>Email</dt>
            <dd>{{ me.email }}</dd>
          </div>
        </dl>

        <form class="auth-form" @submit.prevent="saveProfile">
          <label>
            <span>Имя в интерфейсе</span>
            <input v-model="displayName" placeholder="Как показывать в ленте" maxlength="100" />
          </label>
          <label>
            <span>О себе</span>
            <textarea
              v-model="bio"
              class="me-textarea"
              placeholder="Несколько строк о себе"
              rows="4"
              maxlength="2000"
            />
          </label>
          <label>
            <span>URL аватара</span>
            <input
              v-model="avatarUrl"
              placeholder="https://…"
              type="url"
              maxlength="500"
            />
          </label>
          <button type="submit" class="primary-button" :disabled="saving">
            {{ saving ? "Сохраняем…" : "Сохранить" }}
          </button>
        </form>

        <button type="button" class="ghost-button" @click="logout">Выйти</button>
      </template>
    </section>
  </main>
</template>
