<template>
    <!-- <div class="database">
      <h1>This is the database page. </h1>
      <h1>Show tables? Filtering? Editing? Visualistion?</h1>
      <h1>To be implemented :)</h1>
    </div> -->
    <div>
      <GeneralPatientIterator />
      <router-view></router-view>
    </div>
    
  </template>
  
  <script setup>
  import GeneralPatientIterator from '@/components/DatabaseView/GeneralPatientIterator.vue';

  </script>