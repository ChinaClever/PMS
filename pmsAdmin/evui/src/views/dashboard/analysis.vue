<template>
  <div class="ele-body ele-body-card">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="15">
      <el-col :lg="6" :md="12">
        <el-card class="analysis-chart-card" shadow="never">
          <div slot="header" class="ele-cell">
            <div class="ele-cell-content">生产总数量</div>
            <el-tag size="mini">年</el-tag>
          </div>
          <div class="analysis-chart-card-num">98724,254</div>
          <div class="analysis-chart-card-content" style="padding-top: 18px;">
            <span class="ele-action">
              <span>周同比12%</span>
              <i class="el-icon-caret-top ele-text-danger"></i>
            </span>
            <span class="ele-action">
              <span>日同比11%</span>
              <i class="el-icon-caret-bottom ele-text-success"></i>
            </span>
          </div>
          <el-divider/>
          <div class="analysis-chart-card-text">本日生产数量 86,585</div>
        </el-card>
      </el-col>
      <el-col :lg="6" :md="12">
        <el-card class="analysis-chart-card" shadow="never">
          <div slot="header" class="ele-cell">
            <div class="ele-cell-content">生产总效率</div>
            <el-tag size="mini">年</el-tag>
          </div>
          <div class="analysis-chart-card-num">98%</div>
          <div class="analysis-chart-card-content">
            <ele-chart
              ref="visitChart"
              style="height: 40px;"
              :option="visitChartOption"/>
          </div>
          <el-divider/>
          <div class="analysis-chart-card-text">
            <span class="ele-action">
              <span>周同比45%</span>
              <i class="el-icon-caret-top ele-text-danger"/>
            </span>
            <span class="ele-action">
              <span>日同比57%</span>
              <i class="el-icon-caret-bottom ele-text-success"/>
            </span>
          </div>
        </el-card>
      </el-col>
      <el-col :lg="6" :md="12">
        <el-card class="analysis-chart-card" shadow="never">
          <div slot="header" class="ele-cell">
            <div class="ele-cell-content">总合格率</div>
            <el-tag size="mini">年</el-tag>
          </div>
          <div class="analysis-chart-card-num">99%</div>
          <div class="analysis-chart-card-content">
            <ele-chart
              ref="AllProcedureNumChart"
              style="height: 40px;"
              :option="AllProcedureNumChartOption"/>
          </div>
          <el-divider/>
          <div class="analysis-chart-card-text">
            <span class="ele-action">
              <span>周同比45%</span>
              <i class="el-icon-caret-top ele-text-danger"/>
            </span>
            <span class="ele-action">
              <span>日同比57%</span>
              <i class="el-icon-caret-bottom ele-text-success"/>
            </span>
          </div>
        </el-card>
      </el-col>
      <el-col :lg="6" :md="12">
        <el-card class="analysis-chart-card" shadow="never">
          <div slot="header" class="ele-cell">
            <div class="ele-cell-content">开机率</div>
          </div>
          <div class="analysis-chart-card-num">97%</div>
          <div class="analysis-chart-card-content" style="padding-top: 25px;">
            <el-progress
              :percentage="97"
              :show-text="false"
              :stroke-width="10"
              color="#13c2c2"/>
          </div>
          <el-divider/>
          <div class="analysis-chart-card-text">
            <span class="ele-action">
              <span>周同比45%</span>
              <i class="el-icon-caret-top ele-text-danger"/>
            </span>
            <span class="ele-action">
              <span>日同比57%</span>
              <i class="el-icon-caret-bottom ele-text-success"/>
            </span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- 销售额、访问量 -->
    <el-card shadow="never" body-style="padding: 0;">
      <div class="ele-cell demo-monitor-tool">
        <div class="ele-cell-content">
          <el-tabs
            v-model="saleSearch.type"
            class="demo-monitor-tabs"
            @tab-click="onSaleTypeChange">
            <el-tab-pane label="生产数量" name="procedureNumber"/>
            <el-tab-pane label="效率" name="efficiency"/>
            <el-tab-pane label="合格率" name="pass"/>
          </el-tabs>
        </div>
        <div class="ele-inline-block ele-text-right">
          <el-radio-group v-model="saleSearch.dateType" size="small">
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
          <!--本年的数据-->
          <div v-if="saleSearch.type === 'procedureNumber' && saleSearch.dateType === 'year'">
               <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="yearPNsaleChartOption" />
          </div>
          <div v-else-if="saleSearch.type === 'efficiency' && saleSearch.dateType === 'year'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="yearEFsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'pass' && saleSearch.dateType === 'year'">
              <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="yearPSsaleChartOption"/>
          </div>

          <!--本月的数据-->
          <div v-if="saleSearch.type === 'procedureNumber' && saleSearch.dateType === 'month'">
              <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="monthPNsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'efficiency' && saleSearch.dateType === 'month' ">
               <ele-chart
                ref="saleChart"
                style="height: 285px;"
                :option="monthEFsaleChartOption"/>
          </div>

          <div v-else-if="saleSearch.type === 'pass' && saleSearch.dateType === 'month'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="monthPSsaleChartOption"/>
          </div>

          <!--本周的数据-->
          <div v-if="saleSearch.type === 'procedureNumber' &&saleSearch.dateType === 'week' ">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="weekPNsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'efficiency' && saleSearch.dateType === 'week'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="weekEFsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'pass' && saleSearch.dateType === 'week'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="weekPSsaleChartOption"/>
          </div>

          <!--今日的数据-->
          <div v-if="saleSearch.type === 'procedureNumber' && saleSearch.dateType === 'today'">
            <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="dayPNsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'efficiency' && saleSearch.dateType === 'today'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="dayEFsaleChartOption"/>
          </div>
          <div v-else-if="saleSearch.type === 'pass' && saleSearch.dateType === 'today'">
              <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="dayPSsaleChartOption"/>
          </div>

