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
              <el-tag size="mini">年</el-tag>
            </div>
            <div class="analysis-chart-card-num">{{ AllShipmentModelQuantity }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">模块生产效率</div>
              <el-tag size="mini">年</el-tag>
            </div>
            <div class="analysis-chart-card-num">{{ ModelTotalEfficiency }}%</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="6" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content ele-text-left">模块成品合格率</div>
              <div class="ele-cell-content ele-text-right">模块半成品合格率</div>
            </div>
            <div class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ ModelTotalAllPass }}%</div>
              <div class="analysis-chart-card-num ele-text-right">{{ ModelTotalHalfPass }}%</div>
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
            <div class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ AllUseToolTime }}</div>
              <div class="analysis-chart-card-num ele-text-right">H</div>
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
              @tab-click="onSaleTypeChange">
              <el-tab-pane label="模块生产数量&生产效率" name="procedureNumber"/>
              <el-tab-pane label="模块合格率" name="pass"/>
              <el-tab-pane label="工具使用时长" name="tool_time"/>
            </el-tabs>
          </div>
          <div class="ele-inline-block ele-text-right">
            <el-radio-group v-model="saleSearch.dateType" size="small" @change="onRadioChange">
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
              @change="onChangeDate"/>
          </div>
        </div>
        <el-divider/>
        <el-row>
          <el-col :lg="48" :md="58">
            <div v-if="saleSearch.type === 'procedureNumber'">
                 <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="AllModelsDataChartOption" />
            </div>
            <div v-else-if="saleSearch.type === 'pass'">
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="ModelPassChartOption"/>
            </div>
            <div v-else-if="saleSearch.type === 'tool_time'">
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="tooltimeChartOption"/>
            </div>


<!--  &lt;!&ndash;          时间选择显示柱状图&ndash;&gt;-->
<!--            <div v-if="saleSearch.datetime && saleSearch.type === 'procedureNumber'">-->
<!--              <ele-chart-->
<!--                ref="saleChart"-->
<!--                style="height: 285px;"-->
<!--                :option="chooseTimeShow" />-->
<!--            </div>-->

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
              <el-tag size="mini">年</el-tag>
            </div>
            <div class="analysis-chart-card-num">{{ AllShipmentFinishedQuantity }}</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="8" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content">成品生产效率</div>
              <el-tag size="mini">年</el-tag>
            </div>
            <div class="analysis-chart-card-num">{{ FinishedTotalEfficiency }}%</div>
            <el-divider/>
          </el-card>
        </el-col>
        <el-col :lg="8" :md="12">
          <el-card class="analysis-chart-card" shadow="never">
            <div slot="header" class="ele-cell">
              <div class="ele-cell-content ele-text-left">成品合格率</div>
              <div class="ele-cell-content ele-text-right">半成品合格率</div>
            </div>
            <div class="container">
              <div class="analysis-chart-card-num ele-text-left">{{ FinishedTotalAllPass }}%</div>
              <div class="analysis-chart-card-num ele-text-right">{{ FinishedTotalHalfPass }}%</div>
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
              @tab-click="onSaleTypeChange">
              <el-tab-pane label="成品生产数量&生产效率" name="procedureNumber"/>
<!--              <el-tab-pane label="成品生产效率" name="efficiency"/>-->
              <el-tab-pane label="成品合格率" name="pass"/>
            </el-tabs>
          </div>
          <div class="ele-inline-block ele-text-right">
            <el-radio-group v-model="saleSearch.dateType" size="small" @change="onRadioChange">
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
              @change="onChangeDate"/>
          </div>
        </div>
        <el-divider/>
        <el-row>
          <el-col :lg="48" :md="58">
            <div v-if="saleSearch.type === 'procedureNumber'">
                 <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="AllFinishedDataChartOption" />
            </div>
            <div v-else-if="saleSearch.type === 'pass'">
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="FinishedPassChartOption"/>
            </div>
            <div v-else-if="saleSearch.type === 'tool_time'">
                <ele-chart
                  ref="saleChart"
                  style="height: 285px;"
                  :option="tooltimeChartOption"/>
            </div>


