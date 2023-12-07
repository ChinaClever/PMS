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
          <el-col :span="6">
            <el-select v-model="selectedOption" placeholder="请选择时间范围" @change="calculateTimeRange">
                <el-option label="一天" value="day"></el-option>
                <el-option label="一周" value="week"></el-option>
                <el-option label="一个月" value="month"></el-option>
                <el-option label="一年" value="year"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-date-picker 
                ref="startDatePicker"
                v-model="where.customStartTime" 
                type="datetime"
                value-format="yyyy-MM-dd HH:mm:ss"
                placeholder="开始时间" 
                @change="changeCustomTime">
            </el-date-picker>
          </el-col>
          <el-col :span="6">
            <el-date-picker 
                ref="endDatePicker"
                v-model="where.customEndTime"
                type="datetime"
                value-format="yyyy-MM-dd HH:mm:ss"
                placeholder="结束时间" 
                @change="changeCustomTime">
            </el-date-picker>
          </el-col>
          <el-col :lg="6" :md="12">
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
          
          height="calc(100vh - 415px)">
        </ele-pro-table>
      </el-card>
  
      <el-card shadow="never" body-style="padding: 0;">
      <el-row>
          <el-col :lg="28" :md="26">
            <div class="demo-monitor-title">
              维修报告
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
  
  
  export default {
    name: 'RepairDashboard',
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
              name: '产品名称',
              type: 'category',
              data: this.saleroomData.map(d => d.name),
            }
          ],

          yAxis:[
           {
              type: 'value',
              min:0,
              max:10,
              interval:2,  //纵坐标刻度
            },

          ],
          color:[
            this.saleroomData.map(d => d.color)
          ],
          series:[
            {
              name: '不良数量总和',
              type: 'bar',
              data: this.saleroomData.map(d => d.bad_total),
              showBackground: true,
              barWidth: 50,
              backgroundStyle: {
                color: 'rgba(180, 180, 180, 0.2)'
              },
              barGap: '-100%', // 负值使柱子重叠
              z: -1 ,// 调整柱状图层级，使其在底层
              itemStyle:{
                color: function(params) {
                  return 'orange';
                }
              }
            },
            {
              name: '维修数量总和',
              type: 'bar',
              data: this.saleroomData.map(d => d.repair_total),  
              showBackground: true,
              barWidth: 50,
              backgroundStyle: {
                color: 'rgba(180, 180, 180, 0.2)'
              },
              itemStyle:{
                color: function(params) {
                  return 'blue';
                }
              }
            }
          ]
        };
      },
    },
    data() {
      return {
        // 表格数据接口
        url: '/repairreport/listOfTotal',
        // 表格列配置
        columns: [
          {
            prop: 'id',
            label: 'ID',
            width: 60,
            align: 'center',
            showOverflowTooltip: true,
            fixed: "left"
          },
          {
            prop: 'name',
            label: '产品名称',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'bad_number',
            label: '不良数量',
            // sortable: 'custom',
            showOverflowTooltip: true,
            align: 'center',
            minWidth: 150,
            resizable: false,
            // slot: 'status',
          },
          {
            prop: 'bad_phenomenon',
            label: '不良现象',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100
          },
          {
            prop: 'analysis',
            label: '原因分析',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100,
          },
          {
            prop: 'rate',
            label: '进度',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100,
          },
        ],
        saleroomData: [],
        // 表格搜索条件
        where: {},
        selectedOption: 'day',
      };
    },
    created() {
        this.calculateTimeRange();
        this.loading = true;
        const condition = {
          startTime: this.where.startTime,
          endTime: this.where.endTime,

        };
        this.$http.get('/repairreport/listOf',{params: condition}).then((res) => {
        //this.$http.get('/repairreport/listOf').then((res) => {
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
      // getSaleroomData(){
      //   this.saleroomData = [
      //       {month: 'IP', value: 81},
      //       {month: 'BM', value: 54},
      //       {month: 'SI', value: 91},
      //       {month: 'MPDU-Pro', value: 78},
      //
      //     ];
      // },
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
        if(this.where.customStartTime && this.where.customEndTime){
            this.where.startTime = this.where.customStartTime;
            this.where.endTime = this.where.customEndTime;
            this.where.customStartTime = null;
            this.where.customEndTime = null;
        }
        this.$refs.table.reload({page: 1, where: this.where});
        const condition = {
          startTime: this.where.startTime,
          endTime: this.where.endTime,

        };
        this.$http.get('/repairreport/listOf',{params:condition}).then((res) => {
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
        this.where = {};
      },
      changeCustomTime(){
        this.where.startTime = null;
        this.where.endTime = null;
        this.selectedOption = '';
      },
      reset() {
        this.where = {};
        this.selectedOption = '';
        this.reload();
      },
      calculateTimeRange() {
        const now = new Date();
        let startDate, endDate;
        if (this.selectedOption === 'day') {
            startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(),0,0,0);
            endDate = now;
        } else if (this.selectedOption === 'week') {
            startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 6, 0, 0, 0);
            endDate = now;
        } else if (this.selectedOption === 'month') {
            startDate = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate(), 0, 0, 0);
            endDate = now;
        } else if (this.selectedOption === 'year') {
            startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate(), 0, 0, 0);
            endDate = now;
        }
        this.where = {};
        this.where.startTime = this.formatDate(startDate);
        this.where.endTime = this.formatDate(endDate);
      },
      formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
       }
  
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
    padding: 0 20px;
    margin: 15px 0 5px 0;
    display: flex;
    justify-content: center; /* 水平居中对齐 */
    align-items: center; /* 垂直居中对齐 */
  }
  
  </style>