<template>
    <v-card
    min-height="250" 
    color = "orange"
  >

    <v-card-title style="font-size:xx-large; color: white;" class="text-left">
        Your account has <span v-if="!message">NOT</span> been verified.
    </v-card-title>
    <v-card-subtitle style="font-size:x-large; color:white;" class="text-left">
        <span v-if="!message">Click the button below to link your account!</span>
        <span v-else>You are logged in as {{userRole}}.</span>

    </v-card-subtitle>
    <v-card-text v-if="message" style="font-size:large; color:white;" class="text-left">
        You can access and filter patient mutational profiles, view shared mutations, and create new profiles by entering details and upload new mutation data.
    </v-card-text>
    <v-dialog v-if="!message" attach="body" v-model="dialog">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn style="background-color: orange; color:white; margin-top:30px;" v-bind="activatorProps">
                Click here to link
            </v-btn>
        </template>
        
        <v-card title="Please enter the link ID:" max-width="300" class="mx-auto">
            <v-row dense>
                <v-col cols="12">
                    <v-text-field label="Link ID" v-model="person_id" type="number"></v-text-field>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="6" @click="handleLink">
                    <v-btn>
                        Submit
                    </v-btn>
                </v-col>
                <v-col cols="6">
                    <v-btn @click="dialog = false">
                        Cancel
                    </v-btn>
                </v-col>
            </v-row>
        </v-card>
    </v-dialog>
    
  </v-card>
</template>

<script setup>
import { ref, onMounted, shallowRef,computed } from 'vue';
import { useSessionStore} from '@/stores/useSessionStore';
import apiService from '@/services/apiService';

// The message about whether the account is linked
const message = ref(null); 
const sessionStore = useSessionStore();
const dialog = shallowRef(false);
const person_id = ref('');

const userRole = computed(() => sessionStore.userRole);

const fetchUserLink = async () => {
  try {
    const response = await apiService.getData('/user/link');
    message.value = response.data.message;
  } catch (error) {
    console.error(error);
  }
};

const handleLink = async () => {
  
      try {
        const personIdInt = parseInt(person_id.value, 10);

        // Check if the entered text contains digit only
        if (isNaN(personIdInt)) {
          throw new Error('Invalid person ID.');
        }

        const linkData = {
            person_id: personIdInt
        };
        const response = await apiService.postData('/user/link', linkData);

        // Handle the response for successful registration
        if (response.status === 200 && response.data.status === 'success') {
            const responseProfile = await apiService.getData('/user/profile');
            sessionStore.updateRole(responseProfile.data.data.role);
            dialog.value=false;
            fetchUserLink();
        }
      } catch (error) {
        alert('Linking failed. Please check your link ID.');
        console.error('Error response:', error.message);
      }
    };

onMounted(() => {
  fetchUserLink();
});
</script>