<!--  &lt;!&ndash;          时间选择显示柱状图&ndash;&gt;-->
<!--            <div v-if="saleSearch.datetime && saleSearch.type === 'procedureNumber'">-->
<!--              <ele-chart-->
<!--                ref="saleChart"-->
<!--                style="height: 285px;"-->
<!--                :option="chooseTimeShow" />-->
<!--            </div>-->

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
      //开始和结束日期柱状图数据
      startandendprocedureData:[],

      //开始到结束日期数据
      StartEndValueData:[],

      //模块总生产数量
      AllShipmentModelQuantity:null ,
      //成品总生产数量
      AllShipmentFinishedQuantity:null,
      //模块的总生产效率
      ModelTotalEfficiency:null,
      //成品的总生产效率
      FinishedTotalEfficiency:null,

      //模块的成品合格率
      ModelTotalAllPass:null,
      //模块总半成品合格率
      ModelTotalHalfPass:null,
      //成品的成品合格率
      FinishedTotalAllPass:null,
      //成品总半成品合格率
      FinishedTotalHalfPass:null,

      //总的工具使用时长
      AllUseToolTime:null,

      //所有模块的生产数据
      AllModelsData:[],
      //所有成品的生产数据
      AllFinishedData:[],
      //获取工具的使用时长
      GetToolTime:[],
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
              }
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
    //工具使用时常柱状图   可能还需调整
    tooltimeChartOption(){
       return {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            type: 'category',
            data: this.GetToolTime.map(d => d.data)
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
            data: this.GetToolTime.map(d => d.value)
          }
        ]
      };
    },
    //选择时间显示柱状图（）
    chooseTimeShow(){
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
            data: this.StartEndValueData.map(d => d.product_name)
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
              formatter:this.StartEndValueData.map(d => d.total_quantity)
            }
          },
          {
            type: 'value',
            position:'left',
            axisLine:{
              show:true
            },
            axisLabel:{
              formatter:this.StartEndValueData.map(d => d.efficiency)
            }
          }
        ],
        series: [
          {
            name:'生产数量',
            type: 'bar',
            yAxisIndex:0,
            data: this.StartEndValueData.map(d => d.total_quantity)
          },
          {
            name:'生产效率 个/H',
            type: 'line',
            yAxisIndex:0,
            data: this.StartEndValueData.map(d => d.efficiency)
          }
        ]
      };
    },

  },
  mounted() {
    this.getStartEndData();
    this.getAllNumAndEff();
    this.getModelAndFinishedPass();
    this.getAllUseToolTime();
    this.getAllModelsData();
    this.getAllFinishedData();
    this.getToolUseTime();
  },
  methods: {
    //转换为中文的时间
    convertoChineseDate(date) {
      return date.toLocaleString('zh-CN',{
        year:'numeric',
        month:'long',
        day:'numeric'
      });
    },
      //转换时间成数据库内的格式
    formatDate(date) {
        return date.toLocaleString('zh-CN',{
          year:'numeric',
          month:'2-digit',
          day:'2-digit',
          hour12:false
      }).replace(/\//g, '-');
    },
    //获取生产总数和生产效率（模块和成品）
    getAllNumAndEff(){
      this.$http.get('/workplace/ShipmentAllQuantity').then(res =>{
        if(res.data.code === 0) {
          this.AllShipmentModelQuantity = res.data.AllShipmentModelQuantity;
          this.AllShipmentFinishedQuantity = res.data.AllShipmentFinishedQuantity;
          this.ModelTotalEfficiency = res.data.ModelTotalEfficiency;
          this.FinishedTotalEfficiency = res.data.FinishedTotalEfficiency;
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取模块和成品的合格率
    getModelAndFinishedPass() {
      this.$http.get('/workplace/AllPass').then(res =>{
        if(res.data.code === 0) {
          this.ModelTotalAllPass = res.data.ModelTotalAllPass;
          this.ModelTotalHalfPass = res.data.ModelTotalHalfPass;
          this.FinishedTotalAllPass = res.data.FinishedTotalAllPass;
          this.FinishedTotalHalfPass = res.data.FinishedTotalHalfPass;
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取工具使用的总时长
    getAllUseToolTime(){
      this.$http.get('/workplace/AllUseToolTime').then(res =>{
        if(res.data.code === 0) {
          this.AllUseToolTime = res.data.AllUseToolTime;
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取模块所有数据（生产数量，生产合格率，使用时长）
    getAllModelsData() {
      this.$http.get('/workplace/AllModelsData',{
        params:{
          tag:this.saleSearch.dateType,
          start_date:this.formatDate(this.saleSearch.datetime[0]),
          end_date:this.formatDate(this.saleSearch.datetime[1])
        }
      }).then(res =>{
        if(res.data.code === 0) {
          this.AllModelsData = res.data;
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取成品所有数据（生产数量，生产合格率）
    getAllFinishedData() {
      this.$http.get('/workplace/AllFinishedData',{
        params:{
          tag:this.saleSearch.dateType,
          start_date:this.formatDate(this.saleSearch.datetime[0]),
          end_date:this.formatDate(this.saleSearch.datetime[1])
        }
      }).then(res =>{
        if(res.data.code === 0) {
          this.AllFinishedData = res.data;
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },
    //获取工具的使用时间
    getToolUseTime(){
      const currentDate = new Date();//当前日期
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth();
      const currentDay = currentDate.getDay();
      const totalDays = new Date(currentYear, currentMonth+1, 0).getDate();//获取当月总天数

      this.$http.get('/workplace/GetToolUseTime',{
        params:{
          tag:this.saleSearch.dateType,
          start_date:this.formatDate(this.saleSearch.datetime[0]),
          end_date:this.formatDate(this.saleSearch.datetime[1])
        }
      }).then(res =>{
        if(res.data.code === 0) {
          this.GetToolTime=[];
          if(this.saleSearch.datetime[0] != null && this.saleSearch.datetime[1] != null)
          {
            //等待修改
            this.GetToolTime=[];
          }
          else if(this.saleSearch.dateType === 'year')
          {
            for(let i =0; i<12; i++)
            {
              const getMonthData = {
                data:this.convertoChineseDate(new Date(currentYear, i)),
                value:res.data.data
              }
              this.GetToolTime.push(getMonthData)
            }
          }
          else if(this.saleSearch.dateType === 'month')
          {
            for(let i =1; i<= totalDays; i++){
              const getDayData = {
                data: this.convertoChineseDate(new Date(currentYear, currentMonth, i)),
                value: res.data.data,
              };
            this.GetToolTime.push(getDayData)
            }
          }
          else if(this.saleSearch.dateType === 'week')
          {
            for(let i=1; i<=7; i++) {
              const dayOffset = i-currentDay;
              const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+dayOffset);
              const getWeekData = {
                data:this.convertoChineseDate(dayDate),
                value: res.data.data,
              };
              this.GetToolTime.push(getWeekData)
            }
          }
          else
          {
            for(let i=8; i<21; i++) {
              const gethoursData = {
                data: i,
                value: res.data.data,
              };
              this.GetToolTime.push(gethoursData)
            }
          }
        }
      }).catch(e => {
          this.$message.error(e.message);
      });
    },

    //选择时间获取到的数据
    getStartEndData(){
      if(this.saleSearch.datetime && this.saleSearch.datetime[0] && this.saleSearch.datetime[1]) {
        const startDate = this.formatDate(this.saleSearch.datetime[0]);
        const endDate = this.formatDate(this.saleSearch.datetime[1]);
        console.log('startDate'+startDate)
        console.log('endDate'+endDate)
        // const startTimestamp = startDate.getTime();
        // // const endTimestamp = endDate.getTime();
        // console.log('startTimestamp'+startTimestamp)
        // const days = Math.ceil((endTimestamp - startTimestamp) / (24 * 60 * 60 * 1000));
        this.$http.get('/procedure/getStartEndTime', {
              params:{
                  start_date : startDate,
                  end_date : endDate
              }
          }
        ).then(res => {
            if(res.data.code === 0)
            {
                console.log('获取数据成功')
                if(this.saleSearch.type === 'procedureNumber')
                {
                    this.StartEndValueData = res.data.data;
                    console.log(this.StartEndValueData);
                    console.log(this.StartEndValueData.length);
                }
            }
        }).catch(e => {
            console.log('获取数据失败');
            this.$message.error(e.message);
        });
        // this.startandendprocedureData = [];
        // console.log("进入循环1")
        // for (let i = 0; i <= this.StartEndValueData.length-1; i++) {
        //     console.log("进入循环")
        //   const data = this.StartEndValueData[i];
        //   console.log(data)
        //   // const currentDate = new Date(startDate + i * 24 * 60 * 60 * 1000);
        //   // if(this.saleSearch.type === 'procedureNumber')
        //   // {
        //   //   this.StartEndValueData = Math.floor(Math.random() * 100);
        //   // }
        //   // else if(this.saleSearch.type === 'efficiency')
        //   // {
        //   //   this.StartEndValueData = Math.floor(Math.random() * 1000);
        //   // }
        //   // else if(this.saleSearch.type === 'all_pass')
        //   // {
        //   //   this.StartEndValueData = Math.floor(Math.random() * 160);
        //   // }
        //   // else if(this.saleSearch.type === 'half_pass')
        //   // {
        //   //   this.StartEndValueData = Math.floor(Math.random() * 107);
        //   // }
        //   // else
        //   // {
        //   //   this.StartEndValueData = Math.floor(Math.random() * 130);
        //   // }
        //   const getStartEnd = {
        //     day: data.delivery_date,//this.convertoChineseDate(currentDate),
        //     value: data.quantity,//this.StartEndValueData,//Math.floor(Math.random() * 100),
        //   }
        //   this.startandendprocedureData.push(getStartEnd)
        // }
      }
      else {
        this.startandendprocedureData = [];
      }
    },

    /* 表头tab选择改变事件 */
    onSaleTypeChange() {
      this.getAllUseToolTime();
      this.getAllModelsData();
      this.getAllFinishedData();
      this.getToolUseTime();
    },
    //表头日期选择改变事件
    onRadioChange(){
      this.getAllUseToolTime();
      this.getAllModelsData();
      this.getAllFinishedData();
      this.getToolUseTime();
    },
    //时间周期改变事件
    onChangeDate()
    {
      this.getStartEndData();
    }
  },
  activated() {
    ['saleChart', 'visitHourChart'].forEach((name) => {
      this.$refs[name].resize();
    });
  }
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
.el-icon-arrow-down {
  font-size: 12px;
}

.label{
  margin-right: 400px;
}
.selector{
  margin-top: 10px;
  margin-left: 40px;
}
.left-side{
  flex-grow: 1;
  margin-right: 10px;
}
.right-side{
  flex-grow: 1;
  margin-left: 10px;
}
</style>
