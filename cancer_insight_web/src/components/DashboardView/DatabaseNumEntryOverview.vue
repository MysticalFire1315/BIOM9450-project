<template>
    <v-card  color="#e3ebed">
      <v-card-title>
        Database Size
      </v-card-title>
      <v-card-text>
      <Doughnut :data="data" :options="options" />
      </v-card-text>
    </v-card>
    
  </template>
  
  <script>
  import { ref } from 'vue'
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
  // Updated import path
  import * as chartConfig from '@/config/DashboardView/DatabaseNumEntryOverviewChartConfig.js'
  
  ChartJS.register(ArcElement, Tooltip, Legend)
  
  export default {
    name: 'DatabaseNumEntryOverview',
    components: {
      Doughnut
    },
    setup() {

      const data = ref(chartConfig.data)
      const options = ref(chartConfig.options)
  
      return {
        data,
        options
      }
    }
  }
  </script>
  