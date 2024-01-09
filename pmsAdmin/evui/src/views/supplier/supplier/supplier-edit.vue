<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改':'添加'"
    :visible="visible"
    width="600px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="100px">
      <el-form-item
          label="单号:"
          prop="work_order">
          <el-autocomplete
          v-model="form.work_order"
          :disabled="isUpdate"
          clearable
          :fetch-suggestions="querySearchAsync"
          @select="handleSelect1"
          @clear="handleClear"
          @keyup.enter.native="handleEnterKey"
          placeholder="请输入单号"
        ></el-autocomplete>  
      </el-form-item>
      <el-form-item
        label="客户:"
        prop="customer">
        <el-input
          :disabled="disabled" 
          :maxlength="20"
          v-model="form.customer"
          placeholder="请输入客户"
          clearable/>
      </el-form-item>

      <el-form-item
        label="产品:"
        prop="product_name">
        <el-input
          :disabled="disabled"
          :maxlength="20"
          v-model="form.product_name"
          placeholder="请输入产品"         
          clearable/>
      </el-form-item>
      <el-form-item
        label="产品类型:"
        prop="product_type">
        <el-input
          :disabled="disabled"
          :maxlength="20"
          v-model="form.product_type"
          placeholder="请输入产品类型"
          clearable/>
      </el-form-item>
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
      <el-row>
      <el-table :data="dataTable" editable>
        <el-table-column prop="part_code" label="物料编码">
          <template slot-scope="scope">
            <el-input 
              :id="`part_code_inputId_` + scope.$index"
              v-model="scope.row.part_code"></el-input>
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
      <el-button @click="addInput">添加输入框</el-button>
        <el-button v-if="this.dataTable.length > 0" @click="removeInput">删除最后一个输入框</el-button>
     </el-row>
      <el-form-item
        label="数量:"
        prop="product_number">
        <el-input
          :maxlength="20"
          v-model="form.product_number"
          placeholder="请输入数量"
          clearable/>
      </el-form-item>
      <el-form-item label="备注:" prop="notes" >
          <el-input
            v-model="form.notes"
            :rows="4"
            maxlength="150"
            show-word-limit
            type="textarea"/>
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
  name: 'LevelEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({
        status: 1,
        type : 1,
        product_name:'',
        dataTable : [],
      }, this.data),
      // 物料表格
      dataTable:[
        { part_code: '', supplier: '' , parts: '' }
      ],
      // 表单验证规则
      rules: {
        /*name: [
          {required: true, message: '请输入职级名称', trigger: 'blur'}
        ],
        status: [
          {required: true, message: '请选择职级状态', trigger: 'blur'}
        ],
        sort: [
          {required: true, message: '请输入排序号', trigger: 'blur'}
        ],*/
        work_order: [
        {required: false, message: '请输入单号', trigger: 'blur'},
        {validator: (rule, value, callback) => this.checkWorkOrderIsNull(rule, value, callback)},
         
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
        {required: true, message: '请输入PCB编码', trigger: 'blur'},
          {validator: (rule, value, callback) => this.checkPCBCodeIsValid(rule, value, callback), trigger: 'blur'},
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
      // 是否是修改
      isUpdate: false,
      disabled:false,
      // 物料表格索引
      dataTableIndex: 0,
      // 暂存PCB码
      PCB_code_temp: '',
      // 暂存物料编码 用于检验重复扫码
      part_code_temp: [],
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.PCB_code_temp=this.form.PCB_code
        this.dataTable=this.data.dataTable
        this.isUpdate = true;
        this.disabled=true;
      } else {
        this.form = {};
        this.isUpdate = false;
        this.disabled = false;

      }
    }
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          const partCodes = [...this.dataTable.map(item => item.part_code)];
          if(new Set(partCodes).size !== partCodes.length){
            this.$message.error({ message: "物料编码重复", duration: 3000});
            return false;
          }
          else if(new Set(partCodes).has('')){
            this.$message.error({ message: "物料编码不能为空", duration: 3000});
            return false;
          }
          const partCodeString = this.dataTable.map(item => item.part_code).join(',');
          const supplierString = this.dataTable.map(item => item.supplier).join(',');
          const partsString = this.dataTable.map(item => item.parts).join(',');
          this.form.part_code = partCodeString;
          this.form.supplier = supplierString;
          this.form.parts = partsString;
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/supplier/update' : '/supplier/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {};
                this.dataTable = [{ part_code: '', supplier: '' , parts: '' }];
                this.dataTableIndex = 0;
                this.part_code_temp = [];
              }
              this.disabled=false
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
    // 异步查询产品名称
    querySearchAsync(queryString, cb) {
      var work_orders = this.work_orders;
      var filteredResults = queryString ? work_orders.filter(this.createStateFilter1(queryString)) : work_orders;
      var results = filteredResults.slice(0, 10); // 限制结果最多显示10条

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 300 * Math.random());
    },
    createStateFilter1(queryString) {
        return (state) => {
          return (state.value.toLowerCase().includes(queryString.toLowerCase()));
        };
      },
    handleSelect1(item) {
        this.form.work_order = item.value
        this.$refs.form.validateField('work_order', () => {});
        // 根据选择的单号查其他数据自动填入
        this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
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

      handleClear(){
        // this.form={
        //   product_name:'',
        //   customer: '',
        //   product_type :''
        // }
        this.form.work_order=''
        this.form.product_name = ''
        this.form.customer = ''
        this.form.product_type  = ''
        this.disabled=false;

      },
      // 单号检测到回车触发
      handleEnterKey(event){
      console.log("进入")
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
        if(this.isUpdate){
          if(!(this.PCB_code_temp==this.form.PCB_code)){
            //不能重复
            this.$http.get('/supplier/PCBisRepeat/'+value).then((res) => {
              if (res.data.code === 0){
                callback();
              }else{
                callback(new Error(res.data.msg)); 
              }
            }) 
          }
          else{
            callback();
          }
        }else{
          //不能重复
          this.$http.get('/supplier/PCBisRepeat/'+value).then((res) => {
            if (res.data.code === 0){
              callback();
            }else{
              callback(new Error(res.data.msg)); 
            }
          }) 
        }
        
      }else{
        callback(new Error('PCB编码格式错误,需以PCB开头')); 
      }
      
    },
    // 物料编码输入框检测到回车触发
    // handlePartCodeEnterKey(event){
    //   const isPCB_code = event.target.value.startsWith("PCB");
    //   if(!isPCB_code){
    //     // 验证字符串中是否有且仅有两个加号
    //     const regex = /^[^+]*\+[^+]*\+[^+]*$/;
    //     const hasTwoPlus = regex.test(event.target.value);
    //     if(hasTwoPlus){
    //       // 验证没重复扫码
    //       if (!this.part_code_temp.includes(event.target.value)) {
    //         const parts = event.target.value.split("+");
    //         this.dataTable[this.dataTableIndex].part_code = parts[0];
    //         this.dataTable[this.dataTableIndex].supplier = parts[1];
    //         this.dataTable[this.dataTableIndex].parts = parts[2];
    //         this.part_code_temp.push(event.target.value)
    //         // 焦点设在下一行物料编码输入框
    //         this.dataTableIndex += 1;
    //         this.dataTable.push({ part_code: '', supplier: '', parts: '' });       
    //         const self = this; // 保存this.dataTableIndex的引用
    //         setTimeout(function() {
    //           const nextInput = document.getElementById(`part_code_inputId_${self.dataTableIndex}`);
    //           if(nextInput){
    //             nextInput.focus();
    //           }
    //         }, 100); // 添加100毫秒的延迟
    //       }else{
    //         this.dataTable.pop();
    //         this.dataTable.push({ part_code: '', supplier: '', parts: '' });  
    //         this.$message.error({ message: "重复扫码", duration: 3000,});
    //       }
    //     }else{
    //       this.dataTable.pop();
    //       this.dataTable.push({ part_code: '', supplier: '', parts: '' });  
    //       this.$message.error({ message: "物料编码格式错误", duration: 3000});
    //     }
    //   }else{
    //     // 扫到PCB码触发提交
    //     this.PCB_code_temp = event.target.value;
    //     this.clickSave();
    //   }
    // },
    // 点击提交按钮触发
    // clickSave(){
    //   this.dataTable.pop();
    //   if ( this.dataTable.length === 0 ){
    //     this.dataTable.push({ part_code: '', supplier: '', parts: '' });
    //     const input = document.getElementById(`part_code_inputId_${this.dataTableIndex}`);
    //     input.focus();  
    //     this.$message.error({ message: "物料信息不能为空", duration: 3000});
    //   }else{
    //     this.save();
    //   }
    // },
    //添加行
    // addInput() {
    //   if (this.dataTable[this.dataTable.length - 1].part_code && !this.part_code_temp.includes(this.dataTable[this.dataTable.length - 1].part_code) ) {
    //     this.part_code_temp.push(this.dataTable[this.dataTable.length - 1].part_code)
    //     this.dataTable.push(
    //     {
    //       part_code: '', 
    //       supplier: '', 
    //       parts: ''
    //     });
    //   }else if(!this.dataTable[this.dataTable.length - 1].part_code){
    //     this.$message.error({ message: "物料编码未填写", duration: 3000});
    //   }
    //   else{
    //     this.$message.error({ message: "物料编码重复", duration: 3000});
    //   }
    // },
    addInput() {
        this.dataTable.push(
        {
          part_code: '', 
          supplier: '', 
          parts: ''
        });     
    },
    //删除行
    removeInput() {
      this.dataTable.pop();
      if (this.dataTable.length === 0) {
        this.dataTable.push({ part_code: '', supplier: '', parts: '' }); 
      }
    }
  },
  mounted() {
    this.loadAll();
  }
}
</script>

<style scoped>
</style>
