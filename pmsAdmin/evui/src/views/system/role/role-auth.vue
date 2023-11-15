<!-- 角色权限分配弹窗 -->
<template>
  <el-dialog
    title="分配权限"
    :visible="visible"
    width="440px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-scrollbar
      v-loading="authLoading"
      style="height: 50vh;"
      wrapStyle="overflow-x: hidden;">
      <el-tree
        ref="tree"
        :data="authData"
        :props="{label: 'title'}"
        node-key="id"
        :default-expand-all="true"
        :default-checked-keys="checked"
        show-checkbox>
        <span slot-scope="{ data }">
          <i :class="data.icon"></i>
          <span> {{ data.title }}</span>
        </span>
      </el-tree>
    </el-scrollbar>
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
  name: 'RoleAuth',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 当前角色数据
    data: Object
  },
  data() {
    return {
      // 权限数据
      authData: [],
      // 权限数据请求状态
      authLoading: false,
      // 提交状态
      loading: false
    };
  },
  computed: {
    // 权限树选中数据
    checked() {
      let checked = [];
      this.$util.eachTreeData(this.authData, d => {
        if (d.checked && (!d.children || !d.children.length)) {
          checked.push(d.id);
        }
      });
      return checked;
    }
  },
  watch: {
    visible() {
      if (this.visible) {
        this.query();
      }
    }
  },
  methods: {
    /* 查询权限数据 */
    query() {
      this.authData = [];
      if (!this.data) return;
      this.authLoading = true;
      this.$http.get('/rolemenu/index/' + this.data.id).then(res => {
        this.authLoading = false;
        if (res.data.code === 0) {
          this.authData = this.$util.toTreeData(res.data.data, 'id', 'parentId');
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.authLoading = false;
        this.$message.error(e.message);
      });
    },
    /* 保存权限分配 */
    save() {
      this.loading = true;
      let ids = this.$refs.tree.getCheckedKeys().concat(this.$refs.tree.getHalfCheckedKeys());
      this.$http.post('/rolemenu/save', {roleId: this.data.id, menuIds: ids}).then(res => {
        this.loading = false;
        if (res.data.code === 0) {
          this.$message.success(res.data.msg);
          this.updateVisible(false);
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.loading = false;
        this.$message.error(e.message);
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
