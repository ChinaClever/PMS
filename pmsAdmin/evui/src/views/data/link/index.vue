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
            <el-form-item label="友链名称:">
              <el-input
                clearable
                v-model="where.name"
                placeholder="请输入友链名称"/>
            </el-form-item>
          </el-col>
          <el-col :lg="6" :md="12">
            <el-form-item label="友链类型:">
              <el-select
                clearable
                v-model="where.type"
                placeholder="请选择友链类型"
                class="ele-fluid">
                <el-option label="友情链接" value="1"/>
                <el-option label="合作伙伴" value="2"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :lg="6" :md="12">
            <el-form-item label="投放平台:">
              <el-select
                clearable
                v-model="where.platform"
                placeholder="请选择投放平台"
                class="ele-fluid">
                <el-option label="PC站" value="1"/>
                <el-option label="WAP站" value="2"/>
                <el-option label="微信小程序" value="3"/>
                <el-option label="APP应用" value="4"/>
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
        <!-- 表头工具栏 -->
        <template slot="toolbar">
          <el-button
            size="small"
            type="primary"
            icon="el-icon-plus"
            class="ele-btn-icon"
            @click="openEdit(null)"
            v-if="permission.includes('sys:link:add')">添加
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            class="ele-btn-icon"
            @click="removeBatch"
            v-if="permission.includes('sys:link:dall')">删除
          </el-button>
        </template>
        <!-- 操作列 -->
        <template slot="action" slot-scope="{row}">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit"
            @click="openEdit(row)"
            v-if="permission.includes('sys:link:update')">修改
          </el-link>
          <el-popconfirm
            class="ele-action"
            title="确定要删除此友链吗？"
            @confirm="remove(row)">
            <el-link
              type="danger"
              slot="reference"
              :underline="false"
              icon="el-icon-delete"
              v-if="permission.includes('sys:link:delete')">删除
            </el-link>
          </el-popconfirm>
        </template>
        <!-- 友链类型列 -->
        <template slot="type" slot-scope="{row}">
          <el-tag v-if="row.type === 1" type="success" size="small">友情链接</el-tag>
          <el-tag v-if="row.type === 2" type="warning" size="small">合作伙伴</el-tag>
        </template>
        <!-- 投放平台列 -->
        <template slot="platform" slot-scope="{row}">
          <el-tag v-if="row.platform === 1" type="success" size="small">PC站</el-tag>
          <el-tag v-if="row.platform === 2" type="warning" size="small">WAP站</el-tag>
          <el-tag v-if="row.platform === 3" type="danger" size="small">微信小程序</el-tag>
          <el-tag v-if="row.platform === 4" type="info" size="small">APP应用</el-tag>
        </template>
        <!-- 状态列 -->
        <template slot="status" slot-scope="{row}">
          <el-switch
            v-model="row.status"
            @change="editStatus(row)"
            :active-value="1"
            :inactive-value="2"/>
        </template>
        <!-- 头像 -->
        <template slot="image" slot-scope="{row}">
          <el-avatar shape="square" :size="25" :src="row.image"/>
        </template>
        <!-- 友链形式 -->
        <template slot="form" slot-scope="{row}">
          <ele-dot :type="['', 'success'][row.form-1]" :ripple="row.form===0"
                   :text="['文字链接','图片链接'][row.form-1]"/>
        </template>
      </ele-pro-table>
    </el-card>
    <!-- 编辑弹窗 -->
    <link-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import LinkEdit from './link-edit';

export default {
  name: 'SystemLink',
  components: {LinkEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: '/link/list',
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
          label: '友链名称',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center',
        },
        {
          prop: 'type',
          label: '友情类型',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
          slot: 'type',
        },
        {
          prop: 'platform',
          label: '投放平台',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
          slot: 'platform',
        },
        {
          prop: 'status',
          label: '友链状态',
          sortable: 'custom',
          align: 'center',
          width: 150,
          resizable: false,
          slot: 'status',
        },
        {
          prop: 'url',
          label: '友链URL',
          showOverflowTooltip: true,
          minWidth: 200,
          align: 'center'
        },
        {
          columnKey: 'image',
          label: '友链图片',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 100,
          slot: 'image'
        },
        {
          prop: 'form',
          label: '友链形式',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
          slot: 'form',
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
          width: 200
        },
        {
          prop: 'create_time',
          label: '创建时间',
          sortable: 'custom',
          showOverflowTooltip: true,
          minWidth: 160,
          align: 'center',
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
        },
        {
          prop: 'update_time',
          label: '更新时间',
          sortable: 'custom',
          showOverflowTooltip: true,
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
        this.$http.get('/link/detail/' + row.id).then((res) => {
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
      this.$http.delete('/link/delete/' + row.id).then(res => {
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
      this.$confirm('确定要删除选中的友链吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({lock: true});
        this.$http.delete('/link/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      this.$http.put('/link/status',  {id: row.id, status: row.status}).then(res => {
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
    }
  }
}
</script>

<style scoped>
</style>
