<!-- 职级编辑弹窗 -->
<template>
    <el-dialog
      title="导入数据"
      :visible="visible"
      width="600px"
      top="5vh"
      :lock-scroll="false"
      @update:visible="updateVisible">

      <div style="height: 300px;">
        <el-steps direction="vertical">
          <el-step title="步骤 1  下载排期表单Excel模板" status="process" icon="el-icon-download" slot="description"> 
            <template slot="description">
              <!-- @click="downloadExcel" -->
              <el-button  class="ele-btn-icon" size="small">下载</el-button>
            </template>
          </el-step>
          <el-step title="步骤 2  在模板内填入想导入的数据" status="process" icon="el-icon-edit"></el-step>
          <el-step title="步骤 3  上传该Excel文件" status="process" icon="el-icon-upload"></el-step>
        </el-steps>
      </div>
    
      <div slot="footer">
        <el-button @click="updateVisible(false)">取消</el-button>
        <el-button
          type="primary"
          >保存
        </el-button>
      </div>
    </el-dialog>
  </template>

  <script>
  export default {
    name: 'ShipmentImport',
    props: {
      // 弹窗是否打开
      visible: Boolean
    },
    data() {
      return {
      };
    },
   
    methods: {
     /* 更新visible */
     updateVisible(value) {
        this.$emit('update:visible', value);
      },
    },
  }
  </script>

  <style scoped>
   
  </style>

