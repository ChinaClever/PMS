<template>
  <div class="ele-body">
    <el-card shadow="never">
      
      <el-dialog
        title="导入文件"
        :visible.sync="showImport"
        width="30%">
        <!-- 这里放置上传文件的表单 -->
        <el-upload
          class="upload-demo"
          action="http://localhost:8000/safety/upload"
          accept=".xls,.xlsx"     
          :on-success="importFile"
          :on-error="handleUploadError" 
          :show-file-list="false">
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload>
      </el-dialog>
      <!-- 搜索表单 -->
      <el-form
        :model="where"
        label-width="77px"
        class="ele-form-search"
        @keyup.enter.native="reload"
        @submit.native.prevent>
        <el-row :gutter="15">
          <el-col :lg="6" :md="19">
            <el-form-item label="查询:">
              <el-input
                clearable
                v-model="where.keyword"
                @clear="reload"
                placeholder="请输入单号"/>
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
                start-placeholder="创建时间开始日期"
                end-placeholder="创建时间结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd"
                @clear="reload"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect">
              </el-date-picker>
            </div>

            <div class="ele-text-center">
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

         <!-- 结果列 -->
         <template slot="result" slot-scope="{row}">
          <el-tag v-if="row.result === '通过'" type="success" size="small">通过</el-tag>
          <el-tag v-if="row.result === '失败'" type="danger" size="small">失败</el-tag>
        </template>
        <!-- 表头工具栏 -->
        <template slot="toolbar">
          <el-button
            size="small"
            type="primary"
            icon="el-icon-plus"
            class="ele-btn-icon"
            @click="openEdit(null)"
            v-if="permission.includes('sys:safety:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:safety:dall')">删除
          </el-button>

           <!-- 导出按钮 -->
           <el-button
            size="small"
            type="success"
            icon="el-icon-download"
            class="ele-btn-icon"
            @click="exportToExcel">导出
          </el-button>

          
          <el-button
            @click="showImport = true"
            icon="el-icon-upload2"
            class="ele-btn-icon"
            size="small">导入
          </el-button>
         
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:safety:update')">修改
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
              v-if="permission.includes('sys:safety:delete')">删除
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
    <safety-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
  
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import SafetyEdit from './safety-edit';
import XLSX from 'xlsx'
import { saveAs } from 'file-saver';



export default {
  name: 'SystemSafety',
  components: {SafetyEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/safety/list',
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
          prop: 'work_order',
          label: '单号',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'softwareType',
          label: '软件类型',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'productType',
          label: '产品类型',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'productSN',
          label: '产品序列号',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'Gnd',
          label: '接地电阻',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'Ir',
          label: '绝缘电阻',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'Dcw',
          label: '直流耐压',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'Acw',
          label: '交流耐压',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'result',
          label: '结果',
          slot: 'result',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'softwareVersion',
          label: '软件版本',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'companyName',
          label: '公司名称',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'protocolVersion',
          label: '协议版本',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'testStartTime',
          label: '测试开始时间',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'testEndTime',
          label: '测试结束时间',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'testTime',
          label: '测试时间',
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
      // 选择的日期范围
      selectDateRange: '',
      // 表格搜索条件
      where: {},
      // 表格选中数据
      selection: [],
      // 当前编辑数据
      current: null,
      // 是否显示编辑弹窗
      showEdit: false,
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
      // 是否显示导入弹窗
      showImport: false
    };
  },
  methods: {
      // 显示导入弹窗
  showImportDialog() {
    this.showImport = true;
  },

  // 导入文件处理
  importFile(response) {
    console.log(response)
    if (response.code === -1) {
            this.$message.error(response.msg);
          }
        this.reload();
        this.showImport=false
      },
  handleUploadError(err) {  
    console.log(err)
    // console.log(this.$message.error(res.msg))
    // this.$message.error(res.msg);  // 打印错误信息
  },  
    /* 刷新表格 */
    reload() {
      console.log(this.selection)
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
        this.$http.get('/safety/detail/' + row.id).then((res) => {
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
      this.$http.delete('/safety/delete/' + row.id).then(res => {
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
        this.$http.delete('/safety/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
    // make() {
    //   // 在这里调用后端函数
    //   this.$http.get('/safety/make')
    //     .then(response => {
    //       // 处理成功响应
    //       console.log(response.data);
    //       // 可以在这里更新页面或执行其他操作
    //       this.reload();
    //     })
    //     .catch(error => {
    //       // 处理错误响应
    //       console.error(error);
    //     });
    // },
    /* 更改状态 */
    editStatus(row) {
      const loading = this.$loading({lock: true});
      this.$http.put('/safety/status', {id: row.id, status: row.status}).then(res => {
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
      const worksheet = XLSX.utils.json_to_sheet(this.selection);

      // 获取字段名称（中文）
      const header = this.columns
        .slice(2, -1) // 排除排除第一列和最后一列,这里我排除的是我的id列和操作列
        .map(column => column.label);

      // 获取要导出的数据（排除第一列和最后一列）
      const data = this.selection.map(row =>
        this.columns
          .slice(2, -1) // 排除第一列和最后一列
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
      const fileName = '安规测试表.xlsx';
      
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
