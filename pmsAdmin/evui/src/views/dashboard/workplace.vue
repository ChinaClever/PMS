<template>
  <div class="ele-body ele-body-card">
<!--      模块数据-->
    <el-card>
      <!-- 顶部统计卡片 -->

      <el-row :gutter="15">
        <div class="ele-text-left">
          <el-tag type="info" size="medium">模块数据</el-tag>
        </div>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">模块生产总数量</div>
              <el-tag size="mini">个</el-tag>
            </div>
            <div v-if="ShipmentAllDataIsLoading" class="analysis-chart-card-num">0</div>
            <div v-else class="analysis-chart-card-num">{{ ShipmentAllData.AllShipmentModelQuantity }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">模块生产效率</div>
              <el-tag size="mini">个/天</el-tag>
            </div>
            <div v-if="ShipmentAllDataIsLoading" class="analysis-chart-card-num">0</div>
            <div v-else class="analysis-chart-card-num">{{ ShipmentAllData.ModelTotalEfficiency }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content ele-text-left">模块成品合格率</div>
              <el-tag  size="mini">总</el-tag>
              <div class="ele-cell-content ele-text-right">模块半成品合格率</div>
            </div>
            <div v-if="AllPassDataIsLoading" class="container">
              <div class="analysis-chart-card-num ele-text-left">0%</div>
              <div class="analysis-chart-card-num ele-text-right">0%</div>
            </div>
            <div v-else class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ AllPassData.ModelTotalAllPass }}%</div>
              <div class="analysis-chart-card-num ele-text-right">{{ AllPassData.ModelTotalHalfPass }}%</div>
            </div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">工具使用时长</div>
              <el-tag size="mini">总</el-tag>
            </div>
            <div v-if="AllUseToolTimeLoading" class="container">
              <div class="analysis-chart-card-num ele-text-left">0</div>
            </div>
            <div v-else class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ AllUseToolTime.AllUseToolTimeHours }}H</div>
            </div>
            <el-divider/>
          </el-card>
        </el-col>

      </el-row>
<!--        柱状图-->
      <el-card shadow="never" body-style="padding: 0;">
        <div class="ele-cell demo-monitor-tool">
          <div class="ele-cell-content">
            <el-tabs
              v-model="ModelsaleSearch.type"
              class="demo-monitor-tabs"
              @tab-click="onModelsSaleTypeChange">
              <el-tab-pane label="模块生产数量&生产效率" name="procedureNumber"/>
              <el-tab-pane label="模块合格率" name="pass"/>
              <el-tab-pane label="工具使用时长" name="tooltime"/>
            </el-tabs>
          </div>
          <div class="ele-inline-block ele-text-right">
            <el-radio-group v-model="ModelsaleSearch.dateType" size="small" @change = "onModelsSaleTypeChange">
              <el-radio-button
                v-for="button in buttons"
                :key="button.value"
                :label="button.value"
                border>{{button.label}}
              </el-radio-button>
            </el-radio-group>
          </div>
          <div class="ele-inline-block ele-text-right"  style="width: 260px;">
            <el-date-picker
              unlink-panels
              type="daterange"
              class="ele-fluid"
              end-placeholder="结束日期"
              start-placeholder="开始日期"
              v-model="ModelsaleSearch.datetime"
              range-separator="至" size="small"
              @change = "onModelsSaleTypeChange"/>
          </div>
        </div>
        <el-divider/>
        <el-row>
          <el-col :lg="48" :md="58">
            <div v-if="ModelsaleSearch.type === 'procedureNumber'">
              <div v-if="AllModelsDataIsLoading">数据正在加载中。。。</div>
              <div v-else>
                <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="AllModelsDataChartOption" />
              </div>
            </div>
            <div v-else-if="ModelsaleSearch.type === 'pass'">
              <div v-if="AllModelsDataIsLoading">数据正在加载中。。。</div>
              <div v-else>
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="ModelPassChartOption"/>
              </div>
            </div>
            <div v-else-if="ModelsaleSearch.type === 'tooltime'">
              <div v-if="GetToolTimeIsLoading">数据正在加载中。。。</div>
              <div v-else>
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="tooltimeChartOption"/>
              </div>
            </div>

          </el-col>
        </el-row>
      </el-card>
    </el-card>
