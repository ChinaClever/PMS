<!-- 职级编辑弹窗 -->
<template>
    <el-dialog
      :title="isUpdate?'修改排期表单':'添加排期表单'"
      :visible="visible"
      width="800px"
      :destroy-on-close="true"
      :lock-scroll="false"
      @update:visible="updateVisible">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="100px"
        :validate-on-rule-change="false">
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item
          label="工单号:"
          prop="work_order">
          <el-input
            v-model="form.work_order"
            placeholder="请输入工单号"
            clearable/>
        </el-form-item>
        </el-col>
        <el-col :span="12">
        <el-form-item
          label="客户名称:"
          prop="client_name">
          <el-input
            v-model="form.client_name"
            placeholder="请输入客户名称"
            clearable/>
        </el-form-item>
        </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item
          label="成品编码:"
          prop="product_code">
          <el-input
            v-model="form.product_code"
            placeholder="请输入成品编码"
            clearable
            />
        </el-form-item>
      </el-col>
        <el-col :span="12">
        <el-form-item label="产品名称:" prop="product_name">
         <!-- <el-cascader
          v-model="form.product_name"
          :options="options"
          :props="{ expandTrigger: 'hover' }"
          :show-all-levels="false"
          leafOnly>
        </el-cascader> -->
        <el-autocomplete
          v-model="form.product_name"
          :fetch-suggestions="querySearchAsync"
          @select="handleSelect"
        ></el-autocomplete>
        </el-form-item>
        </el-col>
        </el-row>
      
        <el-form-item label="规格型号:" prop="shape">
          <el-input
            v-model="form.shape"
            placeholder="请输入规格型号"
            clearable/>
        </el-form-item>
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item label="数量:" prop="product_count">
          <el-input-number
            :min="0"
            v-model="form.product_count"
            placeholder="请输入数量"
            controls-position="right"
            class="ele-fluid ele-text-left"/>
        </el-form-item>
       </el-col>
        <el-col :span="12">
        <el-form-item label="SO/RQ号:" prop="SO_RQ_id">
          <el-input
            v-model="form.SO_RQ_id"
            placeholder="请输入SO/RQ号"
            clearable/>
        </el-form-item>
      </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
        <el-form-item label="订单日期:" prop="order_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.order_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择订单日期"/>
        </el-form-item>
        </el-col>
        <el-col :span="12">
        <el-form-item label="交货日期:" prop="delivery_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.delivery_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择交货日期"/>
        </el-form-item>
      </el-col>
        </el-row>
        <el-row :gutter="6">
        <el-col :span="12">
          <el-form-item label="更改日期:" prop="update_delivery_date" v-if="isUpdate">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.update_delivery_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择更改日期"/>
        </el-form-item>
      </el-col>
        <el-col :span="12">
          <el-form-item label="完成日期:" prop="finish_date">
            <el-date-picker
              type="date"
              class="ele-fluid"
              v-model="form.finish_date"
              value-format="yyyy-MM-dd"
              placeholder="请选择完成日期"/>
        </el-form-item>
      </el-col>
        </el-row>
        <el-form-item label="成品/模块:" prop="product_module">
            <el-radio-group
              v-model="form.product_module">
              <el-radio :label="1">成品</el-radio>
              <el-radio :label="2">模块</el-radio>
            </el-radio-group>
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
    name: 'ShipmentReportEdit',
    props: {
      // 弹窗是否打开
      visible: Boolean,
      // 修改回显的数据
      data: Object
    },
    data() {
      return {
        product_names: [],
        state: '',
        timeout:  null,
        // 表单数据
        form: Object.assign({product_code: '', product_name:'', shape:''}, this.data),
        // 产品名称选项
        options: [{
          value: '1',
          label: '成品',
          children: [{
            value: 'MPDU ',
            label: 'MPDU '
          }, {
            value: 'ATS',
            label: 'ATS'
          }, {
            value: 'Switched',
            label: 'Switched'
          }, {
            value: 'Sensor Box-I',
            label: 'Sensor Box-I'
          }, {
            value: 'RPDU',
            label: 'RPDU'
          }, {
            value: 'NODE',
            label: 'NODE'
          }, {
            value: 'ZPDU',
            label: 'ZPDU'
          }, {
            value: 'PDU',
            label: 'ATS'
          }, {
            value: '其他',
            label: '其他'
          }
        ]
        }, {
          value: '2',
          label: '模块',
          children: [{
            value: 'BM-PDU2020',
            label: 'BM-PDU2020'
          },{
            value: 'BM-PDU2017',
            label: 'BM-PDU2017'
          }, {
            value: 'BM-PDU ',
            label: 'BM-PDU '
          }, {
            value: 'IP-PDU2020',
            label: 'IP-PDU2020'
          },{
            value: 'IP-PDU2017',
            label: 'IP-PDU2017'
          }, {
            value: 'IP-PDU6',
            label: 'IP-PDU6'
          }, {
            value: 'IP-PDU',
            label: 'IP-PDU'
          },{
            value: 'SI-PDU2022',
            label: 'SI-PDU2022'
          },{
            value: 'SI-PDU2020',
            label: 'SI-PDU2020'
          },{
            value: 'SI-PDU2017',
            label: 'SI-PDU2017'
          }, {
            value: 'SI-PDU',
            label: 'SI-PDU'
          }, {
            value: '配件',
            label: '配件'
          }, {
            value: '插接箱',
            label: '插接箱'
          },  {
            value: '始端箱',
            label: '始端箱'
          }, {
            value: '工业屏',
            label: '工业屏'
          },{
            value: '主控屏',
            label: '主控屏'
          }, {
            value: '传感器',
            label: '传感器'
          },{
            value: 'BASE功能模块',
            label: 'BASE功能模块'
          },{
            value: 'NODE功能模块',
            label: 'NODE功能模块'
          },{
            value: 'IMM接线模块',
            label: 'IMM接线模块'
          },{
            value: 'Switch功能插座模块',
            label: 'Switch功能插座模块'
          },{
            value: '插拔箱',
            label: '插拔箱'
          },
        ]
        }],
        // 表单验证规则
        rules: {
          work_order: [
          {required: true, message: '请输入工单号', trigger: 'blur'},
          { validator: (rule, value, callback) => this.checkWorkOrderId(rule, value, callback), trigger: 'blur' }
        ],
        client_name: [
          {required: true, message: '请选择客户名称', trigger: 'blur'}
        ],
        product_code: [
          {required: true, message: '请输入成品编码', trigger: 'blur'}
        ],
        product_name: [
          {required: true, message: '请输入产品名称', trigger: 'blur'}
        ],
        shape: [
          {required: true, message: '请输入规格型号', trigger: 'blur'}
        ],
        product_count: [
          {required: true, message: '请输入数量', trigger: 'blur'}
        ],
        order_date: [
          {required: true, message: '请选择订单日期', trigger: 'blur'}
        ],
        delivery_date: [
          {required: true, message: '请选择交货日期', trigger: 'blur'},
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        update_delivery_date: [
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        finish_date: [
          { validator: (rule, value, callback) => this.checkFinishTime(rule, value, callback), trigger: 'blur' }
        ],
        SO_RQ_id: [
          {required: true, message: '请选择SO/RQ号', trigger: 'blur'}
        ],
        product_module: [
          {required: true, message: '请选择成品/模块', trigger: 'blur'}
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
            // 获取产品名称最后节点的名字
            let lastNode = this.form.product_name[this.form.product_name.length - 1];
            this.form.product_name = lastNode

            this.$http[this.isUpdate ? 'put' : 'post'](this.isUpdate ? '/shipmentreport/update' : '/shipmentreport/add', this.form).then(res => {
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
       // 订单号自动填入数据
      checkWorkOrderId(rule, value, callback){
        const regex = /^[a-zA-Z0-9]+[+][a-zA-Z0-9]+$/;
        const regex1 = /^[a-zA-Z0-9]+$/;
        if (value.includes("+")) {
          if (regex.test(value)) {
            const parts = value.split("+");
            this.form.work_order = parts[0];
            this.form.product_code = parts[1];
            //根据产品编码查产品名称 规格
            this.$http.get('/shipmentreport/product/detail/' + this.form.product_code).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
             this.form.product_name = res.data.data.product_name
             this.form.shape  = res.data.data.shape
            } 
            })
            callback();
          } else {
             callback(new Error('存在除一个+号外的非法字符')); 
        }
        }else {
          if (!regex1.test(value)) {
            callback(new Error('存在非法字符')); 
          }

          callback();
        }
      },

       // 检测填入日期是否晚于订单日期
      checkFinishTime(rule, value, callback) {
        const orderDate = this.form.order_date; 
        const thisDate = value; 
        if (!orderDate || !thisDate) {
          callback(); 
        } else if (orderDate > thisDate) {
          callback(new Error('此日期必须晚于订单日期')); 
        } else {
          callback(); 
        }
      },

      loadAll() {
        // this.$http.get('/shipmentreport/product/list').then((res) => {
        //     this.loading = false;
        //     if (res.data.code === 0) {
        //       const json = res.data.data
        //       const array = JSON.parse(json).map(item => {
        //       return {
        //         id: item.id,
        //         product_code: item.product_code,
        //         product_name: item.product_name,
        //         shape: item.shape,
        //         product_module: item.product_module
        //       };
        //     });
        //     console.log(array);
        //     } 
        //   })

        return [
          { "value": "三全鲜食（北新泾店）", "address": "长宁区新渔路144号" },
          { "value": "Hot honey 首尔炸鸡（仙霞路）", "address": "上海市长宁区淞虹路661号" },
          { "value": "新旺角茶餐厅", "address": "上海市普陀区真北路988号创邑金沙谷6号楼113" },
          { "value": "泷千家(天山西路店)", "address": "天山西路438号" },
          { "value": "胖仙女纸杯蛋糕（上海凌空店）", "address": "上海市长宁区金钟路968号1幢18号楼一层商铺18-101" },   
        ];
      },

      querySearchAsync(queryString, cb) {
        var product_names = this.product_names;
        var results = queryString ? product_names.filter(this.createStateFilter(queryString)) : product_names;

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
        this.form.product_name = item.value
        this.$refs.form.validateField('product_name', () => {});
      },

    },
    mounted() {
      this.product_names = this.loadAll();
    }
  }
  </script>

  <style scoped>
   .el-row {
    margin-bottom: 16px;

  }
  </style>

