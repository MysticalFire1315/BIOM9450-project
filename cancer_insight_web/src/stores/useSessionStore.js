import { defineStore } from 'pinia';

export const useSessionStore = defineStore('session', {
  state: () => ({
    userName:null,
    userEmail:null,
    userRole:null
  }),
  actions: {
    login(userName, userEmail, userRole) {
      this.userName = userName; 
      this.userEmail = userEmail; 
      this.userRole = userRole;

      localStorage.setItem('userName', userName);
      localStorage.setItem('userEmail', userEmail);
      localStorage.setItem('userRole', userRole);
    },
    logout() {
      this.userName=null;
      this.userEmail=null;
      this.token = null;

      // Remove all caches from localStorage when logging out
      localStorage.removeItem('userName');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userRole');
    },
    // Optionally, add a method to initialize the store from localStorage
    initializeSession() {
      const storedUserName = localStorage.getItem('userName');
      const storedUserEmail = localStorage.getItem('userEmail');
      const storedUserRole = localStorage.getItem('userRole')

      if (storedUserName) {
        this.userName = storedUserName;
      }
      if (storedUserEmail) {
        this.userEmail = storedUserEmail;
      }
      if (storedUserRole) {
        this.userRole = storedUserRole;
      }
    }
  },
});
