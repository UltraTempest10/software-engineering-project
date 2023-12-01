<template>
    <div>
        <div class="header">
            <div class="box1">
                <h1>
                    <span>玻璃幕墙智库</span>
                </h1>
            </div>

            <div class="box1">
                <nav class="nav_link">
                    <router-link class="link_btn" active-class="active" to="/Home">首页</router-link>
                </nav>              
                <nav class="nav_link">
                    <router-link class="link_btn" active-class="active" to="/FramePlayer">图片播放</router-link>
                </nav>
                <nav class="nav_link">
                    <router-link class="link_btn" active-class="active" to="/DataView">数据展示</router-link>
                </nav>
                <nav class="nav_link">
                    <router-link class="link_btn" active-class="active" to="/AlarmView">自动报警</router-link>
                </nav>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NavBar"
    }
</script>

<style>
    .header{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        height: 70px;
        background-color:#ffffff;
        color: #ffffff;
        border-bottom: 1px solid #ececec;
        overflow: hidden;
    }
    .box1{
        display: flex;
        align-items: center;
        overflow: hidden;
    }
    h1{
        display: flex;
        align-items: center;
        font: normal 24px Cookie;
        padding: 0px 20px;
        color:#2c2c2c;
        font-weight: bold;
    }
    .img_title{
        width: 40px;
        height: 40px;
    }

    .nav_link{
        display: flex;
        align-items: center;
        padding: 0 30px;
    }
    .link_btn{
        text-decoration:none;
        color: #7F7F7F;
        font-size: 16px;
        font-weight: normal;
    }
    .img_btn{
        width: 30px;
        height: 30px;
    }
</style>
