<!-- 字典编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改字典':'添加字典'"
    :visible="visible"
    width="440px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      :model="form"
      ref="form"
      :rules="rules"
      label-width="82px">
      <el-form-item
        label="字典名称:"
        prop="name">
        <el-input
          :maxlength="20"
          v-model="form.name"
          placeholder="请输入字典名称"
          clearable/>
      </el-form-item>
      <el-form-item
        label="字典值:"
        prop="code">
        <el-input
          :maxlength="30"
          v-model="form.code"
          placeholder="请输入字典值"
          clearable/>
      </el-form-item>
      <el-form-item
        label="排序号:"
        prop="sort">
        <el-input-number
          v-model="form.sort"
          controls-position="right"
          :min="0"
          :max="9999"
          placeholder="请输入排序号"
          class="ele-fluid ele-text-left"/>
      </el-form-item>
      <el-form-item label="备注:">
        <el-input
          v-model="form.note"
          placeholder="请输入备注"
          :rows="3"
          :maxlength="200"
          type="textarea"/>
      </el-form-item>
    </el-form>
    <div slot="footer">
      <el-button
        @click="updateVisible(false)">取消
      </el-button>
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
  name: 'DictEdit',
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
        name: [
          {required: true, message: '请输入字典名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入字典值', trigger: 'blur'}
        ],
        sort: [
          {required: true, message: '请输入排序号', trigger: 'blur'}
        ]
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/dict/update' : '/dict/add', this.form).then(res => {
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
