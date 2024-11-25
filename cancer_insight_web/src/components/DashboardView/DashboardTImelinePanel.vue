<template>
  <div>

  <v-card color="#FEAEBC">
    <v-card-title class="text-left" style="font-size:xx-large;" >
      Navigation
    </v-card-title>
    <v-card-text>
      <v-timeline direction="horizontal" side="end">
      <v-timeline-item
        v-for="(item, i) in items"
        :key="i"
        :dot-color="item.color"
        :icon="item.icon"
        fill-dot
      >
        <v-card>
          <v-card-title :class="['text-h6', `bg-${item.color}`]">
            {{ item.activity_title }}
          </v-card-title>
          <v-card-text class="bg-white text--primary">
            <!-- <p>{{ item.activity_timestamp }}</p> -->
            <v-btn :color="item.color" variant="outlined" @click="navigateTo(`${item.link}`)">
              Go there!
            </v-btn>
          </v-card-text>
        </v-card>
      </v-timeline-item>
    </v-timeline>
    </v-card-text>
  </v-card>

</div>
  
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const navigateTo = (route) => {
    router.push(route);
};

const items = [
  {
    color: 'red-lighten-2',
    icon: 'mdi-star',
    activity_title: "Add a patient",
    link: "/database/create-patient"

  },
  {
    color: 'purple-lighten-2',
    icon: 'mdi-book-variant',
    activity_title: "Add a Model",
    activity_timestamp: "Nov 7, 2024 8:34am",
    link: "/predictive/new-training"
  },
  {
    color: 'green-lighten-1',
    icon: 'mdi-airballoon',
    activity_title: "Feature Prediction",
    activity_timestamp: "Nov 9, 2024 5:34am",
    link: "/predictive/new-prediction"
  },
]

</script>
