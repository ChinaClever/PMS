<template>
  <div class="ele-body">
    <el-card shadow="never">
      <!-- 数据表格 -->
<!--      <el-table ref="table" :data="Data"  v-loading="loading" row-key="id" default-expand-all border-->
<!--                height="calc(50vh - 100px)" highlight-current-row >-->
<!--        <el-table-column label="序号" type="index" width="60" align="center" fixed="left"/>-->
<!--        <el-table-column prop="work_order" label="工单号" min-width="150" align="center"/>-->
<!--        <el-table-column prop="customer_name" label="客户名称" min-width="150" align="center"/>-->
<!--        <el-table-column prop="specification_model" label="规格型号" min-width="150" align="center"/>-->
<!--        <el-table-column prop="delivery_time" label="交期" min-width="150" align="center"/>-->
<!--        <el-table-column prop="start_date" label="开始日期" min-width="150" align="center"/>-->
<!--        <el-table-column prop="burn_date" label="烧录数量" min-width="100" align="center"/>-->
<!--        <el-table-column prop="debug_quantity" label="调试数量" min-width="100" align="center"/>-->
<!--        <el-table-column prop="quality_quantity" label="质检数量" min-width="100" align="center"/>-->
<!--        <el-table-column prop="maintenance_quantity" label="维修数量" min-width="100" align="center"/>-->
<!--        <el-table-column prop="end_date" label="完成日期" min-width="160" align="center"/>-->
<!--      </el-table>-->
      <ele-pro-table
              ref="table"
              :datasource="url"
              :columns="columns"
              :selection.sync="selection"
              height="calc(60vh - 215px)">
      </ele-pro-table>
    </el-card>
    <el-card shadow="never" body-style="padding: 0;" align="center">
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
// import CityEdit from './city-edit';

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
      // 表格选中数据
      selection: [],
      // //数据
      // Data:[],
      //交付数量
      DeliveryData:[],

    };
  },
  mounted() {
    this.getAllData();
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
    }

  }
}

</script>

<style scoped>
</style>
