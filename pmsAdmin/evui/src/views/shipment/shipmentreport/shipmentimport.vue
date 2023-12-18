<!-- 职级编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改排期表单':'添加排期表单'"
      :visible="visible"
      width="800px"
      top="5vh"
      :destroy-on-close="true"
      :lock-scroll="false"
      @import:visible="importVisible">
    
      <div slot="footer">
        <el-button @click="updateVisible(false)">取消</el-button>
        <el-button
          type="primary"
          @click="save"
          :loading="loading">保存
        </el-button>
      </div>
    </el-dialog>
  </template>

  <script>
  export default {
    name: 'ShipmentReportEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        // 提交状态
        loading: false,
      };
    },
   
    methods: {
     
 

    },
  }
  </script>

  <style scoped>
   
  </style>

