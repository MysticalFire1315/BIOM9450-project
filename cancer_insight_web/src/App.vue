<template>
  <v-app class="app-container">
    <AppBar />
    
    <SideBar />
    <v-main :class="{backgroundImageClass: isBackgroundImageClass}">
      <router-view></router-view>
    </v-main>
    
  </v-app>
</template>


<script>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import SideBar from './components/SideBar.vue'; 
import AppBar from './components/AppBar.vue'
import { useAuthStore } from './stores/useAuthStore';
import {computed} from 'vue'

export default {
  name: 'App',
  components: {
    SideBar,
    AppBar
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    const routesWithBackground = ['home', 'about', 'login', 'registration', 'logout'];

    const isBackgroundImageClass = computed(() => routesWithBackground.includes(route.name));

    const handleCancerInsightLogoClick = () => {
      if (route.name === 'about') {
        // If we're on the About page, go back to the previous page
        router.go(-1);
      } else {
        // If we're not on the About page, navigate to the About page
        router.push({ name: 'about' });
      }
    };
    
    onMounted(() => {
      authStore.initializeAuth();
    });

    return {
      handleCancerInsightLogoClick,
      isBackgroundImageClass
    };
  },
};
</script>



<style>
#app {
  font-family: "Gowun Batang", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}


body {
    margin: 0;
    height: 100vh; /* Ensure it covers the full height of the viewport */
    background-color: #ffffff;
    background-image:  linear-gradient(#bbe7fe 8px, transparent 8px), linear-gradient(90deg, #bbe7fe 8px, transparent 8px), linear-gradient(#bbe7fe 4px, transparent 4px), linear-gradient(90deg, #bbe7fe 4px, #ffffff 4px);
    background-size: 200px 200px, 200px 200px, 40px 40px, 40px 40px;
    background-position: -8px -8px, -8px -8px, -4px -4px, -4px -4px;
}

.cancer-insight-logo {
  width: 200px;
  position: absolute;
  top: -30px;
  right: -30px;
  cursor: pointer;
}

.backgroundImageClass {
  background-image: url('@/assets/background.png');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
}

</style>
