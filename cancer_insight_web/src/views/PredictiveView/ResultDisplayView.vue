<template>
    <div>
    <!-- <AccuracyLineChart /> -->
     <F1MacroLineChart/>
     <F1WeightedLineChart/>
    </div>
</template>

<script setup>
    // import AccuracyLineChart from '@/components/PredictiveView/AccuracyLineChart.vue';
    import F1MacroLineChart from '@/components/PredictiveView/F1MacroLineChart.vue';
    import F1WeightedLineChart from '@/components/PredictiveView/F1WeightedLineChart.vue';
</script>