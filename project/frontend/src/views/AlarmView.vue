<template>
    <div class="intro">
    <span class="intro-title">自动报警</span>
    <div class="block-container">
      <Feature
        :image="require('@/assets/img/monitoring.png')"
        title="实时监测"
        description="24小时监测玻璃幕墙加速度数据，不放过任何异常。"
      />
      <Feature
        :image="require('@/assets/img/alarm.png')"
        title="邮件报警"
        description="发现异常后，通过邮件向用户发送警告，以便即使处理风险。"
      />
    </div>
  </div>
</template>
  
<script>
import Feature from '/src/components/IntroBlock.vue';
  
export default {
    components: {
        Feature,
    },
};
</script>
