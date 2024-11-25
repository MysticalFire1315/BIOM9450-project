<template>
    <v-container class="d-flex justify-center align-center" style="height: 100vh;">
      <v-card class="pa-4" style="width: 50%;">
        <v-card-title class="text-h5 text-center">Submit Model ID</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="handleSubmit">
            <!-- Model ID Input -->
            <v-text-field
              v-model="modelId"
              label="Model ID"
              outlined
              :rules="validationRules"
              required
              type="text"
              class="mb-4"
              placeholder="Enter a number"
            ></v-text-field>
  
            <!-- Submit Button -->
            <v-btn color="orange" block type="submit">
              Submit
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Reactive state
  const modelId = ref('');
  
  // Validation rules
  const validationRules = [
    (value) => !!value || 'Model ID is required.',
    (value) => !isNaN(value) || 'Model ID must be a number.',
  ];
  
  // Submission handler
  const handleSubmit = () => {
    const parsedModelId = parseInt(modelId.value, 10);
  
    if (isNaN(parsedModelId)) {
      alert('Invalid Model ID! Please enter a valid number.');
      return;
    }
  
    // Construct the JSON payload
    const payload = {
      model_id: parsedModelId,
    };
  
    console.log('Payload submitted:', payload);
  
    alert('Model ID submitted successfully!');
  };
  </script>
  