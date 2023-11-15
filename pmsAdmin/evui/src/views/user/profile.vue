<template>
  <div class="ele-body">
    <el-row :gutter="15">
      <el-col :md="6" :sm="8">
        <el-card shadow="never" body-style="padding: 25px;">
          <div class="user-info-card">
            <!-- 头像上传 -->
            <uploadImage :limit="1" v-model="form.avatar" style="left: 0px"></uploadImage>
            <h2 class="user-info-name">一米阳光</h2>
            <div class="user-info-desc">
              打造一款基于Python语言的敏捷开发框架，用先进的技术思维和软件框架产品赋能开发者、助力企业发展，为企业提供全方位的解决方案！
            </div>
          </div>
          <div class="user-info-list">
            <div class="user-info-item">
              <i class="el-icon-user"></i>
              <span>资深架构师</span>
            </div>
            <div class="user-info-item">
              <i class="el-icon-user"></i>
              <span>北京DjangoAdmin研发中心</span>
            </div>
            <div class="user-info-item">
              <i class="el-icon-location-information"></i>
              <span>中国 • 北京市 • 朝阳区</span>
            </div>
            <div class="user-info-item">
              <i class="el-icon-_school"></i>
              <span>Python、Django、Vue、ElementUI、AntDesign</span>
            </div>
          </div>
          <div style="margin: 30px 0 20px 0;">
            <el-divider class="ele-divider-dashed ele-divider-base"/>
          </div>
          <h6 class="ele-text" style="margin-bottom: 8px;">标签</h6>
          <div class="user-info-tags">
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
            <el-tag size="mini" type="info">一米阳光</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :md="18" :sm="16">
        <el-card shadow="never" body-style="padding-top: 5px;">
          <el-tabs v-model="active" class="user-info-tabs">
            <el-tab-pane label="基本信息" name="info">
              <el-form
                ref="infoForm"
                :model="form"
                :rules="rules"
                label-width="90px"
                style="max-width: 450px;padding-top: 40px;"
                @keyup.enter.native="save"
                @submit.native.prevent>
                <el-form-item label="姓名:" prop="realname">
                  <el-input
                    v-model="form.realname"
                    placeholder="请输入姓名"
                    clearable/>
                </el-form-item>
                <el-form-item label="昵称:" prop="nickname">
                  <el-input
                    v-model="form.nickname"
                    placeholder="请输入昵称"
                    clearable/>
                </el-form-item>
                <el-form-item label="性别:" prop="gender">
                  <el-select
                    v-model="form.gender"
                    placeholder="请选择性别"
                    class="ele-fluid"
                    clearable>
                    <el-option label="男" :value="1"/>
                    <el-option label="女" :value="2"/>
                    <el-option label="保密" :value="3"/>
                  </el-select>
                </el-form-item>
                <el-form-item label="联系方式:" prop="mobile">
                  <el-input
                    v-model="form.mobile"
                    placeholder="请输入联系方式"
                    clearable/>
                </el-form-item>
                <el-form-item label="邮箱:" prop="email">
                  <el-input
                    v-model="form.email"
                    placeholder="请输入邮箱"
                    clearable/>
                </el-form-item>
                <el-form-item label="详细地址:">
                  <el-input
                    v-model="form.address"
                    placeholder="请输入详细地址"
                    clearable/>
                </el-form-item>
                <el-form-item label="个人简介:">
                  <el-input
                    v-model="form.intro"
                    placeholder="请输入个人简介"
                    :rows="4"
                    type="textarea"/>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    @click="save"
                    :loading="loading">保存更改
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
    <!-- 头像裁剪弹窗 -->
    <ele-cropper-dialog
      :show.sync="showCropper"
      @crop="onCrop"
      :src="form.avatar"
      :lock-scroll="false"/>
  </div>
</template>

<script>
import EleCropperDialog from 'ele-admin/packages/ele-cropper-dialog';
import setting from '@/config/setting';
import uploadImage from '@/components/uploadImage'

