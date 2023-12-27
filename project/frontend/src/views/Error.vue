<template>
    <div class="error-container">
        <div class="error-title-container">
            <span class="error-title">抱歉！</span>
        </div>
        <div class="error-body-container">
            <h2 class="error-subtitle">您访问的页面不存在</h2>

            <p>请检查您输入的网址，或点击下方按钮返回首页。</p>

            <a class="error-button" href="#/index">{{ jumpTime }}s&nbsp;返回首页</a>
        </div>
    </div>
</template>
    
<script>
import { onMounted, onBeforeUnmount, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'Error',
    setup() {
        const router = useRouter();
        const timer = ref(0);
        const jumpTime = ref(5);
        const timeChange = () => {
        let timer = null;
        timer = setInterval(() => {
            if (jumpTime.value > 0) {
                jumpTime.value --;
            } else {
                router.push("/");
                // router.push({path:'/home', query:{id:'12' }})
                clearInterval(timer);
            }
        }, 1000)
        };
        onMounted(() => {
            timeChange();
        });
        onBeforeUnmount(() => {
            clearInterval(timer);
        });
        return {
            jumpTime,
            timer,
        }
    },
}
</script>
  
<style>
.error-title {
    font-size: 60px;
    font-weight: 700;
    letter-spacing: 0px;
    line-height: 88px;
    text-align: center;
    vertical-align: top;
}

.error-subtitle {
    text-align: left;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 0px;
    line-height: 28px;
    vertical-align: top;
}

.error-container {
    /* align-items: center; */
    /* justify-content: space-between; */
    padding-left: 40px;
    padding-right: 40px;
    margin-top: 200px;
    margin-bottom: auto;
    margin-left: auto;
    margin-right: auto;
}

.error-title-container {
    text-align: center;
    align-items: center;
    justify-content: space-between;
    padding-left: 40px;
    padding-right: 40px;
    padding-bottom: 40px;
}

.error-body-container {
    text-align: left;
    align-items: center;
    justify-content: space-between;
    padding-left: 40px;
    padding-right: 40px;
}

.error-button {
    display: block;
    float: left;
    width: 110px;
    height: 36px;
    font-size: 14px;
    line-height: 36px;
    color: #fff;
    text-align: center;
    cursor: pointer;
    background: #409EFF;
    border-radius: 5px;
    /* opacity: 0; */
    text-decoration: none;
    margin-top: 20px;
    margin-left: 100px;
}
</style>