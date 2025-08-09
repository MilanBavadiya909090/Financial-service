import axios from 'axios';

// Configure base URL for the backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://financial-app-alb-721574606.us-east-1.elb.amazonaws.com:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Get all financial plans
  getFinancialPlans: async () => {
    try {
      const response = await apiClient.get('/api/plans/');
      return {
        success: true,
        data: response.data.data,
        total: response.data.total_plans
      };
    } catch (error) {
      console.error('Error fetching financial plans:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message,
        data: []
      };
    }
  },

  // Create new enrollment
  createEnrollment: async (enrollmentData) => {
    try {
      // Transform frontend data to match backend schema
      const backendData = {
        name: enrollmentData.name,
        email: enrollmentData.email,
        phone: enrollmentData.phone,
        address: enrollmentData.address,
        selected_plan_id: enrollmentData.selectedPlan.id,
        monthly_contribution: parseFloat(enrollmentData.monthlyContribution)
      };

      const response = await apiClient.post('/api/enroll', backendData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error creating enrollment:', error);
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  },

  // Get enrollment by ID
  getEnrollment: async (enrollmentId) => {
    try {
      const response = await apiClient.get(`/api/enroll/${enrollmentId}`);
      return {
        success: true,
        data: response.data.data
      };
    } catch (error) {
      console.error('Error fetching enrollment:', error);
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
};

export default apiService;
