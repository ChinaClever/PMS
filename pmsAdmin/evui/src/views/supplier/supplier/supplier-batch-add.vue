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
            prop="customer">
            <el-input
            :disabled="disabled" 
            v-model="form.customer"
            clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item
            label="产品:"
            prop="product_name">
            <el-input
            :disabled="disabled"
            v-model="form.product_name"       
            clearable/>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item
            label="产品类型:"
            prop="product_type">
            <el-input
            :disabled="disabled"
            v-model="form.product_type"
            clearable/>
          </el-form-item>
        </el-col>
      </el-row>
    <hr>
    <br>
      <el-row>
       <el-col :span="6">
        <el-form-item
            label="PCB编码:"
            prop="PCB_code">
            <el-input
              id="PCB_code_inputId"
              v-model="form.PCB_code"
              placeholder="请扫码输入PCB编码"
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
        <el-table-column prop="part_code" label="物料编码">
          <template slot-scope="scope">
            <el-input 
              :id="`part_code_inputId_` + scope.$index"
              v-model="scope.row.part_code"
              @keyup.enter.native="handlePartCodeEnterKey"></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="supplier" label="供应商">
          <template slot-scope="scope">
            <el-input v-model="scope.row.supplier"></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="parts" label="物料">
          <template slot-scope="scope">
            <el-input v-model="scope.row.parts"></el-input>
          </template>
        </el-table-column>
      </el-table>
     </el-row>
     <br>
     <el-row :gutter="20">
       <el-col :span="6">
        <el-form-item
            label="数量:"
            prop="product_number">
            <el-input
            v-model="form.product_number"
            placeholder="请输入数量"
            clearable/>
        </el-form-item>
       </el-col>
       <el-col :span="18">
        <el-form-item label="备注:" prop="notes" >
            <el-input
                v-model="form.notes"
                :rows="2"
                maxlength="500"
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
      // 物料表格
      dataTable:[
        { part_code: '', supplier: '' , parts: '' }
      ],
      // 表单验证规则
      rules: {
        work_order: [
          {validator: (rule, value, callback) => this.checkWorkOrderIsNull(rule, value, callback)},
          {required: false, message: '请输入单号', trigger: 'blur'},
        ],
      
        PCB_code: [
          {required: true, message: '请输入PCB编码', trigger: 'blur'},
          {validator: (rule, value, callback) => this.checkPCBCodeIsValid(rule, value, callback), trigger: 'blur'},
  
        ],
        
        product_number: [
          {required: true, message: '请输入数量', trigger: 'blur'}
        ],
      },
      work_orders: [],
      state: '',
      timeout:  null,
      // 提交状态
      loading: false,
      // 单号选择后禁用相应输入框
      disabled:false,
      // 物料表格索引
      dataTableIndex: 0,
      // 暂存PCB码
      PCB_code_temp: '',
      // 暂存物料编码 用于检验重复扫码
      part_code_temp: [],
      //已绑定的PCB个数
      count_PCB: 0,
    };
  },

  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          const partCodeString = this.dataTable.map(item => item.part_code).join(',');
          const supplierString = this.dataTable.map(item => item.supplier).join(',');
          const partsString = this.dataTable.map(item => item.parts).join(',');
          this.form.part_code = partCodeString;
          this.form.supplier = supplierString;
          this.form.parts = partsString;

          this.loading = true;
          this.$http['post']('/supplier/batch/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success({ message: res.data.msg, duration: 3000 });
              this.count_PCB += 1;
              // 页面数据重置
              this.dataTable = [{ part_code: '', supplier: '' , parts: '' }];
              this.form.PCB_code = this.PCB_code_temp
              this.dataTableIndex = 0;
              this.part_code_temp = [];
              const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
              input.focus();

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
                this.form.product_name = shipmentData.product_name
                this.form.customer = shipmentData.client_name
                this.form.product_type  = shipmentData.shape
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
            this.form.product_name = shipmentData.product_name
            this.form.customer = shipmentData.client_name
            this.form.product_type  = shipmentData.shape
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
        this.form = {};
        this.disabled = false;
      }
      callback();
    },

    // PCB_code输入框检测到回车触发
    handlePCBCodeEnterKey(){
      this.$refs['form'].validate((valid) => {
        if (valid) {
          // 焦点设在第一行物料编码输入框
          const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
          input.focus();
        }else{
          this.form.PCB_code = '';
        }
      });
  
    },

    // 验证PCB_code是否合法
    checkPCBCodeIsValid(rule, value, callback){
      const isPCB_code = value.startsWith("PCB");
      if(isPCB_code){
        //不能重复
        this.$http.get('/supplier/PCBisRepeat/'+value).then((res) => {
          if (res.data.code === 0){
            callback();
          }else{
            callback(new Error(res.data.msg)); 
          }
        }) 
      }else{
        callback(new Error('PCB编码格式错误,需以PCB开头')); 
      }
      
    },

    // 物料编码输入框检测到回车触发
    handlePartCodeEnterKey(event){
      const isPCB_code = event.target.value.startsWith("PCB");
      if(!isPCB_code){
        // 验证字符串中是否有且仅有两个加号
        const regex = /^[^+]*\+[^+]*\+[^+]*$/;
        const hasTwoPlus = regex.test(event.target.value);
        if(hasTwoPlus){
          // 验证没重复扫码
          if (!this.part_code_temp.includes(event.target.value)) {
            const parts = event.target.value.split("+");
            this.dataTable[this.dataTableIndex].part_code = parts[0];
            this.dataTable[this.dataTableIndex].supplier = parts[1];
            this.dataTable[this.dataTableIndex].parts = parts[2];
            this.part_code_temp.push(event.target.value)
            // 焦点设在下一行物料编码输入框
            this.dataTableIndex += 1;
            this.dataTable.push({ part_code: '', supplier: '', parts: '' });       
            const self = this; // 保存this.dataTableIndex的引用
            setTimeout(function() {
              const nextInput = document.getElementById(`part_code_inputId_${self.dataTableIndex}`);
              if(nextInput){
                nextInput.focus();
              }
            }, 100); // 添加100毫秒的延迟
          }else{
            this.dataTable.pop();
            this.dataTable.push({ part_code: '', supplier: '', parts: '' });  
            this.$message.error({ message: "重复扫码", duration: 3000,});
          }
        }else{
          this.dataTable.pop();
          this.dataTable.push({ part_code: '', supplier: '', parts: '' });  
          this.$message.error({ message: "物料编码格式错误", duration: 3000});
        }
      }else{
        // 扫到PCB码触发提交
        this.PCB_code_temp = event.target.value;
        this.clickSave();
      }
    },

    // 点击提交按钮触发
    clickSave(){
      this.dataTable.pop();
      if ( this.dataTable.length === 0 ){
        this.dataTable.push({ part_code: '', supplier: '', parts: '' });
        const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
        input.focus();  
        this.$message.error({ message: "物料信息不能为空", duration: 3000});
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
  width: 20vw !important;
  height: 54px !important;
  font-size: 24px;
  /* border: none !important;
  box-shadow: none !important; */
}
::v-deep .el-input__suffix{
  padding-right: 45px;
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