<template>
    <div class="login-container">
      <h1 v-if="!isLoggedIn">Login</h1>
      
      <form v-if="!isLoggedIn" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Enter username" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Enter password" />
        </div>
        <button type="submit">Login</button>
      </form>
      
      <!-- Only show UserDashboard when logged in -->
      <UserDashboard v-if="isLoggedIn" :username="username" />
    </div>
  </template>
  
  <script>
  import UserDashboard from './UserDashboard.vue';
  
  export default {
    name: "LoginPage",
    components: {
      UserDashboard
    },
    data() {
      return {
        username: "",
        password: "",
        isLoggedIn: false,
      };
    },
    methods: {
      handleLogin() {
        if (this.username === "Evan" && this.password === "4396777") {
          this.isLoggedIn = true; // Set login state to true
        } else {
          alert("Invalid credentials. Please try again.");
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: calc(100vh - 50px); /* Adjust height for the top bar */
  }
  </style>
  