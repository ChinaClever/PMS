<!-- 编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改调试数据':'添加调试数据'"
    :visible="visible"
    width="650px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="120px">
      <el-form-item label="成品序列号:" prop="key">
        <el-input
          v-model="form.key"
          placeholder="序列号"
          clearable/>
      </el-form-item>
        <div v-for="(input) in form.module" :key="input.no">
          <span>模块 {{ input.no }}</span>
          <el-input v-model="input.key" placeholder="序列号"></el-input>
        </div>
        
        <el-button @click="addInput">添加输入框</el-button>
        <el-button v-if="form.module.length > 0" @click="removeInput">删除最后一个输入框</el-button>
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
  name: 'DebugDataEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({module:[]}, this.data),
      // 表单验证规则
      rules: {
        key: [
        {required: true, message: '请输入单号', trigger: 'blur'},
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      idCounter: 1 // 输入框id计数器
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.isUpdate = true;
      } else {
        this.form = {module : []};
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/bind/update' : '/bind/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {module:[]};
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
      while(this.form.module.length > 0){
        this.removeInput();
      }
    },
    /* 更新visible */
    updateVisible(value) {
      this.$emit('update:visible', value);
    },

    addInput() {
      this.form.module.push({
        no: this.idCounter,
        key: '',
      });
      this.idCounter++;
    },
    removeInput() {
      this.form.module.pop();
      if (this.form.module.length === 0) {
        this.idCounter = 1; // 如果没有输入框了，重置计数器为1
      } else {
        this.idCounter = this.form.module[this.form.module.length - 1].id + 1; // 更新计数器为最后一个输入框的id加1
      }
    }
  }
}
</script>

<style scoped>
</style>

