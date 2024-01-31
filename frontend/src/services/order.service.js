import { apiInstance } from "@/api/index.js";
import { notification } from "@/utils/helpers.js";

export const Order = {
  getAll(params) {
    return apiInstance.get("/orders/getAll/", { params }).then(res => res.data);
  },
  getOrder(order_id) {
    return apiInstance.get(`/orders/get/${order_id}`);
  },
  getAmount() {
    return apiInstance.get("/orders/getAmount");
  },
  update(order_id, body) {
    return apiInstance.put(`/orders/update/${order_id}`, body).then(res => {
      if (res.data.success) {
        notification(res.data.message, "success");
      }
    });
  },
  delete(order_id) {
    return apiInstance.delete(`/orders/delete/${order_id}`);
  },
};
