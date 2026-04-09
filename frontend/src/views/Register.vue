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
  <main class="auth-shell">
    <section class="auth-hero">
      <p class="eyebrow">JustTalk</p>
      <h1>Собери свой круг общения без лишнего шума.</h1>
      <p class="hero-copy">
        Лента близких людей, быстрые мысли, приватные диалоги и ощущение, что
        соцсеть снова сделана для людей, а не для алгоритма.
      </p>

      <div class="hero-points">
        <div class="point-card">
          <span class="point-title">Живые профили</span>
          <span class="point-text">Короткие статусы, голос, фото и привычки в одном месте.</span>
        </div>
        <div class="point-card">
          <span class="point-title">Камерные круги</span>
          <span class="point-text">Создавай свои закрытые пространства для друзей и команд.</span>
        </div>
        <div class="point-card">
          <span class="point-title">Без перегруза</span>
          <span class="point-text">Только понятные действия: написать, позвать, поделиться.</span>
        </div>
      </div>
    </section>

    <section class="auth-panel">
      <div class="panel-inner">
        <p class="panel-kicker">Ранний доступ</p>
        <h2>Создай аккаунт</h2>
        <p class="panel-copy">Займёт меньше минуты. Потом можно будет сразу настроить профиль.</p>

        <div v-if="error" class="form-error">{{ error }}</div>

        <form class="auth-form" @submit.prevent="submit">
          <label>
            <span>Имя пользователя</span>
            <input v-model="username" placeholder="@petarda" autocomplete="username" />
          </label>

          <label>
            <span>Email</span>
            <input v-model="email" placeholder="name@example.com" autocomplete="email" />
          </label>

          <label>
            <span>Пароль</span>
            <input
              v-model="password"
              placeholder="Минимум 6 символов"
              type="password"
              autocomplete="new-password"
            />
          </label>

          <button type="submit" class="primary-button">Зарегистрироваться</button>
        </form>

        <p class="panel-footer">
          Уже есть аккаунт?
          <router-link to="/login">Войти</router-link>
        </p>
      </div>
    </section>
  </main>
</template>
