<!-- 职级编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改烧录报表':'添加烧录报表'"
    :visible="visible"
    width="800px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="100px">
      <el-row :gutter="10">
      <el-col :span="12">
      <el-form-item
        label="单号:"
        prop="work_order">
          <el-autocomplete
          :disabled="isUpdate"
          v-model="form.work_order"
          :fetch-suggestions="querySearchAsync"
          @select="handleSelect"
          @clear="handleClear"
          @keyup.enter.native="handleEnterKey"
          placeholder="请输入单号"
          clearable
          style="width: 277px;"
        ></el-autocomplete>  
      </el-form-item>
    </el-col>
    
      <el-col :span="12">
        <el-form-item
        label="客户名称:"
        prop="name">
        <el-input
        :disabled="disabled"  
        v-model="form.name"
          placeholder="请输入客户名称"
          clearable/>
      </el-form-item>
      </el-col>
    </el-row>
    
    <el-row :gutter="10">
    <el-col :span="12">    
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
    </el-col>

    <el-col :span="12">
      <el-form-item
        label="订单数量:"
        prop="quantity">
        <el-input
        :disabled="disabled"  
        :maxlength="20"
          v-model="form.quantity"
          placeholder="请输入订单数量"
          clearable/>
      </el-form-item>
    </el-col>
    </el-row> 

    <el-row :gutter="6">
    <el-col :span="12">  
      <el-form-item
        label="订单日期:"
        prop="order_time">
        <el-date-picker
        :disabled="disabled"      
        type="date"
              class="ele-fluid"
              v-model="form.order_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择订单日期"/>
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item
        label="交货日期:"
        prop="delivery_time">
        <el-date-picker
        :disabled="disabled"      
        type="date"
              class="ele-fluid"
              v-model="form.delivery_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择交货日期"/>
      </el-form-item>
    </el-col>
    </el-row>

    <el-row :gutter="6">
    <el-col :span="12">
      <el-form-item
        label="* 软件版本号:"
        prop="version">
        <el-input
          :maxlength="255"
          v-model="form.version"
          placeholder="请输入软件版本号"
          clearable/>
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item
        label="* 程序要求:"
        prop="require">
        <el-input
          :maxlength="255"
          v-model="form.require"
          placeholder="请输入程序要求"
          clearable/>
      </el-form-item>
    </el-col>
    </el-row>
    
    <el-row>
      <el-table :data="dataTable" editable>
        <el-table-column prop="start_time" label="开始时间">
          <template slot-scope="scope">
            <el-date-picker
              class="ele-fluid"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              :id="`part_code_inputId_` + scope.$index"
              v-model="scope.row.start_time"
              placeholder="请选择开始时间"/>
          </template>
        </el-table-column>
        <el-table-column prop="finish_time" label="完成时间">
          <template slot-scope="scope">
            <el-date-picker
              class="ele-fluid"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
               v-model="scope.row.finish_time"
               placeholder="请选择完成时间"/>
          </template>
        </el-table-column>
        <el-table-column prop="work_hours" label="工时">
          <template slot-scope="scope">
            <el-input v-model="scope.row.work_hours"></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="PCB_code" label="PCB编码">
          <template slot-scope="scope">
            <el-input v-model="scope.row.PCB_code"></el-input>
          </template>
        </el-table-column>
      </el-table>
      <el-button @click="addInput">添加输入框</el-button>
        <el-button v-if="this.dataTable && this.dataTable.length > 0" @click="removeInput">删除最后一个输入框</el-button>
     </el-row>

    <el-row :gutter="6">
    <el-col :span="12">
      <el-form-item
        label="烧录数量:"
        prop="burning_quantity">
        <el-input
          :maxlength="20"
          v-model="form.burning_quantity"
          placeholder="请输入烧录数量"
          clearable/>
      </el-form-item>
    </el-col>
    </el-row>

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
        label="* rcerder:"
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
      form: Object.assign({status: 1, name: '',code : '',dataTable : [],}, this.data),
      // 物料表格
      dataTable:[
        { start_time: '', finish_time: '' , work_hours: '',PCB_code:'' }
      ],
      // 表单验证规则
      rules: {
        work_order: [
          {required: true, message: '请输入单号', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入客户名称', trigger: 'blur'}
        ],
        code: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
        
        quantity: [
          { required: true, message: '请输入订单数量', trigger: 'blur' },
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
        burning_quantity: [
          { required: true, message: '请输入烧录数量', trigger: 'blur' },
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
        
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 表格索引
      dataTableIndex: 0,
      // 是否禁用输入框
      disabled: false,
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.dataTable=this.data.burndata
        this.isUpdate = true;
        this.disabled = true;
      } else {
        this.form = {};
        this.dataTable=[{ start_time: '', finish_time: '' , work_hours: '' ,PCB_code: '',}];
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
          this.form.quantity  = shipmentData.product_count
          this.form.order_time  = shipmentData.order_date
          this.form.delivery_time  = shipmentData.delivery_date
          this.disabled = true;
     
        } 
      })
    },
    handleClear(){
      this.form.name = ''
      this.form.code  = ''
      this.form.quantity  = ''
      this.form.order_time  = ''
      this.form.delivery_time  =  ''
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
          this.form.quantity  = shipmentData.product_count
          this.form.order_time  = shipmentData.order_date
          this.form.delivery_time  = shipmentData.delivery_date
          this.disabled = true;
        } 
      })
    },
    // 监听workorder为空时解除其他输入框禁用
    checkWorkOrderIsNull(rule, value, callback){
        if (value == '') {
          this.form = {
          };
          this.disabled = false;
        }
        callback();
      },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          const PCBCodes = [...this.dataTable.map(item => item.PCB_code)];
          if(new Set(PCBCodes).size !== PCBCodes.length){
            this.$message.error({ message: "PCB编码重复", duration: 3000});
            return false;
          }
          else if(new Set(PCBCodes).has('')){
            this.$message.error({ message: "PCB不能为空", duration: 3000});
            return false;
          }


          const start_timeString = this.dataTable.map(item => item.start_time).join(',');
          const finish_timeString = this.dataTable.map(item => item.finish_time).join(',');
          const work_hoursString = this.dataTable.map(item => item.work_hours).join(',');
          const PCB_codeString = this.dataTable.map(item => item.PCB_code).join(',');
          this.form.start_time = start_timeString;
          this.form.finish_time = finish_timeString;
          this.form.work_hours = work_hoursString;
          this.form.PCB_code = PCB_codeString;
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/burningreport/update' : '/burningreport/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {};
                this.dataTable = [{ start_time: '', finish_time: '' , work_hours: '', PCB_code:'',}];
                this.dataTableIndex = 0;
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
    // 输入框检测到回车触发
    addInput() {
        this.dataTable.push(
        {
          start_time: '', 
          finish_time: '', 
          work_hours: '',
          PCB_code:''
        });     
    },
    //删除行
    removeInput() {
      this.dataTable.pop();
        if (this.dataTable.length === 0) {
        this.dataTable.push({ start_time: '', finish_time: '', work_hours: '' ,PCB_code:''}); 
      }
      
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
