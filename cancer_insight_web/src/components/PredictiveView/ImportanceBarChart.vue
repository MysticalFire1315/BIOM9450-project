<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

const rank_chart = ref(null);
let chartInstance = null;

// 初始化图表实例
const initChart = () => {
    if (rank_chart.value) {
        // Ensure the chart container has valid dimensions
        console.log("Chart container dimensions:", rank_chart.value.clientWidth, rank_chart.value.clientHeight);
        if (rank_chart.value.clientWidth > 0 && rank_chart.value.clientHeight > 0) {
            chartInstance = echarts.init(rank_chart.value, 'chalk'); // Initialize chart with the 'chalk' theme
        } else {
            console.warn('Chart container has no dimensions');
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

// 数据存储
const allData = ref([]);

// 硬编码数据
const hardcodedData = [
    { category: "hsa-miR-132", value: "58.90909090909089" },
    { category: "hsa-miR-129-5p", value: "55.11961722488037" },
    { category: "hsa-miR-146b-5p", value: "51.42857142857142" },
    { category: "cg04126866", value: "46.233766233766225" },
    { category: "cg08367223", value: "46.233766233766225" },
    { category: "cg19485804", value: "46.233766233766225" },
    { category: "hsa-miR-129-3p", value: "44.326812428078235" },
    { category: "hsa-miR-2114", value: "44.326812428078235" },
    { category: "cg18149207", value: "42.70396270396268" },
    { category: "hsa-miR-24", value: "40.90909090909089" },
    { category: "hsa-miR-143", value: "40.90909090909089" },
    { category: "cg03894103", value: "39.201773835920164" },
    { category: "hsa-miR-660", value: "37.57575757575757" },
    { category: "hsa-miR-185", value: "37.57575757575757" },
    { category: "cg13468685", value: "35.96933187294633" },
    { category: "cg08952029", value: "35.90909090909089" },
    { category: "cg01182697", value: "35.90909090909089" },
    { category: "hsa-miR-1308", value: "34.323725055432355" },
    { category: "cg15789095", value: "32.97805642633227" },
    { category: "cg20793071", value: "32.6374859708193" },
    { category: "ENSG00000105419.11", value: "31.778656126482208" },
    { category: "hsa-miR-448", value: "31.150054764512582" },
    { category: "hsa-miR-432", value: "31.150054764512582" },
    { category: "cg24192663", value: "29.999999999999982" },
    { category: "cg12556134", value: "29.732620320855595" },
    { category: "cg00754253", value: "29.445676274944567" },
    { category: "ENSG00000174607.6", value: "28.97360703812315" },
    { category: "ENSG00000165175.11", value: "28.97360703812315" },
    { category: "cg15775914", value: "28.051948051948038" },
    { category: "hsa-miR-130b", value: "28.051948051948038" }
];

// 异步获取数据 (用硬编码数据代替 API 调用)
const getData = async () => {
    try {
        console.log('硬编码数据:', hardcodedData); // 打印硬编码的数据结构

        // 检查数据格式
        if (!hardcodedData || !Array.isArray(hardcodedData)) {
            throw new Error('数据格式错误，期望为数组');
        }

        // 解析字段，确保字段名称和格式正确
        allData.value = hardcodedData.map(item => ({
            feat_name: item.category || 'Unknown', // 确保字段名正确
            imp: parseFloat(item.value || 0), // 确保 `imp` 转换为数字
        }));

        console.log('解析后的数据:', allData.value); // 打印解析后的数据
        updateChart(); // 数据到达后更新图表
    } catch (error) {
        console.error('获取数据失败:', error);
    }
};

// 更新图表
const updateChart = () => {
    if (!chartInstance) {
        console.error('图表实例未初始化');
        return;
    }

    const colorArr = [
        ['#8B0000', '#FFA07A'], // 红色渐变
        ['#FFA500', '#FFFACD'], // 橙色渐变
        ['#ADFF2F', '#006400'], // 绿色渐变
        ['#40E0D0', '#008B8B'], // 蓝色渐变
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
            data: allData.value.map(item => item.feat_name), // 使用特征名称作为 X 轴
            axisLabel: {
                interval: 0, // 显示所有标签
                rotate: 30, // 旋转标签防止重叠
            },
        },
        yAxis: {
            type: 'value', // 使用标准类型
            name: 'Importance', // Y 轴名称
        },
        series: [
            {
                name: 'Importance',
                type: 'bar',
                data: allData.value.map(item => item.imp), // 使用 `imp` 作为数据
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
            show: false, // 是否显示数据缩放工具
            start: dataZoomStart.value, // 数据窗口的起始位置
            end: dataZoomEnd.value, // 数据窗口的结束位置
        },
    };

    // 将配置应用到图表实例
    chartInstance.setOption(option);
};

// 自适应屏幕
const screenAdapter = () => {
    chartInstance.resize(); // 调整图表大小以适配容器
    const titleFontSize = rank_chart.value.offsetWidth / 100 * 3.6; // 动态计算字体大小
    const AdapterOption = {
        title: {
            textStyle: {
                fontSize: rank_chart.value.offsetWidth / 100 * 2.5, // 调整标题字体大小
            },
        },
        series: {
            barWidth: titleFontSize, // 调整柱宽
            itemStyle: {
                borderRadius: [titleFontSize / 2, titleFontSize / 2, 0, 0], // 圆角柱状图
            },
        },
    };
    chartInstance.setOption(AdapterOption); // 应用新的适配选项
};

// 定义数据缩放范围和定时器
const dataZoomStart = ref(0);
const dataZoomEnd = ref(50);
const timeId = ref(null);

// 启动定时器，实现图表动态滚动
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

// 清理定时器
const stopInterval = () => {
    timeId.value && clearInterval(timeId.value);
};

// 组件生命周期
onMounted(() => {
    initChart();
    getData(); // Load data and update the chart
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
