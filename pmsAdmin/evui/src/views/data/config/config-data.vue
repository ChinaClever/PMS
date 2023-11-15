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
            <el-col :md="8">
              <el-form-item>
                <el-input
                  v-model="where.name"
                  placeholder="请输入配置项名称"
                  clearable
                  size="small"/>
              </el-form-item>
            </el-col>
            <el-col :md="8">
              <el-form-item>
                <el-input
                  v-model="where.code"
                  placeholder="请输入配置项值"
                  clearable
                  size="small"/>
              </el-form-item>
            </el-col>
            <el-col :md="8">
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
                  v-if="permission.includes('sys:config:add')">添加
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
          v-if="permission.includes('sys:config:update')">修改
        </el-link>
        <el-popconfirm
          title="确定要删除此配置项吗？"
          @confirm="remove(row)"
          class="ele-action">
          <el-link
            slot="reference"
            icon="el-icon-delete"
            type="danger"
            :underline="false"
            v-if="permission.includes('sys:config:delete')">删除
          </el-link>
        </el-popconfirm>
      </template>
      <!-- 配置类型列 -->
      <template slot="type" slot-scope="{row}">
        <el-tag v-if="row.type === 'readonly'" type="" size="small">只读文本</el-tag>
        <el-tag v-if="row.type === 'number'" type="success" size="small">数字</el-tag>
        <el-tag v-if="row.type === 'text'" type="success" size="small">单行文本</el-tag>
        <el-tag v-if="row.type === 'textarea'" type="warning" size="small">多行文本</el-tag>
        <el-tag v-if="row.type === 'array'" type="danger" size="small">数组</el-tag>
        <el-tag v-if="row.type === 'password'" type="" size="small">密码</el-tag>
        <el-tag v-if="row.type === 'radio'" type="success" size="small">单选框</el-tag>
        <el-tag v-if="row.type === 'checkbox'" type="info" size="small">复选框</el-tag>
        <el-tag v-if="row.type === 'select'" type="warning" size="small">下拉框</el-tag>
        <el-tag v-if="row.type === 'icon'" type="danger" size="small">字体图标</el-tag>
        <el-tag v-if="row.type === 'date'" type="" size="small">日期</el-tag>
        <el-tag v-if="row.type === 'datetime'" type="success" size="small">时间</el-tag>
        <el-tag v-if="row.type === 'image'" type="info" size="small">单张图片</el-tag>
        <el-tag v-if="row.type === 'images'" type="" size="small">多张图片</el-tag>
        <el-tag v-if="row.type === 'file'" type="success" size="small">单个文件</el-tag>
        <el-tag v-if="row.type === 'files'" type="warning" size="small">多个文件</el-tag>
        <el-tag v-if="row.type === 'ueditor'" type="danger" size="small">富文本编辑器</el-tag>
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
    <!-- 编辑弹窗 -->
    <config-data-edit
      :visible.sync="showEdit"
      :data="current"
      :config-id="configId"
      @done="reload"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ConfigDataEdit from './config-data-edit';

export default {
  name: 'ConfigData',
  components: {ConfigDataEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  props: {
    // 配置id
    configId: Number
  },
  data() {
    return {
      // 表格数据接口
      url: '/configdata/list',
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
          prop: 'title',
          label: '配置项标题',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
        },
        {
          prop: 'code',
          label: '配置编码',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150
        },
        {
          prop: 'type',
          label: '配置类型',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150,
          slot: 'type',
        },
        {
          prop: 'value',
          label: '配置值',
          align: 'center',
          showOverflowTooltip: true,
          minWidth: 150
        },
        {
          prop: 'status',
          label: '状态',
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
        configId: this.configId
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
        this.$http.get('/configdata/detail/' + row.id).then((res) => {
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
      this.$http.delete('/configdata/delete/' + row.id).then(res => {
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
    /* 更改状态 */
    editStatus(row) {
      const loading = this.$loading({lock: true});
      this.$http.put('/configdata/status',  {id: row.id, status: row.status}).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message.success(res.data.msg);
        } else {
          row.status = !row.status ? 1 : 2;
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    }
  },
  watch: {
    // 监听配置id变化
    configId() {
      this.where.configId = this.configId;
      this.reload();
    }
  }
}
</script>

<style scoped>
</style>
