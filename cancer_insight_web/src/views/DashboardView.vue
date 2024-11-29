<template>
  <v-container style="margin-left: 5%;">
    <v-row style="width:135%">
      <v-col cols="7">
        <GreetingPanel/>
      </v-col>
      <v-col cols="5">
        <IdentityPanel/>
      </v-col>
    </v-row>

    <v-row style="width:135%">
      <v-col>
        <DashboardTImelinePanel/>
      </v-col>
    </v-row>

    <v-row style="width:135%">
      <v-col>
        <NavigationPanel/>
      </v-col>
    </v-row>
    
    <!-- <v-row style="width:135%">
      <v-col cols="4">
        <PatientNumEntryOverview/>
      </v-col>
      <v-col cols="4">
        <DatabaseNumEntryOverview/>
      </v-col>
      <v-col cols="4">
        <ModelOverview/>
      </v-col>
    </v-row> -->
    
  </v-container>
</template>
  

<script setup>
import GreetingPanel from '@/components/DashboardView/GreetingPanel.vue'; 
import IdentityPanel from '@/components/DashboardView/IdentityPanel.vue';
// import DatabaseNumEntryOverview from '@/components/DashboardView/DatabaseNumEntryOverview.vue';
import DashboardTImelinePanel from '@/components/DashboardView/DashboardTImelinePanel.vue';
import NavigationPanel from '@/components/DashboardView/NavigationPanel.vue';
// import PatientNumEntryOverview from '@/components/DashboardView/PatientNumEntryOverview.vue';
// import ModelOverview from '@/components/DashboardView/ModelOverview.vue';
</script>