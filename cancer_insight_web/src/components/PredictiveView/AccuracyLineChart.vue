<!-- This is the trend chart for ACC -->
<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import * as echarts from 'echarts';

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

// Adjust chart on window resize
const resizeChart = () => {
    if (chartInstance) {
        chartInstance.resize();
    }
};

const allData = ref([]);
const hardcodedData = ref([
    { epoch: 0, acc: 0.408, f1_weighted: 0.380, f1_macro: 0.385 },
    { epoch: 50, acc: 0.620, f1_weighted: 0.589, f1_macro: 0.585 },
    { epoch: 100, acc: 0.804, f1_weighted: 0.799, f1_macro: 0.797 },
    { epoch: 150, acc: 0.931, f1_weighted: 0.931, f1_macro: 0.931 },
    { epoch: 200, acc: 0.963, f1_weighted: 0.963, f1_macro: 0.963 },
    { epoch: 250, acc: 0.963, f1_weighted: 0.963, f1_macro: 0.963 },
    { epoch: 300, acc: 0.976, f1_weighted: 0.976, f1_macro: 0.975 },
    { epoch: 350, acc: 0.971, f1_weighted: 0.971, f1_macro: 0.971 },
    { epoch: 400, acc: 0.976, f1_weighted: 0.976, f1_macro: 0.975 },
    { epoch: 450, acc: 0.984, f1_weighted: 0.984, f1_macro: 0.984 },
    { epoch: 500, acc: 0.980, f1_weighted: 0.980, f1_macro: 0.980 },
    { epoch: 550, acc: 0.980, f1_weighted: 0.980, f1_macro: 0.980 },
    { epoch: 600, acc: 0.976, f1_weighted: 0.976, f1_macro: 0.976 },
    { epoch: 650, acc: 0.967, f1_weighted: 0.967, f1_macro: 0.967 },
    { epoch: 700, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 750, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 800, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 850, acc: 0.984, f1_weighted: 0.984, f1_macro: 0.984 },
    { epoch: 900, acc: 0.992, f1_weighted: 0.992, f1_macro: 0.992 },
    { epoch: 950, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 1000, acc: 0.984, f1_weighted: 0.984, f1_macro: 0.984 },
    { epoch: 1050, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1100, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 1150, acc: 0.984, f1_weighted: 0.984, f1_macro: 0.984 },
    { epoch: 1200, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1250, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1300, acc: 0.992, f1_weighted: 0.992, f1_macro: 0.992 },
    { epoch: 1350, acc: 0.992, f1_weighted: 0.992, f1_macro: 0.992 },
    { epoch: 1400, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 1450, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 1500, acc: 0.980, f1_weighted: 0.980, f1_macro: 0.980 },
    { epoch: 1550, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 1600, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 1650, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 1700, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1750, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1800, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 1850, acc: 0.992, f1_weighted: 0.992, f1_macro: 0.992 },
    { epoch: 1900, acc: 0.996, f1_weighted: 0.996, f1_macro: 0.996 },
    { epoch: 1950, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2000, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2050, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 2100, acc: 0.988, f1_weighted: 0.988, f1_macro: 0.988 },
    { epoch: 2150, acc: 0.976, f1_weighted: 0.976, f1_macro: 0.976 },
    { epoch: 2200, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2250, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2300, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2350, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2400, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2450, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 },
    { epoch: 2500, acc: 1.000, f1_weighted: 1.000, f1_macro: 1.000 }
]);

const chartData = ref([]);

// Fetch chart data
const getChartData = async () => {
    try {
        allData.value = hardcodedData.value.map(item => ({
            epoch: item.epoch,
            acc: item.acc,
            f1_weighted: item.f1_weighted,
            f1_macro: item.f1_macro,
        }));

        handleChartData();
    } catch (error) {
        console.error("Error fetching chart data:", error);
    }
};

// Process chart data for visualization
const handleChartData = () => {
    chartData.value = allData.value.map(item => [item.epoch, item.acc]);
};

// Update the chart with new data
const updateChart = () => {
    if (!chartInstance) return;

    const option = {
        title: {
            text: 'Training Performance of ACC Over Epochs',
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
            data: ['ACC'],
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
            name: 'ACC',
        },
        series: [
            {
                name: 'ACC',
                type: 'line',
                data: chartData.value.map(item => item[1]),
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: {
                    width: 2,
                    color: '#FF4500',
                },
                itemStyle: {
                    color: '#FF4500',
                },
                areaStyle: {
                    opacity: 0.1,
                },
            },
        ],
    };

    chartInstance.setOption(option);
};

// Lifecycle hooks
onMounted(() => {
    initChart();
    getChartData();
    window.addEventListener('resize', resizeChart);
});

onBeforeUnmount(() => {
    if (chartInstance) {
        chartInstance.dispose();
    }
    window.removeEventListener('resize', resizeChart);
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
    height: 400px; /* Define a fixed height for the container */
}

.trend_chart {
    width: 100%;
    height: 100%; /* Ensure the chart takes full space of the container */
}
</style>
