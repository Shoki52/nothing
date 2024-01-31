import { createRouter, createWebHashHistory } from "vue-router";
import { notification } from "@/utils/helpers.js";
import NProgress from "nprogress";
import Cookies from "js-cookie";
import { useStore } from "vuex";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/admin",
      name: "main",
      redirect: { name: "products" },
      children: [
        {
          path: "",
          name: "main_layout",
          component: () => import("@/components/MainLayout.vue"),
          children: [
            {
              path: "products",
              name: "products",
              redirect: { name: "list_products" },
              children: [
                {
                  path: "list",
                  name: "list_products",
                  meta: {
                    title: "Все продукты",
                  },
                  component: () => import("@/pages/Products/Products.vue"),
                },
                {
                  path: "add",
                  name: "add_product",
                  meta: {
                    title: "Добавить продукт",
                  },
                  component: () => import("@/pages/Products/AddProduct.vue"),
                },
                {
                  path: ":product_id",
                  name: "product",
                  component: () => import("@/pages/Products/Product.vue"),
                },
              ],
            },
            {
              path: "orders",
              name: "orders",
              meta: {
                title: "Заказы",
              },
              redirect: { name: "orders_history" },
              children: [
                {
                  path: "history",
                  name: "orders_history",
                  meta: {
                    title: "История заказов",
                  },
                  component: () => import("@/pages/Products/Orders.vue"),
                },
                {
                  path: ":order_id",
                  name: "order_page",
                  component: () => import("@/pages/Products/Order.vue"),
                },
              ],
            },
          ],
        },
        {
          path: "login",
          name: "login",
          meta: {
            title: "Войти в систему",
          },
          component: () => import("@/pages/Auth/Login.vue"),
        },
      ],
    },
  ],
});

router.beforeEach(async (to, from) => {
  NProgress.start();
  const store = useStore();
  const isAuthenticated = store.getters["auth/isAuth"];

  if (!isAuthenticated && to.name !== "login") {
    notification("Войдите в аккаунт!", "danger");
    Cookies.remove("access_token");
    store.commit("auth/setAuth", false);
    return { name: "login" };
  }

  if (isAuthenticated && to.name === "login") {
    notification("Вы уже авторизованы!", "danger");
    return { name: "products" };
  }

  if (!to.fullPath.includes("admin")) {
    return { name: isAuthenticated ? "products" : "login" };
  }

  return true;
});

router.afterEach((to, from) => {
  NProgress.done();
  document.title = to.meta.title || "Админ";
});

export default router;
