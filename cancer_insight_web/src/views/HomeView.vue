<template>
  <div class="main-container">
    <h2>Transforming Insights into Intelligent AI Solutions for Cancer Prediction</h2>
    <h1>CancerInsight&reg;</h1>
    <p>
      Unlock cancer insights at your fingertips! Input genetic mutation data and let our deep learning model <span>reveal the risk of cancer.</span> Explore trends and connections between <span>mutations and cancer types</span>, <span>ALL in a user-friendly portal</span>. Join us on this journey to better health!
    </p>
    <button @click="navigateTo('/login')">
      Getting Started
    </button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter(); // Get the router instance

    // Function to navigate to the selected route
    const navigateTo = (route) => {
      router.push(route);
    };
    return {navigateTo};
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
