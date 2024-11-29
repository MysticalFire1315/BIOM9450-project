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
        <!-- Scoped slot for the 'sex' field -->
        <template v-slot:item.sex="{ item }">
          {{ item.sex.replace('Sex.', '') }}
        </template>
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
  { key: 'firstname', title: 'First Name', align: 'center' },
  { key: 'lastname', title: 'Last Name', align: 'center' },
  { key: 'date_of_birth', title: 'Date of Birth', align: 'center' },
  { key: 'sex', title: 'Gender', align: 'center' },
];

// Fetch data from the server
const fetchExpertData = async () => {
  try {
    const response = await apiService.getData(`/researcher/list`);
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
