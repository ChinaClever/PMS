<template>
  <div class="mainDiv">
   <div class="pageDiv">
      <el-form
          ref="form"
          :model="form"
          :rules="rules"
          label-width="140px"
          label-position="top">
      <hr>
      <br>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item
              label="单号:"
              prop="work_order">
              <el-autocomplete
              v-model="form.work_order"
              clearable
              :fetch-suggestions="querySearchAsync"
              @select="handleSelect"
              @clear="handleClear"
              @keyup.enter.native="handleEnterKey"
              placeholder="请输入单号"
              ></el-autocomplete>  
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item
              label="客户:"
              prop="name">
              <el-input
              :disabled="disabled" 
              v-model="form.name"
              placeholder="请输入客户"
              clearable/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item
              label="订单数量:"
              prop="quantity">
              <el-input
              :disabled="disabled"
              v-model="form.quantity"
              placeholder="请输入订单数量"         
              clearable/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item
              label="规格类型:"
              prop="code">
              <el-input
              :disabled="disabled"
              v-model="form.code"
              placeholder="请输入规格类型"
              clearable/>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item
              label="订单日期:"
              prop="order_time">
              <el-input
              :disabled="disabled" 
              v-model="form.order_time"
              placeholder="请输入订单日期"
              clearable/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item
              label="交货日期:"
              prop="delivery_time">
              <el-input
              :disabled="disabled"
              v-model="form.delivery_time"
              placeholder="请输入交货日期"         
              clearable/>
            </el-form-item>
          </el-col>
        </el-row>
      <hr>
      <br>
        <el-row>
          <el-col :span="6">
            <el-form-item
              label="程序要求:"
              prop="require">
              <el-input
              id="require_inputId"
              v-model="form.require"
              placeholder="请输入程序要求"         
              clearable/>
            </el-form-item>
          </el-col>
         <el-col :span="6">
          <el-form-item
              label="软件版本号:"
              prop="version">
              <el-input
                v-model="form.version"
                placeholder="请输入软件版本号"
                @keyup.enter.native="handlePCBCodeEnterKey"
                clearable/>
          </el-form-item>
         </el-col>
       <el-col :span="4" :push="4">
        <el-statistic title="已绑定的PCB个数" style="font-size: 28px;"  :value-style="{color:'#1890FF', fontSize:'48px'}">
            <template slot="formatter">
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{count_PCB}}
            </template>
        </el-statistic>
       </el-col>
         
        </el-row>
          <br>
       <el-row>
        <el-table :data="dataTable" editable>
          <el-table-column prop="PCB_code" label="PCB编码">
            <template slot-scope="scope">
              <el-input 
                :id="`PCB_code_inputId_` + scope.$index"
                v-model="scope.row.PCB_code"
                @keyup.enter.native="handlePartCodeEnterKey"></el-input>
            </template>
          </el-table-column>
         
      
        </el-table>
       </el-row>
       <br>
       <el-row :gutter="20">
         <el-col :span="18">
          <el-form-item label="备注:" prop="remark" >
              <el-input
                  v-model="form.remark"
                  :rows="2"
                  maxlength="500"
                  show-word-limit
                  type="textarea"/>
          </el-form-item>
         </el-col>
         <el-col :span="18">
          <el-form-item label="rcerder:" prop="rcerder" >
              <el-input
                  v-model="form.rcerder"
                  :rows="2"
                  type="textarea"/>
          </el-form-item>
         </el-col>
       </el-row>
       <el-form-item>
        <el-button type="primary" @click="clickSave" style="float: right;">提交</el-button>
       </el-form-item>
      </el-form>
  
   </div>
  </div>
  </template>
  
  <script>
  export default {
    name: 'Ed',
    data() {
      return {
        // 表单数据
        form: {
          product_number: 1
        },
        // 表格
        dataTable:[
          { PCB_code: '',}
        ],
        // 表单验证规则
        rules: {
          work_order: [
            {validator: (rule, value, callback) => this.checkWorkOrderIsNull(rule, value, callback)},
            {required: false, message: '请输入单号', trigger: 'blur'},
          ],
        
          version: [
            {required: true, message: '请输入软件版本号', trigger: 'blur'}, 
    
          ],
          
        },
        work_orders: [],
        time: [],
        state: '',
        timeout:  null,
        // 提交状态
        loading: false,
        // 单号选择后禁用相应输入框
        disabled:false,
        // 物料表格索引
        dataTableIndex: 0,
        // 暂存
        version_temp: '',
        // 暂存物料编码 用于检验重复扫码
        PCB_code_temp: [],
        //已绑定的PCB个数
        count_PCB: 0,
      };
    },
  
    methods: {
      /* 保存编辑 */
      save() {      
        this.$refs['form'].validate((valid) => {
          if (valid) {
            var currentTime = new Date();
            var timeString = currentTime.toLocaleString();
            this.time.push(timeString)
            const partCodeString = this.dataTable.map(item => item.PCB_code).join(',');
            this.form.PCB_code = partCodeString;
            this.form.times = this.time
            this.loading = true;
            this.$http['post']('/burningreport/adds', this.form).then(res => {
              this.loading = false;
              this.count_PCB  = 0
              this.time = []
              if (res.data.code === 0) {
                this.$message.success({ message: res.data.msg, duration: 3000 });
                // 页面数据重置
                this.dataTable = [{ PCB_code: '',}];
                this.form.version = this.version_temp
                this.dataTableIndex = 0;
                this.PCB_code_temp = [];
               
  
              } else {
                this.$message.error({ message: res.data.msg, duration: 3000 });
              }
            }).catch(e => {
              this.loading = false;
               this.$message.error({ message: e.message, duration: 3000 });
            });
          } else {
            return false;
          }
        });
      },
      // 查单号下拉框的单号内容
      loadAll() {
          this.$http.get('/shipmentreport/work_order/list').then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.work_orders = res.data.data
              } 
          })
      },
      // 异步查询产品名称
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
  
      // 单号下拉框选择触发
      handleSelect(item) {
          this.form.work_order = item.value
          this.$refs.form.validateField('work_order', () => {});
          this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
              this.loading = false;
              const shipmentData = res.data.data
              if (res.data.code === 0 && res.data.data != null) {
                this.form.name = shipmentData.product_name
                this.form.code  = shipmentData.shape
                this.form.quantity  = shipmentData.product_count
                this.form.order_time  = shipmentData.order_date
                this.form.delivery_time  = shipmentData.delivery_date
                this.disabled = true;
              }        
              // 焦点在PCB输入框
              if(this.form.version){
                this.form.version = ''; 
              }    
              const input = document.getElementById('require_inputId');
              input.focus();
            })
      },
      // 单号清除事件
      handleClear(){
          this.form.work_order=''
          this.form.product_name = ''
          this.form.customer = ''
          this.form.product_type  = ''
          this.disabled=false;
  
      },
      // 单号检测到回车触发
      handleEnterKey(event){
          this.form.work_order = event.target.value.split("+")[0];
          this.$refs.form.validateField('work_order', () => {});
          // 根据选择的单号查其他数据自动填入
          this.$http.get('/shipmentreport/detail/' + event.target.value.split("+")[0]).then((res) => {
              this.loading = false;
              const shipmentData = res.data.data;
              if (res.data.code === 0 && res.data.data != null) {
              this.form.product_name = shipmentData.product_name
              this.disabled=true;
              }
            // 焦点在PCB输入框
            if(this.form.PCB_code){
              this.form.PCB_code = ''; 
            }    
            const input = document.getElementById('PCB_code_inputId');
            input.focus();
          })
      },
      // 监听workorder为空时解除其他输入框禁用
      checkWorkOrderIsNull(rule, value, callback){
        if (value == '') {
          this.disabled = false
          // this.form={
          //   product_name:'',
          //   customer: '',
          //   product_type :''
          // }
          this.form.work_order = ''
          this.form.product_name = ''
          this.form.customer = ''
          this.form.product_type  = ''
        }
        callback();
      },
  
      // version输入框检测到回车触发
      handlePCBCodeEnterKey(){
        this.$refs['form'].validate((valid) => {
          if (valid) {
            // 焦点设在第一行物料编码输入框
            const input = document.getElementById(`PCB_code_inputId_${this.dataTableIndex}`);
            input.focus();
          }else{
            this.form.version = '';
          }
        });
    
      },
  
      // PCB输入框检测到回车触发
      handlePartCodeEnterKey(event){
            if (!this.PCB_code_temp.includes(event.target.value)) {
              const parts = event.target.value
              this.dataTable[this.dataTableIndex].PCB_code = parts;
              this.PCB_code_temp.push(event.target.value)
              // 焦点设在下一行物料编码输入框
              var currentTime = new Date();
              var timeString = currentTime.toLocaleString();
              this.time.push(timeString)
              this.dataTableIndex += 1;
              this.count_PCB += 1;
              this.dataTable.push({ PCB_code: '',});       
              const self = this; // 保存this.dataTableIndex的引用
              setTimeout(function() {
                const nextInput = document.getElementById(`PCB_code_inputId_${self.dataTableIndex}`);
                if(nextInput){
                  nextInput.focus();
                }
              }, 100); // 添加100毫秒的延
        }else {
                // 编码重复，执行你想要的操作，如提示错误信息等
                this.$message.error({ message: 'PCB编码重复' });
             }
      },
  
      // 点击提交按钮触发
      clickSave(){
        this.dataTable.pop();
        if ( this.dataTable.length === 0 ){
          this.dataTable.push({ PCB_code: '',});
          this.$message.error({ message: "信息不能为空", duration: 3000});
        }else{
          this.save();
        }
      }
  
    },
  
  
  
    mounted() {
      this.loadAll();
    }
  }
  </script>
  
  <style scoped>
  /* 全局样式 */
  ::v-deep .cell{
    font-size: 24px !important;
    color: #606266 !important;
    font-style: normal !important;
    line-height: 30px !important;
  }
  
  .mainDiv {
    position: fixed;
    left: 5%;
    padding-right: 0;
    right: 5%;
    height: 100vh;
    overflow-y: auto; 
    overflow-x: hidden;
  }
  .pageDiv {
    margin-top: 2%;
    margin-bottom: 5%;
  }
  
  ::v-deep .el-input__inner{
    width: auto !important;
    height: 54px !important;
    font-size: 24px;
    /* border: none !important;
    box-shadow: none !important; */
  }
  
  ::v-deep .el-form-item__label{
    font-size: 24px;
  }
  
  ::v-deep .el-form-item__error{
    font-size: 18px;
  }
  
  ::v-deep ul.el-scrollbar__view.el-autocomplete-suggestion__list li {
    font-size: 20px !important;
  }
  
  
  ::v-deep .error-message {
    font-size: 24px !important;
  }
  
  </style>