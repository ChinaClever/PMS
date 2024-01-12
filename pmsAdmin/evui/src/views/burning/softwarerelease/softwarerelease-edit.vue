<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改数据':'添加数据'"
    :visible="visible"
    width="800px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="132px">
      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="程序名称:"
        prop="name">
        <el-input
          :maxlength="255"
          v-model="form.name"
          placeholder="请输入程序名称"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="使用产品:"
        prop="products">
        <el-input
          :maxlength="255"
          v-model="form.products"
          placeholder="请输入使用产品"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="历史版本:"
        prop="history_version">
        <el-input
          :maxlength="255"
          v-model="form.history_version"
          placeholder="请输入历史版本"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="当前版本:"
        prop="version">
        <el-input
          :maxlength="255"
          v-model="form.version"
          placeholder="请输入程序要求"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-form-item
        label="修改日期:"
        prop="modify_time">
        <el-date-picker
              type="date"
              class="ele-fluid"
              :picker-options = 'pickerOptions'
              v-model="form.modify_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择修改日期"/>
      </el-form-item>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
      label="版本说明:"
        prop="version_explain">
        <el-input v-model="form.version_explain" placeholder="请选择或输入版本说明" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.version_explain" placeholder="请选择版本说明">
            <el-option label="公司标准" value="公司标准"/>
            <el-option label="特殊说明" value="特殊说明"/>
            <el-option label="版本升级" value="版本升级"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>
      
      <el-col :span="12">
      <el-form-item
        label="此次更新:"
        prop="updata">
        <el-input v-model="form.updata" placeholder="请选择或输入此次更新" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.updata" placeholder="请选择此次更新">
            <el-option label="立刻更新（所有在途订单需升级)" value="立刻更新（所有在途订单需升级)"/>
            <el-option label="正常更新（新订单需升级）" value="正常更新（新订单需升级）"/>
            <el-option label="临时更新（针对某一订单升级）" value="临时更新（针对某一订单升级）"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="烧录方法:"
        prop="burn_method">
        <el-input v-model="form.burn_method" placeholder="请选择或输入烧录方法" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.burn_method" placeholder="请选择烧录方法">
            <el-option label="未变更，与前一版本相同" value="未变更，与前一版本相同"/>
            <el-option label="已变更，见附件" value="已变更，见附件"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>
      
      <el-col :span="12">
      <el-form-item label="升级方法:">
        <el-input v-model="form.upgrade_method" placeholder="请选择或输入升级方法" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.upgrade_method" placeholder="请选择升级方法">
            <el-option label="未变更，与前一版本相同" value="未变更，与前一版本相同"/>
            <el-option label="已变更，见附件" value="已变更，见附件"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>
      </el-row>
      
      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item label="校准方法:">
      <el-input v-model="form.calibration_method" placeholder="请选择或输入校准方法" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.calibration_method" placeholder="请选择校准方法">
            <el-option label="未变更，与前一版本相同" value="未变更，与前一版本相同"/>
            <el-option label="已变更，见附件" value="已变更，见附件"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="用户手册:">
        <el-input v-model="form.User_Manual" placeholder="请选择或输入用户手册" class="ele-fluid">
        <template #prepend>
          <el-select v-model="form.User_Manual" placeholder="请选择用户手册">
            <el-option label="未变更，与前一版本相同" value="未变更，与前一版本相同"/>
            <el-option label="已变更，见附件" value="已变更，见附件"/>
          </el-select>
        </template>
      </el-input>
      </el-form-item>
      </el-col>
      </el-row>

      <el-form-item
        label="升级原因:"
        prop="upgrade_cause">
        <el-input
          :maxlength="255"
          v-model="form.upgrade_cause"
          placeholder="请输入升级原因"
          clearable/>
      </el-form-item>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="程序和文档公盘位置:"
        label-width="120px"
        prop="documentation_position">
         <el-input
          :rows="3"
          type="textarea"
          :maxlength="255"
          v-model="form.documentation_position"
          placeholder="请输入程序和文档公盘位置"
          clearable/> 
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="用户使用手册和协议公盘位置:"
        prop="User_Manual_position">
        <el-input
          :rows="3"
          type="textarea"
          :maxlength="255"
          v-model="form.User_Manual_position"
          placeholder="请输入用户使用手册和协议公盘位置"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      
      <el-form-item label="附件:" prop="attachment">
        <el-upload
          class="upload-demo"
          ref="upload"
          :auto-upload="false"
          :file-list="fileList"
          :on-change="onChange"
          :on-remove="onRemove"
          :on-exceed="handleExceed"
          :limit="5"
          action=""
          multiple
          drag
          >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">支持多文件上传,最多5个,单个文件大小不能超过100MB</div>
        </el-upload>
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
export default {
  name: 'softwarereleaseedit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 让时间可以选择今天昨天
      pickerOptions: {
          disabledDate() {
          },
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          },]
       },
    fileList: [],
    radio1: '公司标准',
    // 表单数据
    form: Object.assign({status: 1, other_explain: ''}, this.data),
      // 表单验证规则
      rules: {
        // name: [
        //   {required: true, message: '请输入程序名称', trigger: 'blur'}
        // ],
        // products: [
        //   {required: true, message: '请输入使用产品', trigger: 'blur'}
        // ],
        // history_version: [
        //   {required: true, message: '请输入历史版本', trigger: 'blur'}
        // ],
        // version: [
        //   {required: true, message: '请输入当前版本', trigger: 'blur'}
        // ],
       
        // modify_time: [
        //   {required: true, message: '请输入修改日期', trigger: 'blur'}
        // ],
        // version_explain: [
        //   {required: true, message: '请输入版本说明', trigger: 'blur'}
        // ],
        // updata: [
        //   {required: true, message: '请输入此次更新', trigger: 'blur'}
        // ],
        // burn_method: [
        //   {required: true, message: '请输入烧录方法', trigger: 'blur'}
        // ],
        // upgrade_method: [
        //   {required: true, message: '请输入升级方法', trigger: 'blur'}
        // ],
        // calibration_method :[
        //   {required: true, message: '请输入校准方法', trigger: 'blur'}
        // ],
        // User_Manual:[
        //   {required: true, message: '请输入用户手册', trigger: 'blur'}
        // ],
        //  upgrade_cause:[
        //   {required: true, message: '请输入升级原因', trigger: 'blur'}
        // ],
        
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
          this.fileList = [];
          // 遍历文件名列表，为每个文件名创建一个文件对象
          if  (this.data.attachmentList != null){
            this.data.attachmentList.forEach((attachment, index) => {
            const file = {
              name: this.data.fileNameList[index],
              uid: attachment, 
              status: 'success', 
              url: '' 
              };
              this.fileList.push(file); 
            });
          }
          // 优先级对应 
          this.isUpdate = true;
        } else { 
          this.isUpdate = false;
        }
      },
      visible(){
        if (this.visible == false){
          this.fileList = [];
          this.deleteFileList = [];
        }
    }
  },
  methods: {
  
  /* 保存编辑 */
  save() {
    this.$refs['form'].validate((valid) => {
      if (valid) {
        // 创建 formData 对象  加入需要删除的文件
        const formData = new FormData()
            if (this.deleteFileList != null){
              formData.append('deleteFileList',this.deleteFileList)
            }
        // 文件上传
        if (this.fileList.length != 0) {         
              this.fileList.forEach((file) => {
                if (file.status === 'success') {
                  // 文件已上传成功，不再重新上传
                  return;
                }
              formData.append('files', file.raw)
            }
          )}
        // 获取表单对象的键
        const keys = Object.keys(this.form);
          // 不写的话保存空的备份会显示null
          if (this.form.remark == null){
            this.form.remark = ''
          }
          // 遍历键，并将数据添加到新的 FormData 对象中
          keys.forEach(key => {
            if (Object.hasOwnProperty.call(this.form, key)) {
              formData.append(key, this.form[key]);
            }
          });

        // 发送请求进行保存操作
        this.loading = true;
        this.$http[this.isUpdate ? 'post' : 'post'](this.isUpdate ? '/softwarerelease/update' : '/softwarerelease/add', formData).then(res => {
          this.loading = false;
          if (res.data.code === 0) {
            this.$message.success(res.data.msg);
            if (!this.isUpdate) {
              this.form = {};
            }
            this.updateVisible(false);
            this.$emit('done');
            //清空fileList
            this.fileList = []
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
  // 文件自定义上传
  onChange(file, fileList) {
        if (file.size === 0) {
            this.$message.error('上传文件不存在').duration(3000);
            this.fileList = fileList.filter(item => item.uid !== file.uid)
            return
          }
        
          // 获取文件大小（单位：字节）
          const fileSize = file.size; 
          // 将文件大小转换为MB
          const fileSizeMB = Math.round(fileSize / (1024 * 1024));
          // 验证文件大小是否超过100MB
          if (fileSizeMB > 100) {
            this.$message.error('文件大小不能超过100MB').duration(3000);
            this.fileList = fileList.filter(item => item.uid !== file.uid)
            return
          }

        this.fileList = fileList
        },

  // 文件移除
  onRemove(file, fileList) {
    this.fileList = fileList.filter(item => item.uid !== file.uid)
    this.deleteFileList.push(file.uid)
  },
  // 文件上传超过数量
  handleExceed(files, fileList) {
    this.$message.warning(`当前限制上传 5 个文件，已选择了 ${fileList.length} 个文件`);
  },

  
}
}
</script>

<style scoped>
.el-row {
  margin-bottom: 16px;

}
</style>