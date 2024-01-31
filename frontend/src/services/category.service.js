import { apiInstance } from "@/api/index.js";

export const Category = {
  getCategories() {
    return apiInstance.get("/products/getCategory");
  },
};
