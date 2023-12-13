<!-- 职级编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改排期表单':'添加排期表单'"
      :visible="visible"
      width="800px"
      top="5vh"
      :destroy-on-close="true"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        enctype="multipart/form-data"
        :model="form"
        :rules="rules"
        label-width="86px"
        :validate-on-rule-change="false">
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item
          label="工单号:"
          prop="work_order">
          <el-input
            v-model="form.work_order"
            placeholder="请输入工单号"
            @keyup.enter.native="handleEnterKey"
            clearable>
            <el-tooltip slot="prefix" effect="dark" placement="top">
              <i class="el-icon-question"></i>
              <div slot="content">
                智能填入步骤：<br>
                1. 光标放在工单号输入框内<br>
                2. 输入法切换至英文大写<br>
                3. 使用扫码枪扫码<br>
                4. 点击表单内任意空白处
              </div>
            </el-tooltip>
          </el-input>
        </el-form-item>
        </el-col>
        <el-col :span="12">
        <el-form-item
          label="客户名称:"
          prop="client_name">
          <el-input
            v-model="form.client_name"
            placeholder="请输入客户名称"
            clearable/>
        </el-form-item>
        </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item
          label="成品编码:"
          prop="product_code">
          <el-input
            v-model="form.product_code"
            placeholder="请输入成品编码"
            clearable
            />
        </el-form-item>
      </el-col>
        <el-col :span="12">
        <el-form-item label="产品名称:" prop="product_name">
        <el-autocomplete
          v-model="form.product_name"
          :fetch-suggestions="querySearchAsync"
          placeholder="请输入产品名称"
          clearable
          @select="handleSelect"
          style="width: 277px;"
        ></el-autocomplete>
        </el-form-item>
        </el-col>
        </el-row>

        <el-form-item label="规格型号:" prop="shape">
          <el-input
            v-model="form.shape"
            placeholder="请输入规格型号"
            clearable/>
        </el-form-item>
        <el-row :gutter="6">
        <el-col :span="12">
          <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
       </el-col>
        <el-col :span="12">
          <el-form-item label="数量:" prop="product_count">
          <el-input-number
            :min="0"
            v-model="form.product_count"
            placeholder="请输入数量"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
       
      </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item label="订单日期:" prop="order_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.order_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择订单日期"/>
        </el-form-item>
        </el-col>
        <el-col :span="12">
        <el-form-item label="交货日期:" prop="delivery_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.delivery_date"
              value-format="yyyy-MM-dd"
              :disabled="isUpdate"
              placeholder="请选择交货日期"/>
        </el-form-item>
      </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
          <el-form-item label="更改日期:" prop="update_delivery_date" v-if="isUpdate">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.update_delivery_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择更改日期"/>
        </el-form-item>
      </el-col>
        <el-col :span="12">
          <el-form-item label="完成日期:" prop="finish_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.finish_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择完成日期"/>
        </el-form-item>
       
      </el-col>
      <el-col :span="12">
       <el-form-item label="SO/RQ号:" prop="SO_RQ_id">
          <el-input
            v-model="form.SO_RQ_id"
            placeholder="请输入SO/RQ号"
            clearable/>
        </el-form-item>
      </el-col>
        </el-row>
       
          <el-form-item label="备注:" prop="remark">
            <el-input
              clearable
              :rows="3"
              type="textarea"
              :maxlength="200"
              v-model="form.remark"
              placeholder="请输入备注"/>
          </el-form-item>

          <el-form-item label="附件:" prop="attachment">
            <el-upload
              class="upload-demo"
              ref="upload"
              :auto-upload="false"
              :file-list="fileList"
              :on-change="onChange"
              :on-remove="onRemove"
              :limit="10"
              action=""
              multiple
              drag>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">支持多文件上传,单个文件大小不能超过100MB</div>
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
    name: 'ShipmentReportEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        fileList: [],
        product_names: [],
        state: '',
        timeout:  null,
        // 表单数据
        form: Object.assign({product_code: '', product_name:'', shape:'', product_module:''}, this.data),
        // 表单验证规则
        rules: {
          work_order: [
          {required: true, message: '请输入工单号', trigger: 'blur'},
          { validator: (rule, value, callback) => this.checkWorkOrderId(rule, value, callback), trigger: 'blur' }
        ],
        client_name: [
          {required: true, message: '请选择客户名称', trigger: 'blur'}
        ],
        product_code: [
          {required: true, message: '请输入成品编码', trigger: 'blur'}
        ],
        product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        shape: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
        product_count: [
          {required: true, message: '请输入数量', trigger: 'blur'}
        ],
        order_date: [
          {required: true, message: '请选择订单日期', trigger: 'blur'}
        ],
        delivery_date: [
          {required: true, message: '请选择交货日期', trigger: 'blur'},
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        update_delivery_date: [
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        finish_date: [
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        SO_RQ_id: [
          {required: true, message: '请选择SO/RQ号', trigger: 'blur'}
        ],
        product_module: [
          {required: true, message: '请选择成品/模块', trigger: 'blur'}
        ],
        },
        // 提交状态
        loading: false,
        // 是否是修改
        isUpdate: false,
        // 需要删除的文件
        deleteFileList: [],
      };
    },
    watch: {
      data() {
        if (this.data && this.data.id) {
          this.form = Object.assign({}, this.data);
          this.fileList = [];
           // 遍历文件名列表，为每个文件名创建一个文件对象
           if (this.data.fileNameList != null){
             this.data.fileNameList.forEach((fileName, index) => {
            const file = {
              name: fileName,
              uid: `file-${index}`, 
              status: 'success', 
              url: '' 
              };
              this.fileList.push(file); 
            });
           }
         
          this.isUpdate = true;
        } else {
          this.form = {product_code: '', product_name:'', shape:'', product_module:''};
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

            // 遍历键，并将数据添加到新的 FormData 对象中
            keys.forEach(key => {
              if (Object.hasOwnProperty.call(this.form, key)) {
                formData.append(key, this.form[key]);
              }
            });
          
            this.loading = true       
            this.$http['post'](this.isUpdate ? '/shipmentreport/update' : '/shipmentreport/add', formData).then(res => {
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
          }else {
            return false;
          }
        });
      },

      /* 更新visible */
      updateVisible(value) {
        this.$emit('update:visible', value);
      },
       // 订单号自动填入数据
      checkWorkOrderId(rule, value, callback){
        const regex = /^[a-zA-Z0-9]+[+][a-zA-Z0-9]+$/;
        const regex1 = /^[a-zA-Z0-9]+$/;
        if (value.includes("+")) {
          if (regex.test(value)) {
            const parts = value.split("+");
            this.form.work_order = parts[0];
            this.form.product_code = parts[1];
            //根据产品编码查产品名称 规格
            this.$http.get('/shipmentreport/product/detail/' + this.form.product_code).then((res) => {
            this.loading = false;
            if (res.data.code === 0 && res.data.data != null) {
             this.form.product_name = res.data.data.product_name
             this.form.shape  = res.data.data.shape
             this.form.product_module = res.data.data.product_module
            } 
            })
            callback();
          } else {
             callback(new Error('存在除一个+号外的非法字符')); 
        }
        }else {
          if (!regex1.test(value)) {
            callback(new Error('存在非法字符')); 
          }

          callback();
        }
      },

       // 检测填入日期是否晚于订单日期
      checkFinishTime(rule, value, callback) {
        const orderDate = this.form.order_date;
        const thisDate = value;
        if (!orderDate || !thisDate) {
          callback();
        } else if (orderDate > thisDate) {
          callback(new Error('此日期必须晚于订单日期'));
        } else {
          callback();
        }
      },

      // 加载全部产品名
      loadAll() {
        this.$http.get('/shipmentreport/product/list').then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.product_names = res.data.data
            } 
          })
      },

      // 异步查询产品名称
      querySearchAsync(queryString, cb) {
        var product_names = this.product_names;
        var results = queryString ? product_names.filter(this.createStateFilter(queryString)) : product_names;

        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          cb(results);
        }, 300 * Math.random());
      },
      createStateFilter(queryString) {
        return (state) => {
          return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },

      // 选择产品名
      handleSelect(item) {
        this.form.product_name = item.value
        this.$refs.form.validateField('product_name', () => {});
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
      this.deleteFileList.push(file.name)
      console.log(this.deleteFileList)
      },

      handleEnterKey(event){
        console.log(event)
        this.$refs.form.validateField('work_order', () => {});
    },

    },

    mounted() {
      // 加载全部产品名
      this.loadAll();
      

    }
  }
  </script>

  <style scoped>
   .el-row {
    margin-bottom: 16px;

  }
  </style>

