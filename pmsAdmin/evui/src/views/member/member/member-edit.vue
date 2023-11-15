<!-- 会员编辑弹窗 -->
<template>
  <el-dialog
    width="750px"
    :visible="visible"
    :lock-scroll="false"
    :destroy-on-close="true"
    custom-class="ele-dialog-form"
    :title="isUpdate?'修改会员':'添加会员'"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-form-item label="会员头像：">
        <uploadImage :limit="1" v-model="form.avatar"></uploadImage>
      </el-form-item>
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item label="会员姓名:" prop="realname">
            <el-input
              clearable
              :maxlength="150"
              v-model="form.realname"
              placeholder="请输入会员姓名"/>
          </el-form-item>
          <el-form-item label="性别:" prop="gender">
            <el-select
              clearable
              class="ele-block"
              v-model="form.gender"
              placeholder="请选择性别">
              <el-option label="男" :value="1"/>
              <el-option label="女" :value="2"/>
              <el-option label="保密" :value="3"/>
            </el-select>
          </el-form-item>
          <el-form-item label="电子邮箱:" prop="email">
            <el-input
              clearable
              :maxlength="150"
              v-model="form.email"
              placeholder="请输入电子邮箱"/>
          </el-form-item>
          <el-form-item label="所在城市:" prop="city">
            <el-cascader
              clearable
              v-model="form.city"
              class="ele-fluid"
              placeholder="请选择省市区"
              :options="regions.cityData"
              popper-class="ele-pop-wrap-higher"/>
          </el-form-item>
          <el-form-item label="会员等级:" prop="member_level">
            <el-select
              filterable
              clearable
              v-model="form.member_level"
              size="small"
              placeholder="-请选择会员等级-"
              class="ele-block">
              <el-option v-for="item in memberLevelList" :key="item.id" :label="item.name" :value="item.id"/>
            </el-select>
          </el-form-item>
          <el-form-item label="会员账号:" prop="username">
            <el-input
              clearable
              :maxlength="150"
              :disabled="isUpdate"
              v-model="form.username"
              placeholder="请输入会员账号"/>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item label="会员昵称:" prop="nickname">
            <el-input
              clearable
              :maxlength="150"
              v-model="form.nickname"
              placeholder="请输入会员昵称"/>
          </el-form-item>
          <el-form-item label="出生日期:" prop="birthday">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.birthday"
              value-format="yyyy-MM-dd"
              placeholder="请选择出生日期"/>
          </el-form-item>
          <el-form-item label="会员来源:" prop="source">
            <el-select
              clearable
              class="ele-block"
              v-model="form.source"
              placeholder="请选择会员来源">
              <el-option label="APP注册" :value="1"/>
              <el-option label="小程序注册" :value="2"/>
              <el-option label="网站注册" :value="3"/>
              <el-option label="WAP站注册" :value="4"/>
              <el-option label="马甲会员" :value="5"/>
            </el-select>
          </el-form-item>
          <el-form-item label="详细地址:" prop="address">
            <el-input
              clearable
              :maxlength="150"
              v-model="form.address"
              placeholder="请输入详细地址"/>
          </el-form-item>
          <el-form-item label="状态:" prop="status">
            <el-radio-group
              v-model="form.status">
              <el-radio :label="1">在用</el-radio>
              <el-radio :label="2">禁用</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item
            label="登录密码:"
            prop="password">
            <el-input
              show-password
              :maxlength="150"
              v-model="form.password"
              placeholder="请输入登录密码"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="个人简介:">
        <el-input
          :rows="3"
          clearable
          type="textarea"
          :maxlength="200"
          v-model="form.intro"
          placeholder="请输入个人简介"/>
      </el-form-item>
      <el-form-item label="个人签名:">
        <el-input
          :rows="3"
          clearable
          type="textarea"
          :maxlength="200"
          v-model="form.signature"
          placeholder="请输入个人签名"/>
      </el-form-item>
    </el-form>
    <div slot="footer">
      <el-button
        @click="updateVisible(false)">取消
      </el-button>
      <el-button
        type="primary"
        :loading="loading"
        @click="save">保存
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import uploadImage from '@/components/uploadImage'
import regions from '@/assets/regions.js'

export default {
  name: 'MemberEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  components: {uploadImage},
  data() {
    return {
      // 省市区数据
      regions: regions,
      // 表单数据
      form: Object.assign({status: 1, gender: 1}, this.data),
      // 表单验证规则
      rules: {
        // username: [
        //   {
        //     required: true,
        //     type: 'string',
        //     trigger: 'blur',
        //     validator: (rule, value, callback) => {
        //       if (!value) {
        //         return callback(new Error('请输入会员账号'));
        //       }
        //       this.$http.get('/member/checkUser?username=' + value).then(res => {
        //         if (res.data.code !== 0 || !res.data.data.length) {
        //           return callback();
        //         }
        //         if (this.isUpdate && res.data.data[0].username === this.data.username) {
        //           return callback();
        //         }
        //         callback(new Error('账号已经存在'));
        //       }).catch(() => {
        //         callback();
        //       });
        //     }
        //   }
        // ],
        realname: [
          {required: true, message: '请输入会员姓名', trigger: 'blur'}
        ],
        nickname: [
          {required: true, message: '请输入会员名', trigger: 'blur'}
        ],
        gender: [
          {required: true, message: '请选择性别', trigger: 'blur'}
        ],
        birthday: [
          {required: true, message: '请选择出生日期', trigger: 'blur'}
        ],
        source: [
          {required: true, message: '请选择注册来源', trigger: 'blur'}
        ],
        city: [
          {required: true, message: '请选择省市区', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择状态', trigger: 'blur'}
        ],
        member_level: [
          {required: true, message: '请选择会员等级', trigger: 'blur'}
        ],
        // password: [
        //   {required: true, pattern: /^[\S]{5,18}$/, message: '密码必须为5-18位非空白字符', trigger: 'blur'}
        // ]
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 会员等级列表
      memberLevelList: [],
    };
  },
  watch: {
    data() {
      if (this.data) {
        this.form = Object.assign({}, this.data, {
          // birthday: this.$util.toDateString(this.data.birthday)
        });
        // 清空密码输入框
        this.form.password = ''
        this.isUpdate = true;
      } else {
        this.form = {};
        this.isUpdate = false;
        // 清空省市区控件
        this.form.city = [];
      }
    }
  },
  mounted() {
    // 获取职级列表
    this.getMemberLevelList();
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/member/update' : '/member/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message({type: 'success', message: res.data.msg});
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
    /**
     * 获取会员等级列表
     */
    getMemberLevelList() {
      this.$http.get('/memberlevel/getMemberLevelList').then(res => {
        if (res.data.code === 0) {
          this.memberLevelList = res.data.data;
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    }
  }
}
</script>

<style scoped>
</style>
