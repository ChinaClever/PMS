<!-- 职级编辑弹窗 -->
<template>
   <el-dialog
      :title="isUpdate?'修改打包记录':'添加打包记录'"
      :visible="visible"
      width="900px"
      top="5vh"
      :destroy-on-close="true"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        enctype="multipart/form-data"
        :model="form"
        :rules="rules"
        label-width="130px"
        :validate-on-rule-change="false">
        <el-row :gutter="6">
        <el-col :span="12" :pull="1">
          <el-form-item
          label="单号:" 
          prop="work_order">
            <el-autocomplete
              :disabled="isUpdate"
              v-model="form.work_order"
              :fetch-suggestions="querySearchAsync"
              @select="handleSelect"
              @clear="handleClear"
              @keyup.enter.native="handleEnterKey"
              placeholder="请输入单号"
              clearable
              style="width: 297px;"
            ></el-autocomplete>  
          </el-form-item>
        </el-col>
        <el-col :span="12" :pull="1">
          <el-form-item
            label="客户名称:"
            prop="client_name">
            <el-input
              :disabled="disabled"
              v-model="form.client_name"
              placeholder="请输入客户名称"
              clearable/>
          </el-form-item>
        </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12" :pull="1">
          <el-form-item
            label="成品编码:"
            prop="product_code">
            <el-input
              :disabled="disabled"
              v-model="form.product_code"
              placeholder="请输入成品编码"
              clearable
              />
          </el-form-item>
        </el-col>
        <el-col :span="12" :pull="1">
          <el-form-item label="产品名称:" prop="product_name">
              <el-input
                :disabled="disabled"
                v-model="form.product_name"
                placeholder="请输入产品名称"
                clearable/>
          </el-form-item>
        </el-col>
        </el-row>
        <el-row :gutter="6">
          <el-col :span="24" :pull="1">
            <el-form-item label="规格型号:" prop="shape">
              <el-input
                :disabled="disabled"
                v-model="form.shape"
                placeholder="请输入规格型号"
                clearable/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12" :pull="1">
          <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
             :disabled="disabled"
              v-model="form.product_module">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
       </el-col>
        <el-col :span="12" :pull="1">
          <el-form-item label="总数量:" prop="product_count">
          <el-input-number
            :disabled="disabled"
            :step="50"
            :min="0"
            v-model="form.product_count"
            placeholder="请输入总数量"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
       
      </el-col>
        </el-row>
        <el-row :gutter="6">
          <el-col :span="12" :pull="1">
            <el-form-item label="订单日期:" prop="order_date">
                <el-date-picker
                :disabled="disabled"
                  type="date"
                  class="ele-fluid"
                  v-model="form.order_date"
                  value-format="yyyy-MM-dd"
                  placeholder="请选择订单日期"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" :pull="1">
            <el-form-item label="交货日期:" prop="delivery_date">
                <el-date-picker
                  type="date"
                  class="ele-fluid"
                  v-model="form.delivery_date"
                  value-format="yyyy-MM-dd"
                  :disabled="disabled"
                  placeholder="请选择交货日期"/>
            </el-form-item>
          </el-col>
        </el-row>
      <el-row :gutter="6">
        <el-col :span="12" :pull="1">
          <el-form-item label="SO/RQ号:" prop="SO_RQ_id">
            <el-input
              :disabled="disabled"
              v-model="form.SO_RQ_id"
              placeholder="请输入SO/RQ号"
              clearable/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="6">
        <el-col :span="24" :pull="1">
          <el-form-item label="备注:" prop="remark">
            <el-input
              :disabled="disabled"
              clearable
              :rows="3"
              type="textarea"
              :maxlength="200"
              v-model="form.remark"
              placeholder="请输入备注"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="6">
        <el-col :span="24" :pull="1">
          <el-form-item label="打包完成时间:" prop="packing_finish_time">
            <el-date-picker
              type="datetime"
              class="ele-fluid"
              v-model="form.packing_finish_time"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="请选择打包完成时间"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="6">
        <el-col :span="12" :pull="1">
          <el-form-item label="工时:" prop="work_hours">
            <el-input-number
              :min="0"
              v-model="form.work_hours"
              placeholder="请输入所用工时(单位/小时):"
              controls-position="right"
              class="ele-fluid ele-text-left"/>
          </el-form-item>
        </el-col>
        <el-col :span="12" :pull="1">
          <el-form-item label="打包数量:" prop="packing_count">
            <el-input-number
              :min="0"
              :step="50"
              v-model="form.packing_count"
              placeholder="请输入打包数量"
              controls-position="right"
              class="ele-fluid ele-text-left"/>
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
  export default {
    name: 'PackingEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        // 表单数据
        form: Object.assign({}, this.data),
        // 表单验证规则
        rules: {
          packing_finish_time: [
            {required: true, message: '请选择打包完成时间', trigger: 'blur'}
          ],
          work_hours: [
            {required: true, message: '请输入工时', trigger: 'blur'},
            {validator: (rule, value, callback) => this.checkNumber(rule, value, callback)},
          ],
          packing_count: [
            {required: true, message: '请输入打包数量', trigger: 'blur'},
            {validator: (rule, value, callback) => this.checkNum(rule, value, callback)},
          ],
          work_order: [
            {validator: (rule, value, callback) => this.checkWorkOrderIsNull(rule, value, callback)},
            {required: true, message: '请输入单号', trigger: 'blur'}   
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
            {required: true, message: '请输入总数量', trigger: 'blur'},
            {validator: (rule, value, callback) => this.checkNumber(rule, value, callback)},
          ],
          order_date: [
            {required: true, message: '请选择订单日期', trigger: 'blur'}
          ],
          delivery_date: [
            {required: true, message: '请选择交货日期', trigger: 'blur'},
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
        // 是否禁用输入框
        disabled: false,
      };
    },
    watch: {
      data() {
        if (this.data && this.data.id) {
          this.form = Object.assign({}, this.data);
          this.isUpdate = true;
          this.disabled = true;
        } else {
          this.form = {};
          this.isUpdate = false;
    
        }
      },
      visible(){
        if (this.visible == false && this.isUpdate == true){
          this.disabled = false;
        }
      }
    },
    methods: {
      /* 保存编辑 */
      save() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.loading = true;
            this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/packing/update' : '/packing/add', this.form).then(res => {
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
      },
      loadAll() {
        this.$http.get('/shipmentreport/work_order/list').then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.work_orders = res.data.data
            } 
          })
      },
      // 异步查询单号
      querySearchAsync(queryString, cb) {
        var work_orders = this.work_orders;
        var filteredResults = queryString ? work_orders.filter(this.createStateFilter(queryString)) : work_orders;
        var results = filteredResults.slice(0, 10); // 限制结果最多显示10条

        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          cb(results);
        }, 300 * Math.random());
      },

      createStateFilter(queryString) {
        return (state) => {
          return (state.value.toLowerCase().includes(queryString.toLowerCase()));
        };
      },

      handleSelect(item) {
        this.form.work_order = item.value
        this.$refs.form.validateField('work_order', () => {});
        // 根据选择的单号查其他数据自动填入
        this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
            this.loading = false;
            const shipmentData = res.data.data;
            if (res.data.code === 0 && res.data.data != null) {
                this.form.product_code = shipmentData.product_code
                this.form.SO_RQ_id = shipmentData.SO_RQ_id
                this.form.product_module = shipmentData.product_module
                this.form.product_name = shipmentData.product_name
                this.form.client_name = shipmentData.client_name
                this.form.product_count = shipmentData.product_count
                this.form.order_date = shipmentData.order_date
                this.form.shape  = shipmentData.shape
                this.form.delivery_date = shipmentData.delivery_date
                this.form.remark = shipmentData.remark

                this.disabled = true;
              } 
            });
      },

      handleClear(){
        this.form = {};
        this.disabled = false;
      },

      handleEnterKey(event){
        this.form.work_order = event.target.value.split("+")[0];
        this.$refs.form.validateField('work_order', () => {});
        // 根据选择的单号查其他数据自动填入
        this.$http.get('/shipmentreport/detail/' + event.target.value.split("+")[0]).then((res) => {
          this.loading = false;
          const shipmentData = res.data.data;
          if (res.data.code === 0 && res.data.data != null) {
            this.form.product_code = shipmentData.product_code
            this.form.SO_RQ_id = shipmentData.SO_RQ_id
            this.form.product_module = shipmentData.product_module
            this.form.product_name = shipmentData.product_name
            this.form.client_name = shipmentData.client_name
            this.form.product_count = shipmentData.product_count
            this.form.order_date = shipmentData.order_date
            this.form.shape  = shipmentData.shape
            this.form.delivery_date = shipmentData.delivery_date
            this.form.remark = shipmentData.remark 

            this.disabled = true;
            } 
          })
   
      },

      // 监听workorder为空时解除其他输入框禁用
      checkWorkOrderIsNull(rule, value, callback){
        if (value == '') {
          this.disabled = false;
          this.form = {};
        }
        callback();
      },
      // 检查数量不能为0
      checkNumber(rule, value, callback){
        if(value == 0){
          callback(new Error('不能为0'));
        }else{
          callback();
        }
      },

       // 打包数量少于等于总数量
       checkNum(rule, value, callback){ 
        if( value > this.form.product_count){
          callback(new Error('打包数量不能大于总数量'));
        }else if(value == 0){
          callback(new Error('不能为0'));
        }else{
          callback();
        }
      }
    },
    mounted() {
      this.loadAll();
    }
  }
  </script>

  <style scoped>
  .el-row {
    margin-bottom: 16px;
  }

  </style>

