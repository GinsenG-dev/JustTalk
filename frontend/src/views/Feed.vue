<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../api";

const posts = ref([]);
const loading = ref(true);
const loadError = ref("");
const composeError = ref("");
const newTitle = ref("");
const newBody = ref("");
const publishing = ref(false);

function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function authorLabel(author) {
  if (!author) return "";
  return author.display_name?.trim() || author.username || "Пользователь";
}

async function fetchPosts() {
  loadError.value = "";
  loading.value = true;
  try {
    posts.value = await apiFetch("/posts");
  } catch (e) {
    loadError.value = e.message;
    posts.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(fetchPosts);

async function publishPost() {
  composeError.value = "";
  publishing.value = true;
  try {
    await apiFetch("/posts", {
      method: "POST",
      body: { title: newTitle.value, body: newBody.value },
    });
    newTitle.value = "";
    newBody.value = "";
    await fetchPosts();
  } catch (e) {
    composeError.value = e.message;
  } finally {
    publishing.value = false;
  }
}
</script>

<template>
  <main class="feed-page">
    <div class="feed-layout">
      <header class="feed-top">
        <div>
          <p class="me-kicker" style="margin-bottom: 6px">JustTalk</p>
          <h1 class="feed-title">Лента</h1>
          <p class="me-lead" style="margin-top: 8px; margin-bottom: 0">
            Посты всех пользователей — новые сверху.
          </p>
        </div>
        <nav class="feed-nav">
          <router-link to="/me" class="feed-nav-link">Профиль</router-link>
        </nav>
      </header>

      <section class="feed-panel feed-compose">
        <h2 class="feed-section-title">Новый пост</h2>
        <div v-if="composeError" class="form-error">{{ composeError }}</div>
        <form class="auth-form" @submit.prevent="publishPost">
          <label>
            <span>Заголовок</span>
            <input v-model="newTitle" maxlength="200" placeholder="Коротко о чём пост" />
          </label>
          <label>
            <span>Текст</span>
            <textarea
              v-model="newBody"
              class="me-textarea"
              rows="4"
              maxlength="10000"
              placeholder="Что хочешь сказать?"
            />
          </label>
          <button type="submit" class="primary-button" :disabled="publishing">
            {{ publishing ? "Публикуем…" : "Опубликовать" }}
          </button>
        </form>
      </section>

      <section class="feed-panel">
        <h2 class="feed-section-title">Сейчас в ленте</h2>

        <p v-if="loading" class="feed-muted">Загружаем…</p>
        <div v-else-if="loadError" class="form-error">{{ loadError }}</div>
        <p v-else-if="!posts.length" class="feed-muted">Пока пусто — будь первым.</p>

        <ul v-else class="feed-list">
          <li v-for="p in posts" :key="p.id" class="feed-card">
            <div class="feed-card-head">
              <span class="feed-author">{{ authorLabel(p.author) }}</span>
              <span class="feed-meta">@{{ p.author?.username }} · {{ formatDate(p.created_at) }}</span>
            </div>
            <h3 class="feed-card-title">{{ p.title }}</h3>
            <p class="feed-card-body">{{ p.body }}</p>
          </li>
        </ul>
      </section>
    </div>
  </main>
</template>
