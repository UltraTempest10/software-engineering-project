<template>

<div class="cover">
    <div class="hometitle">
        玻璃幕墙智库
        <div class="subtitle">
        玻璃幕墙智库提供无人机拍摄的玻璃幕墙图片以及传感器监测收集的传感器加速度数据，包括图片播放、数据展示和自动报警三个栏目
        </div>
        
        <el-button type="primary" @click="goToPage">登录</el-button>
    </div> 


</div> 



</template>

<!-- <script setup lang="ts">
import { ref } from 'vue'
 
defineProps<{ msg: string }>()
 
const count = ref(0)

</script> -->

<script>
export default {
  methods: {
    goToPage() {
      this.$router.push('/Login');
    }
  }
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