<template>
  <v-container style="margin-left: 10%;">
    <v-row style="width:135%">
      <v-col cols="7">
        <GreetingPanel/>
      </v-col>
      <v-col cols="5">
        <IdentityPanel/>
      </v-col>
    </v-row>
    
  </v-container>
</template>
  

<script setup>
import GreetingPanel from '@/components/HomeView/GreetingPanel.vue'; 
import IdentityPanel from '@/components/HomeView/IdentityPanel.vue';
</script>