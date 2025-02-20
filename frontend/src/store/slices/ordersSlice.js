import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  orders: [],
  loading: false,
  error: null,
  selectedOrder: null,
  filters: {
    search: '',
    status: 'all',
    dateRange: {
      start: null,
      end: null,
    },
    paymentMethod: 'all',
  },
  pagination: {
    page: 1,
    limit: 10,
    total: 0,
  },
  statistics: {
    totalOrders: 0,
    totalRevenue: 0,
    averageOrderValue: 0,
    ordersByStatus: {},
    revenueByDay: [],
  },
};

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {
    fetchOrdersStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchOrdersSuccess: (state, action) => {
      state.loading = false;
      state.orders = action.payload.orders;
      state.pagination.total = action.payload.total;
    },
    fetchOrdersFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    createOrderStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    createOrderSuccess: (state, action) => {
      state.loading = false;
      state.orders.unshift(action.payload);
    },
    createOrderFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    updateOrderStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    updateOrderSuccess: (state, action) => {
      state.loading = false;
      const index = state.orders.findIndex(o => o.id === action.payload.id);
      if (index !== -1) {
        state.orders[index] = action.payload;
      }
    },
    updateOrderFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    cancelOrderStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    cancelOrderSuccess: (state, action) => {
      state.loading = false;
      const index = state.orders.findIndex(o => o.id === action.payload.id);
      if (index !== -1) {
        state.orders[index] = { ...state.orders[index], status: 'cancelled' };
      }
    },
    cancelOrderFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    setSelectedOrder: (state, action) => {
      state.selectedOrder = action.payload;
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
      state.pagination.page = 1; // Reset page when filters change
    },
    setPagination: (state, action) => {
      state.pagination = { ...state.pagination, ...action.payload };
    },
    updateStatistics: (state, action) => {
      state.statistics = { ...state.statistics, ...action.payload };
    },
    clearOrdersError: (state) => {
      state.error = null;
    },
  },
});

export const {
  fetchOrdersStart,
  fetchOrdersSuccess,
  fetchOrdersFailure,
  createOrderStart,
  createOrderSuccess,
  createOrderFailure,
  updateOrderStart,
  updateOrderSuccess,
  updateOrderFailure,
  cancelOrderStart,
  cancelOrderSuccess,
  cancelOrderFailure,
  setSelectedOrder,
  setFilters,
  setPagination,
  updateStatistics,
  clearOrdersError,
} = ordersSlice.actions;

export default ordersSlice.reducer;

// Selectors
export const selectOrders = (state) => state.orders.orders;
export const selectOrdersLoading = (state) => state.orders.loading;
export const selectOrdersError = (state) => state.orders.error;
export const selectSelectedOrder = (state) => state.orders.selectedOrder;
export const selectOrdersFilters = (state) => state.orders.filters;
export const selectOrdersPagination = (state) => state.orders.pagination;
export const selectOrdersStatistics = (state) => state.orders.statistics; 