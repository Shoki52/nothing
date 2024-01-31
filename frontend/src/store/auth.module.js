import { getAccessToken } from "@/utils/helpers.js";

export default {
  namespaced: true,
  state: {
    auth: !!getAccessToken(),
  },
  mutations: {
    setAuth: (state, payload) => {
      state.auth = payload;
    },
  },
  getters: {
    isAuth: state => state.auth,
  },
};
