<!-- 职级编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改产品名称':'添加产品名称'"
      :visible="visible"
      width="800px"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="100px">
        <el-row :gutter="6">
        <el-col :span="12">
          <el-form-item
          label="成品编码:"
          prop="product_code">
          <el-input
            v-model="form.product_code"
            placeholder="请输入成品编码"
            clearable/>
        </el-form-item>
      </el-col>
        <el-col :span="12">
          <el-form-item
          label="产品名称:"
          prop="product_name">
          <el-input
            v-model="form.product_name"
            placeholder="请输入产品名称"
            clearable/>
        </el-form-item>
        </el-col>
        </el-row>
      
        <el-form-item
          label="规格型号:"
          prop="shape">
          <el-input
            :maxlength="20"
            v-model="form.shape"
            placeholder="请输入规格型号"
            clearable/>
        </el-form-item>

        <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
  
      </el-form>
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
    name: 'WeldingEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        // 表单数据
        form: Object.assign({}, this.data),
        // 表单验证规则
        rules: {
          product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
          shape: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
          product_code: [
          {required: true, message: '请输入成品编码', trigger: 'blur'}
        ],
          product_module: [
          {required: true, message: '请选择成品/模块', trigger: 'blur'}
        ],
        },
        // 提交状态
        loading: false,
        // 是否是修改
        isUpdate: false
      };
    },
    watch: {
      data() {
        if (this.data && this.data.id) {
          this.form = Object.assign({}, this.data);
          this.isUpdate = true;
        } else {
          this.form = {};
          this.isUpdate = false;
        }
      }
    },
    methods: {
      /* 保存编辑 */
      save() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.loading = true;
            this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/shipmentreport/productname/update' : '/shipmentreport/productname/add', this.form).then(res => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
                if (!this.isUpdate) {
                  this.form = {};
                }
                this.updateVisible(false);
                this.$emit('done');
              } else {
                this.$message.error(res.data.msg);
              }
            }).catch(e => {
              this.loading = false;
              this.$message.error(e.message);
            });
          } else {
            return false;
          }
        });
      },
      /* 更新visible */
      updateVisible(value) {
        this.$emit('update:visible', value);
      },
     
    },
   
  }
  </script>

  <style scoped>
  .el-row {
    margin-bottom: 16px;

  }
  </style>

