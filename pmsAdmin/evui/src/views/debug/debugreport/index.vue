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
                  placeholder="单号、客户名称、规格型号或客户名称"
                  @clear="clearSearchHandle"/>
              </el-form-item>
            </el-col>
            
            <el-col :lg="9" :md="24">
              <div class="container">
                <div class="time-picker">
                  <el-date-picker
                    v-model="selectDateRange"
                    type="daterange"
                    align="right"
                    unlink-panels
                    range-separator="至"
                    start-placeholder="完成日期开始日期"
                    end-placeholder="完成日期结束日期"
                    format="yyyy 年 MM 月 dd 日"
                    value-format="yyyy-MM-dd"
                    :picker-options="pickerOptions"
                    @change="dateRangeHandleSelect">
                  </el-date-picker>
                </div>
                <div class="ele-form-actions">
                  <el-button
                    type="primary"
                    icon="el-icon-search"
                    class="ele-btn-icon"                
                    @click="reload">查询
                  </el-button>
                  <el-button @click="reset">重置</el-button>
                </div>
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
              @click="exportToExcel">导出
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
          <!-- 成品模块列 -->
          <template slot="product_module" slot-scope="{row}">
            <el-tag v-if="row.product_module === 1" type="success" size="medium">成品</el-tag>
            <el-tag v-if="row.product_module === 2" size="medium">模块</el-tag>
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
  import XLSX from 'xlsx';
  import { saveAs } from 'file-saver';

  export default {
    name: 'SystemDebugReport',
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
            label: '单号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'start_time',
            label: '调试开始时间',
            showOverflowTooltip: true,
            minWidth: 200,
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
            label: '调试完成时间',
            showOverflowTooltip: true,
            minWidth: 200,
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
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'debug_count',
            label: '调试数量',
            width: 80,
            align: 'center',
            showOverflowTooltip: true,
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
            label: '产品数量',
            width: 80,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'submit_time',
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
        showImport: false,
        // 查询日期范围的左边栏快捷选项
        pickerOptions: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 3);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近半年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 6);
              picker.$emit('pick', [start, end]);
            }
          }
          , {
            text: '最近一年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 12);
              picker.$emit('pick', [start, end]);
            }
          }
        ]
        },
        // 选择的日期范围
        selectDateRange: '',
      };
    },
    methods: {
       // 选择日期范围查询
       dateRangeHandleSelect(){
        if (this.selectDateRange != null){
          this.where.selectStartDate = this.selectDateRange[0]
          this.where.selectEndDate = this.selectDateRange[1]
        }else{
          this.where.selectStartDate = null
          this.where.selectEndDate = null
          this.$refs.table.reload({page: 1, where: this.where});
        }
      },

      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 重置搜索 */
      reset() {
        this.selectDateRange = null;
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

      // 清除搜索框
      clearSearchHandle(){
        this.$refs.table.reload({page: 1, where: this.where});
      },

      //导出数据到excel
      async exportToExcel() {
      const workbook = XLSX.utils.book_new();
      //去除不需要的字段，这里我不希望显示id，所以id不返回
      let temp = this.selection;
      if(this.selection.length == 0){
        await this.$http.get(this.url,{ params : {...this.where} }).then((res) => {
          if (res.data.code === 0) {
            // eslint-disable-next-line
            this.selection = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        }).catch((e) => {
          this.$message.error(e.message);
        });
      } 
      // eslint-disable-next-line
      this.selection = this.selection.map(({ id, ...rest }) => rest);

      this.selection = this.selection.map(obj => {
        if (obj.product_module === 2) {
          return { ...obj, product_module: '模块' };
        } else if (obj.product_module === 1) {
          return { ...obj, product_module: '成品' };
        }
        return obj;
      });
      
      // 获取字段名称（中文）
      const header = this.columns
        .slice(1, -1)
        .map(column => column.label);

      // 获取要导出的数据（排除第一列和最后一列）
      const data = this.selection.map(row =>
        this.columns
          .slice(1, -1) 
          .map(column => row[column.prop])
      );
      const worksheet = XLSX.utils.json_to_sheet(data);
      // 将字段名称添加到 Excel 文件中
      XLSX.utils.sheet_add_aoa(worksheet, [header], { origin: 'A1' });

      // 将数据添加到 Excel 文件中
      XLSX.utils.sheet_add_aoa(worksheet, data, { origin: 'A2' });

      // 将工作表添加到工作簿中
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

      // 保存 Excel 文件
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
      // 导出的文件名,下面代码在后面加了时间，如果不加可以直接saveAs(blob, fileName);
      const fileName = '调试报表.xlsx';
      
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0');
      const date = String(currentDate.getDate()).padStart(2, '0');
      const hours = String(currentDate.getHours()).padStart(2, '0');
      const minutes = String(currentDate.getMinutes()).padStart(2, '0');
      const seconds = String(currentDate.getSeconds()).padStart(2, '0');

      const formattedDate = `${year}年${month}月${date}日${hours}时${minutes}分${seconds}秒`;
      const newFileName = `${fileName.split('.')[0]}_${formattedDate}.${fileName.split('.')[1]}`;

      saveAs(blob, newFileName);
      this.selection = temp;
    },  
    }
  }
  </script>
  
  <style scoped>
  .container{
    display: flex;
    align-items: flex-start;
  }
  .time-picker{
    flex: 1;
  }
  </style>
  
  