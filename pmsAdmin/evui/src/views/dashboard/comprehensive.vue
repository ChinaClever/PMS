<template>
  <div class="ele-text-center">
    <el-card class="custom-table">

      <ele-pro-table
          ref="table"
          :datasource="url"
          :columns="columns"
          border class="custom-table"
          :cell-style="cellStyle"
          height="calc(110vh - 215px)">
         <template slot="toolbar">
        <el-tooltip content="提示:交付日期邻近,还未进行生产或生产数量不足">
          <span class="custom-tooltip-red"></span>
        </el-tooltip>
        <el-tooltip content="提示:交付日期邻近,生产数量完毕">
          <span class="custom-tooltip-green"></span>
        </el-tooltip>
        <el-tooltip content="提示:未邻近交付日期,正常显示">
          <span class="custom-tooltip-white"></span>
        </el-tooltip>
        </template>
      </ele-pro-table>
    </el-card>
    <el-card class="custom-table" body-style="padding: 0;" align="center">
      <el-col :lg="48" :md="46">
        <div class="demo-monitor-title">
          交付数量
        </div>
        <ele-chart
        ref="saleChart"
        border class="custom-chart"
        :option="deliveryChartOption"/>
      </el-col>
    </el-card>
  </div>
</template>

<script>
import EleChart from 'ele-admin/packages/ele-chart';

export default {
  name: 'DashboardComprehensive',
  components: {EleChart},
  data() {
    return {
      loading: true,  // 加载状态
      // 表格数据接口
      url: '/comprehensive/DetailAll',
      // 表格列配置
      columns: [
          {
            prop: 'work_order_id',
            label: '工单号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'name',
            label: '客户名称',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'model',
            label: '规格型号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'deliveryDate',
            label: '交期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
          },
          {
            prop: 'startDate',
            label: '开始日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
          },
          {
            prop: 'product_count',
            label: '订单数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'burning_quantity',
            label: '烧录数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'debug_quantity',
            label: '调试数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'inspect_quantity',
            label: '质检数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'repair_quantity',
            label: '维修数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'endDate',
            label: '完成日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
          },
          {
            prop: 'inspect_duration_days',
            label: '质检天数',
            show:false,
          },
          {
            prop: 'debug_duration_days',
            label: '调试天数',
            show:false,
          },
          {
            prop: 'burning_duration_days',
            label: '烧录天数',
            show:false,
          },
        ],
      //交付数量
      DeliveryData:[],
    };
  },
  computed: {
    deliveryChartOption(){
      return {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            type: 'category',
            data: this.DeliveryData.map(d => d.name),
            axisLabel: {
            color: 'white' // 设置 x 轴标签的颜色为白色
            },
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisLabel: {
              color: 'white' // 设置 y 轴标签的颜色为白色
            },
          }
        ],
        series: [
          {
            type: 'bar',
            data: this.DeliveryData.map(d => d.product_count)
          }
        ]
      };
    },
  },
  mounted() {
    this.getAllData();
  },
  methods: {
    //转换时间成数据库内的格式
    formatDate(date) {
      if (date != null){
        return date.toLocaleString('zh-CN',{
          year:'numeric',
          month:'2-digit',
          day:'2-digit',
          hour12:false
      }).replace(/\//g, '-');
      }
    },
    getAllData(){
      this.loading = true;
      this.DeliveryData = [];
      this.$http.get('/comprehensive/ShipmentData').then(res => {
        this.loading = false;
        if (res.data.code === 0) {
          this.DeliveryData = res.data.data;
           // console.log(res.data.data)
          } else {
            this.loading = false;
            this.$message.error(res.data.msg || '获取工单号对应的数据失败');
          }
        }).catch(e => {
          this.loading = false;
          this.$message.error(e.message);
        })
    },
    // //改变表格某一列或者某一个单元格文本颜色
    cellStyle({row,column,rowIndex}) {
        //质检数量
        if(column.property === 'inspect_quantity' && row.deliveryDate && row.inspect_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const inspect_duration_days = row.inspect_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + inspect_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.inspect_quantity)
            {
              return {
                backgroundColor: '#123782',
                color: 'green',
              };
            }
            return {
              backgroundColor: '#123782',
              color: 'red',
            };
          }
        }
        //维修数量
        // if(column.property === 'repair_quantity' && row.deliveryDate && row.repair_duration_days)
        // {
        //   const completionTime = new Date(row.deliveryDate); //交付时间
        //   const repair_duration_days = row.repair_duration_days;
        //   const nowDate = new Date()
        //   const dueDate = new Date(nowDate.getTime() + repair_duration_days*24*60*60*1000)
        //   if(dueDate > completionTime)
        //   {
        //     if(row.product_count === row.repair_quantity)
        //     {
        //       return {
        //         backgroundColor: '#123782',
        //         color: 'green',
        //       };
        //     }
        //     return {
        //       backgroundColor: '#123782',
        //       color: 'red',
        //     };
        //   }
        // }
        //烧录数量
        if(column.property === 'burning_quantity' && row.deliveryDate && row.burning_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const burning_duration_days = row.burning_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + burning_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.burning_quantity)
            {
              return {
                backgroundColor: '#123782',
                color: 'green',
              };
            }
            return {
              backgroundColor: '#123782',
              color: 'red',
            };
          }
        }
        //调试数量
        if(column.property === 'debug_quantity' && row.deliveryDate && row.debug_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const debug_duration_days = row.debug_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + debug_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.debug_quantity)
            {
              return {
                backgroundColor: '#123782',
                color: 'green',
              };
            }
            return {
              backgroundColor: '#123782',
              color: 'red',
            };
          }
        }
        if (rowIndex % 2 === 0) {
          return {
            backgroundColor: '#123782',
            color: 'white',
          };
        }
        return {};
    },

    activated() {
      ['saleChart', ].forEach((name) => {
        this.$refs[name].resize();
      });
    }
  }
}
</script>

