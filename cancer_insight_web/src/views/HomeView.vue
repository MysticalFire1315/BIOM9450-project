<template>
  <div class="home">
    <div class="login-window">
      <h1>Login</h1>
      <!-- <form @submit.prevent="handleLogin"> -->
      <!-- <form> -->
        <input type="text" v-model="username" placeholder="Username" />
        <!-- should add required later -->
        <input type="password" v-model="password" placeholder="Password"/>
        <button type="submit" @click="handleLogin">Login</button>
      <!-- </form> -->
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'; // Import ref for reactive variables
import { useAuthStore } from '../stores/useAuthStore';
import { useRouter } from 'vue-router';

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter();
    const username = ref('');
    const password = ref('');
    const authStore = useAuthStore(); // Correctly get the auth store instance

    const handleLogin = () => {
      authStore.login(); // Login
      router.push({name:'dashboard'});
    };

    return {
      username,
      password,
      authStore,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
}

.login-window {
  background: rgba(255, 255, 255, 0.4); /* Semi-transparent white */
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px); /* Blurry effect */
  width: 800px;
  text-align: center;
  display:flex;
  align-items:center;
  flex-direction:column;
  font-family: "Gowun Batang",Arial, sans-serif;
  padding-top:100px;
}

input {
  width: 500px;
  padding: 20px;
  margin-top:20px;
  margin-bottom:20px;
  border: none;
  display: block;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.5); /* Semi-transparent background for input */
  backdrop-filter: blur(5px); /* Blurry effect for input */
  font-size: 16px;
  font-family: "Gowun Batang",Arial, sans-serif;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  background-color: #9ed9f5; /* Button color */
  color: white;
  font-size: 16px;
  cursor: pointer;
  font-family: "Gowun Batang",Arial, sans-serif;
  padding-bottom:10px;
  margin-bottom:100px;
  margin-top:20px;
  width:500px;
}

button:hover {
  background-color: #46a9fa; /* Darker button color on hover */
}

h1 {
  display:block;
  
}
</style>
