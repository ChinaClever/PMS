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
              合格率
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
    name: 'InspectDashboard',
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
              name: '产品型号',
              type: 'category',
              data: this.saleroomData.map(d => d.item_number),
  
            }
          ],
          yAxis: [
            {
              type: 'value',
              min:0,
              max:100,
              interval:10,  //纵坐标刻度
            }
          ],
          series: [
            {
              name: '合格率',
              type: 'bar',
              data: this.saleroomData.map(d => d.target_actual_pass_rate),
              showBackground: true, //背景颜色
              barWidth:50,  //柱状图宽度
              backgroundStyle: {
                color:'rgba(180,180,180,0.2)'
              },
            }
          ]
        };
      },
    },
    data() {
      return {
        // 表格数据接口
        url: '/inspectreport/listOfTotal',
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
            prop: 'item_number',
            label: '产品型号',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'examine_amount_total_amount',
            label: '检验数量累计',
            // sortable: 'custom',
            showOverflowTooltip: true,
            align: 'center',
            minWidth: 150,
            resizable: false,
            // slot: 'status',
          },
          {
            prop: 'examine_bad_total_amount',
            label: '检验不良累计',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100
          },
          {
            prop: 'target_actual_pass_rate',
            label: '合格率',
            align: 'center',
            showOverflowTooltip: true,
            minWidth: 100,
            formatter: (row, column, cellValue) => {
            return cellValue + '%';
          }
          },
        ],
        saleroomData: [],
        // 表格搜索条件
        where: {},
        selectedOption: 'week',
      };
    },
    created() {
        this.calculateTimeRange();
        this.loading = true;
        this.$http.get('/inspectreport/listOfTotal').then((res) => {
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
        console.log(this.saleroomData)
        this.saleroomData = [
             {month: this.saleroomData.map(d => d.item_number), value: this.saleroomData.map(d => d.num)},
           ];
        console.log(this.saleroomData)
      },
      reload() {
        if(this.where.customStartTime && this.where.customEndTime){
            this.where.startTime = this.where.customStartTime;
            this.where.endTime = this.where.customEndTime;
            this.where.customStartTime = null;
            this.where.customEndTime = null;
        }
        this.$refs.table.reload({page: 1, where: this.where});
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
        if (this.selectedOption === 'week') {
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
  }
  
  </style>
  