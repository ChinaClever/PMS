<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改维修报表':'添加维修报表'"
    :visible="visible"
    width="800px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-row :gutter="15" >
        <el-col :span="10">
          <el-form-item
            label="单号:"
            prop="work_order">
            <el-autocomplete
            :disabled="isUpdate"
            v-model="form.work_order"
            clearable
            :fetch-suggestions="querySearchAsync"
            @select="handleSelect1"
            @clear="handleClear"
            @keyup.enter.native="handleEnterKey"
            placeholder="请输入单号"
          ></el-autocomplete>  
          </el-form-item>
          <el-form-item
            label="不良数量:"
            prop="bad_number">
            <el-input
              :maxlength="20"
              v-model="form.bad_number"
              placeholder="请输入不良数量"
              clearable/>
          </el-form-item>
          <el-form-item label="维修时间:" prop="repair_time">
            <el-date-picker
              class="ele-fluid"
              v-model="form.repair_time"
              type="date"
              format="yyyy-MM-dd"
              placeholder="选择日期时间"
            ></el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="产品名称" prop="name">
            <el-autocomplete
              class="inline-input"
              v-model="form.name"
              :fetch-suggestions="querySearch4"
              placeholder="请输入产品名称"
              :disabled="disabled"
              @select="handleSelect"
            ></el-autocomplete>
          </el-form-item>
          <el-form-item
            label="维修数量:"
            prop="repair_number">
            <el-input
              :maxlength="20"
              v-model="form.repair_number"
              placeholder="请输入维修数量"
              clearable/>
          </el-form-item>
          <el-form-item
            label="工时:"
            prop="work_hours">
            <el-input
              :maxlength="20"
              v-model="form.work_hours"
              placeholder="请输入工时"
              clearable/>
          </el-form-item>
          
        </el-col>
      </el-row>
      <el-row :gutter="15" class="row-spacing" >
      <el-form-item label="不良现象" prop="bad_phenomenon">
        <el-autocomplete
          class="inline-input"
          v-model="form.bad_phenomenon"
          :fetch-suggestions="querySearch"
          style="width: 100%;"
          placeholder="请输入不良现象"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="原因分析" prop="analysis">
        <el-autocomplete
          class="inline-input"
          v-model="form.analysis"
          :fetch-suggestions="querySearch2"
          style="width: 100%;"
          placeholder="请输入内容"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="解决方法" prop="solution">
        <el-autocomplete
          class="inline-input"
          v-model="form.solution"
          :fetch-suggestions="querySearch3"
          style="width: 100%;"
          placeholder="请输入内容"
        ></el-autocomplete>
      </el-form-item>         
      <el-form-item label="备注:" prop="notes" >
                  <el-input
                    v-model="form.notes"
                    :rows="4"
                    maxlength="150"
                    show-word-limit
                    type="textarea"/>
      </el-form-item>
      </el-row>
      <!--<div class="block">
        <span class="demonstration">维修时间</span>
           <el-date-picker
           v-model="form.repair_time"
          type="datetime"
           placeholder="选择日期时间">
          </el-date-picker>
      </div>-->
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
  name: 'NoticeEdit',
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
        name:'',
        repair_time:new Date().toISOString()
      }, this.data),
      // 表单验证规则
      rules: {
        name:[
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        work_order:[
          {required: true, message: '请输入单号', trigger: 'blur'},
          {validator: (rule, value, callback) => this.checkWorkOrderIsNull(rule, value, callback)},
        ],
        bad_number:[
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于0的整数'));
              } else {
                callback();
              }
            },
            required: true,
            trigger: 'blur'
          }
        ],
        repair_number:[
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              const badValue= this.form.bad_number

              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为大于0的整数'));
              } else if(intValue>badValue){
                callback(new Error('维修数量必须小于等于不良数量'))
              }
              else {
                callback();
              }
            },
            required: true,
            trigger: 'blur'
          }
        ],
        work_hours:[
          {
            validator: (rule, value, callback) => {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue < 0) {
                callback(new Error('数量必须为非负的整数'));
              } else {
                callback();
              }
            },
            required: true,
            trigger: 'blur'
          }
        ],


      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      //一键填入
      work_orders: [],
      state: '',
      timeout:  null,
      
      repair_time: null,
      //不良现象返回值
      bad_phenomenonlist: [],
      analysislist:[],
      solutionlist:[],
      namelist:[],
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
        this.form = {repair_time:new Date().toISOString()};
        this.isUpdate = false;
        this.disabled = false;
      }
    },
      
  },
  computed: {
    ...mapGetters(["permission"])
    },
  methods: {
    getCurrentTime() {
    return new Date().toISOString();
  },
    formatDateTime(date1) {//修改时间格式
      var date = new Date(date1);
      var month = ("0" + (date.getMonth() + 1)).slice(-2);
      var day = ("0" + date.getDate()).slice(-2);
      //var hours = ("0" + date.getHours()).slice(-2);
      //var minutes = ("0" + date.getMinutes()).slice(-2);
      return date.getFullYear() + "-" + month + "-" + day 
    },
    /* 保存编辑 */
    save() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true;
          if(this.form.repair_time){
          this.form.repair_time = this.formatDateTime(this.form.repair_time)}
          this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/repairreport/update' : '/repairreport/add', this.form).then(res => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              if (!this.isUpdate) {
                this.form = {name:'',repair_time:new Date().toISOString()};
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
    //不良现象实现方法
    querySearch(queryString, cb) {
      var bad_phenomenonlist = this.bad_phenomenonlist;
      var results = queryString ? bad_phenomenonlist.filter(this.createFilter(queryString)) : bad_phenomenonlist;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    querySearch2(queryString, cb){
      var analysislist = this.analysislist;
      var results = queryString ? analysislist.filter(this.createFilter(queryString)) : analysislist;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    querySearch3(queryString, cb){
      var solutionlist = this.solutionlist;
      var results = queryString ? solutionlist.filter(this.createFilter(queryString)) : solutionlist;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    querySearch4(queryString, cb){
      var namelist = this.namelist;
      var results = queryString ? namelist.filter(this.createFilter(queryString)) : namelist;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (namelist) => {
        return (namelist.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    loadnamelist() {
      this.$http['get']('/repairreport/namelist').then(res => {
        this.namelist = res.data.data;
      }).catch(e => {
          this.loading = false;
          this.$message.error(e.message);
        });
      
    },
    loadbad_phenomenonlist(name) {
      this.$http['get']('/repairreport/bad_phenomenonlist'+'?name='+name).then(res => {
        this.bad_phenomenonlist = res.data.data;
        }).catch(e => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    loadanalysislist(name) {
      this.$http['get']('/repairreport/analysislist'+'?name='+name).then(res => {
        this.analysislist = res.data.data;
        }).catch(e => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    loadsolutionlist(name) {
      this.$http['get']('/repairreport/solutionlist'+'?name='+name).then(res => {
        this.solutionlist = res.data.data;
        }).catch(e => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    
    handleSelect(item) {
      this.$refs.form.validateField('name'); // 手动触发验证
      this.bad_phenomenonlist = this.loadbad_phenomenonlist(item.value);
      this.analysislist = this.loadanalysislist(item.value);
      this.solutionlist = this.loadsolutionlist(item.value);
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
              this.form.name = shipmentData.product_name
              this.bad_phenomenonlist = this.loadbad_phenomenonlist(shipmentData.product_name);
              this.analysislist = this.loadanalysislist(shipmentData.product_name);
              this.solutionlist = this.loadsolutionlist(shipmentData.product_name);
              this.disabled=true
            } 
          })
      },

      handleClear(){
        // this.form={
        //   name:''
        // }
        this.form.name='';
        this.form.work_order = ''
        this.disabled=false
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
          this.form.name = shipmentData.product_name
          this.bad_phenomenonlist = this.loadbad_phenomenonlist(shipmentData.product_name);
          this.analysislist = this.loadanalysislist(shipmentData.product_name);
          this.solutionlist = this.loadsolutionlist(shipmentData.product_name);
          this.disabled=true
        }
      })
      this.disabled=true
    },
        // 监听workorder为空时解除其他输入框禁用
    checkWorkOrderIsNull(rule, value, callback){
      if (value == '') {
        this.disabled = false;
        // this.form={
        //   name:''
        // }
        this.form.name=''
        this.form.work_order = ''
      }
      callback();
    },

  },
  mounted() {
    this.loadnamelist();
    this.loadAll();
  }
  
}

</script>
 
<style scoped>

.row-spacing {
  margin-top: 20px; /* 调整第二个 <el-row> 的顶部间距 */
}
</style>