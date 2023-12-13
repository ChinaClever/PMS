<template>
  <div class="ele-body ele-body-card">
    <!-- 销售额、访问量 -->
        <el-row :gutter="15">
            <el-col :lg="12" :md="16">
                <el-card >
                  <div class="card-header">
                    <div class="card-label">维修数量占比</div>
                      <div class="card-month"></div>
                      <el-date-picker
                      v-model="value2"
                      type="month"
                      placeholder="选择月份"
                      @change="getPayNumData">
                      </el-date-picker>
                  </div>
                  <div>
                  <ele-chart
                    ref="browserChart"
                    style="height: 280px;"
                    :option="saleChartOption"/>
                  </div>
                </el-card>

            </el-col>
            <el-col :lg="12" :md="16">
                <el-card>
                  <div class="card-header">
                    <div class="card-label">维修数量</div>
                      <div class="card-month"></div>
                      <el-date-picker
                      v-model="value2"
                      type="month"
                      placeholder="选择月">
                      </el-date-picker>
                  </div>
                  <div>
                  <ele-chart
                    ref="browserChart"
                    style="height: 280px;"
                    :option="saleChartOption"/>
                  </div>
                </el-card>
            </el-col>
        </el-row>
    <!-- 最近1小时访问情况 -->
      <div>
        <el-row :gutter="15">
        <el-col :lg="12" :md="16">
          <el-card header="维修原因">
            <ele-word-cloud
              ref="hotSearchChart"
              :data="hotSearchData"
              style="height: 303px;"/>
          </el-card>
        </el-col>
        <el-col :lg="12" :md="16">
          <el-card header="维修原因排名">
          <div
            v-for="(item, index) in saleroomRankData"
            :key="index"
            class="demo-monitor-rank-item ele-cell">
            <el-tag
              size="mini"
              type="info"
              :effect="index < 3 ? 'dark' : 'light'"
              :color="index < 3 ? '#314659' : 'hsla(0, 0%, 60%, .2)'"
              style="border-color: transparent;"
              class="ele-tag-round">
              {{ index + 1 }}
            </el-tag>
            <div class="ele-cell-content">{{ item.name }}</div>
            <div class="ele-text-secondary">{{ item.value }}</div>
          </div>
          </el-card>
        </el-col>
      </el-row>
      </div>
  </div>
</template>

<script>
import EleChart from 'ele-admin/packages/ele-chart';
import EleWordCloud from 'ele-admin/packages/ele-word-cloud';

export default {
  name: 'DashboardAnalysis',
  components: {EleChart, EleWordCloud},
  data() {
    return {
      // 支付笔数
      payNumData: [],
      // 销售量数据
      saleroomData: [],
      // 销售量排名数据
      saleroomRankData: [],
      // 词云数据
      hotSearchData: [],
      value2:null
    };
  },
  computed: {
    // 销售额柱状图配置
    saleChartOption() {
        return {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: this.payNumData.map(d => d.name),
          bottom: 10,
          itemWidth: 20,
          itemHeight: 20,
          icon: 'circle',
        },
        series: [
          {
            type: 'pie',
            radius: ['45%', '70%'],
            center: ['50%', '43%'],

            label: {
              show: false
            },
            data: this.payNumData
          }
        ]
      };
    },
  },
  mounted() {
    this.getPayNumData();
    this.getSaleroomData();
    this.getWordCloudData();
  },
  methods: {
    /* 获取支付笔数数据 */
    getPayNumData() {
      console.log("选择的月份",this.value2);
      this.payNumData = [
        {name: 'IP-PDU', value: 9052},
        {name: 'M-PDU', value: 535},
        {name: 'SI-PDU', value: 1610},
        {name: 'BM-PDU', value: 2800},
        {name: '执行板', value: 3200},
        {name: 'Other', value: 1700}
      ];
    },
    /* 获取销售量数据 */
    getSaleroomData() {
        this.saleroomData = [
          {month: '1月', value: 816},
          {month: '2月', value: 542},
          {month: '3月', value: 914},
          {month: '4月', value: 781},
          {month: '5月', value: 355},
          {month: '6月', value: 796},
          {month: '7月', value: 714},
          {month: '8月', value: 1195},
          {month: '9月', value: 1055},
          {month: '10月', value: 271},
          {month: '11月', value: 384},
          {month: '12月', value: 1098}
        ];

      this.saleroomRankData = [
        {name: '硬件维修', value: '124,643'},
        {name: '软件BUG', value: '456,465'},
        {name: '测试软件BUG', value: '776,679'},
        {name: '电源损坏', value: '456,658'},
        {name: '芯片损毁', value: '245,466'},
        {name: '模具损毁', value: '887,344'},
        {name: '线路损坏', value: '897,233'},
        {name: '无软件', value: '887,344'},
      ];
      this.saleroomRankData = this.saleroomRankData.sort((a,b)=>a.value-b.value).slice(0,8)
    },
    /* 获取词云数据 */
    getWordCloudData() {
      this.hotSearchData = [
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
        {name: "硬件维修", value: 23},
        {name: "软件", value: 23},
        {name: "电源芯片损坏", value: 23},
        {name: "通讯芯片损坏", value: 22},
      ];
    },
    /* 销售量tab选择改变事件 */
    onSaleTypeChange() {
      this.getSaleroomData();
    }
  },
  activated() {
    ['browserChart', 'payNumChart', 'saleChart', 'visitHourChart', 'hotSearchChart'].forEach((name) => {
      this.$refs[name].resize();
    });
  }
}
</script>

<style scoped>

.demo-monitor-tool ::v-deep .el-tabs__nav-wrap:after {
  display: none;
}

.demo-monitor-tool ::v-deep .el-tabs__item {
  height: 50px;
  line-height: 50px;
  font-size: 15px;
}

.demo-monitor-tool .el-date-editor {
  width: 256px;
  margin-left: 10px;
}

/* 排名item */
.demo-monitor-rank-item {
  padding: 0 20px;
  line-height: 20px;
  margin-top: 18px;
}
.card-header{
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-label{
    text-align: left;
    font-weight: bold;
}
.card-month{
    text-align: right;
}
</style>
