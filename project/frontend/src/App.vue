<template>
  <a-config-provider :locale="locale">
    <div class="container">
      <NavBar />
      <router-view />
    </div>
  </a-config-provider>
</template>

<script>
import NavBar from './components/TabNav.vue'
import { ConfigProvider } from "ant-design-vue"
import zhCN from "ant-design-vue/es/locale/zh_CN"

export default {
  name: "App",
  components: { NavBar, AConfigProvider: ConfigProvider },
  data() {
    return {
      locale: zhCN,
    }
  },
}

</script>

<style lang="scss">
#app {

  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.intro {
  background-color: #FCFCFC;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding-left: 95px;
  padding-right: 40px;
}

.intro-title {
  color: #000;
  font-size: 48px;
  font-weight: 600;
}

.block-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.main {
  // border-radius: 10px;
  // box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
  background-color: #FCFCFC;
  padding-left: 70px;
  padding-right: 70px;
  padding-bottom: 30px;
}

.el-container {
  .el-aside {
    border-radius: 10px;
    box-shadow: 0px 0px 8px rgba(10, 10, 10, 0.3);
    padding: 40px;
    text-align: center;
  }

  .el-main {
    display: flex;
    justify-content: right;
    align-items: center;
  }

  .el-form-item {
    margin-bottom: 0px;
  }
}

.tool-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

// .header {
//   display: flex;
//   align-items: center;
//   justify-content: flex-start;
//   height: 70px;
//   background-color: #FFFFFF;
//   color: #FFFFFF;
// }

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #1D2129;
    }
  }
}
</style>
