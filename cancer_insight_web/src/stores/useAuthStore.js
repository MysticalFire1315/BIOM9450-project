import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false, // Default state
    token: null, // To store the JWT token
  }),
  actions: {
    login(token) {
      this.isLogin = true; // Update the login state
      this.token = token; // Store the JWT token

      // Optionally store the token in localStorage for persistence
      localStorage.setItem('jwtToken', token);
    },
    logout() {
      this.isLogin = false;
      this.token = null;

      // Remove the token from localStorage when logging out
      localStorage.removeItem('jwtToken');
    },
    // Optionally, add a method to initialize the store from localStorage
    initializeAuth() {
      const storedToken = localStorage.getItem('jwtToken');
      if (storedToken) {
        this.token = storedToken;
        this.isLogin = true; // Set as logged in if a token exists
      }
    }
  },
});
