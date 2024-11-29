<template>
    <v-container class="d-flex justify-center align-center" style="height: 100vh;">
      <v-card class="pa-4" style="width: 50%;">
        <v-card-title class="text-h5 text-center">Model Configuration</v-card-title>
        <v-card-text>
          <v-form>
            <!-- Name Combobox -->
            <v-combobox
              v-model="name"
              :items="nameOptions"
              label="Name"
              outlined
              class="mb-4"
              placeholder="Select a dataset"
            ></v-combobox>
  
            <!-- num_epoch_pretrain Slider -->
            <v-slider
              v-model="numEpochPretrain"
              label="Number of Epochs (Pretrain)"
              min="150"
              max="500"
              step="50"
              class="mb-2"
            ></v-slider>
            <v-text-field
              v-model="numEpochPretrain"
              label="Epochs (Pretrain)"
              outlined
              readonly
              class="mb-4"
            ></v-text-field>
  
            <!-- num_epoch Slider -->
            <v-slider
              v-model="numEpoch"
              label="Number of Epochs"
              min="500"
              max="2500"
              step="50"
              class="mb-2"
            ></v-slider>
            <v-text-field
              v-model="numEpoch"
              label="Epochs"
              outlined
              readonly
              class="mb-4"
            ></v-text-field>
  
            <!-- lr_e_pretrain Label -->
            <v-row class="mb-2">
              <v-col>
                <span class="font-weight-bold">lr_e_pretrain:</span> 0.001
              </v-col>
            </v-row>
  
            <!-- lr_e Label -->
            <v-row class="mb-2">
              <v-col>
                <span class="font-weight-bold">lr_e:</span> 0.0005
              </v-col>
            </v-row>
  
            <!-- lr_c Label -->
            <v-row class="mb-4">
              <v-col>
                <span class="font-weight-bold">lr_c:</span> 0.001
              </v-col>
            </v-row>
  
            <!-- Submit Button -->
            <v-btn
              color="orange"
              block
              @click="submitConfig"
              :disabled="!name || !numEpochPretrain || !numEpoch"
            >
              Start Training
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
  const name = ref('ROSMAP'); // Default to 'ROSMAP'
  const numEpochPretrain = ref(150); // Default to minimum value
  const numEpoch = ref(500); // Default to minimum value
  const nameOptions = ['ROSMAP', 'BRCA'];
  
  // Method to handle form submission
  const submitConfig = async () => {
    // Construct the message
    const message = {
      name: name.value,
      num_epoch_pretrain: parseInt(numEpochPretrain.value),
      num_epoch: parseInt(numEpoch.value),
      lr_e_pretrain: 0.001,
      lr_e: 0.0005,
      lr_c: 0.001,
    };
  
    console.log('Constructed Message:', JSON.stringify(message, null, 2));
  
    alert('Configuration submitted successfully!');

    try {
        // Make the login request with Axios
        await apiService.postData('/ml/train', message);
        alert('Submission Successful!');
      } catch (error) {
        console.log(error)
      }
  };
  </script>
  
  <style>
  /* Add custom styles here if needed */
  </style>
  