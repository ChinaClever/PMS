<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改报表':'添加报表'"
    :visible="visible"
    width="1500px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="120px">
      <el-row :gutter="15">
        <el-col :sm="12">
          <el-form-item
            label="单号:"
            ref="work_order"
            prop="work_order">
            <el-autocomplete
            v-model="form.work_order"
            :disabled="isUpdate"
            clearable
            :fetch-suggestions="querySearchAsync"
            @select="handleSelect"
            @clear="handleClear"
            @keyup.enter.native="handleEnterKey"
            placeholder="请输入单号"
            style="width: 277px;"
          ></el-autocomplete>  
          </el-form-item>
          <el-form-item
            label="产品型号:"
            ref="item_number"
            prop="item_number">
            <el-input
              :maxlength="20"
              v-model="form.item_number"
              :disabled="disabled"
              placeholder="请输入产品型号"
              clearable/>
          </el-form-item>
          <el-form-item
          label="产品名称:"
          ref="product_name"
          prop="product_name">
          <el-input
            :maxlength="20"
            v-model="form.product_name"
            :disabled="disabled"
            placeholder="请输入产品名称"
            clearable/>
        </el-form-item>
        <el-form-item 
            label="成品/模块:" 
            ref="product_module"
            prop="product_module">
            <el-radio-group
              v-model="form.product_module" 
              :disabled="disabled">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item 
            label="返工原因:" 
            ref="rw_reason"
            prop="rw_reason">
            <el-radio-group
              v-model="form.rw_reason" 
             >
              <el-radio :label="1">物料不良/半成品/成品返工工时</el-radio>
              <el-radio :label="2">返工/正常作业/原料报废</el-radio>
              <el-radio :label="3">客户退回产品的维修</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item
            label="责任归属人:"
            ref="respon"
            prop="respon">
            <el-input
              :maxlength="20"
              v-model="form.respon"
              placeholder="请输入责任归属人"
              clearable/>
          </el-form-item>
          <el-form-item
            label="返工数量:"
            ref="rw_qty"
            prop="rw_qty">
            <el-input
              :maxlength="20"
              v-model="form.rw_qty"
              placeholder="请输入返工数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="损耗工时:"
            ref="loss_time"
            prop="loss_time">
            <el-input
              :maxlength="20"
              v-model="form.loss_time"
              placeholder="请输入损耗工时"
              clearable/>
          </el-form-item>
          
          <el-form-item
            label="损耗材料数量:"
            ref="loss_material_qty"
            prop="loss_material_qty">
            <el-input
              :maxlength="20"
              v-model="form.loss_material_qty"
              placeholder="请输入损耗材料数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="损耗材料名称:"
            ref="loss_material_name"
            prop="loss_material_name">
            <el-input
              v-model="form.loss_material_name"
              placeholder="请输入损耗材料名称"
              clearable/>
          </el-form-item>
        </el-col>
      </el-row>
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
import { mapGetters } from "vuex";

export default {
  name: 'ReworkEdit',
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object
  },
  data() {
    return {
      work_orders: [],
      state: '',
      timeout:  null,
      // 表单数据
      form: Object.assign({ 
        product_name : '',
        item_number: '',
        product_module:'',
      }, this.data),
      // 表单验证规则
      rules: {
        work_order:[
          {required: true, message: '请输入单号', trigger: 'blur'},
          {validator:(rule,value,callback)=> this.checkWorkOrderIsNull(rule, value, callback)}
        ],
        product_module:[
          {
            required: true,
            message: '请选择成品或模块',
            trigger: 'blur'
          }
        ],
        rw_reason: [
          {required: true, message: '请选择返工原因', trigger: 'blur'}
        ],
        respon: [
          {required: true, message: '请输入责任负责人', trigger: 'blur'}
        ],
        product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        item_number: [
          {required: true, message: '请输入产品型号', trigger: 'blur'}
        ],
        rw_qty:[
          {
            required: true, 
            message: '请输入返工数量', 
            trigger: 'blur'
          },
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于等于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        loss_time:[
          {required: true, message: '请输入损耗工时', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于等于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        loss_material_qty:[
          {required: true, message: '请输入损耗材料数量', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于等于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        loss_material_name:[
          {required: true, message: '请输入损耗材料名词', trigger: 'blur'}
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      disabled:false
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.isUpdate = true;
        this.disabled=true;
      } else {
        this.form = {
          product_name : '',
          item_number: '',
          product_module:'',};

        this.isUpdate = false;
        this.disabled = false;
      }
    },
    visible(){
      if (!(this.data && this.data.id)) {
        this.form = {
          product_name : '',
          item_number: '',
          product_module:'',
        };
      }
    }
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid,object) => {
        if (valid) {
          this.loading = true;
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/rework/update' : '/rework/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {
                  product_name : '',
                  item_number: '',
                  product_module:'',};
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
          let dom = this.$refs[Object.keys(object)[0]];
          if (Object.prototype.toString.call(dom) !== "[object Object]") {
            dom = dom[0];
          }
          // 定位代码
          dom.$el.scrollIntoView({
            block: "center",
            behavior: "smooth",
          });
          return false;
        }
      });
    },
    /* 更新visible */
    updateVisible(value) {
      this.$emit('update:visible', value);
    },
    isNubmer(rule, value, callback) {
      const intValue = Number(value);
      if (!Number.isInteger(intValue) || intValue <= 0) {
        callback(new Error('数量必须为大于0的整数'));
      } else {
        callback();
      }
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
      var filteredResults = queryString ? work_orders.filter(this.createStateFilter(queryString)) : work_orders;
      var results = filteredResults.slice(0, 10); // 限制结果最多显示10条

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 300 * Math.random());
    },
    createStateFilter(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
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
          this.form.product_name = shipmentData.product_name
          this.form.item_number  = shipmentData.shape
          this.form.product_module = shipmentData.product_module
          this.disabled=true;
        } 
      })
    },
    handleClear(){
      this.form.work_order=''
      this.form.product_name = ''
      this.form.item_number  = ''
      this.form.product_module = ''
      this.disabled=false;
    },
    handleEnterKey(event){
      this.form.work_order = event.target.value.split("+")[0];
      this.$refs.form.validateField('work_order', () => {});
      // 根据选择的单号查其他数据自动填入
      this.$http.get('/shipmentreport/detail/' + event.target.value.split("+")[0]).then((res) => {
        this.loading = false;
        const shipmentData = res.data.data;
        if (res.data.code === 0 && res.data.data != null) {
          this.form.product_name = shipmentData.product_name
          this.form.item_number  = shipmentData.shape
          this.form.product_module = shipmentData.product_module
          this.disabled=true;
        } 
      })
    },
    handleStartTimeInput(value){
      if (value) {
        const currentDate = new Date();
        const currentDateString = currentDate.toISOString().split('T')[0];
        const timeString = value.split(' ')[1];
        const dateTimeString = `${currentDateString} ${timeString}`;
        this.form.start_time = dateTimeString;
      }
    },
    handleEndTimeInput(value) {
      if (value) {
        const currentDate = new Date();
        const currentDateString = currentDate.toISOString().split('T')[0];
        const timeString = value.split(' ')[1];
        const dateTimeString = `${currentDateString} ${timeString}`;
        this.form.end_time = dateTimeString;
      }
    },
    checkWorkOrderIsNull(rule, value, callback){
      if (value == '') {
        this.form.work_order=''
        this.form.product_name = ''
        this.form.item_number  = ''
        this.form.product_module = ''
        this.disabled=false;
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
.el-radio {
    display: block;
  }
</style>
