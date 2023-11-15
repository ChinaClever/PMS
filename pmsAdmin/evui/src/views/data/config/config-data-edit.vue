<!-- 配置项编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改配置项':'添加配置项'"
    :visible="visible"
    width="700px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      :model="form"
      ref="form"
      :rules="rules"
      label-width="96px">
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item
            label="配置项标题:"
            prop="title">
            <el-input
              :maxlength="20"
              v-model="form.title"
              placeholder="请输入配置项标题"
              clearable/>
          </el-form-item>
          <el-form-item
            label="配置项编码:"
            prop="code">
            <el-input
              :maxlength="20"
              v-model="form.code"
              placeholder="请输入配置项编码"
              clearable/>
          </el-form-item>
          <el-form-item label="状态:" prop="status">
            <el-radio-group
              v-model="form.status">
              <el-radio :label="1">在用</el-radio>
              <el-radio :label="2">停用</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item label="配置类型:" prop="type">
            <el-select
              clearable
              class="ele-block"
              v-model="form.type"
              placeholder="请选择配置类型">
              <el-option label="只读文本" value="readonly"/>
              <el-option label="数字" value="number"/>
              <el-option label="单行文本" value="text"/>
              <el-option label="多行文本" value="textarea"/>
              <el-option label="数组" value="array"/>
              <el-option label="密码" value="password"/>
              <el-option label="单选框" value="radio"/>
              <el-option label="复选框" value="checkbox"/>
              <el-option label="下拉框" value="select"/>
              <el-option label="字体图标" value="icon"/>
              <el-option label="日期" value="date"/>
              <el-option label="时间" value="datetime"/>
              <el-option label="单张图片" value="image"/>
              <el-option label="多张图片" value="images"/>
              <el-option label="单个文件" value="file"/>
              <el-option label="多个文件" value="files"/>
              <el-option label="富文本编辑器" value="ueditor"/>
            </el-select>
          </el-form-item>
          <el-form-item
            label="配置项值:"
            prop="value">
            <el-input
              :maxlength="20"
              v-model="form.value"
              placeholder="请输入配置项值"
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
        </el-col>
      </el-row>
      <el-row :gutter="15">
        <el-form-item label="配置选项:">
          <el-input
            v-model="form.options"
            placeholder="请输入配置选项"
            :rows="3"
            :maxlength="200"
            type="textarea"/>
        </el-form-item>
      </el-row>
      <el-row :gutter="15">
        <el-form-item label="配置项备注:">
          <el-input
            v-model="form.note"
            placeholder="请输入配置项备注"
            :rows="3"
            :maxlength="200"
            type="textarea"/>
        </el-form-item>
      </el-row>
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
  name: 'ConfigDataEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 配置id
    configId: Number
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        name: [
          {required: true, message: '请输入配置项名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入配置项值', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择配置项状态', trigger: 'blur'}
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
          if (!this.isUpdate) {
            this.form.config_id = this.configId
          }
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/configdata/update' : '/configdata/add', this.form).then(res => {
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
