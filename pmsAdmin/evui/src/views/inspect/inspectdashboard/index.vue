<template>
    <div>
    <div class="ele-body">
      <el-card shadow="never">
        <el-form
        :model="where"
        label-width="100px"
        class="ele-form-search"
        @keyup.enter.native="reload"
        @submit.native.prevent>
        <el-row :gutter="10">
          <el-col :lg="6" :md="12"  >
            <el-date-picker
                v-model="selectDateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd HH:mm:ss"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect"
                @clear="handleClear">
              </el-date-picker>
          </el-col>
          <el-col :lg="6" :md="12" :offset="3">
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
          height="calc(100vh - 415px)">
          <template slot="toolbar">
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
        </ele-pro-table>
      </el-card>
  
      <el-card shadow="never" body-style="padding: 0;">
      <el-row>
          <el-col :lg="28" :md="26">
            <div class="demo-monitor-title">
              合格率
            </div>
            <ele-chart
              ref="saleChart"
              style="height: 385px;width: 100%"
              :option="saleChartOption"/>
          </el-col>
      </el-row>
      </el-card>
    </div>
    </div>
  </template>
  
  <script>
  import EleChart from 'ele-admin/packages/ele-chart';
  import { mapGetters } from "vuex";
  import XLSX from 'xlsx'
  import { saveAs } from 'file-saver';  
  
  
  export default {
    name: 'InspectDashboard',
    components: {EleChart},
  
    computed: {
      ...mapGetters(["permission"]),
  
          // 柱状图配置
      saleChartOption() {
        return {
          tooltip: {
            trigger: 'axis'
          },
          xAxis: [
            {
              name: '产品型号',
              type: 'category',
              data: this.saleroomData.map(d => d.item_number),
            }
          ],
          yAxis: [
            {
              type: 'value',
              min:0,
              max:100,
              interval:10,  //纵坐标刻度
            }
          ],
          series: [
            {
              name: '合格率',
              type: 'bar',
              data: this.saleroomData.map(d => d.target_actual_pass_rate),
              showBackground: true, //背景颜色
              barWidth:50,  //柱状图宽度
              backgroundStyle: {
                color:'rgba(180,180,180,0.2)'
              },
              itemStyle: {
                color: function(params) {
                  // 根据横坐标值动态设置颜色
                  if (params.data >= 95) {
                    return 'green';  // 偶数项为蓝色
                  } else {
                    return 'red';   // 奇数项为红色
                  }
                }
              }
            }
          ],
          color:[
            this.saleroomData.map(d => d.color)
          ]
        };
      },
    },
    data() {
      return {
        // 表格数据接口
        url: '/inspectreport/listOfTotal',
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
            prop: 'item_number',
            label: '产品型号',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'examine_amount_total_amount',
            label: '检验数量累计',
            // sortable: 'custom',
            showOverflowTooltip: true,
            align: 'center',
            minWidth: 150,
            resizable: false,
            // slot: 'status',
          },
          {
            prop: 'examine_bad_total_amount',
            label: '检验不良累计',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100
          },
          {
            prop: 'target_actual_pass_rate',
            label: '合格率',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100,
            formatter: (row, column, cellValue) => {
              return cellValue + '%';
            }
          },
        ],
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
        saleroomData: [],
        selection: [],
        // 表格搜索条件
        where: {},
        selectDateRange: '',
      };
    },
    created() {
        this.loading = true;
        this.$http.get('/inspectreport/listOfTotal',{params: this.where}).then((res) => {
          this.loading = false;
          if (res.data.code === 0) {
              this.saleroomData = res.data.data
              
          } else {
              this.$message.error(res.data.msg);
          }
          }).catch((e) => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    mounted() {
      this.getSaleroomData();
    },
    methods: {
      getSaleroomData(){
        // const months = ['IP','BM','SI','MPDU-Pro'];
        // this.saleroomData = months.map(month =>({
        //   month,
        //   value:Math.floor(Math.random()*100)
        // }))

        this.saleroomData = [
              {month: this.saleroomData.map(d => d.item_number), value: this.saleroomData.map(d => d.num),color:this.saleroomData.map(d => d.color)},
            ];
      },
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
        this.$http.get('/inspectreport/listOfTotal',{params: this.where}).then((res) => {
        this.loading = false;
        if (res.data.code === 0) {
            this.saleroomData = res.data.data
            
        } else {
            this.$message.error(res.data.msg);
        }
        }).catch((e) => {
        this.loading = false;
        this.$message.error(e.message);
        });
        this.getSaleroomData();
      },
      reset() {
        this.where = {};
        this.reload();
      },
      formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      },
      exportToExcel() {
        // 创建 Excel 文件
        const workbook = XLSX.utils.book_new();
        //去除不需要的字段，这里我不希望显示id，所以id不返回
        let temp = this.selection;
        // eslint-disable-next-line
        this.selection = this.selection.map(({ id, ...rest }) => rest);
        //可以将对应字段的数字经过判断转为对应的中文

        const worksheet = XLSX.utils.json_to_sheet(this.selection);

        // 获取字段名称（中文）
        const header = this.columns
          .slice(1) // 排除排除第一列,这里我排除的是我的id列
          .map(column => column.label);

        // 获取要导出的数据（排除第一列）
        const data = this.selection.map(row =>
          this.columns
            .slice(1) // 排除第一列
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
        const fileName = '质检报表统计.xlsx';
        
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
        // 选择日期范围查询
      dateRangeHandleSelect(){
        this.where.year = null
        this.where.month = null
        this.selectDate = null
        this.where.startTime = this.selectDateRange[0]
        this.where.endTime = this.selectDateRange[1]
      },
      handleClear(){
        this.reload();
      },
    },
    
    activated() {
      ['saleChart', ].forEach((name) => {
        this.$refs[name].resize();
      });
    },
  }
  </script>
  
  <style scoped>
  /* 小标题 */
  .demo-monitor-title {
    padding: 0 20px;
    margin: 15px 0 5px 0;
  }
  </style>
  