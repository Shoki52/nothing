<template>
  <div class="w-full h-full items-center">
    <h1 class="text-3xl mb-3">История заказов</h1>

    <el-table
      v-loading="loadingHistories"
      :data="histories"
      class="w-full"
      @rowClick="handleCLickOrder"
      class-name="cursor-pointer"
    >
      <el-table-column prop="order_id" label="ID" width="50" />
      <el-table-column prop="delivery_address" label="Адресс доставки" />
      <el-table-column prop="order_price" label="Цена, ₸" width="250" />
      <el-table-column prop="delivery_status" label="Статус">
        <template #default="scope">
          <div
            class="flex gap-2 items-center"
            :style="{
              backgroundColor: statusColor(scope.row.delivery_status, 'bg'),
              width: 'max-content',
              padding: '5px 15px',
              borderRadius: '5px',
            }"
          >
            <div
              :style="{
                backgroundColor: statusColor(scope.row.delivery_status),
                width: '8px',
                height: '8px',
                borderRadius: '100%',
              }"
            ></div>
            <p :style="{ color: statusColor(scope.row.delivery_status), fontSize: '16px' }">
              {{ scope.row.delivery_status }}
            </p>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        small
        background
        layout="prev, pager, next"
        @update:current-page="v => (page = v)"
        :total="amount"
        :page-size="params.limit"
        v-if="amount > params.limit"
      />
    </div>
  </div>
</template>

<script>
import { Order } from "@/services/order.service.js";

export default {
  name: "History",
  data() {
    return {
      loadingHistories: false,
      histories: [],
      page: 1,
      amount: null,
      params: {
        limit: 20,
        skip: 0,
      },
    };
  },
  computed: {
    delivery_statuses() {
      return this.$store.getters["order/getDeliveryStatuses"];
    },
  },
  watch: {
    async page() {
      this.params.skip = (this.page - 1) * this.params.limit;
      await this.getHistories();
    },
  },
  async created() {
    await this.getHistories();
    await this.getAmount();
  },
  methods: {
    async getHistories() {
      this.loadingHistories = true;
      await Order.getAll(this.params)
        .then(data => {
          this.histories = data;
        })
        .finally(() => {
          this.loadingHistories = false;
        });
    },
    async getAmount() {
      await Order.getAmount().then(res => {
        this.amount = res.data.amount;
      });
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
    handleCLickOrder(order) {
      this.$router.push({ name: "order_page", params: { order_id: order.order_id } });
    },
  },
};
</script>

<style scoped lang="scss">
.pagination-container {
  @apply flex justify-center py-8 w-full mx-auto;
}
</style>
