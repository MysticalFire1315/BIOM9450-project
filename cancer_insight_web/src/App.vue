<template>
  <div id="app">
    <TopBar />
    <LoginPage />
  </div>
</template>

<script>
import TopBar from './components/TopBar.vue';
import LoginPage from './components/LoginPage.vue';

export default {
  components: {
    TopBar,
    LoginPage
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
