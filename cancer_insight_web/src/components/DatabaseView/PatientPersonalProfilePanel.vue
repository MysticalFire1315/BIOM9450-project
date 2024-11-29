<template>
    <v-card>
      <v-toolbar
        color="blue-grey"
        dark
        flat
      >
        <v-toolbar-title>Patient Personal Profile for Patient ID {{ patientId }}</v-toolbar-title>
      </v-toolbar>
  
      <v-card-text>
        <v-text-field
          label="Patient ID"
          :model-value="personal_message.id"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="First Name"
          :model-value="personal_message.firstname"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Last Name"
          :model-value="personal_message.lastname"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Date of Birth"
          :model-value="personal_message.date_of_birth"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Gender"
          :model-value="personal_message.sex"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Address"
          :model-value="message.address"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Country"
          :model-value="message.country"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Emergency Contact Name"
          :model-value="message.emergency_contact_name"
          variant="filled"
          readonly
        ></v-text-field>

        <v-text-field
          label="Emergency Contact Phone"
          :model-value="message.emergency_contact_phone"
          variant="filled"
          readonly
        ></v-text-field>


  
        <v-divider class="my-2"></v-divider>

      </v-card-text>
  
    </v-card>
  </template>



<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import apiService from '@/services/apiService';

// Get the current route object
const route = useRoute();

// Extract the patientId from the dynamic route parameter
const patientId = computed(() => route.params.patientId);
const message = ref(''); 
const personal_message = ref('');

const fetchPatientPersonalData = async () => {
    try {
      const response = await apiService.getData(`/patient/profile/${patientId.value}`);
      message.value = response.data.data;
      personal_message.value = message.value.person;
    console.log(personal_message.value);
    console.log(`THe address is ${message.value.address}`)
    } catch (error) {
      console.error(error);
    }
  };

// Watch for changes in patientId and call the fetch function when it changes
// eslint-disable-next-line
watch(patientId, (newPatientId) => {
  fetchPatientPersonalData();
});

onMounted(() => {
    fetchPatientPersonalData();
  });

</script>