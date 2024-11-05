<!-- <template>
    <h1>We are in the login page.</h1>
</template> -->
<template>
    <div class="home">
      <v-container class="d-flex justify-center align-center" fill-height>
        <v-card class="login-window">
          <v-card-title class="text-h4" style="padding-bottom: 30px">Login</v-card-title>

            <v-form @submit.prevent="handleLogin">
            <v-text-field
            v-model="email"
            label="Email"
            type="text"
            required
            ></v-text-field>

            <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
            ></v-text-field>
  
            <v-btn type="submit" block>
                Login
            </v-btn>
  
            <v-divider></v-divider>
  
            <v-card-text class="text-center mt-2">
            <label
                @click="goToRegistration"
                style="color: #1976d2; cursor: pointer;" 
            >
                Don't have an account? Click here to register!
            </label>
            </v-card-text>

            </v-form>

        </v-card>
      </v-container>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useAuthStore } from '../stores/useAuthStore';  // Pinia library
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'HomeView',
    setup() {
      const router = useRouter();
      const email = ref('');
      const password = ref('');
      const authStore = useAuthStore();
  
      const handleLogin = async () => {
        try {
          const loginData = {
            email: email.value,
            password: password.value,
          };
  
          // Make the login request with Axios
          const response = await axios.post('http://127.0.0.1:5000/auth/login', loginData, {
            headers: {
              'Content-Type': 'application/json',
              'accept': 'application/json',
            },
          });
  
          if (response.status === 200) {
            const jwtToken = response.data.Authorization;
  
            // Store the JWT token using Pinia
            authStore.login(jwtToken);
  
            // Redirect to the dashboard page after successful login
            router.push({ name: 'dashboard' });
          } else {
            console.error('Login failed:', response.data.message);
            alert('Login failed. Please check your credentials.');
          }
        } catch (error) {
          // console.error('Error during login:', error);
          // alert('An error occurred. Please try again.');
  
            // Error catching fallback
            if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Error response:', error.response.data);
            console.error('Status code:', error.response.status);
            // alert(`Login failed with status ${error.response.status}: ${error.response.data.message || error.response.data}`);
            alert(`Login failed with status ${error.response.status}: ${error.response.data.message}`);
          } else if (error.request) {
            // The request was made but no response was received
            console.error('No response received:', error.request);
            alert('No response from server. Please make sure the server is running.');
          } else {
            // Something happened in setting up the request that triggered an error
            console.error('Error setting up the request:', error.message);
            alert(`Error: ${error.message}`);
          }
        }
      };
  
      const goToRegistration = () => {
        router.push({ name: 'registration' }); // Adjust according to the route name
      };
  
      return {
        email,
        password,
        authStore,
        handleLogin,
        goToRegistration
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
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px); /* Blurry effect */
    width: 80%;
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
    border: 2px solid #d3b5e5;
    display: block;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.5); /* Semi-transparent background for input */
    backdrop-filter: blur(5px); /* Blurry effect for input */
    font-size: 16px;
    font-family: "Gowun Batang",Arial, sans-serif;
  }
  
  .v-btn {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    background-color: #9ed9f5; /* Button color */
    color: white;
    font-size: 16px;
    cursor: pointer;
    font-family: "Gowun Batang",Arial, sans-serif;
    padding-bottom:10px;
    margin-bottom:30px;
    margin-top:20px;
    width:500px;
    text-transform: none;
  }
  
  button:hover {
    background-color: #46a9fa; /* Darker button color on hover */
  }
  
  h1 {
    display:block;
  }
  
  h5 {
    cursor:pointer;
  }
  </style>
  