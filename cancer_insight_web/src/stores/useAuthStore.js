import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false, // Default state
  }),
  actions: {
    login() {
      this.isLogin = true; // Toggle the login state
    },
    logout() {
        this.isLogin = false;
    }
  },
});
