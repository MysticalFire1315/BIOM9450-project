<template>
    <div>
      <v-card flat>
        <v-card-title>
          Our Researchers
        </v-card-title>
  
        <!-- Search field -->
        <v-text-field
          v-model="search"
          label="Search"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
        ></v-text-field>
  
        <!-- Data table -->
        <v-data-table
          :headers="headers"
          :items="information"
          :search="search"
        >
          
        </v-data-table>
      </v-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import apiService from '@/services/apiService';
  
  // State
  const message = ref([]); // Initialize message as an array
  const search = ref('');
  
  // Table headers
  const headers = [
    { key: 'name', title: 'Model Name', align: 'center' },
    { key: 'time_created', title: 'Time Created', align: 'center' },
    { key: 'num_epoch_pretrain', title: 'Number of pretrain epoches', align: 'center' },
    { key: 'num_epoch', title: 'Number of Epoches', align: 'center' },
    { key: 'lr_e_pretrain', title: 'lr_e_pretrain', align: 'center' },
    { key: 'lr_e', title: 'lr_e', align: 'center' },
    { key: 'lr_c', title: 'lr_c', align: 'center' },
    { key: 'ready', title: 'Model is Ready', align: 'center' },
  ];
  
  // Fetch data from the server
  const fetchExpertData = async () => {
    try {
      const response = await apiService.getData(`/ml/list`);
      message.value = response.data.data; // Assign the array to `message`
    } catch (error) {
      console.error(error);
    }
  };
  
  // Computed property for the information
  const information = computed(() => message.value);
  
  // Fetch data on component mount
  onMounted(() => {
    fetchExpertData();
  });
  </script>
  