<template>
  <div class="w-full h-full flex items-center bg-[#43435e]">
    <!--    <img src="@/assets/bg-login.jpg" class="absolute h-full w-full opacity-50 -z-10" />-->
    <el-form class="form">
      <h1 class="text-center text-white mb-4 text-4xl font-medium">SARA</h1>
      <p class="text-center text-gray-400 text-2xl m-0 mb-4">Admin Dashboard</p>
      <el-form-item>
        <el-input v-model="form.login" placeholder="Login"></el-input>
      </el-form-item>

      <el-form-item>
        <el-input v-model="form.password" type="password" placeholder="Password"></el-input>
      </el-form-item>
      <el-button v-loading="loading" type="" round plain @click="login">Login</el-button>
    </el-form>
  </div>
</template>

<script>
import { notification } from "@/utils/helpers.js";
import { apiInstance } from "@/api/index.js";
import Cookies from "js-cookie";

export default {
  name: "Login",
  data() {
    return {
      loading: false,
      form: {
        login: "",
        password: "",
      },
      rules: [],
    };
  },
  methods: {
    async login() {
      this.loading = true;
      await apiInstance
        .post("/login", { ...this.form })
        .then(res => {
          if (res.data.success) {
            Cookies.set("access_token", res.data.access_token);
            notification("Успешно!", "success");
            this.$store.commit("auth/setAuth", true);
            this.$router.push({ name: "list_products" });
            this.loading = false;
          } else {
            notification(res.data.message, "danger");
            this.form = { login: "", password: "" };
          }
        })
        .catch(error => {
          console.log(error);
          notification(error.response.data.message, "danger");
          this.form = { login: "", password: "" };
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
.form {
  @apply w-1/4 mx-auto bg-[#43435e] p-10 rounded-lg;
  box-shadow: 0 3px 10px rgb(0, 0, 0, 0.2);
}
</style>
