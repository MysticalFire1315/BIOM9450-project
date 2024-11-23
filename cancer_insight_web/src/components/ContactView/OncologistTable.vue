<template>
    <div>
      <v-card flat>
        <v-card-title>
          Our Oncologist
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

        <template v-slot:item.affiliations="{ item }">
            {{ item.affiliations.join(', ') }}
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
    { key: 'phone', title: 'Phone', align: 'center' },
    { key: 'email', title: 'Email', align: 'center' },
    { key: 'affiliations', title: 'Affiliation', align: 'center' },
    { key: 'sex', title: 'Gender', align: 'center' },
  ];
  
  // Fetch data from the server
  const fetchExpertData = async () => {
    try {
      const response = await apiService.getData(`/oncologist/list`);
      message.value = response.data.data.map((item) => ({
      id: item.person.id, // Unique identifier
      firstname: item.person.firstname,
      lastname: item.person.lastname,
      date_of_birth: item.person.date_of_birth,
      sex: item.person.sex,
      specialization: item.specialization,
      phone: item.phone,
      email: item.email,
      affiliations: item.affiliations,
    }));
    console.log(message.value);
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
  