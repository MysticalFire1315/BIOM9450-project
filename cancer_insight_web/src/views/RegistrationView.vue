<template>
    <div class="registration">
        <div class="registration-window">
        <h1>Create your account!</h1>
        <form @submit.prevent="handleRegister">
            <input type="email" v-model="email" placeholder="Email" required />
            <input type="text" v-model="username" placeholder="Username" required />
            <input type="password" v-model="password" placeholder="Password" required />
            <button type="submit">Register</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        <p v-if="successMessage" class="redirect-message">Logging-in in {{ redirectCountdown }} seconds ...</p>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

export default {
  name: 'RegistrationVue',
  setup() {
    const email = ref('');
    const username = ref('');
    const password = ref('');
    const redirectCountdown = ref(0);
    const errorMessage = ref('');
    const successMessage = ref('');
    const router = useRouter();
    const authStore = useAuthStore();

    const handleRegister = async () => {
      errorMessage.value = '';
      successMessage.value = '';

      try {
        // Replace this URL with your actual registration endpoint
        const response = await axios.post('http://127.0.0.1:5000/user/', {
          email: email.value,
          username: username.value,
          password: password.value,
          public_id: 'string', // Replace with a real ID generation logic if needed
          admin: true, // Set to true or false depending on your application's needs
        });

        // Handle the response for successful registration
        if (response.status === 201 && response.data.status === 'success') {
          successMessage.value = response.data.message || 'Successfully registered. Please log in.';
          redirectCountdown.value = 7;
          const jwtToken = response.data.Authorization;// Store the JWT token using Pinia
          authStore.login(jwtToken);
        }
      } catch (error) {
        // Check for 409 conflict error when the user already exists
        if (error.response && error.response.status === 409) {
          errorMessage.value = error.response.data.message || 'User already exists. Please log in.';
        } else {
          // General error message for other cases
          errorMessage.value = error.response?.data?.message || 'An error occurred during registration.';
        }
      }
    };

    watch(redirectCountdown, (newValue) => {
      if (newValue > 0) {
        setTimeout(() => {
          redirectCountdown.value--;
        }, 1000); // Decrease the countdown every second
      } else if (newValue === 0 && successMessage.value) {
       
          // Redirect to the dashboard page after successful login
        router.push({ name: 'dashboard' });
      }
    });

    return {
      email,
      username,
      password,
      redirectCountdown,
      handleRegister,
      errorMessage,
      successMessage,
    };
  },
};
</script>


<style scoped>

.registration {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
}


.registration-window {
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


h1 {
  text-align: center;
  margin-bottom: 20px;
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
  margin-bottom:30px;
  margin-top:20px;
  width:500px;
}

button:hover {
  background-color: #46a9fa; /* Darker button color on hover */
}


.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
  font-family: "Gowun Batang",Arial, sans-serif;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
  font-family: "Gowun Batang",Arial, sans-serif;
}

.redirect-message {
  color: blue;
  text-align: center;
  margin-top: 10px;
  font-family: "Gowun Batang",Arial, sans-serif;
}
</style>