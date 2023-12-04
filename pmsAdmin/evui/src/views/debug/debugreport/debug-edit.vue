<!-- 编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改调试报表':'添加调试报表'"
      :visible="visible"
      width="580px"
      :destroy-on-close="true"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="100px">

        <el-form-item
          label="工单号:"
          prop="work_order">
          <el-input
            v-model="form.work_order"
            placeholder="请输入工单号"
            clearable/>
        </el-form-item>

        <el-form-item label="下单日期:" prop="order_time">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.order_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择下单日期"/>
          </el-form-item>

        <el-form-item
          label="客户名称:"
          prop="client_name">
          <el-input
            :maxlength="20"
            v-model="form.client_name"
            placeholder="请输入客户名称"
            clearable/>
        </el-form-item>

        <el-form-item
          label="规格型号:"
          prop="shape">
          <el-input
            :maxlength="20"
            v-model="form.shape"
            placeholder="请输入规格型号"
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

        <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module" >
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
          </el-form-item>

        <el-form-item label="数量:" prop="product_count">
          <el-input-number
            :min="0"
            v-model="form.product_count"
            placeholder="请输入产品数量"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>

        <el-form-item label="交期:" prop="submit_time">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.submit_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择交期"/>
          </el-form-item>

          <el-form-item label="开始日期:" prop="start_time">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.start_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择开始日期"/>
          </el-form-item>

          <el-form-item label="完成日期:" prop="finish_time" >
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.finish_time"
              value-format="yyyy-MM-dd"
              placeholder="请选择完成日期"/>
          </el-form-item>

          <el-form-item label="所用工时:" prop="work_hours">
          <el-input-number
            :min="0"
            v-model="form.work_hours"
            placeholder="请输入所用工时"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>

        <el-form-item label="具体说明:" prop="instruction">
            <el-input
              :rows="3"
              clearable
              type="textarea"
              :maxlength="200"
              v-model="form.instruction"
              placeholder="请输入具体说明"/>
          </el-form-item>

          <el-form-item label="备注:" prop="remark">
            <el-input
              clearable
              :rows="3"
              type="textarea"
              :maxlength="200"
              v-model="form.remark"
              placeholder="请输入备注"/>
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
    name: 'DebugEdit',
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
          work_order: [
          {required: true, message: '请输入工单号', trigger: 'blur'}
        ],
          order_time: [
          {required: true, message: '请输入下单时间', trigger: 'blur'}
        ],
          client_name: [
          {required: true, message: '请输入客户名称', trigger: 'blur'}
        ],
          shape: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
          product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
          product_count: [
          {required: true, message: '请输入产品数量', trigger: 'blur'}
        ],
          submit_time: [
          {required: true, message: '请输入交期', trigger: 'blur'}
        ],
          start_time: [
          {required: true, message: '请输入开始时间', trigger: 'blur'}
        ],
          finish_time: [
          {required: true, message: '请输入完成时间', trigger: 'blur'},
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
          work_hours: [
          {required: true, message: '请选择工时', trigger: 'blur'},
        ],
          product_module: [
          {required: true, message: '请选择成品/模块', trigger: 'blur'},
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
      /* 保存编辑 */
      save() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.loading = true;
            this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/debugreport/update' : '/debugreport/add', this.form).then(res => {
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

      // 自定义校验规则函数
      checkFinishTime(rule, value, callback) {
        const startTime = this.form.start_time; // 获取开始日期的值
        const finishTime = value; // 获取完成日期的值

        if (!startTime || !finishTime) {
          callback(); // 如果开始日期或完成日期为空，则不进行校验
        } else if (startTime > finishTime) {
          callback(new Error('完成日期必须晚于开始日期')); // 如果完成日期早于开始日期，则返回错误信息
        } else {
          callback(); // 校验通过
        }
      }
    }
  }
  </script>

  <style scoped>
  </style>

