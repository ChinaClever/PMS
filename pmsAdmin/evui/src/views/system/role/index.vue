<template>
  <div class="ele-body">
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
            <el-form-item label="角色名称:">
              <el-input
                clearable
                v-model="where.name"
                placeholder="请输入角色名称"/>
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
            v-if="permission.includes('sys:role:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:role:dall')">删除
          </el-button>
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:role:update')">修改
          </el-link>
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-finished"
            @click="openAuth(row)"
            v-if="permission.includes('sys:role:permission')">分配权限
          </el-link>
          <el-popconfirm
            class="ele-action"
            title="确定要删除此角色吗？"
            @confirm="remove(row)">
            <el-link
              type="danger"
              slot="reference"
              :underline="false"
              icon="el-icon-delete"
              v-if="permission.includes('sys:role:delete')">删除
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
    <role-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    <!-- 权限分配弹窗 -->
    <role-auth
      :data="current"
      :visible.sync="showAuth"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import RoleEdit from './role-edit';
import RoleAuth from './role-auth';

export default {
  name: 'SystemRole',
  components: {RoleEdit, RoleAuth},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/role/list',
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
          prop: 'name',
          label: '角色名称',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 200
        },
        {
          prop: 'code',
          label: '角色标识',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150
        },
        {
          prop: 'status',
          label: '职级状态',
          sortable: 'custom',
          align: 'center',
          width: 150,
          resizable: false,
          slot: 'status',
        },
        {
          prop: 'sort',
          label: '排序号',
          align: 'center',
          showOverflowTooltip: true,
          width: 100
        },
        {
          prop: 'note',
          label: '备注',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 200
        },
        {
          prop: 'create_time',
          label: '创建时间',
          sortable: 'custom',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 160,
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
        },
        {
          prop: 'update_time',
          label: '更新时间',
          sortable: 'custom',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 160,
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
        },
        {
          columnKey: 'action',
          label: '操作',
          width: 230,
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
      // 是否显示导入弹窗
      showAuth: false
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
        this.$http.get('/role/detail/' + row.id).then((res) => {
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
    /* 显示分配权限 */
    openAuth(row) {
      this.current = row;
      this.showAuth = true;
    },
    /* 删除 */
    remove(row) {
      const loading = this.$loading({lock: true});
      this.$http.delete('/role/delete/' + row.id).then(res => {
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
      this.$confirm('确定要删除选中的角色吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({lock: true});
        this.$http.delete('/role/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      this.$http.put('/role/status',  {id: row.id, status: row.status}).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message({type: 'success', message: res.data.msg});
        } else {
          row.status = !row.status ? 1 : 0;
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    }
  }
}
</script>

<style scoped>
</style>
