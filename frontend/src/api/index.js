import axios from "axios";
import { getAccessToken } from "../utils/helpers.js";
import Cookies from "js-cookie";

const axiosOptions = {
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
};
const photoOptions = {
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "multipart/form-data",
  },
};

export const apiInstance = axios.create(axiosOptions);
export const apiPhoto = axios.create(photoOptions);

apiInstance.interceptors.request.use(res => {
  res.headers.Authorization = `Bearer ${getAccessToken()}`;

  return res;
});
apiInstance.interceptors.response.use(
  config => config,
  async config => {
    const store = (await import("@/store/index.js")).default;
    const router = (await import("@/router/index.js")).default;
    if (config.response.status === 403) {
      Cookies.remove("access_token");
      store.commit("auth/setAuth", false);
      router.push({ name: "login" });
    } else {
      store.commit("auth/setAuth", true);
    }

    return config.response;
  }
);

apiPhoto.interceptors.request.use(res => {
  res.headers.Authorization = `Bearer ${getAccessToken()}`;

  return res;
});
