<template>
    <Doughnut :data="data" :options="options" />
  </template>
  
  <script>
  import { ref } from 'vue'
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
  // Updated import path
  import * as chartConfig from '@/config/DatabaseNumEntryOverviewChartConfig.js'
  
  ChartJS.register(ArcElement, Tooltip, Legend)
  
  export default {
    name: 'DatabaseNumEntryOverview',
    components: {
      Doughnut
    },
    setup() {
      // Define data and options using Composition API
      const data = ref(chartConfig.data)
      const options = ref(chartConfig.options)
  
      return {
        data,
        options
      }
    }
  }
  </script>
  