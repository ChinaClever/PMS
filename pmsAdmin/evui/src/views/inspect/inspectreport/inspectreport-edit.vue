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
            prop="work_order">
            <el-autocomplete
            v-model="form.work_order"
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
            placeholder="选择日期">
          </el-date-picker>
          </el-form-item>
          <el-form-item
            label="开始时间:"
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
            prop="item_number">
            <el-input
              :maxlength="20"
              v-model="form.item_number"
              placeholder="请输入产品型号"
              clearable/>
          </el-form-item>
          <el-form-item
          label="产品名称:"
          prop="product_name">
          <el-input
            :maxlength="20"
            v-model="form.product_name"
            placeholder="请输入产品名称"
            clearable/>
        </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module" >
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item
            label="检验数量:"
            prop="examine_an_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_an_amount"
              placeholder="请输入检验数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验不良数量:"
            prop="examine_a_bad_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_a_bad_amount"
              placeholder="请输入检验不良数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验数量累计:"
            prop="examine_amount_total_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_amount_total_amount"
              placeholder="请输入检验数量累计"
              clearable/>
          </el-form-item>
          <el-form-item
            label="检验不良累计:"
            prop="examine_bad_total_amount">
            <el-input
              :maxlength="20"
              v-model="form.examine_bad_total_amount"
              placeholder="请输入检验不良累计"
              clearable/>
          </el-form-item>
          <el-form-item
            label="ERP目标合格率:"
            prop="target_pass_rate">
            <el-input
              :maxlength="20"
              v-model="form.target_pass_rate"
              placeholder="不填默认95%"
              clearable/>
          </el-form-item>
        </el-col>
          
       
      </el-row>
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
        ],
        start_time:[
          {
            required: true,
            trigger: 'blur'
          }
        ],
        product_module:[
          {
            required: true,
            trigger: 'blur'
          }
        ],
        product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        end_time:[
          {
            required: true,
            trigger: 'blur'
          },
          {
            validator: (rule, value, callback) => {
                // 获取订单日期的值
                const startTime = new Date(this.form.start_time);
                console.log(startTime);
                // 获取交货日期的值
                const endTime = new Date(value);
                console.log(endTime);
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
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.isUpdate = true;
      } else {
        this.form = {
          product_name : '',
          item_number: '',
          product_module:'',};
        this.isUpdate = false;
      }
    }
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
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
        } 
      })
    },
    handleClear(){
      this.form.product_name = ''
      this.form.item_number  = ''
      this.form.product_module = ''
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
          this.form.product_name = shipmentData.product_name
          this.form.item_number  = shipmentData.shape
          this.form.product_module = shipmentData.product_module
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
  },
  mounted() {
      this.loadAll();
  }
}
</script>

<style scoped>
</style>
