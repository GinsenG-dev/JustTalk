import { createRouter, createWebHistory } from "vue-router";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Me from "./views/Me.vue";
import { getToken } from "./api";

const routes = [
    { path: "/", redirect: "/me" },
    { path: "/login", component: Login },
    { path: "/register", component: Register },
    { path: "/me", component: Me },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to) => {
    const publicPages = ["/login", "/register"];
    const authed = !!getToken();
    if (!publicPages.includes(to.path) && !authed) return "/login";
});

export default router;