<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改意见':'添加意见'"
    :visible="visible"
    width="1400px"
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
          <el-form-item 
            label="类型:" 
            ref="type"
            prop="type">
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
            ref="priority"
            prop="priority">
            <el-input
              :maxlength="20"
              v-model="form.priority"
              placeholder="请输入优先级(1-10)"
              clearable/>
          </el-form-item>
          <el-form-item 
            label="状态:"
            ref="status" 
            prop="status" 
            v-if="isUpdate && permission.includes('sys:feedback:status')">
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
      <br />
      <el-form-item
       label="需求或建议:"
       ref="content" 
       prop="content">
        <tinymce-editor 
          v-model="form.content" 
          :init="initEditor"/>
      </el-form-item>
      <el-form-item 
        label="反馈意见:" 
        prop="feedback" 
        v-if="isUpdate && permission.includes('sys:feedback:status')">
        <tinymce-editor 
          v-model="form.feedback" 
          :init="initEditor"/>
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
import TinymceEditor from '@/components/TinymceEditor';

export default {
  name: 'NoticeEdit',
  components: {TinymceEditor},
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
          {required: true,message: '请输入类型', trigger: 'blur'}
        ],
        status:[
          {required: true,message: '请选择一个状态', trigger: 'blur'}
        ],
        content: [
          {required: true, message: '请输入', trigger: 'blur'}
        ],
        priority:[
          {required: true, message: '请输入优先值', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue <= 0) {
                callback(new Error('数量必须为大于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
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
        this.form = {status : 1,type : 1};
        this.form.content = '';
        this.isUpdate = false;
      }
    }
  },
  computed: {
    ...mapGetters(["permission"]),
    // 初始化富文本
    initEditor() {
      return {
        height: 300,
        branding: false,
        skin_url: '/tinymce/skins/ui/oxide',
        content_css: '/tinymce/skins/content/default/content.css',
        language_url: '/tinymce/langs/zh_CN.js',
        language: 'zh_CN',
        plugins: 'code print preview fullscreen paste searchreplace save autosave link autolink image imagetools media table codesample lists advlist hr charmap emoticons anchor directionality pagebreak quickbars nonbreaking visualblocks visualchars wordcount',
        toolbar: 'fullscreen preview code | undo redo | forecolor backcolor | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | formatselect fontselect fontsizeselect | link image media emoticons charmap anchor pagebreak codesample | ltr rtl',
        toolbar_drawer: 'sliding',
        images_upload_handler: (blobInfo, success, error) => {
          let file = blobInfo.blob();
          // 使用axios上传
          const formData = new FormData();
          formData.append('file', file, file.name);
          this.$http.post('/upload/uploadImage', formData).then(res => {
            if (res.data.code == 0) {
              success(res.data.data.fileUrl);
            } else {
              error(res.data.msg);
            }
          }).catch(e => {
            console.error(e);
            error(e.message);
          });
        },
        file_picker_types: 'media',
        file_picker_callback: () => {
        }
      }
    },
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid,object) => {
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
          let dom = this.$refs[Object.keys(object)[0]];
          if (Object.prototype.toString.call(dom) !== "[object Object]") {
            dom = dom[0];
          }
          // 定位代码
          dom.$el.scrollIntoView({
            block: "center",
            behavior: "smooth",
          });
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
