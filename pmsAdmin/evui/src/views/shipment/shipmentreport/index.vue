<template>
    <div class="ele-body">
      <el-card shadow="never">
        <!-- 搜索表单 -->
        <el-form
          :model="where"
          label-width="77px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="15">
            <el-col :lg="6" :md="12">
              <el-form-item label="查询:">
                <el-input
                  clearable
                  v-model="where.keyword"
                  placeholder="工单号、成品编码、客户名称、产品名称或SO/RQ号"/>
              </el-form-item>
            </el-col>
            <el-col :lg="6" :md="12">
              <div class="ele-form-actions">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  class="ele-btn-icon"                
                  @click="reload">查询
                </el-button>
                <el-button @click="reset">重置</el-button>
              </div>
            </el-col>
          </el-row>
        </el-form>
        <!-- 数据表格 -->
        <el-row :gutter="10">
          <el-col :span="2">
           
            <el-menu
        default-active="1-1"
        :unique-opened="true"
        class="el-menu-vertical-demo"
        @select="handleSelect"
        >
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-box"></i>
            <span>成品</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="1-1">一月份</el-menu-item>
            <el-menu-item index="1-2">二月份</el-menu-item>
            <el-menu-item index="1-3">三月份</el-menu-item>
            <el-menu-item index="1-4">四月份</el-menu-item>
            <el-menu-item index="1-5">五月份</el-menu-item>
            <el-menu-item index="1-6">六月份</el-menu-item>
            <el-menu-item index="1-7">七月份</el-menu-item>
            <el-menu-item index="1-8">八月份</el-menu-item>
            <el-menu-item index="1-9">九月份</el-menu-item>
            <el-menu-item index="1-10">十月份</el-menu-item>
            <el-menu-item index="1-11">十一月份</el-menu-item>
            <el-menu-item index="1-12">十二月份</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-suitcase-1"></i>
            <span>模块</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="2-1">一月份</el-menu-item>
            <el-menu-item index="2-2">二月份</el-menu-item>
            <el-menu-item index="2-3">三月份</el-menu-item>
            <el-menu-item index="2-4">四月份</el-menu-item>
            <el-menu-item index="2-5">五月份</el-menu-item>
            <el-menu-item index="2-6">六月份</el-menu-item>
            <el-menu-item index="2-7">七月份</el-menu-item>
            <el-menu-item index="2-8">八月份</el-menu-item>
            <el-menu-item index="2-9">九月份</el-menu-item>
            <el-menu-item index="2-10">十月份</el-menu-item>
            <el-menu-item index="2-11">十一月份</el-menu-item>
            <el-menu-item index="2-12">十二月份</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
            </el-menu>

          </el-col>
          <el-col :span="22">
            <ele-pro-table
              ref="table"
              :where="where"
              :datasource="url"
              :columns="columns"
              :selection.sync="selection"
              height="calc(100vh - 315px)">
              <!-- 表头工具栏 -->
              <template slot="toolbar">
                 
                <el-button
                  size="small"
                  type="primary"
                  icon="el-icon-plus"
                  class="ele-btn-icon"
                  @click="openEdit(null)"
                  v-if="permission.includes('sys:shipmentreport:add')">添加
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  icon="el-icon-delete"
                  class="ele-btn-icon"
                  @click="removeBatch"
                  v-if="permission.includes('sys:shipmentreport:dall')">删除
                </el-button>

                 <el-date-picker
                v-model="currentDate"
                style="width: 160px; margin-left: 200px;"
                type="month"
                format="yyyy 年 MM 月"
                placeholder="选择年月"
                @change="yearAndMonthHandleSelect"
                >
              </el-date-picker>

                <!-- <el-button
                  @click="showImport=true"
                  icon="el-icon-upload2"
                  class="ele-btn-icon"
                  size="small">导入
                </el-button> -->
                <!-- <el-button
                  size="small"
                  type="success"
                  icon="el-icon-download"
                  class="ele-btn-icon"
                  @click="exportExcel"
                  v-if="permission.includes('sys:shipmentreport:export')">导出
                </el-button> -->
              </template>
              <!-- 操作列 -->
              <template slot="action" slot-scope="{row}">
                <el-link
                  type="primary"
                  :underline="false"
                  icon="el-icon-edit"
                  @click="openEdit(row)"
                  v-if="permission.includes('sys:shipmentreport:update')">修改
                </el-link>
                <el-popconfirm
                  class="ele-action"
                  title="确定要删除此数据吗？"
                  @confirm="remove(row)">
                  <el-link
                    type="danger"
                    slot="reference"
                    :underline="false"
                    icon="el-icon-delete"
                    v-if="permission.includes('sys:shipmentreport:delete')">删除
                  </el-link>
                </el-popconfirm>
              </template>
              <!-- 状态列 -->
              <template slot="status" slot-scope="{row}">
                <el-switch
                  v-model="row.status"
                  @change="editStatus(row)"
                  :active-value="1"
                  :inactive-value="2"/>
              </template>
            </ele-pro-table>
          </el-col>        
        </el-row>
      </el-card>
      <!-- 编辑弹窗 -->
    <Shipmentreport-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import ShipmentreportEdit from './shipmentreport-edit';

  export default {
    name: 'SystemShipmentReport',
    components: {ShipmentreportEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格数据接口
        url: '/shipmentreport/list',
        // 表格列配置
        columns: [
          {
            columnKey: 'selection',
            type: 'selection',
            width: 45,
            align: 'center',
            fixed: "left"
          },
          {
            prop: 'work_order',
            label: '工单号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'client_name',
            label: '客户名称',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_code',
            label: '成品编码',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_name',
            label: '产品名称',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'shape',
            label: '规格型号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_count',
            label: '数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'order_date',
            label: '订单日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'delivery_date',
            label: '交货日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'update_delivery_date',
            label: '更改交期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'finish_date',
            label: '完成日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'SO_RQ_id',
            label: 'SO/RQ号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'remark',
            label: '备注',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
  
          {
            columnKey: 'action',
            label: '操作',
            width: 150,
            align: 'center',
            resizable: false,
            slot: 'action',
            fixed: "right"
          }
        ],
        // 表格搜索条件
        where: {
        },
        currentDate: '',
        // 表格选中数据
        selection: [],
        // 当前编辑数据
        current: null,
        // 是否显示编辑弹窗
        showEdit: false,
        // 是否显示导入弹窗
        showImport: false
      };
    },
    created () {
      this.getDefaultYear();
    },
    methods: {
      // 初始获取当前年份
      getDefaultYear() {
        this.currentDate = new Date();
      },
      // 选择年月
      yearAndMonthHandleSelect() {
        this.where.year = this.currentDate.getFullYear();
        // getMonth 方法返回的月份是从 0 开始计数的，即 0 表示一月
        this.where.month = this.currentDate.getMonth() + 1;
        console.log(this.where)
        this.$refs.table.reload({page: 1, where: this.where});
      },
      // 点击左侧月份
      handleSelect(keyPath) {
        this.where.product_module = keyPath[0];
        this.where.month = keyPath.split("-")[1];
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 刷新表格 */
      reload() {
        this.where.year = this.currentDate.getFullYear();
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 重置搜索 */
      reset() {
        this.where = {};
        this.reload();
      },
      /* 显示编辑 */
      openEdit(row) {
        if (!row) {
          // 添加
          this.current = null;
          this.showEdit = true;
        } else {
          // 编辑
          this.loading = true;
          this.$http.get('/shipmentreport/detail/' + row.id).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.current = Object.assign({}, res.data.data);
              this.showEdit = true;
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch((e) => {
            this.loading = false;
            this.$message.error(e.message);
          });
        }
      },
      /* 删除 */
      remove(row) {
        const loading = this.$loading({lock: true});
        this.$http.delete('/shipmentreport/delete/' + row.id).then(res => {
          loading.close();
          if (res.data.code === 0) {
            this.$message.success(res.data.msg);
            this.reload();
          } else {
            this.$message.error(res.data.msg);
          }
        }).catch(e => {
          loading.close();
          this.$message.error(e.message);
        });
      },
      /* 批量删除 */
      removeBatch() {
        if (!this.selection.length) {
          this.$message.error('请至少选择一条数据');
          return;
        }
        this.$confirm('确定要删除选中的数据吗?', '提示', {
          type: 'warning'
        }).then(() => {
          const loading = this.$loading({lock: true});
          this.$http.delete('/shipmentreport/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
            loading.close();
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              this.reload();
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch(e => {
            loading.close();
            this.$message.error(e.message);
          });
        }).catch(() => {
        });
      },
    }
  }
  </script>
  
  <style scoped>
  </style>
  
  