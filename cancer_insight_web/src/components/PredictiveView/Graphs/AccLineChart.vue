Acc<!-- This is the trend chart for Acc -->
<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue';
import * as echarts from 'echarts';
import apiService from '@/services/apiService';
import { useRoute } from 'vue-router';

const trend_chart = ref(null);
let chartInstance = null;

// Initialize the chart
const initChart = () => {
    nextTick(() => {
        if (trend_chart.value) {
            chartInstance = echarts.init(trend_chart.value, 'chalk');
            updateChart();
        }
    });
};

const chartData = ref([]);

// Process data for the chart
const handleChartData = async () => {
    const route = useRoute();

    // Extract the modelId from the dynamic route parameter
    const modelId = computed(() => route.params.modelId);

    const enquiryData = {
        model_id: parseInt(modelId.value),
        metric_type: "training",
        interval: 50
    };

    const message = ref([]);

    try {
        const response = await apiService.postData('/ml/metrics', enquiryData);
        message.value = response.data
    } catch (error) {
        alert(error);
    }

    chartData.value = message.value.map(item => [item.epoch, item.acc]); 
    updateChart();
};

// Update the chart options and render it
const updateChart = () => {
    if (!chartInstance) return;

    const option = {
        title: {
            text: 'Training Performance of Acc Over Epochs',
            left: 20,
            top: 20,
        },
        grid: {
            top: '20%',
            left: '10%',
            right: '5%',
            bottom: '10%',
        },
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: ['Acc'],
            top: '10%',
        },
        xAxis: {
            type: 'category',
            data: chartData.value.map(item => item[0]),
            name: 'Epoch',
            axisLabel: {
                interval: 0,
                rotate: 30,
            },
        },
        yAxis: {
            type: 'value',
            name: 'Acc',
        },
        series: [
            {
                name: 'Acc',
                type: 'line',
                data: chartData.value.map(item => item[1]),
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: {
                    width: 2,
                    color: '#FFD700',
                },
                itemStyle: {
                    color: '#FFD700',
                },
                areaStyle: {
                    opacity: 0.1,
                },
            },
        ],
    };

    chartInstance.setOption(option);
};

// Resize the chart on window resize
const resizeChart = () => {
    chartInstance?.resize();
};

// Lifecycle hooks
onMounted(() => {
    initChart();
    handleChartData();
    window.addEventListener('resize', resizeChart);
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart);
    if (chartInstance) chartInstance.dispose();
});
</script>

<template>
    <div class="trend_container">
        <div class="trend_chart" ref="trend_chart"></div>
    </div>
</template>

<style scoped>
.trend_container {
    width: 100%;
    height: 400px; /* Ensure a fixed height to avoid "can't get DOM width or height" issue */
}

.trend_chart {
    width: 100%;
    height: 100%;
}
</style>