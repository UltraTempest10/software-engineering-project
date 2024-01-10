<!-- Home.vue: 首页 -->

<template>

  <div class="cover">
    <div class="hometitle">
      玻璃幕墙智库
      <div class="subtitle">
        玻璃幕墙智库提供无人机拍摄的玻璃幕墙图片以及传感器监测收集的传感器加速度数据，包括图片播放、数据展示和自动报警三个栏目
      </div>
        
      <el-button type="primary" @click="showMore">了解更多</el-button>
    </div> 
    <a-modal v-model:visible="more" title="玻璃幕墙智库" :footer="null" closable>
      <p class="more" style="margin-top: 25px">玻璃幕墙智库是为解决高层建筑玻璃幕墙检测和监控而开发的平台。平台整合了无人机图像和传感器数据，为维护人员提供了一种高效、安全且低成本的检测手段。</p>
      <p class="more">玻璃幕墙智库旨在成为现代建筑维护领域的优良解决方案，提高幕墙检测的效率和准确性。</p>
    </a-modal>

  </div> 

</template>

<!-- <script setup lang="ts">
import { ref } from 'vue'
 
defineProps<{ msg: string }>()
 
const count = ref(0)

</script> -->

<script>
import { ref } from 'vue';
import { Modal } from 'ant-design-vue';

export default {
  components: {
    'a-modal': Modal,
  },

  setup() {
    const more = ref(false);

    const showMore = () => {
      more.value = true;
    };

    return {
      more,
      showMore,
    };
  },
  // methods: {
  //   goToPage() {
  //     this.$router.push('/Login');
  //   }
  // }
}
</script>


<style>
.hometitle{
  color:white;
  font-size: 80px;
  font-weight: 700;
  letter-spacing: 0px;
  line-height: 88px;
  position:relative;
  top:240px;
  text-align:center;
  vertical-align: top;
  text-shadow: 1px 1px 2px #0F0F0F;
}

.subtitle{
  color:white;
  font-size: 18px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 28px;
  position:relative;
  top:10px;
  text-align:center;
  vertical-align: top;
  text-shadow: 1px 1px 2px #0F0F0F;
}

.more{
  text-indent:2em;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 28px;
}

.cover{
  width:100%;
  height:100%;
  position:relative;
  text-align:center;
  line-height:300px;
  color:white;
}

.cover::before{    
  content:'';
  position:absolute;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background:transparent url("/src/assets/img/background.png") center center no-repeat;
  filter:blur(5px);
  background-size:cover;
}
</style>