<!--      成品数据-->
    <el-card>
      <!-- 顶部统计卡片 -->
      <el-row :gutter="15">
        <div class="ele-text-left">
          <el-tag type="info" size="medium">成品数据</el-tag>
        </div>
        <el-col :lg="8" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">成品生产总数量</div>
              <el-tag size="mini">个</el-tag>
            </div>
            <div v-if="ShipmentAllDataIsLoading" class="analysis-chart-card-num">0</div>
            <div v-else class="analysis-chart-card-num">{{ ShipmentAllData.AllShipmentFinishedQuantity }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="8" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">成品生产效率</div>
              <el-tag size="mini">个/天</el-tag>
            </div>
            <div v-if="ShipmentAllDataIsLoading" class="analysis-chart-card-num">0</div>
            <div v-else class="analysis-chart-card-num">{{ ShipmentAllData.FinishedTotalEfficiency }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="8" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content ele-text-left">成品合格率</div>
              <el-tag  size="mini">总</el-tag>
              <div class="ele-cell-content ele-text-right">半成品合格率</div>
            </div>
            <div v-if="AllPassDataIsLoading" class="container">
              <div class="analysis-chart-card-num ele-text-left">0%</div>
              <div class="analysis-chart-card-num ele-text-right">0%</div>
            </div>
            <div v-else class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ AllPassData.FinishedTotalAllPass }}%</div>
              <div class="analysis-chart-card-num ele-text-right">{{ AllPassData.FinishedTotalHalfPass }}%</div>
            </div>
            <el-divider/>
          </el-card>
        </el-col>
      </el-row>
<!--        柱状图-->
      <el-card shadow="never" body-style="padding: 0;">
        <div class="ele-cell demo-monitor-tool">
          <div class="ele-cell-content">
            <el-tabs
              v-model="saleSearch.type"
              class="demo-monitor-tabs"
              @tab-click="onFinishedSaleTypeChange">
              <el-tab-pane label="成品生产数量&生产效率" name="procedureNumber"/>
              <el-tab-pane label="成品合格率" name="pass"/>
            </el-tabs>
          </div>
          <div class="ele-inline-block ele-text-right">
            <el-radio-group v-model="saleSearch.dateType" size="small" @change="onFinishedSaleTypeChange">
              <el-radio-button
                v-for="button in buttons"
                :key="button.value"
                :label="button.value"
                border>{{button.label}}
              </el-radio-button>
            </el-radio-group>
          </div>
          <div class="ele-inline-block ele-text-right" style="width: 260px;">
            <el-date-picker
              unlink-panels
              type="daterange"
              class="ele-fluid"
              end-placeholder="结束日期"
              start-placeholder="开始日期"
              v-model="saleSearch.datetime"
              range-separator="至" size="small"
              @change="onFinishedSaleTypeChange"/>
          </div>
        </div>
        <el-divider/>
        <el-row>
          <el-col :lg="48" :md="58">
            <div v-if="saleSearch.type === 'procedureNumber'">
              <div v-if="AllFinishedDataIsLoading">数据正在加载中。。。</div>
              <div v-else>
                <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="AllFinishedDataChartOption" />
              </div>
            </div>
            <div v-else-if="saleSearch.type === 'pass'">
              <div v-if="AllFinishedDataIsLoading">数据正在加载中。。。</div>
              <div v-else>
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="FinishedPassChartOption"/>
              </div>
            </div>

          </el-col>
        </el-row>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import EleChart from 'ele-admin/packages/ele-chart';
// import EleWordCloud from 'ele-admin/packages/ele-word-cloud';

