<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRoute } from 'vue-router';
import * as echarts from 'echarts';
import apiService from '@/services/apiService';


const rank_chart = ref(null);
let chartInstance = null;

const initChart = () => {
    if (rank_chart.value) {
        // Ensure the chart container has valid dimensions
        // console.log("Chart container dimensions:", rank_chart.value.clientWidth, rank_chart.value.clientHeight);
        if (rank_chart.value.clientWidth > 0 && rank_chart.value.clientHeight > 0) {
            chartInstance = echarts.init(rank_chart.value, 'chalk'); // Initialize chart with the 'chalk' theme
        } else {
            // console.warn('Chart container has no dimensions');
            return; // Prevent further execution if dimensions are invalid
        }
    }

    // Add mouseover and mouseout event listeners
    chartInstance.on('mouseover', () => {
        clearInterval(timeId.value); // Pause the chart animation on mouseover
    });

    chartInstance.on('mouseout', () => {
        startInterval(); // Restart the chart animation on mouseout
    });
};


const allData = ref([]);




const updateChart = () => {
    if (!chartInstance) {
        
        return;
    }

    const colorArr = [
        ['#8B0000', '#FFA07A'], 
        ['#FFA500', '#FFFACD'],
        ['#ADFF2F', '#006400'], 
        ['#40E0D0', '#008B8B'], 
    ];

    const option = {
        title: {
            text: 'Importance of Each Feature',
            left: 20,
            top: 20,
        },
        grid: {
            top: '30%',
            left: '10%',
            right: '5%',
            bottom: '10%',
            containLabel: true,
        },
        tooltip: { show: true },
        xAxis: {
            type: 'category',
            data: allData.value.map(item => item.feat_name), 
            axisLabel: {
                interval: 0, 
                rotate: 30, 
            },
        },
        yAxis: {
            type: 'value', 
            name: 'Importance',
        },
        series: [
            {
                name: 'Importance',
                type: 'bar',
                data: allData.value.map(item => item.imp), 
                itemStyle: {
                    color: arg => {
                        const value = arg.data;
                        let targetColorArr;
                        if (value > 50) {
                            targetColorArr = colorArr[0];
                        } else if (value > 40) {
                            targetColorArr = colorArr[1];
                        } else if (value > 30) {
                            targetColorArr = colorArr[2];
                        } else {
                            targetColorArr = colorArr[3];
                        }
                        return {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [
                                { offset: 0, color: targetColorArr[0] },
                                { offset: 1, color: targetColorArr[1] },
                            ],
                            global: false,
                        };
                    },
                },
            },
        ],
        dataZoom: {
            show: false, 
            start: dataZoomStart.value, 
            end: dataZoomEnd.value, 
        },
    };

    
    chartInstance.setOption(option);
};


const screenAdapter = () => {
    chartInstance.resize(); 
    const titleFontSize = rank_chart.value.offsetWidth / 100 * 3.6; 
    const AdapterOption = {
        title: {
            textStyle: {
                fontSize: rank_chart.value.offsetWidth / 100 * 2.5, 
            },
        },
        series: {
            barWidth: titleFontSize, 
            itemStyle: {
                borderRadius: [titleFontSize / 2, titleFontSize / 2, 0, 0], 
            },
        },
    };
    chartInstance.setOption(AdapterOption); 
};


const dataZoomStart = ref(0);
const dataZoomEnd = ref(50);
const timeId = ref(null);


const startInterval = () => {
    timeId.value && clearInterval(timeId.value);
    timeId.value = setInterval(() => {
        dataZoomStart.value += 10;
        if (dataZoomStart.value > 50) dataZoomStart.value = 0;
        dataZoomEnd.value += 10;
        if (dataZoomEnd.value > 100) dataZoomEnd.value = 50;
        const option = {
            dataZoom: {
                show: false,
                start: dataZoomStart.value,
                end: dataZoomEnd.value,
            },
        };
        chartInstance.setOption(option);
    }, 1000);
};


const stopInterval = () => {
    timeId.value && clearInterval(timeId.value);
};

const message = ref([]);

const route = useRoute();

    // Extract the modelId from the dynamic route parameter
const modelId = computed(() => route.params.modelId);

const fetchImportanceData = async () => {
    try {
        const response = await apiService.getData(`/ml/model/${modelId.value}`);
        
        // Map the response data to the desired format
        message.value = Array.from(response.data.data.features.map(item => ({
            category: item.feat_name,
            value: item.imp.toString(), // Convert `imp` to a string
        })));

        allData.value = message.value.map(item => ({
            feat_name: item.category || 'Unknown', 
            imp: parseFloat(item.value || 0), 
        }));

    
        updateChart(); 

    } catch (error) {
        console.error(error);
    }
};


onMounted(() => {
    /* eslint-disable */
    // console.log(modelId);
    fetchImportanceData();
    initChart();
    // getData(); // Load data and update the chart
    window.addEventListener('resize', screenAdapter); // Adjust chart on window resize
    startInterval(); // Start dynamic scrolling
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', screenAdapter);
    if (chartInstance) chartInstance.dispose(); // Dispose of the chart instance
    stopInterval(); // Stop dynamic scrolling
});
</script>

<template>
    <div class="rank_container">
        <div ref="rank_chart" class="rank_chart"></div>
    </div>
</template>

<style scoped>
.rank_container {
    width: 100%;
    height: 800px; /* Adjust height as needed */
    overflow: hidden;
}

.rank_chart {
    width: 100%;
    height: 100%;
    margin-top: 5%;
}
</style>
