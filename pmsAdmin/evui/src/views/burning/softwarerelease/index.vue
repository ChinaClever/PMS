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
                v-model="where.name"
                @clear="reload"
                placeholder="请输入程序名称"/>
            </el-form-item>
          </el-col>
          
          <el-col :lg="6" :md="12">
              <el-date-picker
                v-model="selectDateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="至"
                start-placeholder="修改日期开始日期"
                end-placeholder="修改日期结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd"
                @clear="reload"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect">
              </el-date-picker>
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
            v-if="permission.includes('sys:softwarerelease:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:softwarerelease:dall')">删除
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
          <!-- <el-button
            @click="showImport=true"
            icon="el-icon-upload2"
            class="ele-btn-icon"
            size="small">导入
          </el-button>
          <el-button
            size="small"
            type="success"
            icon="el-icon-download"
            class="ele-btn-icon"
            @click="exportExcel"
            v-if="permission.includes('sys:softwarerelease:export')">导出
          </el-button> -->
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:softwarerelease:update')">修改
          </el-link>
          <el-popconfirm
            class="ele-action"
            title="确定要删除该信息吗？"
            @confirm="remove(row)">
            <el-link
              type="danger"
              slot="reference"
              :underline="false"
              icon="el-icon-delete"
              v-if="permission.includes('sys:softwarerelease:delete')">删除
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
    </el-card>
    <!-- 编辑弹窗 -->
    <softwarerelease-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
  
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import softwarereleaseEdit from './softwarerelease-edit';
import XLSX from 'xlsx'
import { saveAs } from 'file-saver';


export default {
  name: 'Systemsoftwarerelease',
  components: {softwarereleaseEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/softwarerelease/list',
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
          prop: 'id',
          label: 'ID',
          width: 60,
          align: 'center',
          showOverflowTooltip: true,
          fixed: "left"
        },
        {
          prop: 'name',
          label: '程序名称',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'products',
          label: '使用产品',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'history_version',
          label: '历史版本',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'version',
          label: '当前版本',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'modify_time',
          label: '修改日期',
          sortable:'custom',
          order:'',
          sortableMethod:()=>{
            //排序逻辑
            this.where.order = this.order
            this.reload();
          },
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'version_explain',
          label: '版本说明',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'updata',
          label: '此次更新',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'burn_method',
          label: '烧录方法',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'upgrade_method',
          label: '升级方法',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'calibration_method',
          label: '校准方法',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'User_Manual',
          label: '用户手册',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'upgrade_cause',
          label: '升级原因',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'documentation_position',
          label: '程序和文档公盘位置',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'User_Manual_position',
          label: '用户使用手册和协议公盘位置',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'create_time',
          label: '创建时间',
          sortable: 'custom',
          showOverflowTooltip: true,
          minWidth: 160,
          align: 'center',
          formatter: (row, column, cellValue) => {
            const date = new Date(cellValue);
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            
            return `${year}-${month}-${day}`;
          }
        },
        {
          prop: 'update_time',
          label: '更新时间',
          sortable: 'custom',
          showOverflowTooltip: true,
          minWidth: 160,
          align: 'center',
          formatter: (row, column, cellValue) => {
            const date = new Date(cellValue);
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            
            return `${year}-${month}-${day}`;
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
      selectDateRange: '',
      // 表格搜索条件
      where: {},
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
          }]
       },
    };
  },
  methods: {
    /* 刷新表格 */
    reload() {
      this.$refs.table.reload({page: 1, where: this.where});
    },
    /* 重置搜索 */
    reset() {
      this.selectDateRange = null
      this.selectDate = null
      this.where = {};
      this.reload();
    },
     // 选择日期范围查询
     dateRangeHandleSelect(){
        this.where.year = null
        this.where.month = null
        this.selectDate = null
        if (this.selectDateRange != null){
          this.where.selectStartDate = this.selectDateRange[0]
          this.where.selectEndDate = this.selectDateRange[1]
        }else{
          this.where.selectStartDate = null
          this.where.selectEndDate = null
        }
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
        this.$http.get('/softwarerelease/detail/' + row.id).then((res) => {
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
      this.$http.delete('/softwarerelease/delete/' + row.id).then(res => {
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
      this.$confirm('确定要删除选中的信息吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({lock: true});
        this.$http.delete('/softwarerelease/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      this.$http.put('/softwarerelease/status', {id: row.id, status: row.status}).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message.success(res.data.msg);
        } else {
          row.status = !row.status ? 1 : 2;
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    },
    /* 导出数据Excel */
    exportToExcel() {
       // 创建 Excel 文件
      const workbook = XLSX.utils.book_new();
      //去除不需要的字段，这里我不希望显示id，所以id不返回
      let temp = this.selection;
      // eslint-disable-next-line
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
      console.log(header)

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
      const fileName = '软件发布.xlsx';
      
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
