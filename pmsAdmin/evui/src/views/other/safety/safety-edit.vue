<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改安规测试表':'添加安规测试表'"
    :visible="visible"
    width="800px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="102px">
      
      <el-row :gutter="10">
      <el-col :span="12">
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
            style="width: 273px;"
          ></el-autocomplete>  
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="软件类型:"
        prop="softwareType">
        <el-input
          :maxlength="255"
          v-model="form.softwareType"
          placeholder="请输入软件类型"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="产品类型:"
        prop="productType">
        <el-input
          :maxlength="255"
          v-model="form.productType"
          placeholder="请输入产品类型"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="产品序列号:"
        label-width="100px"
        prop="productSN">
        <el-input
          :maxlength="255"
          v-model="form.productSN"
          placeholder="请输入产品序列号"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>
      
      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="接地电阻:"
        prop="Gnd">
        <el-input
          :maxlength="255"
          v-model="form.Gnd"
          placeholder="请输入接地电阻"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="绝缘电阻:"
        prop="Ir">
        <el-input
          :maxlength="255"
          v-model="form.Ir"
          placeholder="请输入绝缘电阻"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="直流耐压:"
        prop="Dcw">
        <el-input
          :maxlength="255"
          v-model="form.Dcw"
          placeholder="请输入直流耐压"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="交流耐压:"
        prop="Acw">
        <el-input
          :maxlength="255"
          v-model="form.Acw"
          placeholder="请输入交流耐压"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="结果:"
        prop="result">
        <el-input
          :maxlength="255"
          v-model="form.result"
          placeholder="请输入结果"
          clearable/>
      </el-form-item>
      </el-col>
      
      <el-col :span="12">
      <el-form-item
        label="软件版本:"
        prop="softwareVersion">
        <el-input
          :maxlength="255"
          v-model="form.softwareVersion"
          placeholder="请输入软件版本"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>

      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="公司名称:"
        prop="companyName">
        <el-input
          :maxlength="255"
          v-model="form.companyName"
          placeholder="请输入公司名称"
          clearable/>
      </el-form-item>
      </el-col>

      <el-col :span="12">
      <el-form-item
        label="协议版本:"
        prop="protocolVersion">
        <el-input
          :maxlength="255"
          v-model="form.protocolVersion"
          placeholder="请输入协议版本"
          clearable/>
      </el-form-item>
      </el-col>
      </el-row>
      
      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item label="测试开始时间:"
      label-width="120px"
      prop="testStartTime">
        <el-date-picker
          class="ele-fluid"
          type="datetime"
          value-format="yyyy-MM-dd HH:mm:ss"
          v-model="form.testStartTime"
          placeholder="请选择测试开始时间"/>
      </el-form-item>
      </el-col>
      
      <el-col :span="12">
      <el-form-item label="测试结束时间:"
        label-width="120px"
        prop="testEndTime">
          <el-date-picker
            class="ele-fluid"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            v-model="form.testEndTime"
            placeholder="请选择测试结束时间"/>
      </el-form-item>
      </el-col>
      </el-row>
           
      <el-form-item label="测试时间:" prop="testTime">
        <el-input
          v-model="form.testTime"
          placeholder="请输入测试时间"
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
  name: 'SafetyEdit',
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
        //   {required: true, message: '请输入单号', trigger: 'blur'}
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
       
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,

      mk:false
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({ name: '',code : ''}, this.data);
        this.mk = false;
        this.isUpdate = true;
      }else if(this.data && this.data.mk){
        this.form = { name: '',code : ''};
        this.mk = true;
      }else {
        this.mk = false;
        this.form = { name: '',code : ''};
        this.isUpdate = false;
      }
    },
    
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
      // 根据选择的单号查其他数据自动填入
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/safety/update' : '/safety/add', this.form).then(res => {
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
.el-row {
  margin-bottom: 16px;

}
</style>
