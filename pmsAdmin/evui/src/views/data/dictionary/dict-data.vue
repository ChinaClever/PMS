<template>
  <div>
    <!-- 数据表格 -->
    <ele-pro-table
      ref="table"
      :datasource="url"
      :columns="columns"
      :where="where"
      height="calc(100vh - 261px)"
      tool-class="ele-toolbar-form">
      <!-- 表头工具栏 -->
      <template slot="toolbar">
        <el-form
          :model="where"
          class="ele-form-search"
          size="small"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="10">
            <el-col :md="12">
              <el-form-item>
                <el-input
                  v-model="where.name"
                  placeholder="请输入字典项名称"
                  clearable
                  size="small"/>
              </el-form-item>
            </el-col>
            <el-col :md="16">
              <el-form-item>
                <el-button
                  type="primary"
                  @click="reload"
                  icon="el-icon-search"
                  class="ele-btn-icon"
                  size="small">查询
                </el-button>
                <el-button
                  @click="openEdit(null)"
                  type="primary"
                  icon="el-icon-plus"
                  class="ele-btn-icon"
                  size="small"
                  v-if="permission.includes('sys:dictionary:add')">添加
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </template>
      <!-- 操作列 -->
      <template slot="action" slot-scope="{row}">
        <el-link
          @click="openEdit(row)"
          icon="el-icon-edit"
          type="primary"
          :underline="false"
          v-if="permission.includes('sys:dictionary:update')">修改
        </el-link>
        <el-popconfirm
          title="确定要删除此字典项吗？"
          @confirm="remove(row)"
          class="ele-action">
          <el-link
            slot="reference"
            icon="el-icon-delete"
            type="danger"
            :underline="false"
            v-if="permission.includes('sys:dictionary:delete')">删除
          </el-link>
        </el-popconfirm>
      </template>
    </ele-pro-table>
    <!-- 编辑弹窗 -->
    <dict-data-edit
      :visible.sync="showEdit"
      :data="current"
      :dict-id="dictId"
      @done="reload"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DictDataEdit from './dict-data-edit';

export default {
  name: 'DictData',
  components: {DictDataEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  props: {
    // 字典id
    dictId: Number
  },
  data() {
    return {
      // 表格数据接口
      url: '/dictdata/list',
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
          label: '字典项名称',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
        },
        {
          prop: 'value',
          label: '字典项值',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150
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
          showOverflowTooltip: true,
          minWidth: 160,
          formatter: (row, column, cellValue) => {
            return this.$util.toDateString(cellValue);
          }
        },
        {
          columnKey: 'action',
          label: '操作',
          width: 130,
          align: 'center',
          resizable: false,
          slot: 'action',
          fixed: "right"
        }
      ],
      // 表格搜索条件
      where: {
        dictId: this.dictId
      },
      // 当前编辑数据
      current: null,
      // 是否显示编辑弹窗
      showEdit: false
    };
  },
  methods: {
    /* 刷新表格 */
    reload() {
      this.$refs.table.reload({page: 1, where: this.where});
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
        this.$http.get('/dictdata/detail/' + row.id).then((res) => {
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
      this.$http.delete('/dictdata/delete/' + row.id).then(res => {
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
    }
  },
  watch: {
    // 监听字典id变化
    dictId() {
      this.where.dictId = this.dictId;
      this.reload();
    }
  }
}
</script>

<style scoped>
</style>
