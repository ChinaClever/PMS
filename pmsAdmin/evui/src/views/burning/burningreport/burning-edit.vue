<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改客户':'添加客户'"
    :visible="visible"
    width="460px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-form-item
            label="工单号:"
            prop="work_order">
            <el-autocomplete
            v-model="form.work_order"
            clearable
            :fetch-suggestions="querySearchAsync"
            @select="handleSelect"
            @clear="handleClear"
            @keyup.enter.native="handleEnterKey"
            placeholder="请输入工单号"
            style="width: 277px;"
          ></el-autocomplete>  
          </el-form-item>
      <el-form-item
        label="客户名称:"
        prop="name">
        <el-input
          :maxlength="255"
          v-model="form.name"
          placeholder="请输入客户名称"
          clearable/>
      </el-form-item>
      <el-form-item
        label="规格型号:"
        prop="code">
        <el-input
          :maxlength="255"
          v-model="form.code"
          placeholder="请输入规格型号"
          clearable/>
      </el-form-item>
      <el-form-item
        label="版本号:"
        prop="version">
        <el-input
          :maxlength="255"
          v-model="form.version"
          placeholder="请输入版本号"
          clearable/>
      </el-form-item>
      <el-form-item
        label="程序要求:"
        prop="require">
        <el-input
          :maxlength="255"
          v-model="form.require"
          placeholder="请输入程序要求"
          clearable/>
      </el-form-item>
      <el-form-item
        label="订单日期:"
        prop="order_time">
        <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.order_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择订单日期"/>
      </el-form-item>
      <el-form-item
        label="交货日期:"
        prop="delivery_time">
        <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.delivery_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择交货日期"/>
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
        label="备注:"
        prop="remark">
        <el-input
          :maxlength="255"
          v-model="form.remark"
          placeholder="请输入备注"
          clearable/>
      </el-form-item>
      <el-form-item
        label="rcerder:"
        prop="rcerder">
        <el-input
          :maxlength="255"
          v-model="form.rcerder"
          placeholder="请输入rcerder"
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
  name: 'BurningEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({status: 1, name: '',code : ''}, this.data),
      // 表单验证规则
      rules: {
        work_order: [
          {required: true, message: '请输入工单号', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入客户名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
        version: [
          {required: true, message: '请输入版本号', trigger: 'blur'}
        ],
        require: [
          {required: true, message: '请输入程序要求', trigger: 'blur'}
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
        order_time: [
          {required: true, message: '请输入订单日期', trigger: 'blur'}
        ],
        delivery_time: [
          {required: true, message: '请输入交货日期', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              // 获取订单日期的值
              const orderTime = new Date(this.form.order_time);
              // 获取交货日期的值
              const deliveryTime = new Date(value);
              // 比较日期
              if (deliveryTime <= orderTime) {
                callback(new Error('交货日期必须大于订单日期'));
              } else {
                callback();
              }
            },
            trigger: 'change'
          }
        ],
        rcerder: [
          {required: true, message: '请输入rcerder', trigger: 'blur'}
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.isUpdate = true;
      } else {
        this.form = {};
        this.isUpdate = false;
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
      // 根据选择的工单号查其他数据自动填入
      this.$http.get('/shipmentreport/detail/' + item.value).then((res) => {
        this.loading = false;
        const shipmentData = res.data.data;
        if (res.data.code === 0 && res.data.data != null) {
          this.form.name = shipmentData.product_name
          this.form.code  = shipmentData.shape
     
        } 
      })
    },
    handleClear(){
      this.form.name = ''
      this.form.code  = ''
    },
    handleEnterKey(event){
      console.log("进入")
      console.log(event)
      this.form.work_order = event.target.value.split("+")[0];
      this.$refs.form.validateField('work_order', () => {});
      // 根据选择的工单号查其他数据自动填入
      this.$http.get('/shipmentreport/detail/' + event.target.value.split("+")[0]).then((res) => {
        this.loading = false;
        const shipmentData = res.data.data;
        if (res.data.code === 0 && res.data.data != null) {
          this.form.name = shipmentData.client_name
          this.form.code  = shipmentData.shape
         
        } 
      })
    },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/burningreport/update' : '/burningreport/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {name: '',code : ''};
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
    
  },
  mounted() {
    this.loadAll();
  }
}
</script>

<style scoped>
</style>
