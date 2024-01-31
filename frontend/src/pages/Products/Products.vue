<template>
  <div class="w-full h-full mb-40 items-center">
    <h1 class="text-3xl mb-3">Все продукты</h1>
    <Filter @filters-changed="changeFilters" />

    <el-table
      v-loading="loadingProducts"
      :data="products"
      class="w-full"
      @cellClick="handleClickProduct"
      class-name="cursor-pointer"
    >
      <el-table-column label="Картинка" width="180">
        <template #default="scope">
          <div class="flex items-center w-[100px]">
            <el-image :src="scope.row.photo" alt="Изображение товара" />
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="Название" sortable />
      <el-table-column prop="category" label="Категория" />
      <el-table-column prop="price" label="Цена, ₸" sortable />
      <el-table-column prop="availability" label="Наличие в складе" sortable>
        <template #default="scope">
          <p>{{ scope.row.availability ? "Есть" : "Нет" }}</p>
        </template>
      </el-table-column>
      <el-table-column align="right">
        <template #default="scope">
          <el-button size="medium" @click.stop="drawerProduct = scope.row">
            <el-icon size="medium"><EditPen /></el-icon
          ></el-button>
          <el-button
            v-loading="scope.row.id === loadingDeleteId"
            class="p-0"
            type="danger"
            @click.stop="handleDelete(scope.row)"
          >
            <el-icon size="medium"><Delete /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        small
        background
        layout="prev, pager, next"
        :current-page="page"
        @update:current-page="v => (page = v)"
        :total="amount"
        :page-size="params.limit"
        v-if="amount > params.limit"
      />
    </div>

    <update-drawer
      :drawer-product="drawerProduct"
      @close-drawer="drawerProduct = null"
      @product-updated="productUpdated"
    />
  </div>
</template>

<script>
import Filter from "@/pages/Products/components/filter.vue";
import { Delete, EditPen } from "@element-plus/icons-vue";
import { Product } from "@/services/product.service.js";
import { changeUrlQueries, getUrlQueryByKey } from "@/utils/helpers.js";
import UpdateDrawer from "@/pages/Products/components/update-drawer.vue";
import { ElMessageBox } from "element-plus";

export default {
  name: "Products",
  components: { UpdateDrawer, EditPen, Delete, Filter },
  data() {
    return {
      loadingProducts: false,
      loadingDeleteId: -1,
      products: [],
      amount: 0,
      page: 1,
      filters: {
        text: "",
        price: 0,
        sort: 0,
        category: "",
        availability: null,
      },
      params: {
        limit: 20,
        skip: 0,
      },
      drawerVisible: false,
      drawerProduct: null,
    };
  },
  watch: {
    async page(n, o) {
      this.params.skip = (this.page - 1) * this.params.limit;
      await this.getProductsWithFilter();
    },
  },
  async created() {
    await this.$store.dispatch("category/getCategories");
    this.params.skip = (this.page - 1) * this.params.limit;
    await this.getProductsWithFilter();
  },
  methods: {
    async getProductsWithFilter() {
      this.loadingProducts = true;
      await Product.getAllWithFilter(this.filters, this.params).then(res => {
        this.products = res.data.products;
        this.amount = res.data.products_amount;
      });
      this.loadingProducts = false;
    },

    async getProducts() {
      this.loadingProducts = true;
      await Product.getAll(this.params).then(res => {
        this.products = res.data.products;
        this.amount = res.data.products_amount;
      });
      this.loadingProducts = false;
    },

    async handleDelete(product) {
      ElMessageBox.confirm(`Вы действительно хотите удалить товар - ${product.name}?`)
        .then(async () => {
          this.loadingDeleteId = product.id;
          await Product.delete(product.id).finally(() => {
            this.loadingDeleteId = -1;
            this.products = this.products.filter(p => p.id !== product.id);
          });
        })
        .catch(e => {
          console.log(e);
        });
    },
    async changeFilters(filter) {
      this.filters = filter;
      if (this.page === 1) await this.getProductsWithFilter();
      else this.page = 1;
    },
    handleClickProduct(product) {
      this.$router.push({ name: "product", params: { product_id: product.id } });
    },
    async productUpdated() {
      await this.getProductsWithFilter();
    },
  },
};
</script>

<style scoped lang="scss">
.pagination-container {
  @apply flex justify-center py-8 w-full mx-auto;
}
</style>
