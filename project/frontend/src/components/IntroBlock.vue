<!-- IntroBlock.vue: 介绍块 -->

<template>
    <div class="feature">
        <img :src="image" alt="Feature image" />
        <!-- <h2>{{ title }}</h2> -->
        <p>{{ description }}</p>
    </div>
</template>


<script>
export default {
    props: {
        image: String,
        title: String,
        description: String,
    },
};
</script>


<style scoped>
.feature {
    text-align: left;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    width: 360px;
    padding-top: 30px;
    padding-right: 50px;
}

.feature img {
    display: block;
    width: 32px;
    height: 32px;
    margin: auto 0;
}

.feature h2 {
    font-size: 1.5em;
    color: #333;
    text-align: left;
}

.feature p {
    font-size: 1.2em;
    color: #666;
    text-align: left;
    width: 300px;
}
</style>
