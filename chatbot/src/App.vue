<template>
  <div id="app">
    <!-- <Menu />/ -->
    <router-view />
  </div>
</template>
<script>
// @ is an alias to /src
// import Menu from "@/components/menu.vue";

export default {
  name: "app",
  // components: {
  //   Menu
  // },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #0dcaf0 !important;
}
</style>
