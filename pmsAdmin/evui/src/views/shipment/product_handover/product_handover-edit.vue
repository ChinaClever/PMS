<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改客户':'添加客户'"
    :visible="visible"
    width="560px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">

      <el-form-item
        label="日期:"
        prop="time">
        <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.time"
              value-format="yyyy-MM-dd"
              placeholder="请选择日期"/>
      </el-form-item>

      <el-form-item
            label="单号:"
            prop="work_order">
            <el-autocomplete
            :disabled="isUpdate"
            v-model="form.work_order"
            clearable
            :fetch-suggestions="querySearchAsync"
            @select="handleSelect"
            @clear="handleClear"
            @keyup.enter.native="handleEnterKey"
            placeholder="请输入单号"
            style="width: 437px;"
          ></el-autocomplete>  
      </el-form-item>

      <el-form-item
        label="客户名称:"
        prop="name">
        <el-input
          :disabled="disabled"  
          :maxlength="255"
          v-model="form.name"
          placeholder="请输入客户名称"
          clearable/>
      </el-form-item>

      <el-form-item
        label="规格型号:"
        prop="code">
        <el-input
        :disabled="disabled"    
        :maxlength="255"
          v-model="form.code"
          placeholder="请输入规格型号"
          clearable/>
      </el-form-item>

      <el-form-item
        label="安数:"
        prop="remark">
        <el-input  
        :maxlength="255"
          v-model="form.remark"
          placeholder="请输入安数"
          clearable/>
      </el-form-item>
      
      <el-form-item
        label="交期:"
        prop="delivery_time">
        <el-date-picker
              :disabled="disabled"  
              type="date"
              class="ele-fluid"
              v-model="form.delivery_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择交期"/>
      </el-form-item>
      
      <el-form-item
        label="数量:"
        prop="quantity">
        <el-input
          :maxlength="20"
          v-model="form.quantity"
          placeholder="请输入数量"
          clearable/>
      </el-form-item>
      
      <el-form-item
        label="主控板版本号:"
        label-width="120px"
        prop="control_version">
        <el-input
          :maxlength="255"
          v-model="form.control_version"
          placeholder="请输入主控板版本号注"
          clearable/>
      </el-form-item>

      <el-form-item
        label="执行板版本号:"
        label-width="120px"
        prop="execute_version">
        <el-input
          :maxlength="255"
          v-model="form.execute_version"
          placeholder="请输入执行板版本号"
          clearable/>
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
  name: 'Product_handoverEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1, name: '',code : '',delivery_time : '',remark: ''}, this.data),
      // 表单验证规则
      rules: {
        time: [
          {required: true, message: '请输入日期', trigger: 'blur'}
        ],
        work_order: [
          {required: true, message: '请输入单号', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入客户名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
        remark:[
           {required: true, message: '请输入安数', trigger: 'blur'}
        ],
        delivery_time: [
          {required: true, message: '请输入交期', trigger: 'blur'},
        ],
        quantity: [
          { required: true, message: '请输入数量', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue <= 0) {
                callback(new Error('数量必须为大于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        control_version: [
          {required: true, message: '请输入主控板版本号', trigger: 'blur'}
        ],
        execute_version: [
          {required: true, message: '请输入执行板版本号', trigger: 'blur'}
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
    handleSelect(item) {
      this.form.work_order = item.value
      this.$refs.form.validateField('work_order', () => {});
      // 根据选择的单号查其他数据自动填入
      this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
        this.loading = false;
        const shipmentData = res.data.data;
        if (res.data.code === 0 && res.data.data != null) {
          this.form.name = shipmentData.product_name
          this.form.code  = shipmentData.shape
          this.form.delivery_time = shipmentData.delivery_date
          
          const regex = /\s[\S]+A/;  
          const match = shipmentData.shape.match(regex);  
          this.form.remark = match ? match[0] : '';
          if (this.form.remark === '') {
            const match = shipmentData.remark.match(regex);  
            this.form.remark = match ? match[0] : '';
          }
          this.disabled = true;
        } 
      })
    },
    handleClear(){
      this.form.name = ''
      this.form.code  = ''
      this.form.delivery_time = ''
      this.form.remark = ''
      this.disabled = false;
    },
    createStateFilter(queryString) {
        return (state) => {
          return (state.value.toLowerCase().includes(queryString.toLowerCase()));
        };
      },
    handleEnterKey(event){
      console.log("进入")
      console.log(event)
      this.form.work_order = event.target.value.split("+")[0];
      this.$refs.form.validateField('work_order', () => {});
      // 根据选择的单号查其他数据自动填入
      this.$http.get('/shipmentreport/detail/' + event.target.value.split("+")[0]).then((res) => {
        this.loading = false;
        const shipmentData = res.data.data;
        if (res.data.code === 0 && res.data.data != null) {
          this.form.name = shipmentData.client_name
          this.form.code  = shipmentData.shape
          this.form.delivery_time = shipmentData.delivery_date
          
          const regex = /\s[\S]+A/;  
          const match = shipmentData.shape.match(regex);  
          this.form.remark = match ? match[0] : '';
          if (this.form.remark === '') {
            const match = shipmentData.remark.match(regex);  
            this.form.remark = match ? match[0] : '';
          }
          this.disabled = true;
        } 
      })
    },
    // 监听workorder为空时解除其他输入框禁用
    checkWorkOrderIsNull(rule, value, callback){
        if (value == '') {
          this.form = {
            // product_name : '',
            // client_name : '',
            // product_count : '',
            // order_time : '',
            // shape : '',
            // submit_time : '',
            // product_module : '',
            // start_time:'',
            // finish_time:'',
            // work_hours:'',
            // welding_count:''
          };
          this.disabled = false;
        }
        callback();
      },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/product_handover/update' : '/product_handover/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {name: '',code : '',delivery_time: ''};
              }
              this.updateVisible(false);
              this.$emit('done');
            } else {
              this.$message.error(res.data.msg);
            }
            this.disabled = false;
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
    
  },
  mounted() {
    this.loadAll();
  }
}
</script>

<style scoped>
</style>