export default {
  name: 'DashboardWorkplace',
  components: {EleChart},
  data() {
    return {
      // 搜索参数
      ModelsaleSearch: {
        type: 'procedureNumber',
        dateType: 'year',
        datetime: ''
      },
      saleSearch: {
        type: 'procedureNumber',
        dateType: 'year',
        datetime: ''
      },

      buttons:[
        {label:'本年',value:'year'},
        {label:'本月',value:'month'},
        {label:'本周',value:'week'},
        {label:'今天',value:'today'},
      ],

      //生产排单总数据
      ShipmentAllData:{} ,
      ShipmentAllDataIsLoading:true,

      //通过率总数据
      AllPassData:{},
      AllPassDataIsLoading:true,

      //总的工具使用时长
      AllUseToolTime: {},
      AllUseToolTimeLoading:true,

      //所有模块的生产数据
      AllModelsData:[],
      AllModelsDataIsLoading:true,

      //所有成品的生产数据
      AllFinishedData:[],
      AllFinishedDataIsLoading:true,

      //获取工具的使用时长
      GetToolTime: [],
      GetToolTimeIsLoading:true,

    };
  },
  computed: {
    //模块生产数量&生产效率柱状图
    AllModelsDataChartOption(){
      return {
            title:{
              text:"生产数量&生产效率",
              left:'left',
              textStyle:{
                fontSize:10
              }
            },
            tooltip: {
              trigger: 'axis'
            },
            xAxis: [
              {
                type: 'category',
                data: this.AllModelsData.map(d => d.product_name)
              }
            ],
            yAxis: [
              {
                type: 'value',
                position:'left',
                axisLine:{
                  show:true
                },
                axisLabel:{
                  formatter:this.AllModelsData.map(d => d.ModelData)
                }
              },
              {
                type: 'value',
                position:'left',
                axisLine:{
                  show:true
                },
                axisLabel:{
                  formatter:this.AllModelsData.map(d => d.efficiency)
                }
              }
            ],
            series: [
              {
                name:'生产数量',
                type: 'bar',
                yAxisIndex:0,
                data: this.AllModelsData.map(d => d.ModelData)
              },
              {
                name:'生产效率 个/H',
                type: 'line',
                yAxisIndex:0,
                data: this.AllModelsData.map(d => d.efficiency)
              },
            ]
          };
    },
    // 模块合格率折线图配置
    ModelPassChartOption() {
      return {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['半成品', '成品'],
          right: 20
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: this.AllModelsData.map(d => d.product_name)
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '半成品',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.AllModelsData.map(d => d.Model_HalfPass)
          },
          {
            name: '成品',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.AllModelsData.map(d => d.Model_AllPass)
          }
        ]
      }
    },
    //成品生产数量&生产效率柱状图
    AllFinishedDataChartOption(){
      return {
            title:{
              text:"生产数量&生产效率",
              left:'left',
              textStyle:{
                fontSize:10
              }
            },
            tooltip: {
              trigger: 'axis'
            },
            xAxis: [
              {
                type: 'category',
                data: this.AllFinishedData.map(d => d.product_name)
              }
            ],
            yAxis: [
              {
                type: 'value',
                position:'left',
                axisLine:{
                  show:true
                },
                axisLabel:{
                  formatter:this.AllFinishedData.map(d => d.FinishedData)
                }
              },
              {
                type: 'value',
                position:'left',
                axisLine:{
                  show:true
                },
                axisLabel:{
                  formatter:this.AllFinishedData.map(d => d.efficiency)
                }
              }
            ],
            series: [
              {
                name:'生产数量',
                type: 'bar',
                yAxisIndex:0,
                data: this.AllFinishedData.map(d => d.FinishedData)
              },
              {
                name:'生产效率 个/H',
                type: 'line',
                yAxisIndex:0,
                data: this.AllFinishedData.map(d => d.efficiency)
              }
            ]
          };
    },
        // 成品合格率折线图配置
    FinishedPassChartOption() {
      return {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['半成品', '成品'],
          right: 20
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: this.AllFinishedData.map(d => d.product_name)
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '半成品',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.AllFinishedData.map(d => d.Finished_HalfPass)
          },
          {
            name: '成品',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.AllFinishedData.map(d => d.Finished_AllPass)
          }
        ]
      }
    },
    //工具使用时常柱状图   可能还需调整
    tooltimeChartOption(){
       return {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            type: 'category',
            data: ['调试  /  质检']
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
            data: this.GetToolTime.map(d => d.value1)
          },
          {
            type: 'bar',
            data: this.GetToolTime.map(d => d.value2)
          },

        ]
      };
    },

  },
  mounted() {
    this.changeTime();
    this.getAllNumAndEff();
    this.getModelAndFinishedPass();
    this.getAllUseToolTime();
    // this.getModelsStartEndData();
    this.getAllModelsData();
    this.getAllFinishedData();
    this.getToolUseTime();
  },
  methods: {
    //转换为中文的时间
    convertoChineseDate(date) {
      if (date != null) {
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
      }
    },
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
    changeTime() {
      if(this.ModelsaleSearch.datetime == null)
      {
        this.ModelsaleSearch.datetime='';
        this.ModelsaleSearch.datetime[0]='';
        this.ModelsaleSearch.datetime[1]=''
      }
    },
    //获取生产总数和生产效率（模块和成品）
    getAllNumAndEff(){
      this.$http.get('/workplace/ShipmentAllQuantity').then(res =>{
          if(res.data.code === 0) {
          this.ShipmentAllDataIsLoading = false;
          this.ShipmentAllData = res.data.data;
          // console.log(res.data.data)
            if(this.ShipmentAllData === null)
            {
              this.ShipmentAllDataIsLoading = true;
            }
          }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取模块和成品的合格率
    getModelAndFinishedPass() {
      this.$http.get('/workplace/AllPass').then(res =>{
        if(res.data.code === 0) {
          this.AllPassDataIsLoading = false;
          this.AllPassData = res.data.data;
          if(this.AllPassData === null)
          {
            this.AllPassDataIsLoading = true;
          }
        }
      }).catch(e => {
        this.AllPassDataIsLoading = true;
        this.$message.error(e.message);
      });
    },
    //获取工具使用的总时长
    getAllUseToolTime(){
      this.$http.get('/workplace/AllUseToolTime').then(res =>{
        if(res.data.code === 0) {
          this.AllUseToolTimeLoading = false;
          this.AllUseToolTime = res.data.data;
          if(this.AllUseToolTime === null)
          {
            this.AllUseToolTimeLoading = true;
          }
        }
      }).catch(e => {
        this.AllUseToolTimeLoading = true;
        this.$message.error(e.message);
      });
    },
    //获取模块所有数据（生产数量，生产合格率，使用时长）
    getAllModelsData() {
      if(this.ModelsaleSearch.datetime && this.ModelsaleSearch.datetime[0] && this.ModelsaleSearch.datetime[1])
      {
          this.$http.get('/workplace/AllModelsData', {
          params:{
                    tag:this.ModelsaleSearch.dateType,
                    start_date:this.formatDate(this.ModelsaleSearch.datetime[0]),
                    end_date:this.formatDate(this.ModelsaleSearch.datetime[1])
          }
            }).then(res =>{
          if(res.data.code === 0) {
            this.AllModelsDataIsLoading = false;
            this.AllModelsData = res.data.data;
            // console.log(res.data.data)
            if(this.AllModelsData === null)
            {
              this.AllModelsDataIsLoading = true;
            }
          }
        }).catch(e => {
          this.AllModelsDataIsLoading = true;
          this.$message.error(e.message);
        });
      }
      else {
        this.$http.get('/workplace/AllModelsData', {
          params:{
                    tag:this.ModelsaleSearch.dateType,
          }
            }).then(res =>{
          if(res.data.code === 0) {
            this.AllModelsDataIsLoading = false;
            this.AllModelsData = res.data.data;
            // console.log(res.data.data)
            if(this.AllModelsData === null)
            {
              this.AllModelsDataIsLoading = true;
            }
          }
        }).catch(e => {
          this.AllModelsDataIsLoading = true;
          this.$message.error(e.message);
        });
      }
    },
    // //获取成品所有数据（生产数量，生产合格率）
    getAllFinishedData() {
      if(this.saleSearch.datetime && this.saleSearch.datetime[0] && this.saleSearch.datetime[1])
      {
          this.$http.get('/workplace/AllFinishedData', {
          params:{
                    tag:this.saleSearch.dateType,
                    start_date:this.formatDate(this.saleSearch.datetime[0]),
                    end_date:this.formatDate(this.saleSearch.datetime[1])
          }
            }).then(res =>{
          if(res.data.code === 0) {
            this.AllFinishedDataIsLoading = false;
            this.AllFinishedData = res.data.data;
            // console.log(res.data.data)
            if(this.AllFinishedData === null)
            {
              this.AllFinishedDataIsLoading = true;
            }
          }
        }).catch(e => {
            this.$message.error(e.message);
        });
      }
      else {
        this.$http.get('/workplace/AllFinishedData', {
          params:{
                    tag:this.saleSearch.dateType,
          }
            }).then(res =>{
          if(res.data.code === 0) {
            this.AllFinishedDataIsLoading = false;
            this.AllFinishedData = res.data.data;
            // console.log(res.data.data)
            if(this.AllFinishedData === null)
            {
              this.AllFinishedDataIsLoading = true;
            }
          }
        }).catch(e => {
            this.$message.error(e.message);
        });
      }
    },
    //获取工具的使用时间
    getToolUseTime(){
      this.GetToolTime = [];
      if(this.ModelsaleSearch.datetime && this.ModelsaleSearch.datetime[0] && this.ModelsaleSearch.datetime[1])
      {
          this.$http.get('/workplace/GetToolUseTime', {
          params:{
                    tag:this.ModelsaleSearch.dateType,
                    start_date:this.formatDate(this.ModelsaleSearch.datetime[0]),
                    end_date:this.formatDate(this.ModelsaleSearch.datetime[1])
          }
            }).then(res =>{
          if(res.data.code === 0) {
            if(res.data.data === null)
            {
              this.GetToolTimeIsLoading = true;
            }
            this.GetToolTimeIsLoading = false;
            const getdata = {
              value1 : res.data.data.GetUseToolTimeDebugQuantity,
              value2 : res.data.data.GetUseToolTimeTestQuantity
            }
            this.GetToolTime.push(getdata)
            // console.log(this.GetToolTime)
          }
        }).catch(e => {
            this.$message.error(e.message);
        });
      }
      else {
        this.$http.get('/workplace/GetToolUseTime', {
          params:{
                    tag:this.ModelsaleSearch.dateType,
          }
            }).then(res =>{
          if(res.data.code === 0) {
            if(res.data.data === null)
            {
              this.GetToolTimeIsLoading = true;
            }
            this.GetToolTimeIsLoading = false;
            const getdata = {
              value1 : res.data.data.GetUseToolTimeDebugQuantity,
              value2 : res.data.data.GetUseToolTimeTestQuantity
            }
            this.GetToolTime.push(getdata)
            // console.log(this.GetToolTime)
          }
        }).catch(e => {
            this.$message.error(e.message);
        });
      }
    },

    /* 模块表头tab选择改变事件 */
    onModelsSaleTypeChange() {
      // this.getAllUseToolTime();
      this.getAllModelsData();
      this.getToolUseTime();
    },
    /* 成品表头tab选择改变事件 */
    onFinishedSaleTypeChange() {
      this.getAllFinishedData();
    },
  },
}
</script>

<style scoped>
/* 统计卡片 */
.analysis-chart-card-num {
  font-size: 60px;
}
.title-font-size{
  font-size: 60px;
  color: #1c6ca1;
}
.container{
  display: flex;
  justify-content: space-between;
}
.analysis-chart-card-content {
  height: 40px;
  box-sizing: border-box;
  margin-bottom: 12px;
}

.analysis-chart-card-text {
  padding-top: 12px;
}

/* 销售额、访问量工具栏 */
.demo-monitor-tool {
  padding: 0 30px;
}

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

/* 小标题 */
.demo-monitor-title {
  padding: 0 20px;
  margin: 20px 0 10px 0;
}

/* 排名item */
.demo-monitor-rank-item {
  padding: 0 20px;
  line-height: 20px;
  margin-top: 18px;
}

.container{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.char-container{
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-dropdown {
  vertical-align: top;
}
.el-dropdown + .el-dropdown {
  margin-left: 15px;
}

</style>
