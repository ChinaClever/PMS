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
          <el-form-item label="单号:" prop="work_order">
            <el-autocomplete
              v-model="form.work_order"
              clearable
              placeholder="请输入单号"
              :fetch-suggestions="querySearchAsync"
              @select="handleSelect"
              @clear="handleClear"
              @keyup.enter.native="handleEnterKey"
            ></el-autocomplete>  
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="客户名称:" prop="client_name">
            <el-input
              :disabled="disabled" 
              v-model="form.client_name"
              clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="成品编码:" prop="product_code">
            <el-input
              :disabled="disabled"
              v-model="form.product_code"      
              clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="产品名称:" prop="product_name">
            <el-input
              :disabled="disabled"
              v-model="form.product_name"
              clearable/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="成品/模块:" prop="product_module" >
            <el-select v-model="form.product_module" placeholder="">
            <el-option
              v-for="item in product_moduleOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              :disabled="disabled">
            </el-option>
          </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="总数量:" prop="product_count">
          <el-input-number
            :disabled="disabled"
            :step="50"
            :min="0"
            v-model="form.product_count"
            controls-position="left"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="订单日期:" prop="order_date">
            <el-date-picker
            :disabled="disabled"
              type="date"
              class="ele-fluid"
              v-model="form.order_date"
              value-format="yyyy-MM-dd"/>
            </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="交货日期:" prop="delivery_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.delivery_date"
              value-format="yyyy-MM-dd"
              :disabled="disabled"/>
            </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="SO/RQ号:" prop="SO_RQ_id">
            <el-input
              :disabled="disabled"
              v-model="form.SO_RQ_id"
              clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="规格型号:" prop="shape">
              <el-input
                :disabled="disabled"
                v-model="form.shape"
                clearable/>
            </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="备注:" prop="notes" >
            <el-input
              :disabled="disabled"
              v-model="form.notes"
              :rows="2"
              maxlength="500"
              type="textarea"/>
          </el-form-item>
        </el-col>
        
      </el-row> 
    <hr>
    <br>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="成品SN" prop="goods_SN">
            <el-input
              id="goods_SN_inputId"
              v-model="form.goods_SN"
              placeholder="请扫码输入成品SN"
              @keyup.enter.native="handleGoodsSNEnterKey"
              clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <!-- <el-form-item label="打包完成时间:" prop="packing_finish_time">
            <el-date-picker
              type="datetime"
              class="ele-fluid"
              v-model="form.packing_finish_time"
              value-format="yyyy-MM-dd HH:mm:ss"/>
          </el-form-item> -->
        </el-col>
        <el-col :span="6">
          <!-- <el-form-item label="工时(单位/小时):" prop="work_hours">
            <el-input-number
              :min="0"
              v-model="form.work_hours"
              controls-position="left"
              class="ele-fluid ele-text-left"/>
          </el-form-item> -->
          <!-- :precision="6" -->
        </el-col>
        <el-col :span="6">
          <el-form-item label="打包数量:" prop="packing_count">
            <el-input-number
              :min="1"
              :max="1"
              :step="1"
              v-model="form.packing_count"
              controls-position="left"
              class="ele-fluid ele-text-left"/>
          </el-form-item>
        </el-col>
        <el-col :span="5" :push="3">
          <el-statistic title="已绑定的成品SN个数" style="font-size: 28px;"  :value-style="{color:'#1890FF', fontSize:'48px'}">
              <template slot="formatter">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{count_SN}}
              </template>
          </el-statistic>
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
        packing_count: 1
      },
      // 表单验证规则
      rules: {
          // packing_finish_time: [
          //   {required: true, message: '请选择打包完成时间', trigger: 'blur'}
          // ],
          // work_hours: [
          //   {required: true, message: '请输入工时', trigger: 'blur'},
          //   {validator: (rule, value, callback) => this.checkNumber(rule, value, callback)},
          // ],
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
          goods_SN: [
            {required: true, message: '请扫码输入产品SN', trigger: 'blur'},
          ],
        },
      work_orders: [],
      state: '',
      timeout:  null,
      // 提交状态
      loading: false,
      // 成品模块选项
      product_moduleOptions: [{
          value: 1,
          label: '成品'
        }, {
          value: 2,
          label: '模块'
      }],
      // 单号选择后禁用相应输入框
      disabled:false,
      //已绑定的SN个数
      count_SN: 0,
      isFirstSave: true,
      // 暂存上一个要保存的SN码
      goods_SN_temp: '',
      // 暂存上一个打包时间（当作开始时间）
      packing_finish_time_temp: '',
    };
  },

  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http['post']('/packing/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success({ message: res.data.msg, duration: 3000 });
              this.count_SN += 1;
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
    // 单号下拉框选择触发
    handleSelect(item) {
        this.form.work_order = item.value
        this.$refs.form.validateField('work_order', () => {});
        this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
            this.loading = false;
            const shipmentData = res.data.data;
            if (res.data.code === 0 && res.data.data != null) {
                this.form.product_name = shipmentData.product_name;
                this.form.client_name = shipmentData.client_name;
                this.form.product_code  = shipmentData.product_code;
                this.form.shape  = shipmentData.shape;
                this.form.product_module  = shipmentData.product_module;
                this.form.product_count  = shipmentData.product_count;
                this.form.order_date  = shipmentData.order_date;
                this.form.delivery_date  = shipmentData.delivery_date;
                this.form.SO_RQ_id  = shipmentData.SO_RQ_id;
                this.form.remark  = shipmentData.remark;
                this.disabled=true;
            }        
            // 焦点在goods_SN输入框
            if(this.form.goods_SN){
              this.form.goods_SN = ''; 
            }    
            const input = document.getElementById('goods_SN_inputId');
            input.focus();
          })
    },
    // 单号清除事件
    handleClear(){
      this.form = {};
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
              this.form.product_name = shipmentData.product_name;
              this.form.client_name = shipmentData.client_name;
              this.form.product_code  = shipmentData.product_code;
              this.form.shape  = shipmentData.shape;
              this.form.product_module  = shipmentData.product_module;
              this.form.product_count  = shipmentData.product_count;
              this.form.order_date  = shipmentData.order_date;
              this.form.delivery_date  = shipmentData.delivery_date;
              this.form.SO_RQ_id  = shipmentData.SO_RQ_id;
              this.form.remark  = shipmentData.remark;
              this.disabled=true;
            }
            // 焦点在goods_SN_inputId输入框
            if(this.form.goods_SN){
              this.form.goods_SN = ''; 
            }    
            const input = document.getElementById('goods_SN_inputId');
            input.focus();
        })
    },
    // 监听workorder为空时解除其他输入框禁用
    checkWorkOrderIsNull(rule, value, callback){
      if (value == '') {
        this.form = {};
        this.disabled = false
      }
      callback();
    },
    // 产品SN检测到回车触发
    handleGoodsSNEnterKey(event){
      // 打开页面第一次扫码 先验证是否重复
      if ( this.isFirstSave == true ){
        this.checkGoodsSNIsValid(this.form.goods_SN).then((isValid) => {
          if (isValid){
            this.goods_SN_temp = event.target.value;
            this.packing_finish_time_temp = new Date();
            this.form.packing_count = 1;
            this.$message.info({ message: '扫码下一个自动计算工时并保存', duration: 3000 });
            this.isFirstSave = false;
          }else{
            this.form.goods_SN = '';
          }
        }).catch((error) => {
          console.error(error); // 处理错误情况
        });
      // 不是第一次扫码
      }else{
        const new_goods_SN = event.target.value.replace(this.goods_SN_temp,'')
        this.checkGoodsSNIsValid(new_goods_SN).then((isValid) => {
          if (isValid && new_goods_SN != this.goods_SN_temp){
            this.form.goods_SN = event.target.value.replace(this.goods_SN_temp,'')
            this.form.goods_SN = this.goods_SN_temp
            // 第二个打包时间减去第一个是第一个的工时,扫第二个再保存第一个
            this.form.packing_finish_time = this.formatDate(new Date());
            const date1 = this.packing_finish_time_temp;
            const date2 = new Date();
            const secondDiff = Math.abs((date2 - date1) / 1000);
            const hoursDiff = secondDiff / 3600;
            this.form.work_hours = hoursDiff;
            this.save();
            // 保存后初始化数据
            this.packing_finish_time_temp = new Date();
            this.form.goods_SN = event.target.value.replace(this.goods_SN_temp,'');
            this.goods_SN_temp = this.form.goods_SN;
          }else{
            this.form.goods_SN = this.goods_SN_temp;
          }
        }).catch((error) => {
          console.error(error); 
        });
      }
      // 焦点一直在sn码输入框
      const input = document.getElementById('goods_SN_inputId');
      input.focus();

    },
    // 点击提交按钮触发
    clickSave(){
      this.form.packing_finish_time = this.formatDate(new Date());
      const date1 = this.packing_finish_time_temp;
      const date2 = new Date();
      const secondDiff = Math.abs((date2 - date1) / 1000);
      const hoursDiff = secondDiff / 3600;
      this.form.work_hours = hoursDiff;
      this.save();
      this.form = { packing_count:1 };
      this.packing_finish_time_temp = '';
      this.goods_SN_temp = '';
      this.isFirstSave = true;
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
    },
    // 日期格式 
    formatDate(date) {
      let year = date.getFullYear();
      let month = this.addLeadingZero(date.getMonth() + 1);
      let day = this.addLeadingZero(date.getDate());
      let hours = this.addLeadingZero(date.getHours());
      let minutes = this.addLeadingZero(date.getMinutes());
      let seconds = this.addLeadingZero(date.getSeconds());
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    addLeadingZero(value) {
      return value < 10 ? "0" + value : value;
    },
    // 检测sn码是否唯一
    checkGoodsSNIsValid(goods_SN) {
      return new Promise((resolve, reject) => {
        if (this.goods_SN_temp == goods_SN){
          this.$message.error({ message: `SN码:${goods_SN}重复`, duration: 3000 });
          resolve(false);
        }
        this.$http.get('/packing/SNisRepeat/' + goods_SN).then((res) => {
          if(res.data.code === 2){
            this.$message.warning({ message: res.data.msg, duration: 3000 });
            resolve(true); 
          }else if (res.data.code === 0) {
            resolve(true);
          } else {
            this.$message.error({ message: res.data.msg, duration: 3000 });
            resolve(false);
          }
        }).catch((error) => {
          reject(error);
        });
      });
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
  width: 20vw !important;
  height: 54px !important;
  font-size: 24px;
  /* border: none !important;
  box-shadow: none !important; */
}
::v-deep .el-input__suffix{
  padding-right: 30px;
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

::v-deep .el-input-number__decrease{
  height: 42px !important;
  padding-top: 10px;

}

::v-deep .el-input-number__increase{
  height: 42px !important;
  padding-top: 10px;
  margin-right: 33px;
}

</style>