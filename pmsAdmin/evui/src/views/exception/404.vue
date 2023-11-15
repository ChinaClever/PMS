<template>
  <div class="ele-exception ele-text-center">
    <div class="ele-exception-img">
      <img src="@/assets/ic-404.svg" alt="" width="305px" height="245px">
    </div>
    <div class="ele-exception-content ele-text-left">
      <h1 class="ele-text">404</h1>
      <p class="ele-text-secondary">抱歉，你访问的页面不存在</p>
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
  name: 'Exception404'
}
</script>
