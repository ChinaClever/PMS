<!-- 广告位编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改广告位':'添加广告位'"
    :visible="visible"
    width="460px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="100px">
      <el-form-item
        label="广告位描述:"
        prop="description">
        <el-input
          :maxlength="20"
          v-model="form.description"
          placeholder="请输入广告位描述"
          clearable/>
      </el-form-item>
      <el-form-item label="广告位位置:" prop="loc_id">
        <el-input-number
          :min="0"
          v-model="form.loc_id"
          placeholder="请输入广告位位置"
          controls-position="right"
          class="ele-fluid ele-text-left"/>
      </el-form-item>
      <el-form-item label="投放平台:" prop="platform">
        <el-select
          clearable
          class="ele-block"
          v-model="form.platform"
          placeholder="请选择投放平台">
          <el-option label="PC站" :value="1"/>
          <el-option label="WAP站" :value="2"/>
          <el-option label="微信小程序" :value="3"/>
          <el-option label="APP应用" :value="4"/>
        </el-select>
      </el-form-item>
      <el-form-item label="所属栏目:">
        <treeselect
          :options="cateList"
          v-model="form.cate_id"
          :defaultExpandLevel="3"
          :normalizer="normalizer"
          placeholder="请选择所属栏目"/>
      </el-form-item>
      <el-form-item label="排序号:" prop="sort">
        <el-input-number
          :min="0"
          v-model="form.sort"
          placeholder="请输入排序号"
          controls-position="right"
          class="ele-fluid ele-text-left"/>
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
import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

export default {
  name: 'AdSortEdit',
  components: {Treeselect},
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 栏目数据
    cateList: Array
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1}, this.data),
      // 表单验证规则
      rules: {
        description: [
          {required: true, message: '请输入广告位描述', trigger: 'blur'}
        ],
        loc_id: [
          {required: true, message: '请选择广告位状态', trigger: 'blur'}
        ],
        platform: [
          {required: true, message: '请选择投放平台', trigger: 'blur'}
        ],
        cate_id: [
          {required: true, message: '请选择所属栏目', trigger: 'blur'}
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
    /* 下拉树格式化 */
    normalizer(d) {
      return {
        id: d.id,
        label: d.name,
        children: d.children || undefined
      };
    },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/adsort/update' : '/adsort/add', this.form).then(res => {
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
