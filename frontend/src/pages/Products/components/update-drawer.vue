<template>
  <el-drawer v-model="drawerVisible" direction="rtl" :before-close="handleCloseDrawer">
    <template #header>
      <h1>Редактировать продукт</h1>
    </template>
    <template #default>
      <el-form ref="form" :model="form" :rules="rules" label-position="top">
        <el-form-item prop="name" label="Название">
          <el-input v-model="form.name" placeholder="Введите название" />
        </el-form-item>
        <el-form-item prop="description" label="Информация">
          <el-input type="textarea" v-model="form.description" placeholder="Введите информацию" />
        </el-form-item>
        <el-form-item prop="price" label="Цена">
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
          <div class="flex flex-col gap-4">
            <div v-if="form.photo" class="relative rounded-lg overflow-hidden w-1/2">
              <el-image :src="form.photo" />
              <div class="cursor-pointer absolute top-2 right-2">
                <el-icon
                  size="25"
                  @click="
                    form.photo = null;
                    showPhotoError = true;
                  "
                >
                  <Delete />
                </el-icon>
              </div>
            </div>
            <el-upload
              ref="photoRef"
              v-model:file-list="photo"
              class="upload-demo"
              :auto-upload="false"
              accept=".jpg,.png"
            >
              <template #trigger>
                <el-button type="primary">изменить фото</el-button>
              </template>

              <template #tip>
                <div class="el-upload__tip">jpg/png форматы с размером не больше 25мб</div>
                <p class="text-rose-400" v-if="showPhotoError">Прикрепите фотографию товара</p>
              </template>
            </el-upload>
          </div></el-form-item
        >
      </el-form>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="handleCloseDrawer">Отмена</el-button>
        <el-button v-loading="loadingUpdate" type="primary" @click="validate">Принять</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script>
import { ElMessageBox } from "element-plus";
import { Check, Close, Delete, UploadFilled } from "@element-plus/icons-vue";
import { Product } from "@/services/product.service.js";
import { notification } from "@/utils/helpers.js";

export default {
  name: "update-drawer",
  components: {
    Delete,
    UploadFilled,
    Check,
    Close,
  },
  data() {
    return {
      drawerVisible: false,
      form: null,
      loadingUpdate: false,
      showPhotoError: false,
      photo: [],
      rules: {
        name: [{ required: true, message: "Введите название", trigger: "blur" }],
        price: [{ required: true, message: "Введите цену товара", trigger: "blur" }],
        availability: [{ required: true, message: "Выберите доступность", trigger: "blur" }],
        photo: [{ required: true, message: "Выберите картинку", trigger: "blur" }],
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

  watch: {
    drawerProduct(newVal) {
      if (newVal) {
        this.drawerVisible = true;
        this.form = {
          name: this.drawerProduct.name,
          price: this.drawerProduct.price,
          photo: this.drawerProduct.photo,
          description: this.drawerProduct.description,
          availability: this.drawerProduct.availability,
          produced_country: this.drawerProduct.produced_country,
          produced_company: this.drawerProduct.produced_company,
          category: this.drawerProduct.category,
        };
      } else {
        this.drawerVisible = false;
        this.form = {};
      }
    },
  },

  computed: {
    Check() {
      return Check;
    },
    Close() {
      return Close;
    },
    categories() {
      return this.$store.getters["category/categories"];
    },
  },

  props: {
    drawerProduct: Object,
  },

  methods: {
    handleCloseDrawer(done) {
      ElMessageBox.confirm("Вы действительно хотите закрыть?")
        .then(() => {
          this.drawerVisible = false;
          this.$emit("close-drawer");
        })
        .catch(e => {
          console.log(e);
        });
    },
    inputPrice() {
      if (+this.form.price < 0) this.form.price = 0;
      if (isNaN(+this.form.price)) this.form.price = 0;
    },
    async update() {
      this.loadingUpdate = true;
      await Product.update(this.drawerProduct.id, this.form)
        .then(async res => {
          if (res.data.success) {
            await this.uploadPhoto(this.drawerProduct.id, this.photo[0].raw);
          }
        })
        .finally(() => {
          this.$emit("product-updated", this.form);
          notification("Продукт успешно обновлен", "success");
          this.loadingUpdate = false;
          this.drawerVisible = false;
        });
    },
    async uploadPhoto(product_id, file) {
      const formData = new FormData();
      formData.append("file", file);
      return await Product.updatePhoto(product_id, formData);
    },
    validate() {
      this.$refs["form"].validate(async valid => {
        if (this.showPhotoError) {
          if (this.photo[0]) valid = true;
          else valid = false;
        }

        if (valid) {
          await this.update();
        } else {
          console.log("validation error");
        }
      });
    },
  },
};
</script>

<style scoped></style>
