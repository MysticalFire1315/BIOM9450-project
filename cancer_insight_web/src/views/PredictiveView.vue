<template>
    <div class="predictive">
      <!-- <h1>This is the predictive page. </h1>
      <h1>TODO :)</h1>
      <h1>Use a pretrainted model to predict the outcome</h1>
      <h1>Train a completely new model</h1>
      <h1>Providing feedback to the trained model</h1>
      <ImportanceBarChart />
      <AccuracyLineChart />
      <F1MacroLineChart />
      <F1WeightedLineChart /> -->
      <router-view></router-view>
      <PredictiveDashboard />
    </div>
  </template>
  
<script setup>
  // import ImportanceBarChart from '@/components/PredictiveView/ImportanceBarChart.vue';
  // import AccuracyLineChart from '@/components/PredictiveView/AccuracyLineChart.vue';
  // import F1MacroLineChart from '@/components/PredictiveView/F1MacroLineChart.vue';
  // import F1WeightedLineChart from '@/components/PredictiveView/F1WeightedLineChart.vue';
  import PredictiveDashboard from '@/components/PredictiveView/PredictiveDashboard.vue';
</script>