<!--          时间选择显示柱状图-->
          <div v-if="saleSearch.datetime && saleSearch.type === 'procedureNumber'">
            <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="chooseTimeShow" />
          </div>
          <div v-else-if="saleSearch.datetime && saleSearch.type === 'efficiency'">
            <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="chooseTimeShow" />
          </div>
          <div v-else-if="saleSearch.datetime && saleSearch.type === 'pass'">
            <ele-chart
              ref="saleChart"
              style="height: 285px;"
              :option="chooseTimeShow" />
          </div>

        </el-col>
      </el-row>
    </el-card>
    <!-- 最近1小时访问情况 -->
    <el-row :gutter="30">
      <el-col :lg="36" :md="32">
        <el-card
          shadow="never"
          header="最近24小时生产情况"
          body-style="padding: 20px 10px 0 0;">
          <ele-chart
            ref="visitHourChart"
            style="height: 323px;"
            :option="visitHourChartOption"/>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import EleChart from 'ele-admin/packages/ele-chart';
// import EleWordCloud from 'ele-admin/packages/ele-word-cloud';

export default {
  name: 'DashboardAnalysis',
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

      //生产数量数据
      yearprocedureNumberData:[],
      monthprocedureNumberData:[],
      weekprocedureNumberData:[],
      dayprocedureNumberData:[],

      // 效率数据
      yearefficiencyData: [],
      monthefficiencyData: [],
      weekefficiencyData: [],
      dayefficiencyData: [],
      //通过率数据
      yearpassData:[],
      monthpassData:[],
      weekpassData:[],
      daypassData:[],

      // 最近1小时访问情况数据
      visitHourData: [],

      //开始到结束日期数据
      StartEndValueData:null,

    };
  },
  computed: {
    // 生产总效率折线图配置
    visitChartOption() {
      return {
        color: '#975fe5',
        tooltip: {
          trigger: 'axis',
          formatter: '<i class="ele-chart-dot" style="background: #975fe5;"></i>{b0}: {c0}'
        },
        grid: {
          top: 10,
          bottom: 0,
          left: 0,
          right: 0
        },
        xAxis: [
          {
            show: false,
            type: 'category',
            boundaryGap: false,
            data: this.yearefficiencyData.map(d => d.month)
          }
        ],
        yAxis: [
          {
            show: false,
            type: 'value',
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.yearefficiencyData.map(d => d.value)
          }
        ]
      };
    },
    // 总合格率柱状图配置
    AllProcedureNumChartOption() {
      return {
        tooltip: {
          trigger: 'axis',
          formatter: '<i class="ele-chart-dot" style="background: #3aa1ff;"></i>{b0}: {c0}'
        },
        grid: {
          top: 10,
          bottom: 0,
          left: 0,
          right: 0
        },
        xAxis: [
          {
            show: false,
            type: 'category',
            data: this.yearpassData.map(d => d.month)
          }
        ],
        yAxis: [
          {
            show: false,
            type: 'value',
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            type: 'bar',
            data: this.yearpassData.map(d => d.value)
          }
        ]
      }
    },

    //选择时间显示柱状图（）
    chooseTimeShow(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.startandendprocedureData.map(d => d.day)
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
                  data: this.startandendprocedureData.map(d => d.value)
                }
              ]
            };
    },
    //生产数量柱状图（年）
    yearPNsaleChartOption(){
      return {
            tooltip: {
              trigger: 'axis'
            },
            xAxis: [
              {
                type: 'category',
                data: this.yearprocedureNumberData.map(d => d.month)
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
                data: this.yearprocedureNumberData.map(d => d.value)
              }
            ]
          };
    },
    //生产数量柱状图（月）
    monthPNsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.monthprocedureNumberData.map(d => d.day)
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
                  data: this.monthprocedureNumberData.map(d => d.value)
                }
              ]
            };

    },
    //生产数量柱状图（周）
    weekPNsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.weekprocedureNumberData.map(d => d.day)
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
                  data: this.weekprocedureNumberData.map(d => d.value)
                }
              ]
            };

    },
    //生产数量柱状图（日）
    dayPNsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.dayprocedureNumberData.map(d => d.hour)
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
                  data: this.dayprocedureNumberData.map(d => d.value)
                }
              ]
            };

    },

    //生产效率(年)
    yearEFsaleChartOption(){
     return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.yearefficiencyData.map(d => d.month)
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
                  data: this.yearefficiencyData.map(d => d.value)
                }
              ]
            };
    },
    //生产效率（月）
    monthEFsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.monthefficiencyData.map(d => d.day)
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
                  data: this.monthefficiencyData.map(d => d.value)
                }
              ]
            };

    },
    //生产效率（周）
    weekEFsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.weekefficiencyData.map(d => d.day)
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
                  data: this.weekefficiencyData.map(d => d.value)
                }
              ]
            };

    },
    //生产效率（日）
    dayEFsaleChartOption(){
      return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.dayefficiencyData.map(d => d.hour)
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
                  data: this.dayefficiencyData.map(d => d.value)
                }
              ]
            };

    },

    //合格率(年)
    yearPSsaleChartOption(){
     return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.yearpassData.map(d => d.month)
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
                  data: this.yearpassData.map(d => d.value)
                }
              ]
            };
    },
    //合格率(月)
    monthPSsaleChartOption(){
     return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.monthpassData.map(d => d.month)
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
                  data: this.monthpassData.map(d => d.value)
                }
              ]
            };
    },
    //合格率(周)
    weekPSsaleChartOption(){
     return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.weekpassData.map(d => d.day)
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
                  data: this.weekpassData.map(d => d.value)
                }
              ]
            };
    },
    //合格率(天)
    dayPSsaleChartOption(){
     return {
              tooltip: {
                trigger: 'axis'
              },
              xAxis: [
                {
                  type: 'category',
                  data: this.daypassData.map(d => d.hour)
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
                  data: this.daypassData.map(d => d.value)
                }
              ]
            };
    },
    // 最近1小时访问情况折线图配置
    visitHourChartOption() {
      /*if (!this.visitHourData.length) {
        return {};
      }*/
      return {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['生产数量', '合格率'],
          right: 20
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: this.visitHourData.map(d => d.time)
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '生产数量',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.visitHourData.map(d => d.number)
          },
          {
            name: '合格率',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {
              opacity: 0.5
            },
            data: this.visitHourData.map(d => d.pass)
          }
        ]
      }
    },

  },
  mounted() {
    this.getVisitHourData();
    this.getProNumData();
    this.getPassData();
    this.getEfficiencyData();
    this.getStartEndData();
  },

  methods: {
    //转换为中文的时间
    convertoChineseDate(date)
    {
      return date.toLocaleString('zh-CN',{
        year:'numeric',
        month:'long',
        day:'numeric'
      });
    },
    // 生产数量获取数据
    getProNumData(){
      const currentDate = new Date();//当前日期
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth();
      const currentDay = currentDate.getDay();
      const totalDays = new Date(currentYear, currentMonth+1, 0).getDate();//获取当月总天数

      //清空之前的数据
      this.yearprocedureNumberData=[];
      for(let i =0; i<12; i++)
      {
          const getMonthData = {
            month:this.convertoChineseDate(new Date(currentYear, i)),
            value:Math.floor(Math.random() * 100)
          }
          this.yearprocedureNumberData.push(getMonthData)
        }

      this.monthprocedureNumberData=[];
      for(let i =1; i<=totalDays; i++){
        const getDayData = {
          day: this.convertoChineseDate(new Date(currentYear, currentMonth, i)),
          value: Math.floor(Math.random() * 100)
        };
      this.monthprocedureNumberData.push(getDayData)
      }

      this.weekprocedureNumberData=[];
      for(let i=1; i<=7; i++) {
        const dayOffset = i-currentDay;
        const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+dayOffset);
        const getWeekData = {
          day: this.convertoChineseDate(dayDate),
          value: Math.floor(Math.random() * 100)
        };
        this.weekprocedureNumberData.push(getWeekData)
      }

      this.dayprocedureNumberData=[];
      for(let i=8; i<21; i++) {
        const gethourData = {
          hour: i,
          value: Math.floor(Math.random() * 100)
        };
        this.dayprocedureNumberData.push(gethourData)
      }

    },
    // 生产效率获取数据
    getEfficiencyData(){
      const currentDate = new Date();//当前日期
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth();
      const currentDay = currentDate.getDay();
      const totalDays = new Date(currentYear, currentMonth+1, 0).getDate();//获取当月总天数
      this.yearefficiencyData=[];
      for(let i =0; i<12; i++)
      {
        const getMonthData = {
          month:this.convertoChineseDate(new Date(currentYear, i)),
          value:Math.floor(Math.random() * 100)
        }
        this.yearefficiencyData.push(getMonthData)
      }

      this.monthefficiencyData=[];
      for(let i =1; i<=totalDays; i++){
        const getDayData = {
          day: this.convertoChineseDate(new Date(currentYear, currentMonth, i)),
          value: Math.floor(Math.random() * 100)
        };
      this.monthefficiencyData.push(getDayData)
      }

      this.weekefficiencyData=[];
      for(let i=1; i<=7; i++) {
        const dayOffset = i-currentDay;
        const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+dayOffset);
        const getWeekData = {
          day: this.convertoChineseDate(dayDate),
          value: Math.floor(Math.random() * 100)
        };
        this.weekefficiencyData.push(getWeekData)
      }

      this.dayefficiencyData=[];
      for(let i=8; i<21; i++) {
        const gethourData = {
          hour: i,
          value: Math.floor(Math.random() * 100)
        };
        this.dayefficiencyData.push(gethourData)
      }
    },
    //生产合格率获取数据
    getPassData(){
      const currentDate = new Date();//当前日期
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth();
      const currentDay = currentDate.getDay();
      const totalDays = new Date(currentYear, currentMonth+1, 0).getDate();//获取当月总天数

      this.yearpassData=[];
      for(let i =0; i<12; i++)
      {
        const getMonthData = {
          month:this.convertoChineseDate(new Date(currentYear, i)),
          value:Math.floor(Math.random() * 100)
        }
        this.yearpassData.push(getMonthData)
      }

      this.monthpassData=[];
      for(let i =1; i<= totalDays; i++){
        const getDayData = {
          month: this.convertoChineseDate(new Date(currentYear, currentMonth, i)),
          value: Math.floor(Math.random() * 100)
        };
      this.monthpassData.push(getDayData)
      }

      this.weekpassData=[];
      for(let i=1; i<=7; i++) {
        const dayOffset = i-currentDay;
        const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+dayOffset);
        const getWeekData = {
          day:this.convertoChineseDate(dayDate),
          value: Math.floor(Math.random() * 100)
        };
        this.weekpassData.push(getWeekData)
      }

      this.daypassData=[];
      for(let i=8; i<21; i++) {
        const gethourData = {
          hour: i,
          value: Math.floor(Math.random() * 100)
        };
        this.daypassData.push(gethourData)
      }

    },

    //选择时间获取到的数据
    getStartEndData(){
      if(this.saleSearch.datetime && this.saleSearch.datetime[0] && this.saleSearch.datetime[1]) {
        const startDate = this.saleSearch.datetime[0];
        const endDate = this.saleSearch.datetime[1];

        const startTimestamp = startDate.getTime();
        const endTimestamp = endDate.getTime();

        const days = Math.ceil((endTimestamp - startTimestamp) / (24 * 60 * 60 * 1000));
        this.startandendprocedureData = [];
        for (let i = 0; i <= days; i++) {
          const currentDate = new Date(startTimestamp + i * 24 * 60 * 60 * 1000);
          if(this.saleSearch.type === 'procedureNumber')
          {
            this.StartEndValueData = Math.floor(Math.random() * 100);
          }
          else if(this.saleSearch.type === 'efficiency')
          {
            this.StartEndValueData = Math.floor(Math.random() * 1000);
          }
          else
          {
            this.StartEndValueData = Math.floor(Math.random() * 10);
          }
          const getStartEnd = {
            day: this.convertoChineseDate(currentDate),
            value: this.StartEndValueData,//Math.floor(Math.random() * 100),
          }
          this.startandendprocedureData.push(getStartEnd)
        }
      }
      else {
        this.startandendprocedureData = [];
      }
    },

    /* 获取最近24小时访问情况数据 */
    getVisitHourData() {
      this.visitHourData = [
        {time: '8:00', number: 15, pass: 45},
        {time: '9:00', number: 39, pass: 169},
        {time: '10:00', number: 152, pass: 400},
        {time: '11:00', number: 94, pass: 285},
        {time: '12:00', number: 102, pass: 316},
        {time: '13:00', number: 86, pass: 148},
        {time: '14:00', number: 39, pass: 150},
        {time: '15:00', number: 38, pass: 234},
        {time: '16:00', number: 95, pass: 158},
        {time: '17:00', number: 30, pass: 100},
        {time: '18:00', number: 86, pass: 266}
      ];
    },

    /* 表头tab选择改变事件 */
    onSaleTypeChange() {
      this.getProNumData();
      this.getPassData();
      this.getEfficiencyData();
      this.getStartEndData();
    },
    //时间周期改变事件
    onChangeDate()
    {
      this.getStartEndData();
    }
  },
  activated() {
    ['visitChart', 'AllProcedureNumChart', 'saleChart', 'visitHourChart'].forEach((name) => {
      this.$refs[name].resize();
    });
  }
}
</script>

<style scoped>
/* 统计卡片 */
.analysis-chart-card-num {
  font-size: 30px;
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
