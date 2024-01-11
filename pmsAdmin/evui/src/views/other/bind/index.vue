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
                  placeholder="成品型号"/>
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
          height="calc(100vh - 315px)">
          <!-- 模块列 -->
        <template slot="module" slot-scope="{row}">
          <el-popover
            placement="bottom"
            width="500"
            trigger="click">
            <el-table 
              :data="row.module" 
              stripe
              :max-height="300">
              <el-table-column width="170" property="key" label="模块序列号"></el-table-column>
            </el-table>
            <el-button slot="reference">查看详情</el-button>
          </el-popover>
        </template>

          <!-- 表头工具栏 -->
          <template slot="toolbar">
            <el-button
              size="small"
              type="primary"
              icon="el-icon-plus"
              class="ele-btn-icon"
              @click="openEdit(null)"
              v-if="permission.includes('sys:bind:add')">添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:bind:dall')">删除
            </el-button>
            <pre>                    </pre>

          </template>
          <!-- 操作列 -->
          <template slot="action" slot-scope="{row}">
            <el-link
              type="primary"
              :underline="false"
              icon="el-icon-edit"
              @click="openEdit(row)"
              v-if="permission.includes('sys:bind:update')">修改
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
                v-if="permission.includes('sys:bind:delete')">删除
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
    <bind-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import BindEdit from './bind-edit';

  export default {
    name: 'bind',
    components: {BindEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格搜索条件
        where: {},
        // 表格数据接口
        url: '/bind/list',
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
            prop: 'key',
            label: '成品序列号',
            showOverflowTooltip: true,
            minWidth: 150,
            align: 'center',
          },
          {
            prop: 'module',
            label: '模块',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
            slot: 'module'
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
        pageVis: true,
      };
    },
    methods: {
      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
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
          this.$http.get('/bind/detail/' + row.id).then((res) => {
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
        this.$http.delete('/bind/delete/' + row.id).then(res => {
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
          this.$http.delete('/bind/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
  
  