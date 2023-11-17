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
          <el-col span="5">
            <el-form-item label="提交者:">
              <el-input
                clearable
                v-model="where.commit_user"
                placeholder="请输入提交者"/>
            </el-form-item>
          </el-col>
          <el-col span="6">
            <el-form-item label="状态:">
              <el-select
                clearable
                v-model="where.status"
                placeholder="请选择状态"
                class="ele-fluid">
                <el-option label="未查看" value="1"/>
                <el-option label="确认" value="2"/>
                <el-option label="完成" value="3"/>
                <el-option label="未通过" value="4"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col span="6">
            <el-form-item label="类型:">
              <el-select
                clearable
                v-model="where.type"
                placeholder="请选择类型"
                class="ele-fluid">
                <el-option label="问题" value="1"/>
                <el-option label="建议" value="2"/>
                <el-option label="新需求" value="3"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col span="7">
            <el-form-item label="优先级:">
              <el-input
                clearable
                v-model="where.priority"
                placeholder="请输入优先级(1-10)"/>
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
        <!-- 表头工具栏 -->
        <template slot="toolbar">
          <el-button
            size="small"
            type="primary"
            icon="el-icon-plus"
            class="ele-btn-icon"
            @click="openEdit(null)"
            v-if="permission.includes('sys:feedback:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:feedback:dall')">删除
          </el-button>
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:feedback:update')">修改
          </el-link>
          <el-popconfirm
            class="ele-action"
            title="确定要删除此通知吗？"
            @confirm="remove(row)">
            <el-link
              type="danger"
              slot="reference"
              :underline="false"
              icon="el-icon-delete"
              v-if="permission.includes('sys:feedback:delete')">删除
            </el-link>
          </el-popconfirm>
        </template>
        <template slot="type" slot-scope="{row}">
          <el-tag v-if="row.type === 1" size="small">问题</el-tag>
          <el-tag v-if="row.type === 2" size="small">建议</el-tag>
          <el-tag v-if="row.type === 3" size="small">新需求</el-tag>
        </template>
        <template slot="status" slot-scope="{row}">
          <el-tag v-if="row.status === 1" type="warning" size="small">未查看</el-tag>
          <el-tag v-if="row.status === 2" type="success" size="small">确认</el-tag>
          <el-tag v-if="row.status === 3" type="success" size="small">完成</el-tag>
          <el-tag v-if="row.status === 4" type="success" size="small">未通过</el-tag>
        </template>
        <template slot="expand_1" slot-scope="{row}">
          <el-popover
            placement="top-start"
            title="内容"
            width="1000"
            trigger="click"
            :content=row.content>
            <el-button slot="reference">{{ row.content }}</el-button>
          </el-popover>
        </template>
        <template slot="expand_2" slot-scope="{row}" v-if="row.feedback">
          <el-popover
            placement="top-start"
            title="反馈"
            width="1000"
            trigger="click"
            :content=row.feedback>
            <el-button slot="reference">{{ row.feedback }}</el-button>
          </el-popover>
        </template>
      </ele-pro-table>
    </el-card>
    <!-- 编辑弹窗 -->
    <suggestion-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import SuggestionEdit from './suggestion-edit';

export default {
  name: 'suggestion',
  components: {SuggestionEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/suggestion/list',
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
          prop: 'id',
          label: 'ID',
          width: 60,
          align: 'center',
          showOverflowTooltip: true,
          fixed: "left"
        },
        {
          prop: 'commit_user',
          label: '提交者',
          width: 70,
          align: 'center',
          showOverflowTooltip: true,
        },
        {
          prop: 'type',
          label: '类型',
          showOverflowTooltip: true,
          minWidth: 100,
          align: 'center',
          resizable: false,
          slot: 'type',
        },
        {
          prop: 'content',
          label: '需求或建议',
          width: 150,
          align: 'center',
          slot: 'expand_1',
        },
        {
          prop: 'status',
          label: '状态',
          minWidth: 100,
          align: 'center',
          resizable: false,
          slot: 'status',
        },
        {
          prop: 'feedback',
          label: '反馈内容',
          width: 150,
          align: 'center',
          slot: 'expand_2',
        },
        {
          prop: 'priority',
          label: '优先级',
          showOverflowTooltip: true,
          minWidth: 95,
          align: 'center',

          sortable: 'custom',
          order: '', // 初始化排序方式为空字符串
          sortableMethod: ()=> {
            // 在这里实现自定义的排序逻辑
            this.where.order = this.order;
            this.reload();
          }
        },
        {
          prop: 'create_time',
          label: '创建时间',
          showOverflowTooltip: true,
          sortable: 'custom',
          minWidth: 160,
          align: 'center',
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
        },
        {
          prop: 'update_time',
          label: '更新时间',
          showOverflowTooltip: true,
          sortable: 'custom',
          minWidth: 160,
          align: 'center',
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
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
      // 表格搜索条件
      where: {},
      // 表格选中数据
      selection: [],
      // 当前编辑数据
      current: null,
      // 是否显示编辑弹窗
      showEdit: false,
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
        this.current = row;
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http.get('/suggestion/detail/' + row.id).then((res) => {
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
      this.$http.delete('/suggestion/delete/' + row.id).then(res => {
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
      this.$confirm('确定要删除选中的通知吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({lock: true});
        this.$http.delete('/suggestion/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
    /* 更改状态 */
    editStatus(row) {
      const loading = this.$loading({lock: true});
      this.$http.put('/notice/status',  {id: row.id, status: row.status}).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message({type: 'success', message: res.data.msg});
        } else {
          row.status = !row.status ? 1 : 2;
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    },
    
  }
}
</script>

<style scoped>
</style>
