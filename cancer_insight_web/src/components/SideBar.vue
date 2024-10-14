<template>
    <div class="sidebar">
      <div class="icon" @click="gotoDashboardHomeOrLogin">
        <img src="@/assets/DashboardIcon.svg" alt="Icon 1" />
        <span>Home</span>
      </div>
      <div v-if="isLogin" class="icon" @click="gotoDatabase">
        <img src="@/assets/DatabaseIcon.svg" alt="Icon 2" />
        <span>Database</span>
      </div>
      <div v-if="isLogin" class="icon" @click="gotoPredictive">
        <img src="@/assets/DeepLearningIcon.svg" alt="Icon 3" />
        <span>Predictive</span>
      </div>
      <div v-if="isLogin" class="icon" @click="logout">
        <img src="@/assets/LogoutIcon.svg" alt="Icon 4" />
        <span>Logout</span>
      </div>
    </div>
</template>


<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';
import { computed } from 'vue'; // Import computed from Vue
import axios from 'axios'; // Import axios

export default {
  name: 'SideBar',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore(); // Use your Pinia store

    const isLogin = computed(() => authStore.isLogin); // Get isLogin from store

    const goToHome = () => {
      router.push({ name: 'home' }); // Adjust according to the route name
    };

    const logout = async () => {
    try {
        // Send a request to the server to invalidate the token
        await axios.post('http://127.0.0.1:5000/auth/logout', {}, {
          headers: {
            'Authorization': authStore.token, // Include the JWT token in the Authorization header
            'accept': 'application/json'
          }
        });

        // If the request was successful, proceed to log out the user
        authStore.logout(); // Call the logout action from the store
        router.push({ name: 'home' }); // Redirect to the home or login page
      } catch (error) {
        console.error('Logout failed:', error); // Log the error if the request fails
        // Optionally, you can add user feedback here (e.g., a notification)
      }
    };

    const gotoDashboardHomeOrLogin = () => {
      if (isLogin.value) {
        // If we already log in, go the the dashboard home page
        router.push({ name: 'dashboard' });
      } else {
        // If we're not yet logged in, go the login page
        router.push({ name: 'home' });
      }
    };

    const gotoDatabase = () => {
      router.push({ name: 'database' }); // Adjust according to the route name
    };

    const gotoPredictive = () => {
      router.push({ name: 'predictive' }); // Adjust according to the route name
    };

    return {
      isLogin,
      goToHome,
      logout,
      gotoDashboardHomeOrLogin,
      gotoDatabase,
      gotoPredictive,
    };
  },
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 100px;
  height: 100vh;
  background-color: #a1c7ec;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
}

.icon {
  margin: 20px 0;
  padding-bottom: 10px;
  padding-top:10px;
  cursor: pointer;
  transition: all 0.15s;
}

.icon:hover {
  background-color: white;
}

.icon img {
  width: 70px;
}

.icon span {
  color: rgb(0, 0, 0); /* Text color */
  font-size: 14px; /* Adjust font size as needed */
}

</style>