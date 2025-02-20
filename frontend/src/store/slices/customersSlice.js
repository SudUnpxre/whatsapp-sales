import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  customers: [],
  loading: false,
  error: null,
  selectedCustomer: null,
  filters: {
    search: '',
    status: 'all',
    dateRange: {
      start: null,
      end: null,
    },
  },
  pagination: {
    page: 1,
    limit: 10,
    total: 0,
  },
  statistics: {
    totalCustomers: 0,
    activeCustomers: 0,
    averageOrderValue: 0,
    customersBySource: {},
    customerActivity: [],
  },
};

const customersSlice = createSlice({
  name: 'customers',
  initialState,
  reducers: {
    fetchCustomersStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchCustomersSuccess: (state, action) => {
      state.loading = false;
      state.customers = action.payload.customers;
      state.pagination.total = action.payload.total;
    },
    fetchCustomersFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    addCustomerStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    addCustomerSuccess: (state, action) => {
      state.loading = false;
      state.customers.unshift(action.payload);
    },
    addCustomerFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    updateCustomerStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    updateCustomerSuccess: (state, action) => {
      state.loading = false;
      const index = state.customers.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.customers[index] = action.payload;
      }
    },
    updateCustomerFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    setSelectedCustomer: (state, action) => {
      state.selectedCustomer = action.payload;
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
    updateCustomerInteraction: (state, action) => {
      const { customerId, interaction } = action.payload;
      const customerIndex = state.customers.findIndex(c => c.id === customerId);
      if (customerIndex !== -1) {
        const customer = state.customers[customerIndex];
        customer.interaction_history = [
          ...(customer.interaction_history || []),
          interaction
        ];
        customer.last_interaction = new Date().toISOString();
      }
    },
    clearCustomersError: (state) => {
      state.error = null;
    },
  },
});

export const {
  fetchCustomersStart,
  fetchCustomersSuccess,
  fetchCustomersFailure,
  addCustomerStart,
  addCustomerSuccess,
  addCustomerFailure,
  updateCustomerStart,
  updateCustomerSuccess,
  updateCustomerFailure,
  setSelectedCustomer,
  setFilters,
  setPagination,
  updateStatistics,
  updateCustomerInteraction,
  clearCustomersError,
} = customersSlice.actions;

export default customersSlice.reducer;

// Selectors
export const selectCustomers = (state) => state.customers.customers;
export const selectCustomersLoading = (state) => state.customers.loading;
export const selectCustomersError = (state) => state.customers.error;
export const selectSelectedCustomer = (state) => state.customers.selectedCustomer;
export const selectCustomersFilters = (state) => state.customers.filters;
export const selectCustomersPagination = (state) => state.customers.pagination;
export const selectCustomersStatistics = (state) => state.customers.statistics; 