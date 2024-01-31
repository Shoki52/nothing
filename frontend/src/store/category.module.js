import { Category } from "@/services/category.service.js";

export default {
  namespaced: true,
  state: {
    categories: [],
  },
  mutations: {
    setCategories: (state, payload) => {
      state.categories = payload;
    },
  },
  actions: {
    async getCategories({ commit }, payload) {
      await Category.getCategories().then(res => {
        commit("setCategories", res.data);
      });
    },
  },
  getters: {
    categories: state => state.categories,
  },
};
