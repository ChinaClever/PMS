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
              <el-date-picker
                v-model="selectDateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="至"
                start-placeholder="订单日期开始日期"
                end-placeholder="订单日期结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect">
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
              name: '数量',
              type: 'value',
              data: this.saleroomData.map(d => d.bad_total),

              interval:10,  //纵坐标刻度
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
                color: function() {
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
                color: function() {
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
        pickerOptions: {
          shortcuts: [{
            text: '最近一天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 );
              picker.$emit('pick', [start, end]);
            }
          },
            {
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
              text: '最近一个月',
              onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                picker.$emit('pick', [start, end]);
              }
            }, {
              text: '最近三个月',
              onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                picker.$emit('pick', [start, end]);
              }
            },{
              text: '最近半年',
              onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 6);
                picker.$emit('pick', [start, end]);
              }
            }, {
              text: '最近一年',
              onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 12);
                picker.$emit('pick', [start, end]);
              }
            }
          ]
        },
        //时间筛选
        selectDateRange:'',
        saleroomData: [],
        // 表格搜索条件
        where: {},
      };
    },
    created() {

        this.loading = true;
        // const condition = {
        //   startTime: this.where.startTime,
        //   endTime: this.where.endTime,

        // };
        this.$http.get('/repairreport/listOf').then((res) => {

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

    methods: {
      //向后端传时间
      dateRangeHandleSelect(){
        this.where.startTime = this.selectDateRange[0]
        this.where.endTime = this.selectDateRange[1]
      },


      reload() {

        this.$refs.table.reload({page: 1, where: this.where});
        const condition = {
          startTime: this.where.startTime ,
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
      },

      reset() {
        this.where = {};

        this.reload();
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
  /* 小标题 */
  .demo-monitor-title {
    padding: 0 20px;
    margin: 15px 0 5px 0;
    display: flex;
    justify-content: center; /* 水平居中对齐 */
    align-items: center; /* 垂直居中对齐 */
  }
  
  </style>