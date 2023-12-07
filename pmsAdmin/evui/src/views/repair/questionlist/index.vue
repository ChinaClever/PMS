<template>
    <div class="ele-body">
      <el-card shadow="never">
        <!-- 意见反馈表单 -->
        <el-form
          :model="where"
          label-width="77px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="10">
            <el-col :span="5">
              <el-form-item label="产品名称:">
                <el-input
                  clearable
                  v-model="where.name"
                  placeholder="请输入产品名称"/>
              </el-form-item>
              <el-form-item label="工单号:">
                <el-input
                  clearable
                  v-model="where.work_order"
                  placeholder="请输入工单号"/>
              </el-form-item>
            </el-col>
            <el-col :span="6" >
            <el-form-item label="排序方式:">
            <el-select v-model="selectedOption" placeholder="请选择排序方式" @change="selectway">
                <el-option label="产品名称" value="name"></el-option>
                <el-option label="工单号" value="work_order"></el-option>
            </el-select>
            </el-form-item>
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
          :selection.sync="selection"
          height="calc(100vh - 315px)">

          <template slot="expand_1" slot-scope="{row}">
            <el-popover
              placement="top-start"
              title="不良现象"
              width="1000"
              trigger="click"
              :content=row.bad_phenomenon>
              <el-button slot="reference">{{ row.bad_phenomenon }}</el-button>
            </el-popover>
          </template>

        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
     
    </div>
  </template>

  <script>
  import { mapGetters } from "vuex";

  export default {
    name: 'repairreport',
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        current:'',
        // 表格数据接口
        url: '/repairreport/questionlist',
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
            prop: 'work_order',
            label: '工单号',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'name',
            label: '产品名称',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'bad_phenomenon',
            label: '不良现象',
            width: 300,
            align: 'center',
            slot: 'expand_1',
          },
          {
            prop: 'num',
            label: '出现次数',
            width: 300,
            align: 'center',
            showOverflowTooltip: true,
          },

        ],
        // 表格搜索条件
        where: {},
        // 表格选中数据
        selection: [],
        selectedOption: 'name',

      };
    },
    created() {
        this.selectway();
        this.loading = true;
        this.$http.get('/repairreport/questionlist').then((res) => {
        this.loading = false;
        }).catch((e) => {
        this.loading = false;
        this.$message.error(e.message);
        });
    },
    methods: {
      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
      },

      /* 重置搜索 */
      reset() {
        this.where = {};
        this.selectedOption = '';
        this.reload();
      },
      selectway() {
        this.where = {};
        if (this.selectedOption=="name"){
          this.where.name1 = this.selectedOption;
        }else if (this.selectedOption=="work_order"){
          this.where.work_order1 = this.selectedOption;
        }
      },


    }
  }
  </script>

  <style scoped>
  </style>
