<template>
  <v-card prepend-icon="mdi-account" title="User Profile">
    <v-card-text>
      <v-row dense>
        <v-col cols="12" md="4" sm="6">
          <v-text-field
            v-model="firstName"
            hint="First Name of the Patient"
            label="First name*"
            required
            @blur="validateFirstName"
          ></v-text-field>
          <span v-if="!isFirstNameValid" class="error-text">Incorrect format</span>
        </v-col>

        <v-col cols="12" md="4" sm="6">
          <v-text-field
            v-model="lastName"
            hint="Last Name of the Patient"
            label="Last name*"
            required
            @blur="validateLastName"
          ></v-text-field>
          <span v-if="!isLastNameValid" class="error-text">Incorrect format</span>
        </v-col>

        <v-col cols="12" md="4" sm="6">
          <v-avatar color="red">
            <template v-if="initials">
              <span class="text-h5">{{ initials }}</span>
            </template>
            <template v-else>
              <v-icon icon="mdi-account-circle"></v-icon>
            </template>
          </v-avatar>
        </v-col>

        <v-col cols="12" md="9" sm="6">
          <v-text-field
            v-model="address"
            label="Address*"
            required
            @blur="validateAddress"
          ></v-text-field>
          <span v-if="!isAddressValid" class="error-text">Address cannot be empty</span>
        </v-col>

        <v-col cols="12" md="3" sm="6">
          <v-text-field
            v-model="country"
            label="Country"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6" sm="6">
          <v-text-field
            v-model="emergencyContactName"
            label="Emergency Contact Name"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6" sm="6">
          <v-text-field
            v-model="emergencyContactPhone"
            label="Emergency Contact Phone"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" sm="6">
          <v-select
            v-model="gender"
            :items="['male', 'female', 'other']"
            label="Gender*"
            required
          ></v-select>
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
            v-model="dateOfBirth"
            hint="Please enter the date of birth following the format YYYY-MM-DD"
            label="Date of Birth*"
            required
            @blur="validateDateOfBirth"
          ></v-text-field>
          <span v-if="!isDateOfBirthValid" class="error-text">Invalid date format (YYYY-MM-DD required)</span>
        </v-col>
      </v-row>

      <small class="text-caption text-medium-emphasis">*indicates required field</small>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>

      <v-btn text="Close" variant="plain" @click="navigateTo('/database')"></v-btn>

      <v-btn color="primary" text="Save" variant="tonal" @click="handleSave"></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue';
import apiService from '@/services/apiService'; // Import the apiService
import { useRouter } from 'vue-router';
const router = useRouter();
    const navigateTo = (route) => {
        router.push(route);
    };

const firstName = ref('');
const lastName = ref('');
const address = ref('');
const country = ref('');
const emergencyContactName = ref('');
const emergencyContactPhone = ref('');
const gender = ref('male'); // Default value set to 'Male'
const dateOfBirth = ref('');

// Validation states
const isFirstNameValid = ref(true);
const isLastNameValid = ref(true);
const isAddressValid = ref(true);
const isDateOfBirthValid = ref(true);

// Regex patterns
const namePattern = /^[a-zA-Z'-]+$/;
const datePattern = /^\d{4}-\d{2}-\d{2}$/; // Matches YYYY-MM-DD format

// Validation logic
const validateFirstName = () => {
  isFirstNameValid.value = namePattern.test(firstName.value.trim());
};

const validateLastName = () => {
  isLastNameValid.value = namePattern.test(lastName.value.trim());
};

const validateAddress = () => {
  isAddressValid.value = address.value.trim() !== '';
};

const validateDateOfBirth = () => {
  isDateOfBirthValid.value = datePattern.test(dateOfBirth.value.trim());
};

// Avatar initials logic
const initials = computed(() => {
  const firstInitial = firstName.value.trim().charAt(0).toUpperCase();
  const lastInitial = lastName.value.trim().charAt(0).toUpperCase();
  return firstInitial && lastInitial ? `${firstInitial}${lastInitial}` : '';
});

// Handle Save
const handleSave = async () => {
  // Validate all fields
  validateFirstName();
  validateLastName();
  validateAddress();
  validateDateOfBirth();

  // Check if all validations passed
  const isFormValid =
    isFirstNameValid.value &&
    isLastNameValid.value &&
    isAddressValid.value &&
    isDateOfBirthValid.value;

  if (isFormValid) {
    const newPatientForm = {
      photo: initials.value || "default_photo", // Use initials or fallback to a default string for photo
      address: address.value.trim(),
      country: country.value.trim(),
      emergency_contact_name: emergencyContactName.value.trim(),
      emergency_contact_phone: emergencyContactPhone.value.trim(),
      person: {
        id: 0, // Default id
        firstname: firstName.value.trim(),
        lastname: lastName.value.trim(),
        date_of_birth: dateOfBirth.value.trim(),
        sex: gender.value,
      },
    };

    try {
      // Send POST request
      const response = await apiService.postData('/patient/create', newPatientForm);
      console.log(response.data);
      alert('Patient data saved successfully!');
      navigateTo('/database');
      // Optionally handle response here (e.g., redirect, reset form, etc.)
    } catch (error) {
      console.error('Error saving patient data:', error);
      alert('An error occurred while saving the data.');
    }
  } else {
    alert('Please fix the errors in the form before saving.');
  }
};
</script>

<style scoped>
.error-text {
  color: red;
  font-size: 12px;
  margin-left: 8px;
}
</style>
