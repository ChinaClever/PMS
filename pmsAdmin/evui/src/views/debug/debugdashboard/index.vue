<template>
    <div>
    <div class="ele-body">
      <el-card shadow="never">
        <el-form
        :model="where"
        label-width="77px"
        class="ele-form-search"
        @keyup.enter.native="reload"
        @submit.native.prevent>
        <el-row :gutter="10">
          <el-col :lg="6" :md="12" >
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
          <el-col :lg="6" :md="12" :offest="4">
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
          :cell-style="cellStyle"
          :where="where"
          :datasource="url"
          :columns="columns"   
          border class="custom-table"     
          height="calc(60vh - 215px)">
        </ele-pro-table>
      </el-card>
  
      <el-card shadow="never" body-style="padding: 0;" align="center">
      <el-row>
          <el-col :lg="48" :md="46">
            <div class="demo-monitor-title">
              调试总数量
            </div>
            <ele-chart
              ref="saleChart"
              border class="custom-chart"
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

  
  export default {
    name: 'RepairDashboard',
    components: {EleChart},
  
    computed: {
      ...mapGetters(["permission"]),
  
          // 柱状图配置
      saleChartOption() {
        return {
          grid: {
                  top: '10%',
                  bottom: '20%'
                },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: [
            {
              type: 'category',
              data: this.saleroomData.map(d => d.product_name),
              axisLabel: {
                color: 'white' // 设置 x 轴标签的颜色为白色
              }
            }
          ],

          yAxis:[
            {
              name: '数量',
              type: 'value',
              data: this.saleroomData.map(d => d.number_total),
              axisLabel: {
                color: 'white' // 设置 x 轴标签的颜色为白色
              }

            },

          ],
          color:[
            this.saleroomData.map(d => d.color)
          ],
          series:[
            {
              name: '数量总和',
              type: 'bar',
              data: this.saleroomData.map(d => d.number_total),
              showBackground: true,
              barWidth: 50,
              backgroundStyle: {
                color: 'transparent'
              },

              itemStyle:{
                color: function() {
                  return 'orange';
                }
              }
            },
          ]
        };
      },
    },
    data() {
      return {
        // 表格数据接口
        url: '/debugreport/listOf1',
        // 表格列配置
        columns: [
          {
            prop: 'work_order',
            label: '单号',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'client_name',
            label: '客户名称',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'product_name',
            label: '产品名称',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'number_total',
            label: '调试数量',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100
          },
          {
            prop: 'product_count',
            label: '产品数量',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100
          },
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
          },
            {
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
        saleroomData: [],
        // 表格搜索条件
        where: {},
      };
    },
    created() {

        this.loading = true;
        this.$http.get('/debugreport/listOf').then((res) => {

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

    methods: {
      //向后端传时间
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


      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
        const condition = {
          startTime: this.where.selectStartDate ,
          endTime: this.where.selectEndDate,

        };
        this.$http.get('/debugreport/listOf',{params:condition}).then((res) => {
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

      reset() {
        this.where = {};
        this.selectDateRange = null;
        this.reload();
      },
       //改变表格偶数行颜色 
       cellStyle({ rowIndex }) {//一定要注意rowIndex是一个数组要用花括号包裹起来，不能没有
      if (rowIndex % 2 === 0) {
        return {
          backgroundColor: '#123782',
          color: 'white',
        };
      }
      return {};
    },

    },
    activated() {
      ['saleChart', ].forEach((name) => {
        this.$refs[name].resize();
      });
    }
  }
  </script>
  
  <style scoped>
  /* 小标题 */
  .demo-monitor-title {
    padding: 0 0;
    margin: 0 0 20px 0;
    font-size: 24px; /* 设置字体大小为 24 像素 */
    height: 20px;
    color:white;
    display: flex;
    justify-content: center; /* 水平居中对齐 */
    align-items: center; /* 垂直居中对齐 */
    /*margin-bottom: -10px;*/

  }

  .custom-chart{
    height: 30vh;
    justify-content: center; /* 在水平方向上居中对齐 */
  
}
  .custom-table {
    padding: 0 0;
    margin: 0 0 0 0;
    background-color: #072e7d !important; /* 设置表格的背景颜色 */
    /* height: 50vh;
    flex: 1;
    overflow: auto;
    display: flex;
    flex-direction: column; */
}
::v-deep .ele-body{
  background-color: #072e7d !important; /* 设置最外面的背景颜色 */
  display: flex;
  flex-direction: column;
  height: 100vh; /* 或者适当的高度 */
}

/* 表格内背景颜色*/
::v-deep .el-table th,
::v-deep .el-table tr,
::v-deep .el-table td {
  background-color:#072e7d;  /* 背景透明*/
  border: 0px;
  color: #93dcfe;  /* 修改字体颜色*/
  font-size: 20px;
  height: 5px;

}
/* 去掉最下面的那一条线*/
.el-table::before {
  height: 0px;
}
/* 修改表头样式-加边框*/
::v-deep .el-table__header-wrapper {
  border: solid 1px white;
  /* box-sizing: border-box;*/
}
/*表格斑马自定义颜色
::v-deep .el-table__row.warning-row {
  background: #090c0f;
}*/


/*修改高亮当前行颜色*/
::v-deep .el-table tbody tr:hover > td {
  background: #4a4c4e !important;
}

/*滚动条样式*/
::v-deep .el-table__body-wrapper::-webkit-scrollbar-track {
  background-color: #063570;
}
 
::v-deep .el-table__body-wrapper::-webkit-scrollbar {
  width: 10px;
  opacity: 0.5;
}
 
::v-deep .el-table__body-wrapper::-webkit-scrollbar-thumb {
  border-radius: 15px;
  background-color: #0257aa;
}



::v-deep .el-table {
  background-color: transparent !important;
}
::v-deep .el-card__body{
  background-color: #072e7d !important; /* 设置表格的背景颜色 */
}
::v-deep  .ele-table-tool.ele-table-tool-default{
  background-color: #072e7d !important; /* 设置的背景颜色 */
}
::v-deep  .el-pagination__total,::v-deep  .el-pagination__jump{
  color: white !important; /* 设置最下面的文字颜色 */
}
::v-deep  .ele-tool-item, ::v-deep .ele-action, ::v-deep  .el-icon-_nav{
  color: white !important; /* 右上方四个按钮 */
}
::v-deep  .el-input__inner{
  background-color:#e9eaf0  !important; /* 各个按键 */
}
  </style>