import { defineStore } from 'pinia';

export const useAuthSession = defineStore('session', {
  state: () => ({
    userName:null,
    userEmail:null,
    isLink:null,    // whether the account is linked to a role
    userRole:null
  }),
  actions: {
    login(userName, userEmail, isLink, userRole) {
      this.userName = userName; 
      this.userEmail = userEmail; 
      this.isLink=isLink;
      this.userRole = userRole;

      localStorage.setItem('userName', userName);
      localStorage.setItem('userEmail', userEmail);
      localStorage.setItem('isLink', isLink);
      localStorage.setItem('userRole', userRole);
    },
    logout() {
      this.userName=null;
      this.userEmail=null;
      this.isLink=null;
      this.token = null;

      // Remove all caches from localStorage when logging out
      localStorage.removeItem('userName');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('isLink');
      localStorage.removeItem('userRole');
    },
    // Optionally, add a method to initialize the store from localStorage
    initializeSession() {
      const storedUserName = localStorage.getItem('userName');
      const storedUserEmail = localStorage.getItem('userEmail');
      const storedIsLink = localStorage.getItem('isLink');
      const storedUserRole = localStorage.getItem('userRole')

      if (storedUserName) {
        this.userName = storedUserName;
      }
      if (storedUserEmail) {
        this.userEmail = storedUserEmail;
      }
      if (storedIsLink) {
        this.isLink = storedIsLink;
      }
      if (storedUserRole) {
        this.userRole = storedUserRole;
      }
    }
  },
});
