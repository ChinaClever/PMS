<!-- 广告编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改广告':'添加广告'"
    :visible="visible"
    width="750px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="100px">
      <el-form-item label="广告图片：">
        <uploadImage :limit="1" v-model="form.cover"></uploadImage>
      </el-form-item>
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item label="广告标题:" prop="title">
            <el-input
              clearable
              :maxlength="20"
              v-model="form.title"
              placeholder="请输入广告标题"/>
          </el-form-item>
          <el-form-item label="广告URL:" prop="url">
            <el-input
              clearable
              :maxlength="20"
              v-model="form.url"
              placeholder="请输入广告URL"/>
          </el-form-item>
          <el-form-item label="广告宽度:" prop="width">
            <el-input-number
              :min="0"
              v-model="form.width"
              placeholder="请输入广告宽度"
              controls-position="right"
              class="ele-fluid ele-text-left"/>
          </el-form-item>
          <el-form-item label="开始时间:">
            <el-date-picker
              type="datetime"
              class="ele-fluid"
              v-model="form.start_time"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="请选择开始时间"/>
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
          <el-form-item label="广告类型:" prop="type">
            <el-select
              clearable
              class="ele-block"
              v-model="form.type"
              placeholder="请选择广告类型">
              <el-option label="图片" :value="1"/>
              <el-option label="文字" :value="2"/>
              <el-option label="视频" :value="3"/>
              <el-option label="推荐" :value="4"/>
            </el-select>
          </el-form-item>
          <el-form-item label="所属广告位:" prop="sort_id">
            <el-select
              filterable
              clearable
              v-model="form.sort_id"
              size="small"
              placeholder="-请选择所属广告位-"
              class="ele-block">
              <el-option v-for="item in sortList" :key="item.id" :label="item.description" :value="item.id"/>
            </el-select>
          </el-form-item>
          <el-form-item label="广告高度:" prop="height">
            <el-input-number
              :min="0"
              v-model="form.height"
              placeholder="请输入广告高度"
              controls-position="right"
              class="ele-fluid ele-text-left"/>
          </el-form-item>
          <el-form-item label="结束时间:">
            <el-date-picker
              type="datetime"
              class="ele-fluid"
              v-model="form.end_time"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="请选择结束时间"/>
          </el-form-item>
          <el-form-item label="广告状态:" prop="status">
            <el-radio-group
              v-model="form.status">
              <el-radio :label="1">正常</el-radio>
              <el-radio :label="2">禁用</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
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
import uploadImage from '@/components/uploadImage'

export default {
  name: 'AdEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 广告位列表
    sortList: Array
  },
  components: {uploadImage},
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1}, this.data),
      // 表单验证规则
      rules: {
        title: [
          {required: true, message: '请输入广告标题', trigger: 'blur'}
        ],
        type: [
          {required: true, message: '请选择广告类型', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择广告状态', trigger: 'blur'}
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
        this.form = Object.assign({}, this.data, {
          start_time: this.$util.toDateString(this.data.start_time),
          end_time: this.$util.toDateString(this.data.end_time),
        });
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/ad/update' : '/ad/add', this.form).then(res => {
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
