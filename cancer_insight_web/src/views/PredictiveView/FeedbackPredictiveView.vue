<template>
    <v-container class="d-flex justify-center align-center" style="height: 100vh;" >
      <v-card class="pa-4" style="width: 80%;" :style="{
      backgroundImage: `url(${require('@/assets/patient_v_card_large.png')})`,
      backgroundSize: 'cover',
      backgroundPosition: 'bottom'
    }">
        <v-card-title class="text-h5 text-center">Please share some feedbacks on the training result</v-card-title>
        <v-card-text>
          <v-form>


            <v-text-field
            v-model="modelID"
            label="Model ID"
            outlined
            class="mb-4"
            placeholder="Enter the model ID"
          ></v-text-field>

            <!-- Feature Name Input -->
            <v-text-field
              v-model="featureName"
              label="Feature Name"
              outlined
              class="mb-4"
              placeholder="Enter feature name"
            ></v-text-field>
  
            <!-- Feedback Input -->
            <v-textarea
              v-model="feedback"
              label="Feedback"
              outlined
              class="mb-4"
              placeholder="Enter your feedback"
              rows="5"
            ></v-textarea>
  
            <!-- Submit Button -->
            <v-btn
              color="orange"
              block
              @click="submitFeedback"
              :disabled="!featureName || !feedback"
            >
              Submit
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import apiService from '@/services/apiService';
  
  // State variables
  const featureName = ref('');
  const feedback = ref('');
  const modelID = ref('');
  // Method to handle form submission
  const submitFeedback = async () => {
    // console.log('Feature Name:', featureName.value);
    // console.log('Feedback:', feedback.value);
  
    // // Clear inputs after submission
    // featureName.value = '';
    // feedback.value = '';
    // alert('Thank you for your feedback!');
    const messageFeedback = {
    model_id: parseInt(modelID.value),
    data: [
      {
        feature: featureName.value,
        feedback: feedback.value,
      },
    ],
  };

  try {
        // Make the login request with Axios
        await apiService.postData('/ml/feedback', messageFeedback);
        alert('Submission Successful!');
        modelID.value = '';
        featureName.value = '';
        feedback.value = '';
      } catch (error) {
        console.log(error)
      }

  };

  
  </script>
  
  <style>
  /* Add custom styles here if needed */
  </style>
  