<!-- 编辑弹窗 -->
<template>
  <el-dialog
    width="750px"
    :visible="visible"
    :lock-scroll="false"
    :destroy-on-close="true"
    custom-class="ele-dialog-form"
    :title="isUpdate?'修改栏目':'添加栏目'"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="92px"
      @keyup.enter.native="save"
      @submit.native.prevent>
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item label="栏目名称:" prop="name">
            <el-input
              clearable
              v-model="form.name"
              placeholder="请输入栏目名称"/>
          </el-form-item>
          <el-form-item label="拼音(全):" prop="pinyin">
            <el-input
              clearable
              v-model="form.pinyin"
              placeholder="请输入拼音全拼"/>
          </el-form-item>
          <el-form-item label="所属站点:" prop="item_id">
            <el-select
              filterable
              clearable
              v-model="form.item_id"
              size="small"
              placeholder="-请选择所属站点-"
              class="ele-block">
              <el-option v-for="item in itemList" :key="item.id" :label="item.name" :value="item.id"/>
            </el-select>
          </el-form-item>
          <el-form-item label="栏目状态:" prop="status">
            <el-radio-group
              v-model="form.status">
              <el-radio :label="1">在用</el-radio>
              <el-radio :label="2">停用</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item label="上级栏目:">
            <treeselect
              :options="cateList"
              v-model="form.pid"
              :defaultExpandLevel="3"
              :normalizer="normalizer"
              placeholder="请选择上级栏目"/>
          </el-form-item>
          <el-form-item label="拼音(简):" prop="code">
            <el-input
              clearable
              v-model="form.code"
              placeholder="请输入拼音简拼"/>
          </el-form-item>
          <el-form-item label="排序号:" prop="sort">
            <el-input-number
              :min="0"
              v-model="form.sort"
              placeholder="请输入排序号"
              controls-position="right"
              class="ele-fluid ele-text-left"/>
          </el-form-item>
          <el-form-item label="有无封面:" prop="is_cover">
            <el-radio-group
              v-model="form.is_cover"
              @change="onis_coverChange">
              <el-radio :label="1">有封面</el-radio>
              <el-radio :label="2">无封面</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item
        label="栏目封面:"
        v-if="form.is_cover === 1">
        <uploadImage :limit="1" v-model="form.cover"></uploadImage>
      </el-form-item>
      <el-form-item label="备注:">
        <el-input
          :rows="4"
          clearable
          type="textarea"
          :maxlength="200"
          v-model="form.note"
          placeholder="请输入备注"/>
      </el-form-item>
    </el-form>
    <div slot="footer">
      <el-button @click="updateVisible(false)">取消</el-button>
      <el-button
        type="primary"
        :loading="loading"
        @click="save">保存
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';
import uploadImage from '@/components/uploadImage'

export default {
  name: 'DeptEdit',
  components: {Treeselect, uploadImage},
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 全部栏目数据
    cateList: Array
  },
  data() {
    return {
      // 表单数据
      form: this.initFormData(this.data),
      // 表单验证规则
      rules: {
        name: [
          {required: true, message: '请输入栏目名称', trigger: 'blur'}
        ],
        pinyin: [
          {required: true, message: '请输入拼音(全拼)', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入拼音(简拼)', trigger: 'blur'}
        ],
        item_id: [
          {required: true, message: '请选择所属站点', trigger: 'blur'}
        ],
        is_cover: [
          {required: true, message: '请选择是否有封面', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择状态', trigger: 'blur'}
        ],
        sort: [
          {required: true, message: '请输入排序号', trigger: 'blur'}
        ]
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 站点列表
      itemList: [],
    };
  },
  watch: {
    data() {
      this.isUpdate = !!(this.data && this.data.id);
      this.form = this.initFormData(this.data);
    }
  },
  mounted() {
    // 获取站点列表
    this.getItemList();
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/itemcate/update' : '/itemcate/add', 
              Object.assign({}, this.form, {
                pid: this.form.pid || 0
              })
            ).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
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
    /* 初始化form数据 */
    initFormData(data) {
      // 初始化默认值
      let form = {status: 1, is_cover: 2};
      if (data) {
        Object.assign(form, data, {
          pid: data.pid === 0 ? null : data.pid,
        });
      }
      return form;
    },
    /* is_cover选择改变 */
    onis_coverChange() {
      console.log(this.form.is_cover)
      if (this.form.is_cover === 1) {
        this.form.is_cover = 1;
      } else {
        this.form.is_cover = 2;
      }
    },
    /**
     * 获取站点列表
     */
    getItemList() {
      this.$http.get('/item/getItemList').then(res => {
        if (res.data.code === 0) {
          this.itemList = res.data.data;
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
