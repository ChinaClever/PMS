<template>
    <div class="ele-body">
      <el-card shadow="never">
        <!-- 意见反馈表单 -->
        <el-form
          :model="where"
          label-width="77px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="10">
            <el-col :span="5">
              <el-form-item label="产品名称:">
                <el-input
                  clearable
                  v-model="where.name"
                  @clear="this.reload"
                  placeholder="请输入产品名称"/>
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="单号:">
                <el-input
                  clearable
                  v-model="where.work_order"
                  @clear="this.reload"
                  placeholder="请输入单号"/>
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
          <el-row :gutter="10">
            <el-col :span="5" >
              <el-form-item label="排序方式:">
              <el-select v-model="selectedOption" placeholder="请选择排序方式" @change="selectway">
                  <el-option label="产品名称" value="name"></el-option>
                  <el-option label="单号" value="work_order"></el-option>
              </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="5">
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
            <!-- 导出按钮 -->
            <el-button
              size="small"
              type="success"
              icon="el-icon-download"
              class="ele-btn-icon"
              @click="exportToExcel">导出
            </el-button>
          </template>
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

        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
     
    </div>
  </template>

  <script>
  import { mapGetters } from "vuex";
  import XLSX from 'xlsx'
  import { saveAs } from 'file-saver';
  export default {
    name: 'repairreport',
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        current:'',
        // 表格数据接口
        url: '/repairreport/questionlist',
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
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'name',
            label: '产品名称',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'bad_phenomenon',
            label: '不良现象',
            width: 300,
            align: 'center',
            slot: 'expand_1',
          },
          {
            prop: 'bad_number_total',
            label: '不良总数量',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'num',
            label: '出现次数',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
 

        ],
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
        selectedOption: 'name',

      };
    },
    // created() {
    //     this.selectway();
    //     this.loading = true;
    //     this.$http.get('/repairreport/questionlist').then((res) => {
    //     this.loading = false;
    //     }).catch((e) => {
    //     this.loading = false;
    //     this.$message.error(e.message);
    //     });
    // },
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
        this.selectedOption = 'name';
        this.reload();
      },
      selectway() {
        this.where = {};
        if (this.selectedOption=="name"){
          this.where.name1 = this.selectedOption;
        }else if (this.selectedOption=="work_order"){
          this.where.work_order1 = this.selectedOption;
        }
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
        .slice(1) // 排除排除第一列和最后一列,这里我排除的是我的id列和操作列
        .map(column => column.label);
      // 获取要导出的数据（排除第一列和最后一列）
      const data = this.selection.map(row =>
        this.columns
          .slice(1) // 排除第一列和最后一列
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
