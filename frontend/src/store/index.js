import { createStore } from "vuex";

import auth from "@/store/auth.module.js";
import category from "@/store/category.module.js";
import order from "@/store/order.module.js";

const store = createStore({
  state() {
    return {};
  },
  modules: {
    auth,
    category,
    order,
  },
});

export default store;
