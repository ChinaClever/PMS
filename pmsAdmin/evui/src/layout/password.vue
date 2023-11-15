<!-- 修改密码弹窗 -->
<template>
  <el-dialog
    width="420px"
    title="修改密码"
    :visible="visible"
    :lock-scroll="false"
    :append-to-body="true"
    @update:visible="updateVisible"
    @closed="onClose">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px"
      @keyup.enter.native="save">
      <el-form-item label="旧密码:" prop="oldPassword">
        <el-input
          show-password
          v-model="form.oldPassword"
          placeholder="请输入旧密码"/>
      </el-form-item>
      <el-form-item label="新密码:" prop="newPassword">
        <el-input
          show-password
          v-model="form.newPassword"
          placeholder="请输入新密码"/>
      </el-form-item>
      <el-form-item label="确认密码:" prop="rePassword">
        <el-input
          show-password
          v-model="form.rePassword"
          placeholder="请再次输入新密码"/>
      </el-form-item>
    </el-form>
    <div slot="footer">
      <el-button @click="cancel">取消</el-button>
      <el-button type="primary" @click="save">确定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'UpdatePwd',
  props: {
    visible: Boolean
  },
  data() {
    return {
      // 表单数据
      form: {
        oldPassword: '',
        newPassword: '',
        rePassword: ''
      },
      // 表单验证
      rules: {
        oldPassword: [
          {required: true, message: '请输入旧密码', trigger: 'blur'}
        ],
        newPassword: [
          {required: true, message: '请输入新密码', trigger: 'blur'}
        ],
        rePassword: [
          {
            required: true,
            message: '请再次输入新密码',
            trigger: 'blur',
            validator: (rule, value, callback) => {
              if (!value) {
                return callback(new Error('请再次输入新密码'));
              } else if (value !== this.form.newPassword) {
                return callback(new Error('两次输入密码不一致'));
              }
              callback();
            }
          }
        ]
      },
      // 按钮loading
      loading: false
    };
  },
  methods: {
    /* 保存修改 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http.put('/index/updatePwd', this.form).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              this.cancel();
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch((e) => {
            this.loading = false;
            this.$message.error(e.message);
          });
        } else {
          return false;
        }
      });
    },
    /* 关闭回调 */
    onClose() {
      this.form = {};
      this.$refs['form'].resetFields();
      this.loading = false;
    },
    /* 取消 */
    cancel() {
      this.updateVisible(false);
    },
    /* 修改visible */
    updateVisible(value) {
      this.$emit('update:visible', value);
    }
  }
}
</script>
