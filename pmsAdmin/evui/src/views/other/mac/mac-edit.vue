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
        label="产品类型:"
        prop="code">
        <el-input
          :maxlength="255"
          v-model="form.code"
          placeholder="请输入产品类型"
          clearable/>
      </el-form-item>
      <el-form-item
        label="序列号:"
        prop="serial_id">
        <el-input
          :maxlength="255"
          v-model="form.serial_id"
          placeholder="请输入序列号"
          clearable/>
      </el-form-item>
      <el-form-item
        label="mac地址:"
        prop="mac_address">
        <el-input
          :maxlength="255"
          v-model="form.mac_address"
          placeholder="请输入mac地址(例如00:00:00:00:00:02)"
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
  name: 'MacEdit',
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
        // work_order: [
        //   {required: true, message: '请输入工单号', trigger: 'blur'}
        // ],
        // name: [
        //   {required: true, message: '请输入客户名称', trigger: 'blur'}
        // ],
        // code: [
        //   {required: true, message: '请输入产品型号', trigger: 'blur'}
        // ],
        // serial_id: [
        //   {required: true, message: '请输入序列号', trigger: 'blur'}
        // ],
        mac_address: [
          {required: true, message: '请输入mac地址', trigger: 'blur'}
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/mac/update' : '/mac/add', this.form).then(res => {
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
    }
  },
  mounted() {
      this.loadAll();
  }
}
</script>

<style scoped>
</style>
