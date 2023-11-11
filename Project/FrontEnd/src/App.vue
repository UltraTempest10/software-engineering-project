<template>
  <NavBar/>

  <router-view/>
</template>

<script>
import NavBar from './components/TabNav.vue'

export default{
  name:"App",
  components: {NavBar}
}

</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header{
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 70px;
        background-color:#F0F0F0;
        color: #F0F0F0;
        border: 1px solid #2c2c2c;
    }

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
