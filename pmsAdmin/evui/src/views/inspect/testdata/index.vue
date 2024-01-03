<template>
    <div class="ele-body" >
      <el-card shadow="never">
        <!-- 搜索表单 -->
        <el-form
          :model="where"
          label-width="77px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="15">
            <el-col :lg="6" :md="12">
              <el-form-item label="查询:">
                <el-input
                  clearable
                  v-model="where.keyword"
                  @clear="handleClear"
                  placeholder="软件类型、产品类型或结果"/>
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
          :needPage="pageVis"
          ref="table"
          :where="where"
          :datasource="url"
          :columns="columns"
          :selection.sync="selection"
          :row-class-name="tableRowClassName"
          height="calc(100vh - 315px)">
          <!-- 测试步骤列 -->
        <template slot="testStep" slot-scope="{row}">
          <el-popover
            placement="bottom"
            width="500"
            trigger="click">
            <el-table 
              :data="row.testStep" 
              stripe
              :max-height="300">
              <el-table-column width="80" property="no" label="序号"></el-table-column>
              <el-table-column width="340" property="name" label="名称"></el-table-column>
              <el-table-column width="80" property="result" label="结果">
                 <template slot-scope="scope">
                  <el-tag v-if="scope.row.result === 1" type="success" size="small">通过</el-tag>
                  <el-tag v-if="scope.row.result === 0" type="danger" size="small">失败</el-tag>
                </template>
              </el-table-column>
            </el-table>
            <el-button slot="reference">查看详情</el-button>
          </el-popover>
        </template>
          <!-- 结果列 -->
        <template slot="result" slot-scope="{row}">
          <el-tag v-if="row.result === 1" type="success" size="small">通过</el-tag>
          <el-tag v-if="row.result === 0" type="danger" size="small">失败</el-tag>
        </template>
          <!-- 表头工具栏 -->
          <template slot="toolbar">
            <el-button
              size="small"
              type="primary"
              icon="el-icon-plus"
              class="ele-btn-icon"
              @click="openEdit(null)"
              v-if="permission.includes('sys:testdata:add')">添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:testdata:dall')">删除
            </el-button>
            <pre>                    </pre>
            <el-switch
              v-model="realTime"
              active-text="实时模式"
              inactive-text="正常模式">
            </el-switch>
          </template>
          <!-- 操作列 -->
          <template slot="action" slot-scope="{row}">
            <el-link
              type="primary"
              :underline="false"
              icon="el-icon-edit"
              @click="openEdit(row)"
              v-if="permission.includes('sys:testdata:update')">修改
            </el-link>
            <el-popconfirm
              class="ele-action"
              title="确定要删除此数据吗？"
              @confirm="remove(row)">
              <el-link
                type="danger"
                slot="reference"
                :underline="false"
                icon="el-icon-delete"
                v-if="permission.includes('sys:testdata:delete')">删除
              </el-link>
            </el-popconfirm>
          </template>
          <!-- 状态列 -->
          <template slot="status" slot-scope="{row}">
            <el-switch
              v-model="row.status"
              @change="editStatus(row)"
              :active-value="1"
              :inactive-value="2"/>
          </template>
        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
    <test-data-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import TestDataEdit from './testdata-edit';

  export default {
    name: 'testdata',
    components: {TestDataEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格搜索条件
        where: {},
        // 表格数据接口
        url: '/testdata/list',
        // 表格列配置
        columns: [
          {
            columnKey: 'selection',
            type: 'selection',
            width: 45,
            align: 'center',
            fixed: "left"
          },
          {
            prop: 'softwareType',
            label: '软件类型',
            showOverflowTooltip: true,
            minWidth: 150,
            align: 'center',
          },
          {
            prop: 'productType',
            label: '产品类型',
            showOverflowTooltip: true,
            minWidth: 350,
            align: 'center',
          },
          {
            prop: 'productSN',
            label: '产品SN',
            showOverflowTooltip: true,
            minWidth: 250,
            align: 'center',
          },
          {
            prop: 'macAddress',
            label: 'mac地址',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'testStep',
            label: '测试步骤',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
            slot: 'testStep'
          },
          {
            prop: 'result',
            label: '结果',
            slot: 'result',
            showOverflowTooltip: true,
            minWidth: 80,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'softwareVersion',
            label: '软件版本',
            width: 80,
            align: 'center',
            showOverflowTooltip: true,
          },
          {
            prop: 'work_order',
            label: '单号',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',         
          },
          {
            prop: 'companyName',
            label: '公司名称',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center', 
          },
          {
            prop: 'protocolVersion',
            label: '协议名称',
            showOverflowTooltip: true,
            minWidth: 80,
            align: 'center',
          },
          {
            prop: 'testStartTime',
            label: '测试开始时间',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'testEndTime',
            label: '测试结束时间',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'testTime',
            label: '测试时间',
            showOverflowTooltip: true,
            minWidth: 80,
            align: 'center',
          },
          {
            columnKey: 'action',
            label: '操作',
            width: 150,
            align: 'center',
            resizable: false,
            slot: 'action',
            fixed: "right"
          }
        ],
        // 表格选中数据
        selection: [],
        // 当前编辑数据
        current: null,
        // 是否显示编辑弹窗
        showEdit: false,
        // 是否显示导入弹窗
        showImport: false,
        // 是否是实时模式
        realTime : false,
        pageVis: true,
        // 实时模式显示几条
        realTimeCount:10,
      };
    },
    watch : {
      // eslint-disable-next-line
      realTime(newValue, oldValue){
        if(newValue){
          this.$refs.table.reload({page: 1, limit:this.realTimeCount ,where: this.where});
          this.startTimer();
          this.pageVis = false;
        } else {
          this.stopTimer();
          this.pageVis = true;
          this.reload();
        }
      }
    },
    created() {
      // 监听 store 的属性变化
      this.$store.watch(
        () => this.$store.state.routerchange.isLeaveTestdata, // 要监听的 store 属性的 getter 函数
        // eslint-disable-next-line
        (newValue, oldValue) => {
          // 当属性发生变化时触发的回调函数
          // newValue 为新值，oldValue 为旧值
          // 在这里可以执行你想要的逻辑
          if (newValue) {
            this.realTime = false;
          }
        }
      );
    },
    beforeDestroy(){
      this.stopTimer();
    },
    methods: {
      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
      },
      startTimer() {
        // 每隔60秒刷新数据
        this.timer = setInterval(() => {
          const elements = document.querySelectorAll('tr.animation');
          // eslint-disable-next-line
          const element = elements[0];
          //现在最新一条数据的id this.$refs.table.data[0].id
          this.$http.get('/testdata/newest?id=' + this.$refs.table.data[0].id).then((res) => {
            if(res.data.data.length > 0){
              res.data.data = res.data.data.slice(-3).reverse();
              res.data.data.forEach((arr,index) => {
                // eslint-disable-next-line
                setTimeout((arr,index) => {
                  if(this.realTime){
                    if(this.$refs.table.data.length >= this.realTimeCount){
                      this.$refs.table.data.pop();
                    }
                    this.$refs.table.data.unshift(arr);
                    element.classList.remove('animation');
                    void element.offsetWidth;
                    element.classList.add("animation");
                  }
                }, 1000 * index,arr,index);
              })
            }
          }).catch((e) => {
            this.loading = false;
            this.$message.error(e.message);
          });
        }, 5000);
      },
      stopTimer() {
        // 停止定时器
        clearInterval(this.timer);
      },
      /* 重置搜索 */
      reset() {
        this.where = {};
        this.reload();
      },
      /* 显示编辑 */
      openEdit(row) {
        if (!row) {
          // 添加
          this.current = null;
          this.showEdit = true;
        } else {
          // 编辑
          this.loading = true;
          this.$http.get('/testdata/detail/' + row.id).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.current = Object.assign({}, res.data.data);
              this.showEdit = true;
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch((e) => {
            this.loading = false;
            this.$message.error(e.message);
          });
        }
      },
      /* 删除 */
      remove(row) {
        const loading = this.$loading({lock: true});
        this.$http.delete('/testdata/delete/' + row.id).then(res => {
          loading.close();
          if (res.data.code === 0) {
            this.$message.success(res.data.msg);
            this.reload();
          } else {
            this.$message.error(res.data.msg);
          }
        }).catch(e => {
          loading.close();
          this.$message.error(e.message);
        });
      },
      /* 批量删除 */
      removeBatch() {
        if (!this.selection.length) {
          this.$message.error('请至少选择一条数据');
          return;
        }
        this.$confirm('确定要删除选中的数据吗?', '提示', {
          type: 'warning'
        }).then(() => {
          const loading = this.$loading({lock: true});
          this.$http.delete('/testdata/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
            loading.close();
            if (res.data.code === 0) {
              this.$message.success(res.data.msg);
              this.reload();
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch(e => {
            loading.close();
            this.$message.error(e.message);
          });
        }).catch(() => {
        });
      },
      // eslint-disable-next-line
      tableRowClassName({row, rowIndex}) {
        // if(rowIndex === 0){
          return 'animation';
        // }
      },
      handleClear(){
        this.reload();
      },
    }
  }
  </script>
  
  <style>
.animation{
  opacity: 0;
  animation: slide-in-left-animation 300ms 0ms forwards ease-out;
}
@keyframes slide-in-left-animation {
  0% {
    opacity: 0;
    transform: translateX(-100%);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}
  </style>
  
  