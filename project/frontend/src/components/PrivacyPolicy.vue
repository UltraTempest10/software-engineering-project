<template>
  <div class="policy-container">
    <div class="policy-title-container">
      <span class="policy-title">隐私政策</span>
    </div>
    <div class="policy-body-container">
      <h2 class="policy-subtitle">1. 信息的收集与使用</h2>
      <p>我们收集和使用的信息主要包括用户提供的邮箱地址。该信息用于提供异常监测报警服务，以及提高幕墙检测的效率。</p>
      <h2 class="policy-subtitle">2. 信息的分享与披露</h2>
      <p>我们不会将你的邮箱地址分享或披露给任何第三方，除非得到你的明确许可，或者在法律要求或允许的范围内。</p>
      <h2 class="policy-subtitle">3. 信息的存储与安全</h2>
      <p>我们采取各种安全措施来保护你的邮箱地址，防止未经授权的访问、使用或泄露。</p>
      <h2 class="policy-subtitle">4. 用户权利</h2>
      <p>你有权访问或更正你的邮箱地址。如果你有任何问题或者请求，欢迎随时联系我们。</p>
      <h2 class="policy-subtitle">5. 隐私政策的修改</h2>
      <p>我们可能会不时地修改本隐私政策。如果我们对处理你的邮箱地址的方式做出任何重大改变，我们会提前通知你。</p>
      <h2 class="policy-subtitle">6. 联系我们</h2>
      <p>如果你对本隐私政策有任何问题或者建议，欢迎随时联系我们。联系邮箱：ultratempest@tongji.edu.cn。</p>
    </div>
  </div>
</template>
  
<script>
export default {
    name: 'PrivacyPolicy'
}
</script>

<style>
.policy-title{
    text-align: center;
    font-size: 60px;
    font-weight: 700;
    letter-spacing: 0px;
    line-height: 88px;
    text-align:center;
    vertical-align: top;
}

.subtitle{
    font-size: 18px;
    font-weight: 400;
    letter-spacing: 0px;
    line-height: 28px;
    text-align:center;
    vertical-align: top;
    text-shadow: 1px 1px 2px #0F0F0F;
}

.policy-container{
    /* align-items: center; */
    /* justify-content: space-between; */
    padding-left: 95px;
    padding-right: 40px;
    margin: auto;
}

.policy-title-container{
    text-align: center;
    align-items: center;
    justify-content: space-between;
    padding-left: 40px;
    padding-right: 40px;
    padding-bottom: 40px;
}

.policy-body-container{
    text-align: left;
    align-items: center;
    justify-content: space-between;
    padding-left: 95px;
    padding-right: 40px;
}
</style>
