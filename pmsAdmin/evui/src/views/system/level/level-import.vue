<!-- 用户导入弹窗 -->
<template>
  <el-dialog
    width="480px"
    title="导入职级"
    :visible="visible"
    :lock-scroll="false"
    :destroy-on-close="true"
    @update:visible="updateVisible">
    <el-upload
      drag
      action=""
      class="ele-block"
      v-loading="loading"
      accept=".xls,.xlsx"
      :show-file-list="false"
      :before-upload="beforeUpload">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或 <em>点击上传</em></div>
      <div class="el-upload__tip ele-text-center" slot="tip">
        <span>只能上传xls、xlsx文件，</span>
        <el-link
          download
          @click="download()"
          type="primary"
          :underline="false"
          style="vertical-align: baseline;">下载模板
        </el-link>
      </div>
    </el-upload>
  </el-dialog>
</template>

<script>
export default {
  name: 'LevelImport',
  props: {
    // 是否打开弹窗
    visible: Boolean
  },
  data() {
    return {
      // 导入请求状态
      loading: false,
      // 导入模板下载地址
      // url: process.env.VUE_APP_API_BASE_URL + "/uploads/level.xlsx"
    };
  },
  methods: {
    // 下载模板
    download() {
      this.$http
        .get("/level/downloadExcel")
        .then((res) => {
          let data = res.data;
          if (data.code == 0) {
            // 下载文件
            window.location.href = data.data;
            this.$message({
              type: "success",
              message: "模板下载成功",
            });
          } else {
            this.$message.error("模板下载失败");
          }
        })
    },
    /* 上传 */
    beforeUpload(file) {
      this.loading = true;
      let formData = new FormData();
      formData.append('file', file);
      this.$http.post('/level/importExcel', formData).then(res => {
        this.loading = false;
        if (res.data.code === 0) {
          this.$message({type: 'success', message: res.data.msg});
          this.updateVisible(false);
          this.$emit('done');
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.loading = false;
        this.$message.error(e.message);
      });
      return false;
    },
    /* 更新visible */
    updateVisible(value) {
      this.$emit('update:visible', value);
    }
  }
}
</script>

<style scoped>
.ele-block ::v-deep .el-upload,
.ele-block ::v-deep .el-upload-dragger {
  width: 100%;
}
</style>
