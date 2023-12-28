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
            <el-step title="步骤 1  下载排期表单Excel模板" status="process" icon="el-icon-download"> 
              <template slot="description">
                <br>
                <el-button class="ele-btn-icon" @click="downloadExcel">下载</el-button>
              </template>
            </el-step>
            <el-step title="步骤 2  在模板内填入想导入的数据" status="process" icon="el-icon-edit"></el-step>
            <el-step title="步骤 3  上传该Excel文件" status="process" icon="el-icon-upload">
              <template slot="description">
                <el-upload
                  class="upload-demo"
                  :action="uploadAction"
                  accept=".xls,.xlsx"     
                  :on-success="importFile"
                  :show-file-list="false">
                  <br>
                  <el-button size="small" type="primary">点击上传</el-button>
                </el-upload>
              </template>
            </el-step>
          </el-steps>
        </div>
    
      <div slot="footer">
        <el-button @click="updateVisible(false)">取消</el-button>
        <el-button type="primary">保存</el-button>
      </div>
    </el-dialog>
  </template>

  <script>
  import XLSX from 'xlsx';
  import { saveAs } from 'file-saver';
  export default {
    name: 'ShipmentImport',
    props: {
      // 弹窗是否打开
      visible: Boolean
    },
    data() {
      return {
        preUrl:process.env.VUE_APP_API_BASE_URL,
      };
    },
   
    methods: {
      /* 更新visible */
      updateVisible(value) {
        this.$emit('update:visible', value);
      },

      // 导入文件处理
      importFile(response) {
        if (response.data){
          this.$alert("单号"+response.data+"导入失败，原因可能是单号已存在或交货日期早于订单日期。", response.msg, {
            confirmButtonText: '确定',
          });
        }else{
          this.$message.success(response.msg);
        }
       
        this.updateVisible(false);
        this.$emit('done');

      },

      async downloadExcel() {
        const workbook = XLSX.utils.book_new();
        const header = [
          '优先级(高中低三选一)',
          '单号',
          '客户名称',
          '成品编码',
          '产品名称',
          '规格型号',
          '数量',
          '订单日期(例如:2023-12-25)',
          '交货日期(例如:2023-12-25)',
          '完成日期(例如:2023-12-25)',
          'SO/RQ号',
          '成品/模块',
          '备注',
          '烧录所需时间(单位:天)',
          '调试所需时间(单位:天)',
          '质检所需时间(单位:天)',
        ];
        // 创建一个空的数据数组
        const data = [];

        const worksheet = XLSX.utils.json_to_sheet(data);

        // 将字段名称添加到 Excel 文件中
        XLSX.utils.sheet_add_aoa(worksheet, [header], { origin: 'A1' });

        // 将工作表添加到工作簿中
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

        // 保存 Excel 文件
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
        const fileName = '排期表单模板.xlsx';

        saveAs(blob, fileName);
      }
    },

    computed: {
    uploadAction() {
      return `${this.preUrl}/shipmentreport/importfile`;
    },
    },
  }
  </script>

  <style scoped>
   
  </style>

