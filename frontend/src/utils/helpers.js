import { useToast } from "vue-toastification";
import Cookies from "js-cookie";

export const notification = (text, type) => {
  const toast = useToast();
  const options = {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: "button",
    icon: true,
    rtl: false,
  };

  type === "danger" ? toast.error(text, options) : toast.success(text, options);
};

export const getAccessToken = () => {
  return Cookies.get("access_token");
};

export const changeUrlQueries = (key, val, title) => {
  const domain = window.location.href.split("?")[0];
  window.history.pushState({}, title, domain + "?" + key + "=" + val);
};

export const getUrlQueryByKey = key => {
  const hash = window.location.href.split("?")[1];
  if (hash) {
    const queries = hash.split("&");
    if (queries.length > 0) {
      for (let i = 0; i < queries.length; i++) {
        const currentKey = queries[i].split("=")[0];
        const value = queries[i].split("=")[1];
        if (currentKey === key) return value;
      }
    }
  }
  return null;
};
