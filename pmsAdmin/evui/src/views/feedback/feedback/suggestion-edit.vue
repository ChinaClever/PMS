<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改意见':'添加意见'"
    :visible="visible"
    width="1100px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item
            label="提交者:"
            prop="commit_user">
            <el-input
              :maxlength="20"
              v-model="form.commit_user"
              placeholder="请输入您的姓名"
              clearable/>
          </el-form-item>
          <el-form-item label="类型:" prop="type">
            <el-radio-group
              v-model="form.type">
              <el-radio :label="1">问题</el-radio>
              <el-radio :label="2">建议</el-radio>
              <el-radio :label="3">新需求</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item
            label="优先级:"
            prop="priority">
            <el-input
              :maxlength="20"
              v-model="form.priority"
              placeholder="请输入优先级(1-10)"
              clearable/>
          </el-form-item>
          <el-form-item label="状态:" prop="status" v-if="permission.includes('sys:feedback:status')">
            <el-radio-group
              v-model="form.status" >
              <el-radio :label="1">未查看</el-radio>
              <el-radio :label="2">确认</el-radio>
              <el-radio :label="3">完成</el-radio>
              <el-radio :label="4">未通过</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="需求或建议:" prop="content">
                  <el-input
                    v-model="form.content"
                    :rows="4"
                    maxlength="200"
                    show-word-limit
                    type="textarea"/>
        </el-form-item>
      <el-form-item label="反馈意见:" prop="feedback" v-if="permission.includes('sys:feedback:status')">
                  <el-input
                    v-model="form.feedback"
                    :rows="4"
                    maxlength="200"
                    show-word-limit
                    type="textarea"/>
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
import { mapGetters } from "vuex";

export default {
  name: 'NoticeEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1,type : 1}, this.data),
      // 表单验证规则
      rules: {
        type:[
          {required: true, trigger: 'blur'}
        ],
        status:[
          {required: true, trigger: 'blur'}
        ],
        content: [
          {required: true, message: '请输入', trigger: 'blur'}
        ],
        priority:[
          {required: true, message: '请输入优先值', trigger: 'blur'}
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
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
  computed: {
    ...mapGetters(["permission"]),
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/suggestion/update' : '/suggestion/add', this.form).then(res => {
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
