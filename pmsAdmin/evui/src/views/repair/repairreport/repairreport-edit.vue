<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改维修报表':'添加维修报表'"
    :visible="visible"
    width="1100px"
    :destroy-on-close="true"
    :lock-scroll="false"
    @update:visible="updateVisible">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="82px">
      <el-row :gutter="15">
        <el-col :sm="6">
          <el-form-item label="产品名称" prop="name">
            <el-autocomplete
              class="inline-input"
              v-model="form.name"
              :fetch-suggestions="querySearch4"
              placeholder="请输入产品名称"
              @select="handleSelect"
            ></el-autocomplete>
          </el-form-item>
          <el-form-item
            label="工单号:"
            prop="work_order">
            <el-input
              :maxlength="20"
              v-model="form.work_order"
              placeholder="请输入工单号"
              clearable/>
          </el-form-item>
          <!--<el-row class="demo-autocomplete">
            <el-col :span="12">
              <div class="sub-title">请输入不良现象</div>
              <el-autocomplete
                class="inline-input"
                v-model="form.bad_phenomenon"
                :fetch-suggestions="querySearch"
                placeholder="请输入内容"
                @select="handleSelect"
              ></el-autocomplete>
            </el-col>
          </el-row>-->
          <!--<el-form-item label="类型:" prop="type">
            <el-radio-group
              v-model="form.type">
              <el-radio :label="1">问题</el-radio>
              <el-radio :label="2">建议</el-radio>
              <el-radio :label="3">新需求</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :sm="12">
          <el-form-item
            label="优先级:"
            prop="priority">
            <el-input
              :maxlength="20"
              v-model="form.priority"
              placeholder="请输入优先级(1-10)"
              clearable/>
          </el-form-item>
          <el-form-item label="状态:" prop="status" v-if="permission.includes('sys:suggestion:status')">
            <el-radio-group
              v-model="form.status" >
              <el-radio :label="1">未查看</el-radio>
              <el-radio :label="2">确认</el-radio>
              <el-radio :label="3">完成</el-radio>
              <el-radio :label="4">未通过</el-radio>
            </el-radio-group>
          </el-form-item>-->
        </el-col>
        <el-col :sm="6">
          <el-form-item label="维修时间:" prop="repair_time">
            <el-date-picker
              v-model="form.repair_time"
              type="datetime"
              placeholder="选择日期时间"
            ></el-date-picker>
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
          <el-form-item
            label="维修数量:"
            prop="repair_number">
            <el-input
              :maxlength="20"
              v-model="form.repair_number"
              placeholder="请输入维修数量"
              clearable/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="不良现象" prop="bad_phenomenon">
        <el-autocomplete
          class="inline-input"
          v-model="form.bad_phenomenon"
          :fetch-suggestions="querySearch"
          placeholder="请输入不良现象"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="原因分析" prop="analysis">
        <el-autocomplete
          class="inline-input"
          v-model="form.analysis"
          :fetch-suggestions="querySearch2"
          placeholder="请输入内容"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="解决方法" prop="solution">
        <el-autocomplete
          class="inline-input"
          v-model="form.solution"
          :fetch-suggestions="querySearch3"
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
      form: Object.assign({status: 1,type : 1}, this.data),
      // 表单验证规则
      rules: {
        name:[
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        work_order:[
          {required: true, message: '请输入工单号', trigger: 'blur'}
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
        ]

      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      //维修时间
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date());
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', date);
          }
        }]
      },
      repair_time: null,
      //不良现象返回值
      bad_phenomenonlist: [],
      analysislist:[],
      solutionlist:[],
      namelist:[],
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
  computed: {
    ...mapGetters(["permission"])
    },
  methods: {
    formatDateTime(date1) {//修改时间格式
      var date = new Date(date1);
      var month = ("0" + (date.getMonth() + 1)).slice(-2);
      var day = ("0" + date.getDate()).slice(-2);
      var hours = ("0" + date.getHours()).slice(-2);
      var minutes = ("0" + date.getMinutes()).slice(-2);
      return date.getFullYear() + "-" + month + "-" + day + " " + hours + ":" + minutes;
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
                this.form = {};
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
      console.log(item);
      this.bad_phenomenonlist = this.loadbad_phenomenonlist(item.value);
      this.analysislist = this.loadanalysislist(item.value);
      this.solutionlist = this.loadsolutionlist(item.value);
    }
  },
  mounted() {
    this.loadnamelist();
  }
  
}

</script>
 
<style scoped>
</style>