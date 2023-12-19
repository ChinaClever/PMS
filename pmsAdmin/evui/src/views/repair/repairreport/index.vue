<template>
    <div class="ele-body">
      <el-card shadow="never">
        <!-- 维修报表表单 -->
        <el-form
          :model="where"
          label-width="77px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="10">
            <el-col :span="5">
              <el-form-item label="单号:">
                <el-input
                  clearable
                  v-model="where.work_order"
                  @clear="this.reload"
                  placeholder="请输入单号"/>
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="产品名称:">
                <el-input
                  clearable
                  v-model="where.name"
                  @clear="this.reload"
                  placeholder="请输入产品名称"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :lg="6" :md="12">
              <el-form-item label="日期范围:">
              <el-date-picker
                v-model="selectDateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="至"
                start-placeholder="订单日期开始日期"
                end-placeholder="订单日期结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect">
              </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :lg="6" :md="12" :offset="5">
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
              v-if="permission.includes('sys:repairreport:add')">添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:repairreport:dall')">删除
            </el-button>
            <!-- 导出按钮 -->
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
              v-if="permission.includes('sys:repairreport:update')">修改
            </el-link>
            <el-popconfirm
              class="ele-action"
              title="确定要删除此通知吗？"
              @confirm="remove(row)">
              <el-link
                type="danger"
                slot="reference"
                :underline="false"
                icon="el-icon-delete"
                v-if="permission.includes('sys:repairreport:delete')">删除
              </el-link>
            </el-popconfirm>
          </template>
          <!--<template slot="type" slot-scope="{row}">
            <el-tag v-if="row.type === 1" size="small">问题</el-tag>
            <el-tag v-if="row.type === 2" size="small">建议</el-tag>
            <el-tag v-if="row.type === 3" size="small">新需求</el-tag>
          </template>
          <template slot="status" slot-scope="{row}">
            <el-tag v-if="row.status === 1" type="warning" size="small">未查看</el-tag>
            <el-tag v-if="row.status === 2" type="success" size="small">确认</el-tag>
            <el-tag v-if="row.status === 3" type="success" size="small">完成</el-tag>
            <el-tag v-if="row.status === 4" type="success" size="small">未通过</el-tag>
          </template>-->
          <template slot="expand_1" slot-scope="{row}">
            <el-popover
              placement="top-start"
              title="不良现象"
              width="1000"
              trigger="click"
              :content=row.bad_phenomenon>
              <el-button slot="reference">{{ row.bad_phenomenon }}</el-button>
            </el-popover>
          </template>
          <template slot="expand_2" slot-scope="{row}">
            <el-popover
              placement="top-start"
              title="原因分析"
              width="1000"
              trigger="click"
              :content=row.analysis>
              <el-button slot="reference">{{ row.analysis }}</el-button>
            </el-popover>
          </template>
          <template slot="expand_3" slot-scope="{row}">
            <el-popover
              placement="top-start"
              title="解决方法"
              width="1000"
              trigger="click"
              :content=row.solution>
              <el-button slot="reference">{{ row.solution }}</el-button>
            </el-popover>
          </template>
          <template slot="expand_4" slot-scope="{row}" v-if="row.notes">
            <el-popover
              placement="top-start"
              title="备注"
              width="1000"
              trigger="click"
              :content=row.notes>
              <el-button slot="reference">{{ row.notes }}</el-button>
            </el-popover>
          </template>
        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
      <repairreport-edit
        :data="current"
        :visible.sync="showEdit"
        @done="reload"/>
    </div>
  </template>

  <script>
  import { mapGetters } from "vuex";
  import RepairreportEdit from './repairreport-edit';
  import XLSX from 'xlsx'
  import { saveAs } from 'file-saver';


  export default {
    name: 'repairreport',
    components: {RepairreportEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格数据接口
        url: '/repairreport/list',
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
            prop: 'repair_user',
            label: '维修员',
            width: 150,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'work_order',
            label: '单号',
            width: 150,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'name',
            label: '产品名称',
            width: 150,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'bad_number',
            label: '不良数量',
            width: 70,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'repair_number',
            label: '维修数量',
            width: 70,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'bad_phenomenon',
            label: '不良现象',
            width: 150,
            align: 'center',
            slot: 'expand_1',
          },

          {
            prop: 'analysis',
            label: '原因分析',
            width: 150,
            align: 'center',
            slot: 'expand_2',
          },
          {
            prop: 'solution',
            label: '解决方法',
            width: 150,
            align: 'center',
            slot: 'expand_3',
          },

          {
            prop: 'notes',
            label: '备注',
            width: 150,
            align: 'center',
            slot: 'expand_4',
          },
          {
            prop: 'repair_time',
            label: '维修时间',
            showOverflowTooltip: true,
            sortable: 'custom',
            default:'',
            minWidth: 160,
            align: 'center',
          },
          {
            prop: 'create_time',
            label: '创建时间',
            showOverflowTooltip: true,
            sortable: 'custom',
            minWidth: 160,
            align: 'center',
            formatter: (row, column, cellValue) => {
              return this.$util.toDateString(cellValue);
            }
          },
          {
            prop: 'update_time',
            label: '更新时间',
            showOverflowTooltip: true,
            sortable: 'custom',
            minWidth: 160,
            align: 'center',
            formatter: (row, column, cellValue) => {
              return this.$util.toDateString(cellValue);
            }

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
         pickerOptions: {
          shortcuts: [{
            text: '最近一天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              //start.setTime(start.getTime() - 3600 * 1000 * 24 );
              picker.$emit('pick', [start, end]);
            }
          },{
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
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit('pick', [start, end]);
            }
          },{
            text: '最近半年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 6);
              picker.$emit('pick', [start, end]);
            }
          }, {
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
        //时间筛选
        selectDateRange:'',
        // 表格搜索条件
        where: {},
        // 表格选中数据
        selection: [],
        // 当前编辑数据
        current: null,
        // 是否显示编辑弹窗
        showEdit: false,
      };
    },
    methods: {
      //向后端传时间
      dateRangeHandleSelect(){
        if(this.selectDateRange!=null){
          this.where.selectStartDate = this.selectDateRange[0]
          this.where.selectEndDate = this.selectDateRange[1]
        }else{
          this.where.selectStartDate = null
          this.where.selectEndDate = null
          this.reload()
        }
      },
      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 重置搜索 */
      reset() {
        this.where = {};
        this.selectDateRange = '';
        this.reload();
      },
      /* 显示编辑 */
      openEdit(row) {
        if (!row) {
          // 添加
          this.current = Object.assign({repair_time:new Date().toISOString()},null);
          this.showEdit = true;
   
        } else {
          // 编辑
          this.loading = true;
          this.$http.get('/repairreport/detail/' + row.id).then((res) => {
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
        this.$http.delete('/repairreport/delete/' + row.id).then(res => {
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
        this.$confirm('确定要删除选中的通知吗?', '提示', {
          type: 'warning'
        }).then(() => {
          const loading = this.$loading({lock: true});
          this.$http.delete('/repairreport/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      async exportToExcel() {
       // 创建 Excel 文件
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

      // 获取字段名称（中文）
      const header = this.columns
        .slice(1, -1) // 排除排除第一列和最后一列,这里我排除的是我的id列和操作列
        .map(column => column.label);
      // 获取要导出的数据（排除第一列和最后一列）
      const data = this.selection.map(row =>
        this.columns
          .slice(1, -1) // 排除第一列和最后一列
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
      const fileName = '维修报表.xlsx';
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
  </style>
