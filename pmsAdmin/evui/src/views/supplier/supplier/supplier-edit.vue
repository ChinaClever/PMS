<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改':'添加'"
    :visible="visible"
    width="460px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-form-item
        label="工单号"
        prop="order_id">
        <el-input
          :maxlength="20"
          v-model="form.work_order"
          placeholder="请输入工单号"
          clearable/>
      </el-form-item>

      <el-form-item
        label="客户:"
        prop="customer">
        <el-input
          :maxlength="20"
          v-model="form.customer"
          placeholder="请输入客户"
          clearable/>
      </el-form-item>

      <el-form-item
        label="产品:"
        prop="product_name">
        <el-input
          :maxlength="20"
          v-model="form.product_name"
          placeholder="请输入产品"
          clearable/>
      </el-form-item>
      <el-form-item
        label="产品类型:"
        prop="product_type">
        <el-input
          :maxlength="20"
          v-model="form.product_type"
          placeholder="请输入产品类型"
          clearable/>
      </el-form-item>
      <el-form-item
        label="供应商:"
        prop="supplier">
        <el-input
          :maxlength="20"
          v-model="form.supplier"
          placeholder="请输入供应商"
          clearable/>
      </el-form-item>
      <el-form-item
        label="部件:"
        prop="parts">
        <el-input
          :maxlength="20"
          v-model="form.parts"
          placeholder="请输入部件"
          clearable/>
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
  name: 'LevelEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1}, this.data),
      // 表单验证规则
      rules: {
        /*name: [
          {required: true, message: '请输入职级名称', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择职级状态', trigger: 'blur'}
        ],
        sort: [
          {required: true, message: '请输入排序号', trigger: 'blur'}
        ],*/
        order_id: [
          {required: true, message: '请输入工单号', trigger: 'blur'}
        ],
        customer: [
          {required: true, message: '请输入客户', trigger: 'blur'}
        ],
        product_name: [
          {required: true, message: '请输入产品', trigger: 'blur'}
        ],
        product_type: [
          {required: true, message: '请输入产品类型', trigger: 'blur'}
        ],
        supplier: [
          {required: true, message: '请输入供应商', trigger: 'blur'}
        ],
        parts: [
          {required: true, message: '请输入部件', trigger: 'blur'}
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/supplier/update' : '/supplier/add', this.form).then(res => {
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
    }
  }
}
</script>

<style scoped>
</style>