export default {
  name: 'UserInfo',
  components: {EleCropperDialog, uploadImage},
  data() {
    return {
      // tab页选中
      active: 'info',
      // 表单数据
      form: {},
      // 表单验证规则
      rules: {
        realname: [
          {required: true, message: '请输入姓名', trigger: 'blur'}
        ],
        nickname: [
          {required: true, message: '请输入昵称', trigger: 'blur'}
        ],
        gender: [
          {required: true, message: '请选择性别', trigger: 'blur'}
        ],
        email: [
          {required: true, message: '请输入邮箱', trigger: 'blur'}
        ]
      },
      // 保存按钮loading
      loading: false,
      // 是否显示裁剪弹窗
      showCropper: false
    };
  },
  mounted() {
    // 获取用户信息
    this.getUserInfo();
  },
  methods: {
    /* 获取当前用户信息 */
    getUserInfo() {
      if (setting.userUrl) {
        this.$http.get(setting.userUrl).then((res) => {
          const result = setting.parseUser ? setting.parseUser(res.data) : res.data;
          if (result.code === 0) {
            // 赋予对象值
            var formData = JSON.parse(JSON.stringify(result.data))
            this.form = Object.assign({
              realname: formData.realname,
              nickname: formData.nickname,
              gender: formData.gender,
              mobile: formData.mobile,
              email: formData.email,
              address: formData.address,
              intro: formData.intro,
              avatar: formData.avatar
            });
          } else {
            this.$message.error(result.msg);
          }
        }).catch((e) => {
          console.error(e);
          this.$message.error(e.message);
        });
      }
    },
    /* 保存更改 */
    save() {
      this.$refs['infoForm'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http.put('/index/userInfo', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success('保存成功');
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
    /* 头像裁剪完成回调 */
    onCrop(res) {
      this.form.avatar = res;
      this.showCropper = false;
      this.$store.dispatch('user/setUser', Object.assign({}, this.$store.state.user.user, {
        avatar: res
      }));
    }
  }
}
</script>

<style scoped>
.ele-body {
  padding-bottom: 0;
}

.el-card {
  margin-bottom: 15px;
}

/* 用户资料卡片 */
.user-info-card {
  padding-top: 8px;
  text-align: center;
}

.user-info-card .user-info-avatar-group {
  position: relative;
  cursor: pointer;
  margin: 0 auto;
  width: 110px;
  height: 110px;
  border-radius: 50%;
  overflow: hidden;
}

.user-info-card .user-info-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info-card .user-info-avatar-group > i {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #FFF;
  font-size: 30px;
  display: none;
  z-index: 2;
}

.user-info-card .user-info-avatar-group:hover > i {
  display: block;
}

.user-info-card .user-info-avatar-group:hover:after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .3);
}

.user-info-card .user-info-name {
  font-size: 24px;
  margin-top: 20px;
}

.user-info-card .user-info-desc {
  margin-top: 8px;
}

/* 用户信息列表 */
.user-info-list {
  margin-top: 30px;
}

.user-info-list .user-info-item {
  margin-bottom: 10px;
  display: flex;
  align-items: baseline;
}

.user-info-item > i {
  margin-right: 10px;
  font-size: 16px;
}

.user-info-item > span {
  flex: 1;
  display: block;
}

/* 用户标签 */
.user-info-tags .el-tag {
  margin: 10px 10px 0 0;
}

/* 用户账号绑定列表 */
.user-account-list {
  margin-top: 10px;
}

.user-account-list .user-account-item {
  padding: 15px;
}

.user-account-list .user-account-item .ele-text-secondary {
  margin-top: 6px;
}

.user-account-list .user-account-item .user-account-icon {
  width: 42px;
  height: 42px;
  line-height: 42px;
  text-align: center;
  color: #FFF;
  font-size: 26px;
  border-radius: 50%;
  background-color: #3492ED;
  box-sizing: border-box;
}

.user-account-list .user-account-item .user-account-icon.el-icon-_wechat {
  background-color: #4DAF29;
  font-size: 28px;
}

.user-account-list .user-account-item .user-account-icon.el-icon-_alipay {
  background-color: #1476FE;
  padding-left: 5px;
  font-size: 32px;
}

/* tab页签 */
.user-info-tabs ::v-deep .el-tabs__nav-wrap {
  padding-left: 20px;
}
</style>
