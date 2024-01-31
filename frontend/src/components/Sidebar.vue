<template>
  <div class="w-min h-full bg-gray-50 py-6 px-4">
    <el-col class="">
      <div
        class="z-20 w-8 h-8 bg-cyan-500 flex items-center justify-center rounded-lg absolute top-5 left-5"
        @click="isOpened = !isOpened"
      >
        <el-icon size="large" color="white">
          <DArrowRight v-if="!isOpened" />
          <DArrowLeft v-else />
        </el-icon>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="!isOpened"
        default-active="2"
        class="el-menu-vertical-demo w-[250px]"
      >
        <template v-for="menu in links" :key="menu.name">
          <el-sub-menu v-if="menu.children" :index="menu.index">
            <template #title>
              <el-icon>
                <component :is="menu.icon" />
              </el-icon>
              <span>{{ menu.title }}</span>
            </template>

            <template v-if="menu.children">
              <el-menu-item
                v-for="child in menu.children"
                :title="child.title"
                :index="child.index"
                @click="handleOpen(child.name)"
              >
                <el-icon>
                  <component :is="child.icon" />
                </el-icon>
                <span>{{ child.title }}</span>
              </el-menu-item>
            </template>
          </el-sub-menu>

          <el-menu-item v-else :index="menu.index" @click="handleOpen(menu.name)">
            <el-icon><component :is="menu.icon" /></el-icon>
            <template #title>{{ menu.title }}</template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-col>
  </div>
</template>

<script>
import {
  DArrowLeft,
  DArrowRight,
  Menu,
  Goods,
  Shop,
  Delete,
  Plus,
  DataAnalysis,
  Timer,
} from "@element-plus/icons-vue";

export default {
  name: "Sidebar",
  components: {
    DArrowLeft,
    DArrowRight,
    Menu,
    Goods,
    Shop,
    Timer,
    Delete,
    Plus,
    DataAnalysis,
  },
  data() {
    return {
      isOpened: true,
      activeMenu: "1-1",
      links: [
        {
          title: "Продукты",
          name: "products",
          index: "1",
          icon: "Goods",
          children: [
            {
              title: "Все",
              name: "list_products",
              index: "1-1",
              icon: "Shop",
            },
            {
              title: "Добавить",
              name: "add_product",
              index: "1-2",
              icon: "Plus",
            },
            {
              title: "История заказов",
              name: "orders_history",
              index: "1-3",
              icon: "Timer",
            },
          ],
        },
        // { title: "Аналитика", name: "analytics", icon: "DataAnalysis" },
      ],
    };
  },
  created() {
    this.checkInitialTab(this.links, 0);
  },
  methods: {
    handleOpen(routeName) {
      this.$router.push({ name: routeName });
    },
    checkInitialTab(array, index) {
      for (let i = 0; i < array.length; i++) {
        if (array[i].name === this.$route.name) {
          this.activeMenu = array[i].index;
          return;
        }
      }

      if (array[index] && array[index].children) {
        this.checkInitialTab(array[index].children, 0);
      }

      index++;
    },
  },
};
</script>

<style scoped></style>
