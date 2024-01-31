<template>
  <div class="filter">
    <div class="filter-item">
      <p class="title">Поиск</p>
      <el-input v-model="filters.text" size="medium" placeholder="поиск" />
    </div>

    <div class="filter-item">
      <p class="title">Цена</p>
      <el-select v-model="filters.sort" size="medium" placeholder="цена">
        <el-option
          v-for="item in [
            { title: 'Нет фильтра', id: 0 },
            { title: 'По возрастанию', id: 1 },
            { title: 'По убыванию', id: 2 },
          ]"
          :key="item.title"
          :value="item.id"
          :label="item.title"
        ></el-option>
      </el-select>
    </div>

    <div class="filter-item">
      <p class="title">Категория</p>
      <el-select v-model="filters.category" size="medium" placeholder="категория">
        <el-option :value="''" label="Все"></el-option>
        <el-option v-for="item in categories" :key="item" :value="item" :label="item"></el-option>
      </el-select>
    </div>

    <div class="filter-item">
      <p class="title">Наличие в складе</p>
      <el-select v-model="filters.availability" size="medium" placeholder="наличие">
        <el-option
          v-for="item in [
            { title: 'Нет фильтра', id: null },
            { title: 'Доступен на складе', id: true },
            { title: 'Недоступен на складе', id: false },
          ]"
          :key="item.title"
          :value="item.id"
          :label="item.title"
        ></el-option>
      </el-select>
    </div>
  </div>
</template>

<script>
export default {
  name: "filter",
  data() {
    return {
      filters: {
        text: "",
        price: 0,
        sort: 0,
        category: "",
        availability: null,
      },
    };
  },
  computed: {
    categories() {
      return this.$store.getters["category/categories"];
    },
  },
  watch: {
    filters: {
      deep: true,
      handler: "changeFilters",
    },
  },
  methods: {
    changeFilters() {
      this.$emit("filters-changed", this.filters);
    },
  },
};
</script>

<style scoped lang="scss">
.filter {
  @apply flex gap-8 w-full rounded-lg border-gray-200 py-2 px-4 h-[80px] bg-gray-50 mb-8;
  border-width: 1px;

  &-item {
    max-width: 210px;

    .title {
      @apply text-gray-400 text-base;
    }
  }
}
</style>
