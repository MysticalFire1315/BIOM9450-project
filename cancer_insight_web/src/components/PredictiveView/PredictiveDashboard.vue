<template>
    <v-container class="d-flex justify-center align-center" style="height: 100vh;">
      <v-row justify="center" align="center">
        <v-col cols="12" class="d-flex justify-center">
          <v-btn class="mb-4" style="width: 50%; background-color: orange; color: white;" @click="trainModel">
            Train a Model
          </v-btn>
        </v-col>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn class="mb-4" style="width: 50%; background-color: orange; color: white;" @click="predictModel">
            Predict a Model
          </v-btn>
        </v-col>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn class="mb-4" style="width: 50%; background-color: orange; color: white;" @click="visualizeResults">
            Result Visualization
          </v-btn>
        </v-col>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn class="mb-4" style="width: 50%; background-color: orange; color: white;" @click="provideFeedback">
            Provide Feedback
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>

    import { useRouter } from 'vue-router';

    const router = useRouter();
    const navigateTo = (route) => {
        router.push(route);
    };

  const trainModel = () => {
    console.log("Train a Model button clicked");
    navigateTo('/predictive/new-training');
  };
  
  const predictModel = () => {
    console.log("Predict a Model button clicked");
    navigateTo('/predictive/new-prediction');
  };
  
  const visualizeResults = () => {
    console.log("Result Visualization button clicked");
    navigateTo('/predictive/result');
  };
  
  const provideFeedback = () => {
    console.log("Provide Feedback button clicked");
    navigateTo('/predictive/feedback');
  };
  </script>
  
  <style>
  /* Add custom styles here if needed */
  </style>
  