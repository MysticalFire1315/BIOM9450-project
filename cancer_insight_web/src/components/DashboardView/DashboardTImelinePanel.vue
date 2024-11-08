<template>
  <v-card color="#FEAEBC">
    <v-card-title class="text-left" style="font-size:xx-large;" >
      Recent Activities
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
            <p>{{ item.activity_timestamp }}</p>
            <v-btn :color="item.color" variant="outlined">
              Go there!
            </v-btn>
          </v-card-text>
        </v-card>
      </v-timeline-item>
    </v-timeline>
    </v-card-text>
  </v-card>
  
</template>

<script setup>
const items = [
  {
    color: 'red-lighten-2',
    icon: 'mdi-star',
    activity_title: "Save a new User",
    activity_timestamp: "Nov 8, 2024 11:59am"

  },
  {
    color: 'purple-lighten-2',
    icon: 'mdi-book-variant',
    activity_title: "Save a new Model",
    activity_timestamp: "Nov 7, 2024 8:34am"
  },
  {
    color: 'green-lighten-1',
    icon: 'mdi-airballoon',
    activity_title: "Train a new Model",
    activity_timestamp: "Nov 9, 2024 5:34am"
  },
]
</script>
