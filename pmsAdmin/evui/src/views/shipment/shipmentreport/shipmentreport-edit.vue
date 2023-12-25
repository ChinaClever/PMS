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
            label="单号:"
            prop="work_order">
            <el-input
              v-model="form.work_order"
              placeholder="请输入单号"
              @keyup.enter.native="handleEnterKey"
              clearable>
              <el-tooltip slot="prefix" effect="dark" placement="top">
                <i class="el-icon-question"></i>
                <div slot="content">
                  智能填入步骤：<br>
                  1. 点击单号输入框<br>
                  2. 输入法切换至英文大写<br>
                  3. 使用扫码枪扫码<br>
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
        <el-col :span="8">
          <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
       </el-col>
       <el-col :span="5">
        <el-form-item label="优先级:" prop="priority">
          <el-select v-model="form.priority" placeholder="">
            <el-option
              v-for="item in priorityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-col>
        <el-col :span="11">
          <el-form-item label="数量:" prop="product_count">
          <el-input-number
            :min="0"
            :step="50"
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
          <el-form-item label="SO/RQ号:" prop="SO_RQ_id">
            <el-input
              v-model="form.SO_RQ_id"
              placeholder="请输入SO/RQ号"
              clearable/>
          </el-form-item>
      </el-col>
        </el-row>
        <el-row :gutter="6">
          <el-col :span="12">
            <el-form-item label="交货日期:" prop="delivery_date">
              <el-date-picker
                type="date"
                class="ele-fluid"
                v-model="form.delivery_date"
                value-format="yyyy-MM-dd"
                placeholder="请选择交货日期"/>
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
        </el-row>
        <el-row :gutter="6">
    </el-row>
    <el-row><el-divider content-position="center" style="color: #000;">完成各模块所需天数</el-divider></el-row>
    <el-row>
      <el-col :span="6">
        <el-form-item label="烧录：" prop="burning_duration_days">
          <el-input-number
            :min="1"
            v-model="form.burning_duration_days"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="调试:" prop="debug_duration_days">
          <el-input-number
            :min="1"
            v-model="form.debug_duration_days"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="质检:" prop="inspect_duration_days">
          <el-input-number
            :min="1"
            v-model="form.inspect_duration_days"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="维修:" prop="repair_duration_days">
          <el-input-number
            :min="1"
            v-model="form.repair_duration_days"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row><el-divider></el-divider></el-row>

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
            {required: true, message: '请输入单号', trigger: 'blur'},
            { validator: (rule, value, callback) => this.checkWorkOrderId(rule, value, callback)}
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
            { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback)}
          ],
          finish_date: [
            { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback)}
          ],
          SO_RQ_id: [
            {required: true, message: '请选择SO/RQ号', trigger: 'blur'}
          ],
          product_module: [
            {required: true, message: '请选择成品/模块', trigger: 'blur'}
          ],
          priority:[
            {required: true, message: '选择优先级', trigger: 'blur'}
          ],
          burning_duration_days: [
            {required: true, message: '输入烧录所需天数', trigger: 'blur'},
            { validator: this.validateDurationDays }
          ],
          debug_duration_days: [
            {required: true, message: '输入调试所需天数', trigger: 'blur'},
            { validator: this.validateDurationDays }
          ],
          inspect_duration_days: [
            {required: true, message: '输入质检所需天数', trigger: 'blur'},
            { validator: this.validateDurationDays}
          ],
          repair_duration_days: [
            {required: true, message: '输入维修所需天数', trigger: 'blur'},
            { validator: this.validateDurationDays}
          ],
        },
        // 提交状态
        loading: false,
        // 是否是修改
        isUpdate: false,
        // 需要删除的文件
        deleteFileList: [],
        // 优先级选项
        priorityOptions: [{
          value: 1,
          label: '低'
        }, {
          value: 2,
          label: '中'
        }, {
          value: 3,
          label: '高'
        }],
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
        }else{
          this.loadAll();
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
      // 天数检测
      validateDurationDays(rule, value, callback) {
        const currentDate = new Date();
        const deliveryDate = new Date(this.form.delivery_date);
        const durationDays = Math.ceil((deliveryDate - currentDate) / (1000 * 60 * 60 * 24));

        if (value > durationDays) {
          callback(new Error('所需天数超过剩余天数'));
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
        this.deleteFileList.push(file.uid)
      },
      // 单号按回车键
      handleEnterKey(event){
        console.log(event)
        this.$refs.form.validateField('work_order', () => {});
      },
      // 文件上传超过数量
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制上传 5 个文件，已选择了 ${fileList.length} 个文件`);
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

