<template>
  <div class="ele-text-center">
    <el-card class="custom-table">
      <ele-pro-table
          ref="table"
          :datasource="url"
          :columns="columns"
          border class="custom-table"
         :header-cell-style="headerCellStyle"
          :cell-style="cellStyle"
          height="calc(110vh - 215px)">
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
            show:true,
          },
          {
            prop: 'debug_duration_days',
            label: '调试天数',
            show:true,
          },
          {
            prop: 'burning_duration_days',
            label: '烧录天数',
            show:true,
          },
          {
            prop: 'repair_duration_days',
            label: '维修天数',
            show:true,
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
    cellStyle({row,column}) {

        if(column.property === 'inspect_quantity' &&
          row.deliveryDate &&
          row.inspect_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const inspect_duration_days = row.inspect_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + inspect_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.inspect_quantity)
            {
              return 'color:green'
            }
            return 'color:red'
          }
          else
          {
            return 'color:green'
          }
        }
        if(column.property === 'repair_quantity' &&
          row.deliveryDate &&
          row.repair_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const repair_duration_days = row.repair_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + repair_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.repair_quantity)
            {
              return 'color:green'
            }
            return 'color:red'
          }
          else
          {
            return 'color:green'
          }
        }
        if(column.property === 'burning_quantity' &&
          row.deliveryDate &&
          row.burning_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const burning_duration_days = row.burning_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + burning_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.burning_quantity)
            {
              return 'color:green'
            }
              return 'color:red'
          }
          else
          {
              return 'color:green'
          }
        }
        if(column.property === 'debug_quantity' &&
          row.deliveryDate &&
          row.debug_duration_days)
        {
          const completionTime = new Date(row.deliveryDate); //交付时间
          const debug_duration_days = row.debug_duration_days;
          const nowDate = new Date()
          const dueDate = new Date(nowDate.getTime() + debug_duration_days*24*60*60*1000)
          if(dueDate > completionTime)
          {
            if(row.product_count === row.debug_quantity)
            {
              return 'color:green'
            }
            return 'color:red'
          }
          else
          {
            return 'color:green'
          }

        }
        return {
          backgroundColor: '#192a56',
          color: 'white',
        }
    },
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

@keyframes blink-animation {
  0%{
    background-color:red;
  }
  50%{
    background-color: transparent;
  }
  100%{
    background-color: red;
  }
}


</style>
