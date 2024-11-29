<template>
  <div class="main-container">
    <h1>CancerInsight&reg;</h1>
    <p>
      Get ready to explore groundbreaking cancer insights with ease! By simply entering genetic mutation data, our deep learning model will uncover the risks tied to different cancers. We'll be diving into powerful datasets like ROSMAP for Alzheimer's Disease and BRCA for breast cancer, helping you discover trends and connections between mutations and cancer types. All of this comes to life in a super intuitive, user-friendly portal. Come join us on this exciting journey toward better health!
    </p>
    <button @click="navigateTo(authStore.isLogin ? '/dashboard': '/login')">
      Getting Started
    </button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/useAuthStore';

export default {
  setup() {
    const router = useRouter(); // Get the router instance
    const authStore = useAuthStore();

    // Function to navigate to the selected route
    const navigateTo = (route) => {
      router.push(route);
    };
    return {navigateTo, authStore};
  }
};
</script>

<style scoped>
  .main-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center align the content */
    text-align: center;  /* Center align text */
    padding: 20px;      /* Optional padding for aesthetics */
    height: 80vh;      /* Full viewport height */
    justify-content: space-between; /* Evenly space elements vertically */
    width: 50%;
    float:left;
  }

  h1, h2, p{
    color: white;
    text-align:left;
    width: 100%;
  }

  h1 {
    font-size: 6vh; 
  }

  h2 {
    font-size: 4vh;
  }

  p {
    font-size: 3vh;
  }

  span {
    color: #e0602e;
  }

  button{
    width: 60%;
    background-color:#e0602e;
    color:white;
    border:none;
    font-size:3vh;
    cursor:pointer;
    transition: background-color 0.2s;
  }

  button:hover {
    background-color:#c93900;
  }

  button:active {
    background-color:#8d2901
  }


</style>
