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
                  placeholder="工单号、客户名称、规格型号或客户名称"/>
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
              v-if="permission.includes('sys:debugreport:add')">添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:debugreport:dall')">删除
            </el-button>
            <!-- <el-button
              @click="showImport=true"
              icon="el-icon-upload2"
              class="ele-btn-icon"
              size="small">导入
            </el-button> -->
            <el-button
              size="small"
              type="success"
              icon="el-icon-download"
              class="ele-btn-icon"
              @click="exportExcel"
              v-if="permission.includes('sys:debugreport:export')">导出
            </el-button>
          </template>
          <!-- 操作列 -->
          <template slot="action" slot-scope="{row}">
            <el-link
              type="primary"
              :underline="false"
              icon="el-icon-edit"
              @click="openEdit(row)"
              v-if="permission.includes('sys:debugreport:update')">修改
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
                v-if="permission.includes('sys:debugreport:delete')">删除
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
          <!-- 成品模块列 -->
          <template slot="product_module" slot-scope="{row}">
            <el-tag v-if="row.product_module === 1" type="success" size="medium">成品</el-tag>
            <el-tag v-if="row.product_module === 2" type="success" size="medium">模块</el-tag>
          </template>
        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
    <debug-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import DebugEdit from './debug-edit';

  export default {
    name: 'SystemDebug',
    components: {DebugEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格搜索条件
        where: {},
        // 表格数据接口
        url: '/debugreport/list',
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
            minWidth: 160,
            align: 'center',
          },
          {
            prop: 'order_time',
            label: '下单日期',
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
            prop: 'client_name',
            label: '客户名称',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
          },
          {
            prop: 'product_name',
            label: '产品名称',
            showOverflowTooltip: true,
            minWidth: 120,
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
            label: '产品数量',
            width: 120,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'submit_time',
            label: '交期',
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
            prop: 'start_time',
            label: '开始日期',
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
            prop: 'finish_time',
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
            prop: 'work_hours',
            label: '工时',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
          },
          {
            prop: 'instruction',
            label: '具体说明',
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
          prop: 'product_module',
          label: '成品/模块',
          minWidth: 100,
          align: 'center',
          resizable: false,
          slot: 'product_module',
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
    methods: {
      /* 刷新表格 */
      reload() {
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
          this.$http.get('/debugreport/detail/' + row.id).then((res) => {
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
        this.$http.delete('/debugreport/delete/' + row.id).then(res => {
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
          this.$http.delete('/debugreport/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
  
  