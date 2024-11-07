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
            Lorem Ipsum Dolor
          </v-card-title>
          <v-card-text class="bg-white text--primary">
            <p>Lorem ipsum dolor sit amet, no nam oblique veritus...</p>
            <v-btn :color="item.color" variant="outlined">
              Button
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
  },
  {
    color: 'purple-lighten-2',
    icon: 'mdi-book-variant',
  },
  {
    color: 'green-lighten-1',
    icon: 'mdi-airballoon',
  },
  {
    color: 'indigo-lighten-2',
    icon: 'mdi-layers-triple',
  },
]
</script>
