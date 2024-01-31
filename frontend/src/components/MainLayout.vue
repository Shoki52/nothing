<template>
  <div
    class="w-full flex justify-between items-center px-8 text-3xl bg-blue-900 text-white h-[80px]"
  >
    <h1 class="ml-8">ADMIN DASHBOARD</h1>
    <el-button v-loading="logoutLoading" round type="danger" @click="logout"
      ><el-icon size="large" color="white"><SwitchButton /></el-icon
    ></el-button>
  </div>

  <div class="w-full h-full flex overflow-y-auto">
    <div class="w-min h-full">
      <sidebar></sidebar>
    </div>
    <div class="w-full h-full overflow-y-auto p-8">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import { apiInstance } from "@/api/index.js";
import { SwitchButton } from "@element-plus/icons-vue";
import Cookies from "js-cookie";

export default {
  name: "MainLayout",
  components: { Sidebar, SwitchButton },
  data() {
    return {
      logoutLoading: false,
    };
  },
  methods: {
    async logout() {
      this.logoutLoading = true;
      await apiInstance
        .get("/logout")
        .then(res => {
          if (res.data.success) {
            Cookies.remove("access_token");
            this.$store.commit("auth/setAuth", false);
            this.$router.push({ name: "login" });
          }
        })
        .catch(e => {
          console.log(e);
        });
      this.logoutLoading = false;
    },
  },
};
</script>

<style scoped></style>
