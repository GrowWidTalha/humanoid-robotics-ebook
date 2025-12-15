/**
 * Authentication service for frontend API calls
 *
 * Provides functions for user registration, login, logout, and session management.
 * Uses axios with credentials for HTTP-only cookie support.
 */
import axios from 'axios';

// Get API URL from environment or default to localhost
const API_URL = 'http://localhost:8000/api';
// const API_URL = "https://growwithtalha-humanoid-robotics-rag.hf.space/api";

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Important: Include HTTP-only cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Register a new user account
 */
export async function register(email, password) {
  const response = await apiClient.post('/auth/register', {
    email,
    password,
  });
  return response.data;
}

/**
 * Login with email and password
 */
export async function login(email, password) {
  const response = await apiClient.post('/auth/login', {
    email,
    password,
  });
  return response.data;
}

/**
 * Logout current user
 */
export async function logout() {
  const response = await apiClient.post('/auth/logout');
  return response.data;
}

/**
 * Get current authenticated user
 */
export async function getCurrentUser() {
  try {
    const response = await apiClient.get('/auth/me');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      // Not authenticated
      return null;
    }
    throw error;
  }
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated() {
  const user = await getCurrentUser();
  return user !== null;
}
