<!-- 通知编辑弹窗 -->
<template>
  <el-dialog
    :title="isUpdate?'修改报表':'添加报表'"
    :visible="visible"
    width="1100px"
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
            label="工单号:"
            prop="work_order_id">
            <el-input
              :maxlength="20"
              v-model="form.work_order_id"
              placeholder="请输入工单号"
              clearable/>
          </el-form-item>
          <el-form-item
            label="开始时间:"
            prop="start_time">
            <el-time-picker
              v-model="form.start_time"
              value-format="yyyy-MM-dd HH:mm"
              format="HH:mm"
              placeholder="任意时间点">
            </el-time-picker>
          </el-form-item>
          <el-form-item
            label="结束时间:"
            prop="end_time">
            <el-time-picker
              v-model="form.end_time"
              value-format="yyyy-MM-dd HH:mm"
              format="HH:mm"
              placeholder="任意时间点">
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
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        work_order_id:[
          {required: true, message: '请输入工单号', trigger: 'blur'},
        ],
        start_time:[
          {
            required: true,
            trigger: 'blur'}
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
        this.form = {};
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
    formatDateTime(date1) {
      var date = new Date(date1);
      var month = ("0" + (date.getMonth() + 1)).slice(-2);
      var day = ("0" + date.getDate()).slice(-2);
      var hours = ("0" + date.getHours()).slice(-2);
      var minutes = ("0" + date.getMinutes()).slice(-2);
      return date.getFullYear() + "-" + month + "-" + day + " " + hours + ":" + minutes;
    },
    isNubmer(rule, value, callback) {
              const intValue = Number(value);
              if (!Number.isInteger(intValue) || intValue <= 0) {
                callback(new Error('数量必须为大于0的整数'));
              } else {
                callback();
              }
            }
  }
}
</script>

<style scoped>
</style>
