import { apiInstance, apiPhoto } from "@/api/index.js";
import { notification } from "@/utils/helpers.js";

export const Product = {
  getAllWithFilter(body, params) {
    return apiInstance.post("/products/getAll/filter/", body, {
      params,
    });
  },
  getAll(params) {
    return apiInstance.get("/products/getAll/", {
      params,
    });
  },
  getProduct(product_id) {
    return apiInstance.get(`/products/get/${product_id}`);
  },
  delete(product_id) {
    return apiInstance.delete(`/products/delete/${product_id}`).then(({ data }) => {
      if (data.success) {
        notification(data.message, "success");
      }
    });
  },
  update(product_id, body) {
    return apiInstance.put(`/products/update/${product_id}`, body);
  },
  create(body) {
    return apiInstance.post("/products/create", body);
  },
  updatePhoto(product_id, formData) {
    return apiPhoto.post(`/products/updatePhoto/${product_id}`, formData);
  },
};
