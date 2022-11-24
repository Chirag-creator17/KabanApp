<template>
  <div id="app">
    <NavBar />
    <div class="container">
      <router-view></router-view>
    </div>
    
  </div>
</template>

<script>

import NavBar from './components/NavBar.vue'
// vuex import

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
