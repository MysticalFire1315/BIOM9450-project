<template>
    <div class="greetingpanel">
        <h2>Welcome back,</h2>
        <h1>Username!</h1>
        <h2>Today is {{ formattedDate }}</h2>
        <h2>You are currently logged in as identity. Click here to link the account.</h2>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// Create a ref to hold the current date
const currentDate = ref(new Date());

// Format the date (e.g., using toLocaleDateString)
const formattedDate = currentDate.value.toLocaleDateString('en-US', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
</script>

<style scoped>
    .greetingpanel {
        width: 80%;
        margin-left:100px;
        
    }

    h1 {
        text-align: left;
        margin-bottom: 25px;
        padding-left: 50px;
    }

    h2 {
        text-align:left;
        padding-left: 50px;
    }
</style>