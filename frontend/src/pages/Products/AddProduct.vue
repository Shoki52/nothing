<template>
  <div class="w-full items-center">
    <h1 class="text-3xl mb-3">Создать товар</h1>

    <el-form ref="form" class="w-2/3" :model="form" :rules="rules" label-position="top">
      <el-form-item prop="name" label="Название">
        <el-input v-model="form.name" placeholder="Введите название" />
      </el-form-item>
      <el-form-item prop="description" label="Информация">
        <el-input type="textarea" v-model="form.description" placeholder="Введите информацию" />
      </el-form-item>
      <el-form-item class="w-40" prop="price" label="Цена">
        <el-input
          type="number"
          v-model="form.price"
          @input="inputPrice"
          placeholder="Введите цену"
        />
      </el-form-item>
      <el-form-item prop="produced_country" label="Страна производства">
        <el-input v-model="form.produced_country" placeholder="Введите страну производства" />
      </el-form-item>
      <el-form-item prop="produced_company" label="Компания производства">
        <el-input v-model="form.produced_company" placeholder="Введите компанию производства" />
      </el-form-item>
      <el-form-item prop="category" label="Категория">
        <el-select v-model="form.category" placeholder="Выберите категорию">
          <el-option v-for="c in categories" :label="c" :value="c" :key="c"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item prop="availability" label="Наличие в складе">
        <el-switch v-model="form.availability" :active-icon="Check" :inactive-icon="Close" />
      </el-form-item>
      <el-form-item>
        <el-upload
          ref="photoRef"
          class="upload-demo"
          drag
          v-model:file-list="form.photo"
          show-file-list
          @change="handleChangeFile"
          :auto-upload="false"
          :multiple="false"
          accept=".jpg,.png"
        >
          <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
          <div class="el-upload__text">
            Вставьте фотографию сюда или <em>нажмите чтобы загрузить</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">jpg/png форматы с размером меньше 25мб</div>
            <p class="text-rose-400" v-if="showPhotoError">Прикрепите фотографию товара</p>
          </template>
        </el-upload></el-form-item
      >
      <el-form-item>
        <el-button
          @click="validate"
          v-loading="loadingCreate"
          class="ml-auto"
          type="primary"
          >Создать товар</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { Check, Close, UploadFilled } from "@element-plus/icons-vue";
import { Product } from "@/services/product.service.js";
import { notification } from "@/utils/helpers.js";

export default {
  name: "AddProduct",
  components: { UploadFilled },
  data() {
    return {
      loadingCreate: false,
      showPhotoError: false,
      form: {
        name: "",
        price: 0,
        photo: [],
        description: "",
        availability: true,
        produced_country: "",
        produced_company: "",
        category: "",
      },
      rules: {
        name: [{ required: true, message: "Введите название", trigger: "blur" }],
        price: [{ required: true, message: "Введите цену товара", trigger: "blur" }],
        availability: [{ required: true, message: "Выберите доступность", trigger: "blur" }],
        photo: [
          { required: true, message: "Выберите картинку", trigger: "blur" },
          {
            type: "file",
            max: 25000,
            message: "Размер картинки должен быть меньше 25мб",
          },
          { accept: [".jpg", ".png"], message: "Только форматы jpg и png" },
        ],
        description: [{ required: true, message: "Напишите информацию", trigger: "blur" }],
        produced_country: [
          { required: true, message: "Введите страну производства", trigger: "blur" },
        ],
        produced_company: [
          { required: true, message: "Введите компанию производства", trigger: "blur" },
        ],
        category: [{ required: true, message: "Выберите категорию товара", trigger: "blur" }],
      },
    };
  },
  computed: {
    Close() {
      return Close;
    },
    Check() {
      return Check;
    },
    categories() {
      return this.$store.getters["category/categories"];
    },
  },
  async created() {
    await this.$store.dispatch("category/getCategories");
  },
  methods: {
    validate() {
      this.$refs["form"].validate(async valid => {
        if (this.form.photo.length === 0) {
          valid = false;
          this.showPhotoError = true;
        } else {
          this.showPhotoError = false;
        }
        if (valid) {
          await this.create();
        } else {
          console.log("validation error");
        }
      });
    },
    async create() {
      let body = {
        name: this.form.name,
        price: this.form.price,
        availability: this.form.availability,
        description: this.form.description,
        produced_country: this.form.produced_country,
        produced_company: this.form.produced_company,
        category: this.form.category,
      };
      this.loadingCreate = true;
      await Product.create(body)
        .then(async ({ data }) => {
          if (data.success) {
            await this.uploadPhoto(
              data.product_id,
              this.form.photo[0] && this.form.photo[0].raw
            ).then(res => {
              if (res.data.success) {
                notification("Продукт успешно создан", "success");
              }
            });
          }
        })
        .finally(() => {
          this.loadingCreate = false;
        });
    },
    async uploadPhoto(product_id, file) {
      const formData = new FormData();
      formData.append("file", file);
      return await Product.updatePhoto(product_id, formData);
    },
    inputPrice() {
      if (+this.form.price < 0) this.form.price = 0;
      if (isNaN(+this.form.price)) this.form.price = 0;
    },
    handleChangeFile() {
      this.form.price += 1;
      this.form.price -= 1;
    },
  },
};
</script>

<style scoped></style>
