<template>
  <div class="ele-body">
    <el-card shadow="never">
      <!-- 质检报表表单 -->
      <el-form
        :model="where"
        label-width="77px"
        class="ele-form-search"
        @keyup.enter.native="reload"
        @submit.native.prevent>
        <el-row :gutter="10">
          <el-col :span="9">
            <el-form-item label="搜索:">
              <el-input
                clearable
                v-model="where.keyword"
                placeholder="请输入填写人或产品型号或工单号"/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="信号:">
              <el-select
                clearable
                v-model="where.signal"
                placeholder="请选择信号"
                class="ele-fluid">
                <el-option label="红色" value="1"/>
                <el-option label="绿色" value="2"/>
              </el-select>
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
            v-if="permission.includes('sys:inspectreport:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:inspectreport:dall')">删除
          </el-button>
           <!-- 导出按钮 -->
          <el-button
            size="small"
            type="success"
            icon="el-icon-download"
            class="ele-btn-icon"
            @click="exportToExcel"
            v-if="selection.length > 0">导出
          </el-button>
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:inspectreport:update')">修改
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
              v-if="permission.includes('sys:inspectreport:delete')">删除
            </el-link>
          </el-popconfirm>
        </template>
        <template slot="singal" slot-scope="{row}">
          <el-tag v-if="row.signal === 1"  effect="dark" type="danger" size="medium"></el-tag>
          <el-tag v-if="row.signal === 2"  effect="dark" type="success" size="medium"></el-tag>
        </template>
        <template slot="expand_1" slot-scope="{row}" v-if="row.problems">
          <el-popover
            placement="top-start"
            title="问题"
            width="1000"
            trigger="click"
            :content=row.problems>
            <el-button slot="reference">{{ row.problems }}</el-button>
          </el-popover>
        </template>
        <template slot="expand_2" slot-scope="{row}" v-if="row.actions">
          <el-popover
            placement="top-start"
            title="行动"
            width="1000"
            trigger="click"
            :content=row.actions>
            <el-button slot="reference">{{ row.actions }}</el-button>
          </el-popover>
        </template>
      </ele-pro-table>
    </el-card>
    <!-- 编辑弹窗 -->
    <inspectreport-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import InspectreportEdit from './inspectreport-edit';
import XLSX from 'xlsx'
import { saveAs } from 'file-saver';

export default {
  name: 'inspectreport',
  components: {InspectreportEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/inspectreport/list',
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
          width: 80,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'start_time',
          label: '开始时间',
          showOverflowTooltip: true,
          sortable: 'custom',
          minWidth: 160,
          align: 'center',
          order: '', // 初始化排序方式为空字符串
          sortableMethod: ()=> {
            // 在这里实现自定义的排序逻辑
            this.where.order = this.order;
            this.reload();
          }
        },
        {
          prop: 'end_time',
          label: '结束时间',
          showOverflowTooltip: true,
          sortable: 'custom',
          minWidth: 160,
          align: 'center',
          order: '', // 初始化排序方式为空字符串
        },
        {
          prop: 'commit_user',
          label: '填写者',
          width: 80,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'item_number',
          label: '产品型号',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'examine_an_amount',
          label: '检验数量',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'examine_a_bad_amount',
          sortable: 'custom',
          label: '检验不良数量',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'examine_amount_total_amount',
          label: '检验数量累计',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'examine_bad_total_amount',
          label: '检验不良累计',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'target_pass_rate',
          label: 'ERP目标合格率',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
          formatter: (row, column, cellValue) => {
            return cellValue + '%';
          }
        },
        {
          prop: 'target_actual_pass_rate',
          sortable: 'custom',
          label: '实际合格率',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
          formatter: (row, column, cellValue) => {
            return cellValue + '%';
          }
        },
        {
          prop: 'singal',
          label: '信号',
          minWidth: 100,
          align: 'center',
          resizable: false,
          slot: 'singal',
        },
        {
          prop: 'problems',
          label: '问题',
          width: 150,
          align: 'center',
          slot: 'expand_1',
        },
        {
          prop: 'actions',
          label: '行动',
          width: 150,
          align: 'center',
          slot: 'expand_2',
        },
        // {
        //   prop: 'create_time',
        //   label: '创建时间',
        //   showOverflowTooltip: true,
        //   sortable: 'custom',
        //   minWidth: 160,
        //   align: 'center',
        //   formatter: (row, column, cellValue) => {
        //     return this.$util.toDateString(cellValue);
        //   },
        //   order: '', // 初始化排序方式为空字符串
        //   sortableMethod: ()=> {
        //     // 在这里实现自定义的排序逻辑
        //     this.where.order = this.order;
        //     this.reload();
        //   }
        // },
        // {
        //   prop: 'update_time',
        //   label: '更新时间',
        //   showOverflowTooltip: true,
        //   sortable: 'custom',
        //   minWidth: 160,
        //   align: 'center',
        //   formatter: (row, column, cellValue) => {
        //     return this.$util.toDateString(cellValue);
        //   }
        // },
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
        this.current = row;
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http.get('/inspectreport/detail/' + row.id).then((res) => {
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
      this.$http.delete('/inspectreport/delete/' + row.id).then(res => {
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
      this.$confirm('确定要删除选中的报表吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({lock: true});
        this.$http.delete('/inspectreport/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
    /* 更改状态 */
    editStatus(row) {
      const loading = this.$loading({lock: true});
      this.$http.put('/notice/status',  {id: row.id, status: row.status}).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message({type: 'success', message: res.data.msg});
        } else {
          row.status = !row.status ? 1 : 2;
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    },
    exportToExcel() {
       // 创建 Excel 文件
      const workbook = XLSX.utils.book_new();
      //去除不需要的字段，这里我不希望显示id，所以id不返回
      let temp = this.selection;
      this.selection = this.selection.map(({ id, ...rest }) => rest);
      //可以将对应字段的数字经过判断转为对应的中文
      this.selection = this.selection.map(obj => {
        if (obj.signal === 2) {
          return { ...obj, signal: '合格' };
        } else if (obj.signal === 1) {
          return { ...obj, signal: '不合格' };
        }
        return obj;
      });
      console.log(this.selection)
      const worksheet = XLSX.utils.json_to_sheet(this.selection);

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
      const fileName = '质检报表.xlsx';
      
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
    }
    
  }
}
</script>

<style scoped>
</style>
