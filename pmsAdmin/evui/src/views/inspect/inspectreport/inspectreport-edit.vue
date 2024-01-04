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
            label="日期:"
            prop="date">
            <el-date-picker
            v-model="form.selectedDate"
            value-format="yyyy-MM-dd HH:mm"
            type="date"
            placeholder="选择日期(不填默认今天)">
          </el-date-picker>
          </el-form-item>
          <el-form-item
            label="开始时间:"
            ref="start_time"
            prop="start_time">
            <el-time-picker
              v-model="form.start_time"
              value-format="yyyy-MM-dd HH:mm"
              format="HH:mm"
              placeholder="任意时间点"
              @input="handleStartTimeInput">
            </el-time-picker>
          </el-form-item>
          <el-form-item
            label="结束时间:"
            ref="end_time"
            prop="end_time">
            <el-time-picker
              v-model="form.end_time"
              value-format="yyyy-MM-dd HH:mm"
              format="HH:mm"
              placeholder="任意时间点"
              @input="handleEndTimeInput">
            </el-time-picker>
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
        </el-col>
        <el-col :sm="12">
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
            label="检验数量:"
            ref="examine_an_amount"
            prop="examine_an_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_an_amount"
              placeholder="请输入检验数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验不良数量:"
            ref="examine_a_bad_amount"
            prop="examine_a_bad_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_a_bad_amount"
              placeholder="请输入检验不良数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验数量累计:"
            ref="examine_amount_total_amount"
            prop="examine_amount_total_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_amount_total_amount"
              placeholder="请输入检验数量累计"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验不良累计:"
            ref="examine_bad_total_amount"
            prop="examine_bad_total_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_bad_total_amount"
              placeholder="请输入检验不良累计"
              clearable/>
          </el-form-item>
          <el-form-item
            label="ERP目标合格率:"
            ref="target_pass_rate"
            prop="target_pass_rate">
            <el-input
              :maxlength="20"
              v-model="form.target_pass_rate"
              placeholder="不填默认95%"
              clearable/>
          </el-form-item>
        </el-col>
          
       
      </el-row>
      <br />
      <el-form-item label="问题:" prop="problems">
                  <el-input
                    v-model="form.problems"
                    :rows="3"
                    maxlength="200"
                    show-word-limit
                    type="textarea"/>
        </el-form-item>
      <el-form-item label="行动:" prop="actions">
                  <el-input
                    v-model="form.actions"
                    :rows="3"
                    maxlength="200"
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
import { mapGetters } from "vuex";

export default {
  name: 'InspectreportEdit',
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
        start_time:[
          {
            required: true,
            message: '请输入开始时间',
            trigger: 'blur'
          }
        ],
        product_module:[
          {
            required: true,
            message: '请选择成品或模块',
            trigger: 'blur'
          }
        ],
        product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        end_time:[
          {
            required: true,
            message: '请输入结束时间',
            trigger: 'blur'
          },
          {
            validator: (rule, value, callback) => {
                // 获取订单日期的值
                const startTime = new Date(this.form.start_time);
                // 获取交货日期的值
                const endTime = new Date(value);
                // 比较日期
                if (endTime <= startTime) {
                  callback(new Error('结束时间必须大于开始时间'));
                } else {
                  callback();
                }
            },
            trigger: 'blur'
          }
        ],
        item_number: [
          {required: true, message: '请输入产品型号', trigger: 'blur'}
        ],
        examine_an_amount:[
          {
            required: true, 
            message: '请输入检验数量', 
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
        examine_a_bad_amount:[
          {required: true, message: '请输入检验不良数量', trigger: 'blur'},
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
        examine_amount_total_amount:[
          {required: true, message: '请输入检验数量累计', trigger: 'blur'},
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
        examine_bad_total_amount:[
          {required: true, message: '请输入检验不良累计', trigger: 'blur'},
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
        target_pass_rate:[
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!intValue) {
                callback();
                return;
              }
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于等于0的整数'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
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
      if (this.data && this.data.id) {
      } else {
        this.form = {
          product_name : '',
          item_number: '',
          product_module:'',
          end_time : ''};
        this.form.end_time = this.demo(this.getNowTimes());
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
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/inspectreport/update' : '/inspectreport/add', this.form).then(res => {
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
    //时间四舍五入
    demo(timeStr) {
      timeStr = timeStr.replace(/-/g, '/')
      var oDate = new Date(timeStr)
      var stamp = oDate.getTime()
      var minute = oDate.getMinutes()
      var last = minute%10
      if(last > 4) {
        stamp += (10-last) * 60 * 1000
      } else {
        stamp -= last * 60 * 1000
      }
      oDate = new Date(stamp)

      var t = {
        year: this.pad_2_0(oDate.getFullYear()),
        month: this.pad_2_0(oDate.getMonth() + 1),
        day: this.pad_2_0(oDate.getDate()),
        hour: this.pad_2_0(oDate.getHours()),
        minute: this.pad_2_0(oDate.getMinutes()),
        second: this.pad_2_0(oDate.getSeconds())
      }

      var  res = t.year + '-' + t.month + '-' + t.day + ' ' + t.hour + ':' + t.minute;
      return res;
    },
    pad_2_0 (num) {
      return num >= 10 ? num : '0' + num
    },
    getNowTimes(){
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0');
      const date = String(currentDate.getDate()).padStart(2, '0');
      const hours = String(currentDate.getHours()).padStart(2, '0');
      const minutes = String(currentDate.getMinutes()).padStart(2, '0');
      const formattedDate = `${year}-${month}-${date} ${hours}:${minutes}`;
      return formattedDate;
    },
  },
  mounted() {
      this.loadAll();
  }
}
</script>

<style scoped>
</style>
