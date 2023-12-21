<template>
  <div class="ele-text-center">
    <el-card class="custom-table">
      <ele-pro-table
          ref="table"
          :datasource="url"
          :columns="columns"
          :row-style="getRowsStyle"
          border class="custom-table"
          :cell-style="cellStyle"
          :header-cell-style="headerCellStyle"
          height="calc(60vh - 215px)">
      </ele-pro-table>
    </el-card>
    <el-card class="custom-table" body-style="padding: 0;" align="center">
      <el-col :lg="48" :md="46">
        <div class="demo-monitor-title">
          交付数量
        </div>
        <ele-chart
        ref="saleChart"
        style="height: 285px;"
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
  computed: {
    deliveryChartOption(){
      return {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            type: 'category',
            data: this.DeliveryData.map(d => d.name)
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            type: 'bar',
            data: this.DeliveryData.map(d => d.product_count)
          }
        ]
      };
    }
  },
  data() {
    return {
      loading: true,  // 加载状态
      // 表格数据接口
      url: '/comprehensive/DetailAll',
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

        ],
      //交付数量
      DeliveryData:[],
      //警告天数获取
      WarningData:[],
      //状态
      status:null,

    };
  },
  mounted() {
    this.getAllData();
    this.getWarningData();
    this.getDaysStyle();
  },
  methods: {
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
    getWarningData(){
      this.WarningData = [];
      this.$http.get('/comprehensive/DetailAll').then(res => {
        if (res.data.code === 0) {
          this.WarningData = res.data.data;
          } else {
            this.$message.error(res.data.msg || '获取工单号对应的数据失败');
          }
        }).catch(e => {
          this.$message.error(e.message);
        })
    },
    // //改变表格某一列或者某一个单元格文本颜色
    // cellStyle({row, column}) {
    //
    //   const dataAndDays = [
    //     {days:this.WarningData.inspect_duration_days},//质检所需天数
    //     {days:this.WarningData.debug_duration_days},//调试所需天数
    //     {days:this.WarningData.burning_duration_days},//烧录所需天数
    //     {days:this.WarningData.repair_duration_days},//维修所需天数
    //   ]
    //   dataAndDays.forEach(item=>{
    //     const dueDate = new Date();
    //     dueDate.setDate(dueDate.getDate()+ item.days)
    //     if(dueDate >= this.WarningData.deliveryDate){  //现在的时间加上排期表单上所需要的时间大于交货的日期，说明时间不够了
    //       this.status = 1;
    //     }
    //     else {
    //       this.status = 0;
    //     }
    //     // 定义样式变量
    //     let cellStyle;
    //     switch (this.status){
    //       case 0:
    //         cellStyle = 'color:#70DB92;background-color:#192a56';
    //         break;
    //
    //       case 1:
    //         cellStyle = 'color:red;background-color:#192a56';
    //         break;
    //
    //       default:
    //         cellStyle = '';
    //     }
    //   })
    //
    //
    //
    //   return cellStyle;
    // },
    headerCellStyle() {
      return {
        backgroundColor: '#192a56',
        color: 'white',
      };
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
.demo-monitor-title {
  padding: 0 0;
  margin: 0 0 0 0;
  font-size: 24px; /* 设置字体大小为 24 像素 */
  color: white; /* 设置字体颜色为白色 */
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  background-color: #192a56 !important; /* 设置表格的背景颜色 */

}
.custom-table {
    padding: 0 0;
    margin: 0 0 0 0;
  background-color: #192a56 !important; /* 设置表格的背景颜色 */
}
/* 表格内背景颜色 */
::v-deep .el-table th,
::v-deep .el-table tr,
::v-deep .el-table td {
  background-color: #192a56;
}
::v-deep .el-table {
  background-color: transparent !important;
}
::v-deep .el-table__row {
  background-color: #192a56 !important;
}
::v-deep .ele-text-center,::v-deep .number.active {
  background-color: #192a56 !important;
}
::v-deep .el-input__inner,::v-deep .ele-table-tool,::v-deep .ele-table-tool-default{
  background-color: #192a56 !important;
}

</style>
