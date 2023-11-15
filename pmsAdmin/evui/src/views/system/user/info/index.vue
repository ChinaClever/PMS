<template>
  <div class="ele-body">
    <el-card shadow="never" header="基本信息">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="82px">
        <el-form-item label="头像：">
          <uploadImage :limit="1" v-model="form.avatar"></uploadImage>
        </el-form-item>
        <el-row :gutter="15">
          <el-col :sm="12">
            <el-form-item label="用户姓名:" prop="realname">
              <el-input
                clearable
                :maxlength="20"
                v-model="form.realname"
                placeholder="请输入用户姓名"/>
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
            <el-form-item label="邮箱:" prop="email">
              <el-input
                clearable
                :maxlength="100"
                v-model="form.email"
                placeholder="请输入邮箱"/>
            </el-form-item>
            <el-form-item label="职级：" prop="level_id">
              <el-select
                filterable
                clearable
                v-model="form.level_id"
                size="small"
                placeholder="-请选择职级-"
                class="ele-block">
                <el-option v-for="item in levelList" :key="item.id" :label="item.name" :value="item.id"/>
              </el-select>
            </el-form-item>
            <el-form-item label="所属部门:" prop="dept_id">
              <treeselect
                v-model="form.dept_id"
                :options="deptList"
                placeholder="请选择所属部门"
                :defaultExpandLevel="3"
                :normalizer="(d)=>{return { id: d.id, label: d.name,children:d.children||undefined }}"/>
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
            <el-form-item label="排序号:" prop="sort">
              <el-input-number
                :min="0"
                v-model="form.sort"
                placeholder="请输入排序号"
                controls-position="right"
                class="ele-fluid ele-text-left"/>
            </el-form-item>
          </el-col>
          <el-col :sm="12">
            <el-form-item label="用户昵称:" prop="nickname">
              <el-input
                clearable
                :maxlength="20"
                v-model="form.nickname"
                placeholder="请输入用户昵称"/>
            </el-form-item>
            <el-form-item label="出生日期:" prop="birthday">
              <el-date-picker
                type="date"
                class="ele-fluid"
                v-model="form.birthday"
                value-format="yyyy-MM-dd"
                placeholder="请选择出生日期"/>
            </el-form-item>
            <el-form-item label="手机号:" prop="mobile">
              <el-input
                clearable
                :maxlength="11"
                v-model="form.mobile"
                placeholder="请输入手机号"/>
            </el-form-item>
            <el-form-item label="岗位：" prop="position_id">
              <el-select
                filterable
                clearable
                v-model="form.position_id"
                size="small"
                placeholder="-请选择岗位-"
                class="ele-block">
                <el-option v-for="item in positionList" :key="item.id" :label="item.name" :value="item.id"/>
              </el-select>
            </el-form-item>
            <el-form-item label="状态:" prop="status">
              <el-radio-group
                v-model="form.status">
                <el-radio :label="1">在用</el-radio>
                <el-radio :label="2">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="详细地址:" prop="address">
              <el-input
                clearable
                :maxlength="150"
                v-model="form.address"
                placeholder="请输入详细地址"/>
            </el-form-item>
            <el-form-item label="角色:" prop="roles">
              <el-select
                multiple
                clearable
                class="ele-block"
                v-model="form.roles"
                placeholder="请选择角色">
                <el-option
                  v-for="item in roleList"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"/>
              </el-select>
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
        <el-form-item>
          <el-button
            type="primary"
            @click="save"
            :loading="loading">保存更改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import {setPageTab} from '@/utils/page-tab-util';
import validate from 'ele-admin/packages/validate';
import uploadImage from '@/components/uploadImage'
import Treeselect from '@riophae/vue-treeselect' // 下拉树
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import regions from '@/assets/regions.js'

export default {
  name: 'SystemUserInfo',
  data() {
    return {
      // 省市区数据
      regions: regions,
      // 选中的省市区
      // city: [],
      // 选中的省市
      provinceCity: [],
      // 选中的省
      province: [],
      // 表单数据
      form: {},
      // 表单验证规则
      rules: {
        realname: [
          {required: true, message: '请输入用户姓名', trigger: 'blur'}
        ],
        nickname: [
          {required: true, message: '请输入用户名', trigger: 'blur'}
        ],
        gender: [
          {required: true, message: '请选择性别', trigger: 'blur'}
        ],
        birthday: [
          {required: true, message: '请选择出生日期', trigger: 'blur'}
        ],
        level_id: [
          {required: true, message: '请选择职级', trigger: 'blur'}
        ],
        position_id: [
          {required: true, message: '请选择岗位', trigger: 'blur'}
        ],
        dept_id: [
          {required: true, message: '请选择部门', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择状态', trigger: 'blur'}
        ],
        city: [
          {required: true, message: '请选择省市区', trigger: 'blur'}
        ],
        sort: [
          {required: true, message: '请输入排序号', trigger: 'blur'}
        ],
        roles: [
          {required: true, message: '请选择角色', trigger: 'blur'}
        ],
        email: [
          {pattern: validate.email, message: '邮箱格式不正确', trigger: 'blur'}
        ],
        password: [
          {required: true, pattern: /^[\S]{5,18}$/, message: '密码必须为5-18位非空白字符', trigger: 'blur'}
        ],
        mobile: [
          {pattern: validate.phone, message: '手机号格式不正确', trigger: 'blur'}
        ]
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 角色列表
      roleList: [],
      // 职级列表
      levelList: [],
      // 岗位列表
      positionList: [],
      // 部门列表
      deptList: [],
    };
  },
  components: {uploadImage, Treeselect},
  mounted() {
    this.query(this.$route.query.id);
    this.queryRoles();  // 查询角色列表
    this.getLevelList(); // 查询职级列表
    this.getPositionList(); // 查询岗位列表
    this.getDeptList(); // 查询部门列表
  },
  methods: {
    /* 查询用户信息 */
    query(id) {
      if (!id) {
        return;
      }
      this.loading = true;
      this.$http.get('/user/detail/' + id).then((res) => {
        this.loading = false;
        if (res.data.code === 0) {
          this.form = Object.assign({}, res.data.data, {
            // birthday: this.$util.toDateString(res.data.data.birthday)
          });
          this.isUpdate = true;
          // 修改页签标题
          setPageTab({
            fullPath: this.$route.fullPath,
            title: this.form.realname + '的详情'
          });
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch((e) => {
        this.loading = false;
        this.$message.error(e.message);
      });
    },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/user/update' : '/user/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message({type: 'success', message: res.data.msg});
              if (!this.isUpdate) {
                this.form = {};
              }
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
    /* 查询角色列表 */
    queryRoles() {
      this.$http.get('/role/getRoleList').then(res => {
        if (res.data.code === 0) {
          this.roleList = res.data.data;
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    },
    /**
     * 获取职级列表
     */
    getLevelList() {
      this.$http.get('/level/getLevelList').then(res => {
        if (res.data.code === 0) {
          this.levelList = res.data.data;
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    },
    /**
     * 获取岗位列表
     */
    getPositionList() {
      this.$http.get('/position/getPositionList').then(res => {
        if (res.data.code === 0) {
          this.positionList = res.data.data;
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    },
    /**
     * 获取部门列表
     */
    getDeptList() {
      this.$http.get('/dept/getDeptList').then(res => {
        if (res.data.code === 0) {
          this.deptList = this.$util.toTreeData(res.data.data, 'id', 'pid');
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    }
  },
  watch: {
    $route() {
      this.query(this.$route.query.id);
    }
  }
}
</script>

<style scoped>
</style>
