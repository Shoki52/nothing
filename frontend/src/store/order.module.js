export default {
  namespaced: true,
  state: {
    delivery_statuses: [
      {
        title: "Заказ в обработке",
        color: "#ef4444",
        backgroundColor: "#fee2e2",
      },
      {
        title: "Заказ передан в службу доставки",
        color: "#8b5cf6",
        backgroundColor: "#ede9fe",
      },
      {
        title: "Заказ находится у курьера",
        color: "#eab308",
        backgroundColor: "#fef9c3",
      },
      {
        title: "Курьер едет к вам",
        color: "#3b82f6",
        backgroundColor: "#dbeafe",
      },
      {
        title: "Заказ получен",
        color: "#65a30d",
        backgroundColor: "#ecfccb",
      },
    ],
  },
  getters: {
    getDeliveryStatuses(state) {
      return state.delivery_statuses;
    },
  },
};
