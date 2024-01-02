<template>
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
            :disabled="isUpdate"
            clearable
            :fetch-suggestions="querySearchAsync"
            @select="handleSelect1"
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
            :maxlength="20"
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
            :maxlength="20"
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
            :maxlength="20"
            v-model="form.product_type"
            placeholder="请输入产品类型"
            clearable/>
          </el-form-item>
        </el-col>
      </el-row>
       
      
        <el-form-item
            label="供应商:"
            prop="supplier">
            <el-input
            :maxlength="20"
            v-model="form.supplier"
            placeholder="请输入供应商"
            clearable/>
        </el-form-item>
        <el-form-item
            label="物料:"
            prop="parts">
            <el-input
            :maxlength="20"
            v-model="form.parts"
            placeholder="请输入物料"
            clearable/>
        </el-form-item>

     <el-row :gutter="20">
       <el-col :span="6">
        <el-form-item
            label="数量:"
            prop="product_number">
            <el-input
            :maxlength="20"
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
    </el-form>
 </div>
</template>

<script>
export default {
  name: 'Ed',
  data() {
    return {
      // 表单数据
      form: [],
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
      disabled:false
    };
  },

  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http['post']('/supplier/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {};
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
  },
  mounted() {
    this.loadAll();
  }
}
</script>

<style scoped>
.pageDiv{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh; /* 设置容器高度为视口高度，以便居中显示 */
}
/* 调整输入框大小的样式类 */
::v-deep .el-input__inner{
  width: 380px !important;
  height: 54px !important;
  font-size: 24px;
}

::v-deep .el-form-item__label{
  font-size: 24px;
}

</style>