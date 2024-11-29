<template>
    <v-card :style="{
      backgroundImage: `url(${require('@/assets/patient_v_card_large.png')})`,
      backgroundSize: 'cover',
      backgroundPosition: 'bottom'
    }">
        
        <v-card-title>
            <span class="me-2 fw-bold">All Patients</span>
        </v-card-title>
        <v-divider
        :thickness="3"
        class="border-opacity-75"
        color="brown"
        ></v-divider>
      <v-data-iterator
        :items="message"
        :items-per-page="12"
        :search="search"
      >
        <template v-slot:header>
          <v-toolbar class="px-2">
            <v-text-field
              v-model="search"
              density="comfortable"
              placeholder="Search"
              prepend-inner-icon="mdi-magnify"
              style="max-width: 300px;"
              variant="solo"
              clearable
              hide-details
            ></v-text-field>
            <v-spacer></v-spacer>

            <v-btn icon @click="navigateTo('/database/create-patient')">
                <v-icon>mdi-plus-circle</v-icon>
            </v-btn>

            

          </v-toolbar>
        </template>
  
        <template v-slot:default="{ items }">
          <v-container class="pa-2" fluid>
            <v-row dense>
              <v-col
                v-for="item in items"
                :key="item.title"
                cols="auto"
                md="3"
              >
                <v-card class="pb-3" border flat :style="{
                  backgroundImage: `url(${require('@/assets/patient_v_card.png')})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'bottom'
                }">
                    <v-avatar :color="item.raw.avatarColor">
                        <!-- <v-img :src="item.raw.img"></v-img> -->
                        <span class="text-h5">{{ item.raw.initials }}</span>
                    </v-avatar>
                  
  
                  <v-list-item :subtitle="`Patient ID ${item.raw.id}`" class="mb-2">

                    <template v-slot:title>
                      <strong class="text-h6 mb-2">{{ item.raw.fullName }}</strong>
                    </template>
                  </v-list-item>
  
                  <div class="d-flex justify-space-between px-4">  
                    <v-btn icon @click="navigateTo(`/database/${item.raw.id}-personal-profile`)">
                        <v-tooltip activator="parent" location="bottom">
                            View Personal Profile
                        </v-tooltip>
                        <v-icon>mdi-account-eye-outline</v-icon>
                    </v-btn>
                    <!-- <v-btn icon>
                        <v-tooltip activator="parent" location="bottom">
                            Add Mutational Profile for ROSMAP
                        </v-tooltip>
                        <v-icon>mdi-tooltip-plus</v-icon>
                    </v-btn>

                    <v-btn icon>
                        <v-tooltip activator="parent" location="bottom">
                            Add Mutational Profile for BRCA
                        </v-tooltip>
                        <v-icon>mdi-tooltip-plus-outline</v-icon>
                    </v-btn> -->
                    
                  </div>
                  <PatientFileInput />
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </template>
  
        <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
          <div class="d-flex align-center justify-center pa-4">
            <v-btn
              :disabled="page === 1"
              density="comfortable"
              icon="mdi-arrow-left"
              variant="tonal"
              rounded
              @click="prevPage"
            ></v-btn>
  
            <div class="mx-2 text-caption">
              Page {{ page }} of {{ pageCount }}
            </div>
  
            <v-btn
              :disabled="page >= pageCount"
              density="comfortable"
              icon="mdi-arrow-right"
              variant="tonal"
              rounded
              @click="nextPage"
            ></v-btn>
          </div>
        </template>
      </v-data-iterator>
    </v-card>
  </template>
  
  <script setup>
  import { shallowRef, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router';
  import apiService from '@/services/apiService';
  import PatientFileInput from './PatientFileInput.vue';

  const message = ref([]); // Initialize message as an array
  const colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink'];

  const fetchPatientList = async () => {
  try {
    const response = await apiService.getData('/patient/list');
    message.value = response.data.data.map(patient => {
  // Create initials by taking the first letter of first name and last name
  const initials = (patient.firstname.charAt(0) + patient.lastname.charAt(0)).toUpperCase();
  
  // Create full name by concatenating first name and last name
  const fullName = `${patient.firstname} ${patient.lastname}`;
  
  // Function to get a random color from the predefined set
  const getRandomColor = () => {
    const randomIndex = Math.floor(Math.random() * colors.length);
    return colors[randomIndex];
  };

  // Return the new object with id, fullName, initials, and a random color
  return {
    id: patient.id,
    fullName: fullName,
    initials: initials,
    avatarColor: getRandomColor()  // Add the color here
  };
});
    // console.log(message.value)
    } catch (error) {
      console.error(error);
    }
  };

    const router = useRouter();
    const navigateTo = (route) => {
        router.push(route);
    };

    const search = shallowRef('')

    onMounted(() => {
    fetchPatientList();
    });
  </script>
  