<style scoped>
.demo-monitor-title {
  padding: 0 0;
  margin: 0 0 0 0;
  font-size: 24px; /* 设置字体大小为 24 像素 */
  color: white; /* 设置字体颜色为白色 */
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  //background-color: #192a56 !important; /* 设置表格的背景颜色 */
}
.custom-chart{
  height: 30vh;
  justify-content: center; /* 在水平方向上居中对齐 */
}
.custom-table {
  padding: 0 0;
  margin: 0 0 0 0;
  background-color: #072e7d !important; /* 设置表格的背景颜色 */
  //height: 50vh;
  //flex: 1;
  //overflow: auto;
  //display: flex;
  //flex-direction: column;
}

::v-deep .ele-body{
  background-color: #072e7d !important; /* 设置最外面的背景颜色 */
  display: flex;
  flex-direction: column;
  height: 100vh; /* 或者适当的高度 */
}
/* 表格内背景颜色 */
::v-deep .el-table th,
::v-deep .el-table tr,
::v-deep .el-table td {
  background-color:#072e7d;  /* 背景透明*/
  border: 0px;
  color: white;  /* 修改字体颜色*/
  font-size: 20px;
  height: 5px;
}
/* 去掉最下面的那一条线*/
.el-table::before {
  height: 0px;
}
/* 修改表头样式-加边框*/
::v-deep .el-table__header-wrapper {
  border: 0px;
  /* box-sizing: border-box;*/
}

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

::v-deep  .el-pagination__total,::v-deep  .el-pagination__jump{
  color: white !important; /* 设置最下面的文字颜色 */
}
::v-deep .el-table {
  background-color: transparent !important;
}
::v-deep .el-table__row {
  background-color: #072e7d !important;
}
::v-deep .ele-text-center,::v-deep .number.active {
  background-color: #072e7d !important;
}

::v-deep .el-input__inner,::v-deep .ele-table-tool,::v-deep .ele-table-tool-default{
  background-color: #072e7d !important;
}

::v-deep .el-card__body{
  background-color: #072e7d !important; /* 设置表格的背景颜色 */
}

::v-deep  .ele-tool-item, ::v-deep .ele-action, ::v-deep  .el-icon-_nav{
  color: white !important; /* 右上方四个按钮 */
}

.custom-tooltip-red{
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: red;
  color: white;
  text-align: center;
  line-height: 20px;
  cursor: pointer;
}
.custom-tooltip-green{
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: green;
  color: white;
  text-align: center;
  line-height: 20px;
  cursor: pointer;
}
.custom-tooltip-white{
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: white;
  color: white;
  text-align: center;
  line-height: 20px;
  cursor: pointer;
}




</style>
