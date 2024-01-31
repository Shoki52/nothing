<template>
  <div v-loading="loadingContent" class="w-full h-full flex flex-col" v-if="order">
    <h1 class="text-3xl font-medium mb-4">Заказ № {{ order.order_id }}</h1>

    <div class="w-full bg-gray-50 border-[1px] border-gray-300 rounded-lg p-4 mb-8">
      <div class="flex mb-2">
        <p class="w-1/3 text-lg text-gray-500 font-medium">Общая цена:</p>
        <p class="text-xl font-bold">{{ order.order_price }} ₸</p>
      </div>
      <div class="flex mb-4">
        <p class="w-1/3 text-lg text-gray-500 font-medium">Всего продуктов:</p>
        <p class="text-xl font-bold">{{ order.products_amount }} шт.</p>
      </div>
      <div class="flex mb-4">
        <p class="w-1/3 text-lg text-gray-500 font-medium">Адресс доставки:</p>
        <p class="text-xl font-bold">{{ order.delivery_address }} шт.</p>
      </div>
      <div class="flex mb-4">
        <p class="w-1/3 text-lg text-gray-500 font-medium">Статус:</p>
        <el-select v-model="order.delivery_status" @change="orderUpdated" v-loading="loadingUpdate">
          <el-option
            v-for="status in delivery_statuses"
            :value="status.title"
            :style="{ color: statusColor(order.delivery_status) }"
          >
            <div class="flex gap-2 items-center">
              <div
                :style="{
                  backgroundColor: statusColor(status.title),
                  width: '8px',
                  height: '8px',
                  borderRadius: '100%',
                }"
              ></div>
              <p :style="{ color: statusColor(status.title), fontSize: '16px' }">
                {{ status.title }}
              </p>
            </div></el-option
          >
        </el-select>
      </div>
    </div>

    <el-table :data="order.products" class="w-full cursor-pointer" @cellClick="handleClickProduct">
      <el-table-column label="Картинка" width="180">
        <template #default="scope">
          <div class="flex items-center w-[100px]">
            <img :src="scope.row.photo" />
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="Название" sortable class-name="cursor-pointer" />
      <el-table-column prop="price" label="Цена, ₸" sortable />
      <el-table-column prop="amount" label="Колличество, шт." sortable />
      <el-table-column prop="category" label="Категория" />
    </el-table>
  </div>
</template>

<script>
import { Delete, EditPen } from "@element-plus/icons-vue";
import { ElMessageBox } from "element-plus";
import { Order } from "@/services/order.service.js";

export default {
  name: "Order",
  components: { EditPen, Delete },
  data() {
    return {
      loadingContent: false,
      loadingUpdate: false,
      loadingDelete: false,
      order: null,
    };
  },
  computed: {
    delivery_statuses() {
      return this.$store.getters["order/getDeliveryStatuses"];
    },
  },
  async created() {
    await this.getOrder();
  },
  methods: {
    async getOrder() {
      this.loadingContent = true;
      await Order.getOrder(this.$route.params.order_id)
        .then(res => {
          this.order = res.data;
        })
        .finally(() => {
          this.loadingContent = false;
        });
    },

    async handleDelete(order) {
      ElMessageBox.confirm(`Вы действительно хотите удалить заказ № ${order.order_id}?`)
        .then(async () => {
          this.loadingDelete = true;
          await Order.delete(order.id).finally(() => {
            this.loadingDelete = false;
            this.$router.push({ name: "orders" });
          });
        })
        .catch(e => {
          console.log(e);
        });
    },

    handleClickProduct(product) {
      this.$router.push({ name: "product", params: { product_id: product.id } });
    },

    statusColor(status, type = "text") {
      for (let i = 0; i < this.delivery_statuses.length; i++) {
        if (this.delivery_statuses[i].title === status) {
          return type === "text"
            ? this.delivery_statuses[i].color
            : this.delivery_statuses[i].backgroundColor;
        }
      }
      return type === "text" ? "#ef4444" : "#fee2e2";
    },

    async orderUpdated(status) {
      this.loadingUpdate = true;
      await Order.update(this.order.order_id, { delivery_status: status }).finally(() => {
        this.loadingUpdate = false;
      });
    },
  },
};
</script>

<style scoped></style>
