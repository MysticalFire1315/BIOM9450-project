<template>
    
    <v-app-bar>

        <v-btn icon @click="navigateTo('/')">
        <v-icon>mdi-home</v-icon>
        </v-btn>

        <v-app-bar-title><b>CancerInsight</b></v-app-bar-title>

        <v-btn icon @click="navigateTo(isLogin ? '/logout' : '/login')">
            <v-tooltip activator="parent" location="bottom">
                {{ isLogin ? 'Logout' : 'Login' }}
            </v-tooltip>
            <v-icon>
                {{ isLogin ? 'mdi-logout' : 'mdi-login' }}
            </v-icon>
        </v-btn>

        <v-btn icon @click="navigateTo('/contact')">
            <v-tooltip activator="parent" location="bottom">
                Contacts
            </v-tooltip>
            <v-icon>mdi-contacts</v-icon>
        </v-btn>

        <v-btn icon @click="navigateTo('/document')">
            <v-tooltip activator="parent" location="bottom">
                Documents
            </v-tooltip>
            <v-icon>mdi-file-document</v-icon>
        </v-btn>

        <v-btn icon @click="navigateTo('/about')">
            <v-tooltip activator="parent" location="bottom">
                About
            </v-tooltip>
            <v-icon>mdi-information</v-icon>
        </v-btn>
    </v-app-bar>
</template>

<script>
// import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';
import { computed } from 'vue'; // Import computed from Vue
import axios from 'axios'; // Import axios

export default {
  setup() {
    const router = useRouter(); // Get the router instance

    const authStore = useAuthStore(); 
    const isLogin = computed(() => authStore.isLogin); // Get isLogin from store
    console.log(isLogin.value);

    // Function to navigate to the selected route
    const navigateTo = (route) => {
        if (route === '/logout') {
            // Call the logout function if the route is '/logout'
            logout();
        } else {
            router.push(route);
        }
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
        router.push({ name: 'logout' }); // Redirect to the home or login page
      } catch (error) {
        console.error('Logout failed:', error); // Log the error if the request fails
        // Optionally, you can add user feedback here (e.g., a notification)
      }
    };

    return {isLogin, navigateTo, logout};
  }
};
</script>


<style scoped>
    .v-app-bar {
        background-color: #2eb5e0 !important;
    }

    .v-icon, .v-app-bar-title {
        color: white;
    }
</style>