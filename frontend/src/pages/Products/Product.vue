<template>
  <div class="w-full h-full flex flex-col" v-if="product">
    <div class="flex justify-between">
      <h1 class="text-4xl mb-3 font-medium">{{ product.name }}</h1>
      <div>
        <el-button size="default" @click="updateProductObject = product">
          <el-icon size="medium"><EditPen /></el-icon
        ></el-button>
        <el-button v-loading="loadingDelete" class="p-0" type="danger" @click="handleDelete">
          <el-icon size="medium"><Delete /></el-icon>
        </el-button>
      </div>
    </div>

    <div class="w-full mt-8 flex gap-8">
      <div class="w-1/4 rounded-lg overflow-hidden">
        <el-image class="max-w-[400px]" :src="product.photo">
          <template #error>
            <div class="image-slot">
              <el-icon class="h-[400px]"><Picture /></el-icon>
            </div> </template
        ></el-image>
      </div>
      <div class="w-3/5 px-8 py-6 text-gray-900 border-[1px] border-gray-300 bg-gray-50 rounded-lg">
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Название:</p>
          <p class="text-xl">{{ product.name }}</p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Описание:</p>
          <p class="text-xl w-2/3">
            {{ product.description }}
          </p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Категория:</p>
          <p class="text-xl">{{ product.category }}</p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Цена:</p>
          <p class="text-xl">{{ product.price }} ₸</p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Наличие в складе:</p>
          <p class="text-xl">
            {{ product.availability ? "Есть в наличии" : "Нет в наличии" }}
          </p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Страна производства:</p>
          <p class="text-xl">{{ product.produced_country }}</p>
        </div>
        <div class="flex mb-4">
          <p class="w-1/3 text-gray-500 font-bold">Компания производства:</p>
          <p class="text-xl">{{ product.produced_company }}</p>
        </div>
      </div>
    </div>

    <update-drawer
      :drawer-product="updateProductObject"
      @close-drawer="updateProductObject = null"
      @product-updated="productUpdated"
    />
  </div>
</template>

<script>
import { Product } from "@/services/product.service.js";
import UpdateDrawer from "@/pages/Products/components/update-drawer.vue";
import { Delete, EditPen, Picture, PictureFilled } from "@element-plus/icons-vue";
import { ElMessageBox } from "element-plus";

export default {
  name: "Product",
  components: { PictureFilled, Picture, UpdateDrawer, EditPen, Delete },
  data() {
    return {
      loadingContent: false,
      loadingDelete: false,
      product: null,
      updateProductObject: null,
    };
  },
  async created() {
    await this.getProduct();
  },
  methods: {
    async getProduct() {
      this.loadingContent = true;
      await Product.getProduct(this.$route.params.product_id)
        .then(res => {
          this.product = res.data;
        })
        .finally(() => {
          this.loadingContent = false;
        });
    },

    async handleDelete() {
      ElMessageBox.confirm(`Вы действительно хотите удалить товар - ${this.product.name}?`)
        .then(async () => {
          this.loadingDelete = true;
          await Product.delete(this.product.id).finally(() => {
            this.loadingDelete = false;
            this.$router.push({ name: "list_products" });
          });
        })
        .catch(e => {
          console.log(e);
        });
    },

    async productUpdated() {
      await this.getProduct();
    },
  },
};
</script>

<style scoped></style>
