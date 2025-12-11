/**
 * API client for chatbot endpoints
 *
 * Configures axios with base URL, credentials, and error handling.
 */
import axios from 'axios';

// Get API URL from environment or default to localhost
// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const API_URL = 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Include HTTP-only cookies
  // headers: {
  //   // 'Content-Type': 'application/json',
  // },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        // Unauthorized - redirect to login
        if (typeof window !== 'undefined' && !window.location.pathname.includes('/auth')) {
          window.location.href = '/auth/login';
        }
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('Network error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
