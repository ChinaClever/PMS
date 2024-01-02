<template>
<div class="mainDiv">
 <div class="pageDiv">
    <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="140px"
        label-position="top">
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
            placeholder="请输入客户"
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
            placeholder="请输入产品"         
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
            placeholder="请输入产品类型"
            clearable/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item
            label="PCB编码:"
            prop="PCB_code">
            <el-input
            id="PCB_code_inputId"
            v-model="form.PCB_code"
            placeholder="请输入PCB编码"
            @keyup.enter.native="handlePCBCodeEnterKey"
            clearable/>
        </el-form-item>
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
                show-word-limit
                type="textarea"/>
        </el-form-item>
       </el-col>
     </el-row>
     <el-form-item>
      <el-button type="primary" @click="save" style="float: right;">提交</el-button>
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
        customer: [
          {required: false, message: '请输入客户', trigger: 'blur'}
        ],
        product_name: [
          {required: false, message: '请输入产品', trigger: 'blur'}
        ],
        product_type: [
          {required: false, message: '请输入产品类型', trigger: 'blur'}
        ],
        PCB_code: [
          {required: true, message: '请输入PCB编码', trigger: 'blur'}
        ],
        part_code: [
          {required: true, message: '请输入物料编码', trigger: 'blur'}
        ],
        supplier: [
          {required: true, message: '请输入供应商', trigger: 'blur'}
        ],
        parts: [
          {required: true, message: '请输入物料', trigger: 'blur'}
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
              this.$message.success(res.data.msg);
              // 页面数据重置
              this.dataTable = [{ part_code: '', supplier: '' , parts: '' }];
              this.form.PCB_code = this.PCB_code_temp
              this.dataTableIndex = 0;
              const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
              input.focus();

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

    // PCB_code输入框检测到回车触发
    handlePCBCodeEnterKey(event){
      const isPCB_code = event.target.value.startsWith("PCB");
      if(isPCB_code){
        // 焦点设在第一行物料编码输入框
        const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
        input.focus();
      }
    },

    // part_code输入框检测到回车触发
    handlePartCodeEnterKey(event){
      const isPCB_code = event.target.value.startsWith("PCB");
      if(!isPCB_code){
        // 验证字符串中是否有且仅有两个加号
        const regex = /^[^+]*\+[^+]*\+[^+]*$/;
        const hasTwoPlus = regex.test(event.target.value);
        if(hasTwoPlus){
          const parts = event.target.value.split("+");
          this.dataTable[this.dataTableIndex].part_code = parts[0];
          this.dataTable[this.dataTableIndex].supplier = parts[1];
          this.dataTable[this.dataTableIndex].parts = parts[2];
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
        }
      }else{
        // 扫到PCB码触发提交
        this.dataTable.pop();
        this.PCB_code_temp = event.target.value;
        this.save();
      }
    },


  },



  mounted() {
    this.loadAll();
  }
}
</script>

<style scoped>
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

/* 调整输入框大小的样式类 */
::v-deep .el-input__inner{
  width: 380px !important;
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

</style>