<template>
  <div class="ele-exception ele-text-center">
    <div class="ele-exception-img">
      <img src="@/assets/ic-403.svg" alt="" width="216px" height="250px">
    </div>
    <div class="ele-exception-content ele-text-left">
      <h1 class="ele-text">403</h1>
      <p class="ele-text-secondary">抱歉，你无权访问该页面</p>
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
  name: 'Exception403'
}
</script>
