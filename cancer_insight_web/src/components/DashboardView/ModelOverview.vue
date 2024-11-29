<template>
    <v-card  color="#e3ebed">
        <v-card-title class="text-left" style="font-size:xx-large;">
        Model Performance Overview
        </v-card-title>
        <v-card-text>
            <Radar :data="data" :options="options" />
        </v-card-text>
    </v-card>
    
  </template>
  
  <script>
  import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
  } from 'chart.js'
  import { Radar } from 'vue-chartjs'
  import * as chartConfig from '@/config/DashboardView/ModelOverview.js'
  
  // Register the components necessary for the radar chart
  ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
  )
  
  export default {
    name: 'ModelOverview',
    components: {
      Radar
    },
    data() {
      return chartConfig 
    }
  }
  </script>
  