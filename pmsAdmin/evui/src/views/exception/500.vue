<template>
  <div class="ele-exception ele-text-center">
    <div class="ele-exception-img">
      <img src="@/assets/ic-500.svg" alt="" width="400px" height="185px">
    </div>
    <div class="ele-exception-content ele-text-left">
      <h1 class="ele-text">500</h1>
      <p class="ele-text-secondary">抱歉，服务器出错了</p>
      <div>
        <router-link to="/">
          <el-button type="primary">返回首页</el-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Exception500'
}
</script>
