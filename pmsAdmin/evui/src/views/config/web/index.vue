<template>
  <div class="ele-body">
    <el-card shadow="never" body-style="padding-top: 5px;">
      <el-tabs v-model="active" @tab-click="handleClick">
        <el-tab-pane v-for="(item,index) in config_list" :key="index" :label="item.config_name" :name="'tab_'+index"
                     style="margin: 20px auto;">
          <el-form :model="form" ref="form" label-width="150px" v-for="(subItem,val) in item.data_list" :key="val">
            <!-- 单行文本框 -->
            <el-form-item v-if="subItem.type=='text'" :label="subItem.title+':'" :prop="subItem.code">
              <el-input v-model="form[subItem.code]" :placeholder="'请输入'+subItem.title" clearable/>
            </el-form-item>
            <!-- 多行文本框 -->
            <el-form-item v-if="subItem.type=='textarea'" :label="subItem.title+':'" :prop="subItem.code">
              <el-input v-model="form[subItem.code]" :placeholder="'请输入'+subItem.title" :rows="3" type="textarea"/>
            </el-form-item>
            <!-- 单图上传 -->
            <el-form-item v-if="subItem.type=='image'" :label="subItem.title+':'">
              <uploadImage :limit="1" v-model="form[subItem.code]"></uploadImage>
            </el-form-item>
            <!-- 多图上传 -->
            <el-form-item v-if="subItem.type=='images'" :label="subItem.title+':'">
              <uploadImage :limit="10" v-model="form[subItem.code]"></uploadImage>
            </el-form-item>
            <!-- 日期选择 -->
            <el-form-item v-if="subItem.type=='date'" :label="subItem.title+':'" :prop="subItem.code">
              <el-date-picker
                v-model="form[subItem.code]"
                type="date"
                :placeholder="'请选择'+subItem.title"
                size="small"
                value-format="yyyy-MM-dd"
                format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
            <!-- 日期时间选择 -->
            <el-form-item v-if="subItem.type=='datetime'" :label="subItem.title+':'" :prop="subItem.code">
              <el-date-picker
                v-model="form[subItem.code]"
                type="datetime"
                :placeholder="'请选择'+subItem.title"
                size="small"
                value-format="yyyy-MM-dd HH:mm:ss"
                format="yyyy-MM-dd HH:mm:ss">
              </el-date-picker>
            </el-form-item>
            <!-- 单选按钮 -->
            <el-form-item v-if="subItem.type=='radio'" :label="subItem.title+':'">
              <el-radio-group v-model="form[subItem.code]">
                <el-radio v-for="(val,key) in subItem.optionsList" :label="key" :key="val">{{ val }}</el-radio>
              </el-radio-group>
            </el-form-item>
            <!-- 数字输入框 -->
            <el-form-item v-if="subItem.type=='number'" :label="subItem.title+':'" :prop="subItem.code">
              <el-input-number v-model="form[subItem.code]" controls-position="right" :min="0"
                               :placeholder="'请输入'+subItem.title" class="ele-fluid ele-text-left"/>
            </el-form-item>
            <!-- 密码输入框 -->
            <el-form-item v-if="subItem.type=='password'" :label="subItem.title+':'" :prop="subItem.code">
              <el-input v-model="form[subItem.code]" :placeholder="'请输入'+subItem.title" show-password/>
            </el-form-item>
            <!-- 复选框 -->
            <el-form-item v-if="subItem.type=='checkbox'" :label="subItem.title+':'" :prop="subItem.code">
              <el-checkbox-group v-model="form[subItem.code]">
                <el-checkbox v-for="(val,key) in subItem.optionsList" :label="key" :key="val">{{ val }}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <!-- 下拉单选框 -->
            <el-form-item v-if="subItem.type=='select'" :label="subItem.title+':'" :prop="subItem.code">
              <el-select v-model="form[subItem.code]" :placeholder="'请选择'+subItem.title" class="ele-block" clearable>
                <el-option v-for="(val,key) in subItem.optionsList" :label="val" :value="key" :key="key"/>
              </el-select>
            </el-form-item>
            <!-- 富文本编辑器 -->
            <el-form-item v-if="subItem.type=='ueditor'" :label="subItem.title+':'">
              <tinymce-editor v-model="form[subItem.code]" :init="initEditor"/>
            </el-form-item>
            <!-- 图标 -->
            <el-form-item v-if="subItem.type=='icon'" :label="subItem.title+':'">
              <ele-icon-picker v-model="form[subItem.code]" :placeholder="'请选择'+subItem.title"/>
            </el-form-item>
          </el-form>
          <div style="margin-left: 150px;">
            <el-button type="primary" @click="save" :loading="loading">保存更改</el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import uploadImage from '@/components/uploadImage'
import TinymceEditor from '@/components/TinymceEditor'

export default {
  name: "ConfigWeb",
  components: {uploadImage, TinymceEditor},
  data() {
    return {
      active: 'tab_0',  // tab页选中
      loading: false,  // 保存按钮loading
      form: {},  // 表单数据
      config_list: [],
    }
  },
  computed: {
    /**
     * 初始化编辑器
     */
    initEditor() {
      return {
        height: 400,
        file_picker_callback: this.file_picker_callback,
        skin_url: this.$store.state.theme.theme === 'dark' ? '/tinymce/skins/ui/oxide-dark' : '/tinymce/skins/ui/oxide',
        content_css: this.$store.state.theme.theme === 'dark' ? '/tinymce/skins/content/dark/content.css' : '/tinymce/skins/content/default/content.css',
        images_upload_handler: (blobInfo, success, error) => {
          let file = blobInfo.blob();
          // 使用axios上传
          const formData = new FormData();
          formData.append('file', file, file.name);
          this.$http.post('/upload/uploadImage', formData).then(res => {
            if (res.data.code == 0) {
              success(res.data.data);
            } else {
              error(res.data.msg);
            }
          }).catch(e => {
            console.error(e);
            error(e.message);
          });
        }
      };
    }
  },
  mounted() {
    this.getConfigInfo();
  },
  methods: {
    // 获取配置信息
    getConfigInfo() {
      this.$http.get('/configweb/index').then(res => {
        if (res.data.code === 0) {
          this.config_list = res.data.data;
          if (this.config_list.length > 0) {
            let data_list = this.config_list[0]['data_list'];
            let itemArr = {};
            data_list.forEach(item => {
              itemArr[item.code] = item.value;
            })
            this.form = itemArr;
          } else {
            this.form = {};
          }
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    },
    /* 保存更改 */
    save() {
      this.loading = true;
      this.$http.put('/configweb/save', this.form).then(res => {
        this.loading = false;
        if (res.data.code === 0) {
          this.$message.success(res.data.msg);
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.loading = false;
        this.$message.error(e.message);
      });
    },
    /**
     * Tab点击事件
     * @param tab
     * @param event
     */
    handleClick(tab, event) {
      console.log(tab, event);
      let data_list = this.config_list[tab.index]['data_list'];
      let itemArr = {};
      data_list.forEach(item => {
        itemArr[item.code] = item.value;
        console.log(item.code + " " + item.value)
      })
      this.form = itemArr;
    }
  }
}
</script>
