<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改客户':'添加客户'"
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
        label="工单号:"
        prop="work_order">
        <el-input
          :maxlength="20"
          v-model="form.work_order"
          placeholder="请输入工单号"
          clearable/>
      </el-form-item>
      <el-form-item
        label="客户名称:"
        prop="name">
        <el-input
          :maxlength="20"
          v-model="form.name"
          placeholder="请输入客户名称"
          clearable/>
      </el-form-item>
      <el-form-item
        label="产品类型:"
        prop="code">
        <el-input
          :maxlength="20"
          v-model="form.code"
          placeholder="请输入产品类型"
          clearable/>
      </el-form-item>
      <el-form-item
        label="序列号:"
        prop="serial_id">
        <el-input
          :maxlength="20"
          v-model="form.serial_id"
          placeholder="请输入序列号"
          clearable/>
      </el-form-item>
      <el-form-item
        label="mac地址:"
        prop="mac_address">
        <el-input
          :maxlength="150"
          v-model="form.mac_address"
          placeholder="请输入mac地址"
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
  name: 'MacEdit',
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
        work_order: [
          {required: true, message: '请输入工单号', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入客户名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入产品型号', trigger: 'blur'}
        ],
        serial_id: [
          {required: true, message: '请输入序列号', trigger: 'blur'}
        ],
        mac_address: [
          {required: true, message: '请输入mac地址', trigger: 'blur'}
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/mac/update' : '/mac/add', this.form).then(res => {
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
