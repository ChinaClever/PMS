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
            <el-form-item
              label="产品名称:"
              prop="name">
              <el-input
                :maxlength="20"
                v-model="form.name"
                placeholder="请输入产品名称"
                clearable/>
            </el-form-item>
            <el-form-item
              label="工单号:"
              prop="name">
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
          </el-col>
        </el-row>
        <el-form-item label="不良现象" prop="bad_phenomenon">
          <el-autocomplete
            class="inline-input"
            v-model="form.bad_phenomenon"
            :fetch-suggestions="querySearch"
            placeholder="请输入内容"
            @select="handleSelect"
          ></el-autocomplete>
        </el-form-item>
        <el-form-item label="原因分析:" prop="analysis">
                    <el-input
                      v-model="form.analysis"
                      :rows="4"
                      maxlength="150"
                      show-word-limit
                      type="textarea"/>
        </el-form-item>
        <el-form-item label="解决方法:" prop="solution">
                    <el-input
                      v-model="form.solution"
                      :rows="4"
                      maxlength="150"
                      show-word-limit
                      type="textarea"/>
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
          type:[
            {required: true, trigger: 'blur'}
          ],
          status:[
            {required: true, trigger: 'blur'}
          ],
          content: [
            {required: true, message: '请输入', trigger: 'blur'}
          ],
          priority:[
            {required: true, message: '请输入优先值', trigger: 'blur'}
          ],
          bad_number:[
            {
              validator: (bad_number, value, callback) => {
                const intValue = Number(value);
                if (!Number.isInteger(intValue) || intValue < 0) {
                  callback(new Error('数量必须为大于0的整数'));
                } else {
                  callback();
                }
              },
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
        repair_time: '',
        //不良现象返回值
        restaurants: [],
        bad_phenomenon: '',


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
    /* 保存编辑 */
      formatDateTime(date1) {//修改时间格式
        var date = new Date(date1);
        var month = ("0" + (date.getMonth() + 1)).slice(-2);
        var day = ("0" + date.getDate()).slice(-2);
        var hours = ("0" + date.getHours()).slice(-2);
        var minutes = ("0" + date.getMinutes()).slice(-2);
        return date.getFullYear() + "-" + month + "-" + day + " " + hours + ":" + minutes;
      },
      save() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.loading = true;
            this.form.repair_time = this.formatDateTime(this.form.repair_time)
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
        var restaurants = this.restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      loadAll() {
        return [
          { "value": "三全鲜食（北新泾店）", "address": "长宁区新渔路144号" },
          { "value": "Hot honey 首尔炸鸡（仙霞路）", "address": "上海市长宁区淞虹路661号" },
          { "value": "新旺角茶餐厅", "address": "上海市普陀区真北路988号创邑金沙谷6号楼113" },
          { "value": "泷千家(天山西路店)", "address": "天山西路438号" },
          { "value": "胖仙女纸杯蛋糕（上海凌空店）", "address": "上海市长宁区金钟路968号1幢18号楼一层商铺18-101" },

        ];
      },
      handleSelect(item) {
        console.log(item);
      }
    },
    mounted() {
      this.restaurants = this.loadAll();
    }
    
  }
  
  </script>
   
  <style scoped>
  </style>