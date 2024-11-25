<template>
    <div>
        <h1>Displaying results for Model {{ modelId }}</h1>
        <ImportanceBarChart />
        
        <AccLineChart />
        <F1WeightedLineChart />
        <F1MacroLineChart />
        <AucLineChart />
        <Precision_valLineChart />
        <LossLineChart />


        <F1AccLineChartTe />
        <F1WeightedLineChartTe />
        <F1MacroLineChartTe />
        <F1AUCLineChartTe1 />
        <F1Precision_valLineChartTe />
        <F1LossLineChartTe />

    </div>
</template>

<script setup>
    import { useRoute } from 'vue-router';
    import { computed } from 'vue';
    import ImportanceBarChart from '@/components/PredictiveView/ImportanceBarChart.vue';

    import F1MacroLineChart from '@/components/PredictiveView/Graphs/F1MacroLineChart.vue';
    import F1WeightedLineChart from '@/components/PredictiveView/Graphs/F1WeightedLineChart.vue';
    import AccLineChart from '@/components/PredictiveView/Graphs/AccLineChart.vue';
    import AucLineChart from '@/components/PredictiveView/Graphs/AucLineChart.vue';
    import Precision_valLineChart from '@/components/PredictiveView/Graphs/Precision_valLineChart.vue';
    import LossLineChart from '@/components/PredictiveView/Graphs/LossLineChart.vue';

    import F1AUCLineChartTe1 from '@/components/PredictiveView/Graphs/F1AUCLineChart-te.vue';
    import F1AccLineChartTe from '@/components/PredictiveView/Graphs/F1AccLineChart-te.vue';
    import F1Precision_valLineChartTe from '@/components/PredictiveView/Graphs/F1Precision_valLineChart-te.vue';
    import F1LossLineChartTe from '@/components/PredictiveView/Graphs/F1LossLineChart-te.vue';
    import F1WeightedLineChartTe from '@/components/PredictiveView/Graphs/F1WeightedLineChart-te.vue';
    import F1MacroLineChartTe from '@/components/PredictiveView/Graphs/F1MacroLineChart-te.vue';


    const route = useRoute();

    // Extract the modelId from the dynamic route parameter
    const modelId = computed(() => route.params.modelId);
</script>
