<!-- 编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改调试数据':'添加调试数据'"
      :visible="visible"
      width="650px"
      :destroy-on-close="true"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="120px">

        <el-form-item
          label="软件类型:"
          prop="softwareType">
          <el-input
            v-model="form.softwareType"
            placeholder="请输入软件类型"
            clearable/>
        </el-form-item>

        <el-form-item
          label="产品类型:"
          prop="productType">
          <el-input
            v-model="form.productType"
            placeholder="请输入产品类型"
            clearable/>
        </el-form-item>

        <el-form-item
          label="产品SN:"
          prop="productSN">
          <el-input
            v-model="form.productSN"
            placeholder="请输入产品SN"
            clearable/>
        </el-form-item>

        <el-form-item
          label="mac地址:"
          prop="macAddress">
          <el-input
            v-model="form.macAddress"
            placeholder="请输入mac地址"
            clearable/>
        </el-form-item>

        <!-- <el-form-item
          label="测试步骤:"
          prop="testStep">
        <el-collapse>
            <el-collapse-item >
              <div v-for="step in form.testStep" :key="step.no">
                <br>     
              <el-divider content-position="center">测试步骤序号  {{ step.no }}</el-divider> 
              <br>     
              <el-form-item label="测试步骤名称:">
                <el-input
                    :maxlength="20"
                    v-model="step.name"
                    placeholder="请输入测试步骤名称"
                    clearable/> 
              </el-form-item>   
              <el-form-item label="结果:">         
                  <el-radio-group
                    v-model="step.result">
                    <el-radio :label="1">通过</el-radio>
                    <el-radio :label="0">失败</el-radio>
                  </el-radio-group>
                </el-form-item>
                  <br>
              </div>  
            </el-collapse-item>
          </el-collapse>
        </el-form-item> -->

        <el-row :gutter="15">
        <el-col :sm="12">
        <el-form-item label="软件版本:" prop="softwareVersion">
          <el-input
            v-model="form.softwareVersion"
            placeholder="请输入软件版本"
            clearable/>
        </el-form-item>

        <el-form-item label="客户名称:" prop="clientName">
          <el-input
            v-model="form.clientName"
            placeholder="请输入客户名称"
            clearable/>
        </el-form-item>
      </el-col>
        <el-col :sm="12">
        <el-form-item label="公司名称:" prop="companyName">
          <el-input
            v-model="form.companyName"
            placeholder="请输入公司名称"
            clearable/>
        </el-form-item>

        <el-form-item label="协议名称:" prop="protocolVersion">
          <el-input
            v-model="form.protocolVersion"
            placeholder="请输入协议名称"
            clearable/>
        </el-form-item>
      </el-col>
    </el-row>
        <el-form-item label="测试开始时间:" prop="testStartTime">
            <el-date-picker
              class="ele-fluid"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              v-model="form.testStartTime"
              placeholder="请选择测试开始时间"/>
          </el-form-item>

          <el-form-item label="测试结束时间:" prop="testEndTime">
            <el-date-picker
              class="ele-fluid"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              v-model="form.testEndTime"
              placeholder="请选择测试结束时间"/>
          </el-form-item>
        
     
          <el-form-item label="测试时间:" prop="testTime">
          <el-input
            v-model="form.testTime"
            placeholder="请输入测试时间"
            clearable/>
         </el-form-item>

          <el-form-item label="结果:" prop="result">
            <el-radio-group
              v-model="form.result">
              <el-radio :label="1">通过</el-radio>
              <el-radio :label="0">失败</el-radio>
            </el-radio-group>
          </el-form-item>

          <div v-for="(input) in form.testStep" :key="input.no">
          <span>测试步骤 {{ input.no }}</span>
          <el-input v-model="input.name" placeholder="名称"></el-input>
          <el-radio-group
            v-model="input.result">
            <el-radio :label="1">通过</el-radio>
            <el-radio :label="0">失败</el-radio>
          </el-radio-group>
        </div>
        <br>
        <el-button @click="addInput">添加测试步骤</el-button>
        <el-button v-if="form.testStep.length > 0" @click="removeInput">删除最后一步测试步骤</el-button>
 

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
    name: 'DebugDataEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        // 表单数据
        form: Object.assign({testStep:[]}, this.data),
        // 表单验证规则
        rules: {
        testEndTime: [
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        },
        // 提交状态
        loading: false,
        // 是否是修改
        isUpdate: false,
        // 输入框id计数器
        idCounter: 1 
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
            this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/debugdata/update' : '/debugdata/add', this.form).then(res => {
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
        const startTime = this.form.testStartTime; // 获取测试开始时间的值
        const finishTime = value; // 获取测试结束时间的值

        if (!startTime || !finishTime) {
          callback(); 
        } else if (startTime > finishTime) {
          callback(new Error('测试结束时间必须晚于测试开始时间')); // 如果完成日期早于开始日期，则返回错误信息
        } else {
          callback(); // 校验通过
        }
      },
      addInput() {
      this.form.testStep.push({
        no: this.idCounter,
        name: '',
        result: ''
      });
      this.idCounter++;
    },
    removeInput() {
      this.form.testStep.pop();
      if (this.form.testStep.length === 0) {
        this.idCounter = 1; // 如果没有输入框了，重置计数器为1
      } else {
        this.idCounter = this.form.testStep[this.form.testStep.length - 1].id + 1; // 更新计数器为最后一个输入框的id加1
      }
    }
    }
  }
  </script>

  <style scoped>
  </style>

