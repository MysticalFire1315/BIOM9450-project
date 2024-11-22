<template>
    <div>
      <v-card flat>
        <v-card-title>
          Our Researchers
        </v-card-title>
  
        <template v-slot:text>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
        </template>
  
        <v-data-table
          :headers="headers"
          :items="information"
          :search="search"
        ></v-data-table>
      </v-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import apiService from '@/services/apiService';
  
  const message = ref([]);  // Initialize message as an array
  const fetchExpertData = async () => {
    try {
      const response = await apiService.getData(`/researcher/list`);
      message.value = response.data.data;  // Assign the data to message
    } catch (error) {
      console.error(error);
    }
  };
  
  const search = ref('');
  const headers = [
    { key: 'firstname', title: 'First Name', align: 'center' },
    { key: 'lastname', title: 'Last Name', align: 'center' },
    { key: 'date_of_birth', title: 'Date of Birth', align: 'center' },
    { key: 'sex', title: 'Gender', align: 'center' },
  ];
  
  // Directly bind the information array to message.value
  const information = computed(() => message.value);
  
  onMounted(() => {
    fetchExpertData();
  });
  </script>
  