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
                      v-model="makeUpModel"
                      type="month"
                      placeholder="选择月份"
                      @change="getRepairDatas1">
                      </el-date-picker>
                  </div>
                  <div>
                  <ele-chart
                    ref="browserChart"
                    style="height: 280px;"
                    v-loading="makeUploading"
                    :option="makeUpChartOption"/>
                  </div>
                </el-card>

            </el-col>
            <el-col :lg="12" :md="16">
                <el-card>
                  <div class="card-header">
                    <div class="card-label">维修数量</div>
                      <div class="card-month"></div>
                      <el-date-picker
                      v-model="numberModel"
                      type="month"
                      placeholder="选择月"
                      @change="getRepairDatas2">
                      </el-date-picker>
                  </div>
                  <div>
                  <ele-chart
                    ref="browserChart"
                    v-loading="numloading"
                    style="height: 280px;"
                    :option="numberChartOption"/>
                  </div>
                </el-card>
            </el-col>
        </el-row>
    <!-- 最近1小时访问情况 -->
      <div>
        <el-row :gutter="15">
        <el-col :lg="12" :md="16">
            <el-card >
            <div class="card-header">
              <div class="card-label">维修原因</div>
            </div>
            <div>
              <ele-word-cloud
              ref="hotSearchChart"
              v-loading="reasonloading"
              :data="getResultData"
              style="height: 303px;"/>
            </div>
          </el-card>
        </el-col>
        <el-col :lg="12" :md="16">
          <el-card class="custom-card" :flex="true">
            <div class="card-header">
              <div class="card-label">维修原因排名</div>
            </div>
            <div
              v-for="(item, index) in getResultData"
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
      // 加载状态
      makeUploading: true,
      numloading:true,
      reasonloading:true,

      //维修数据
      getRepairData1:[],
      getRepairData2:[],
      //原因数据
      getResultData:[],
      getResultData1:[],

      //选择月的模型
      makeUpModel:null,
      numberModel:null,

      startDate:null,
      endDate:null,
    };
  },
  computed: {
    //维修数量占比饼图
    makeUpChartOption(){
      return {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: this.getRepairData1.map(d => d.name),
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
            data: this.getRepairData1
          }
        ]
      };
    },
    //维修数量饼图
    numberChartOption(){
      return {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: this.getRepairData2.map(d => d.name),
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
            data: this.getRepairData2
          }
        ]
      };
    },
  },
  mounted() {
    this.getRepairDatas1();
    this.getRepairDatas2();
    this.getResultDatas();
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
    //获取维修数据
    getRepairDatas1(){
      if(this.makeUpModel === null)
      {
        const now = new Date();
        const year = now.getFullYear();
        this.startDate = this.formatDate(new Date(year, 0, 1));
        this.endDate = this.formatDate(new Date(year, 11, 31));
      }
      else {
        this.startDate = this.formatDate(new Date(this.makeUpModel));
        this.endDate = this.formatDate(new Date(this.makeUpModel));
        this.endDate.setMonth(this.endDate.getMonth()+1)
      }
      this.$http.get('/analysis/RepairData', {
        params:{
                  startTime:this.startDate,
                  endTime:this.endDate
        }
        }).then(res =>{
      if(res.data.code === 0) {
        this.getRepairData1 = res.data.data;
        this.makeUploading = false;
      }
      }).catch(e => {
          this.makeUploading = true;
          this.$message.error(e.message);
      });
    },
    getRepairDatas2(){
      if(this.numberModel === null)
      {
        const now = new Date();
        const year = now.getFullYear();
        this.startDate = this.formatDate(new Date(year, 0, 1));
        this.endDate = this.formatDate(new Date(year, 11, 31));
      }
      else {
        this.startDate = this.formatDate(new Date(this.numberModel));
        this.endDate = this.formatDate(new Date(this.numberModel));
        this.endDate.setMonth(this.endDate.getMonth()+1)
      }
      this.$http.get('/analysis/RepairData', {
        params:{
                  startTime:this.startDate,
                  endTime:this.endDate
        }
        }).then(res =>{
      if(res.data.code === 0) {
        this.getRepairData2 = res.data.data;
        this.numloading = false;
      }
      }).catch(e => {
          this.numloading = true;
          this.$message.error(e.message);
      });
    },
    //获取原因
    getResultDatas(){
      this.$http.get('/analysis/ResultData', ).then(res =>{
      if(res.data.code === 0) {
        this.reasonloading = false;
        // console.log(res.data.data)
        this.getResultData = res.data.data;
        this.getResultData = this.getResultData.sort((a,b)=>a.value-b.value).slice(0,8)
      }
      }).catch(e => {
          this.reasonloading = true;
          this.$message.error(e.message);
      });
    },
  },
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
.custom-card{
  width: 770px;
  height: 355px;
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
