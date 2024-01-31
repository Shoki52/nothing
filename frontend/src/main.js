import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import Toast from "vue-toastification";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "vue-toastification/dist/index.css";
import "nprogress/nprogress.css";

import router from "@/router";
import store from "@/store/index.js";

const app = createApp(App);

app.use(Toast);
app.use(store);
app.use(router);
app.use(ElementPlus);
app.mount("#app");
