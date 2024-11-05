<template>
  <div class="main-container">
    <h2>Transforming Insights into Intelligent AI Solutions for Cancer Prediction.</h2>
    <div class="button-container">
      <v-card title="Start Exploring"></v-card>
      <v-card title="Our Story"></v-card>
    </div>
  </div>
</template>

<style scoped>
  .main-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center align the content */
    text-align: center;  /* Center align text */
    padding: 20px;      /* Optional padding for aesthetics */
    height: 80vh;      /* Full viewport height */
    justify-content: space-between; /* Evenly space elements vertically */
  }

  h1 {
    font-size: 8vh; 
    color: white;
  }

  h2 {
    font-size: 5vh;
    color: white;
    background-color: brown;
  }

  .button-container {
    display: flex;               /* Use Flexbox for alignment */
    flex-direction: row;      /* Align buttons in a column */
    justify-content: space-evenly; /* Evenly space buttons vertically */
    height: 20%;                /* Set height for the button container */
    width: 100%;                /* Full width for alignment */
    margin-top: 20px;          /* Space above the buttons */
  }

</style>
