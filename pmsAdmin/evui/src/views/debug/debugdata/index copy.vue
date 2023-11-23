<template>
  <div class="ele-body">
    <el-card shadow="never">
      <!-- 搜索表单 -->
      <el-form
        :model="where"
        label-width="77px"
        class="ele-form-search"
        @keyup.enter.native="query"
        @submit.native.prevent>
        <el-row :gutter="15">
          <el-col :lg="6" :md="12">
            <el-form-item label="查询:">
                <el-input
                  clearable
                  v-model="where.keyword"
                  placeholder="软件类型、产品类型或结果"/>
              </el-form-item>
          </el-col>
          <el-col :lg="6" :md="12">
            <div class="ele-form-actions">
              <el-button
                type="primary"
                icon="el-icon-search"
                class="ele-btn-icon"
                @click="query">查询
              </el-button>
              <el-button @click="reset">重置</el-button>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <!-- 表头工具栏 -->
      <template slot="toolbar">
            <el-button
              size="small"
              type="primary"
              icon="el-icon-plus"
              class="ele-btn-icon"
              @click="openEdit(null)"
              v-if="permission.includes('sys:debugdata:add')">添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:debugdata:dall')">删除
            </el-button>
          </template>
      <!-- 数据表格 -->
      <el-table ref="table" :data="data" v-loading="loading" row-key="id" default-expand-all border
                height="calc(100vh - 215px)" highlight-current-row lazy
                :load="load"
                :tree-props="{children: 'children', hasChildren: 'haveChild'}">
        <el-table-column label="软件类型" show-overflow-tooltip min-width="150">
          <template slot-scope="{row}">{{ row.softwareType }}</template>
        </el-table-column>
        <el-table-column prop="productType" label="产品类型" min-width="350" align="center"/>
        <el-table-column prop="productSN" label="产品SN" min-width="250" align="center"/>
        <el-table-column prop="macAddress" label="mac地址" min-width="200" align="center"/>
        <el-table-column label="结果" width="100px" align="center">
          <template slot-scope="{row}">
            <el-tag :type="['danger','success'][row.result]" size="mini">
              {{ ['失败', '通过'][row.result ] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="softwareVersion" label="软件版本" min-width="100" align="center"/>
        <el-table-column prop="clientName" label="客户名称" min-width="80" align="center"/>
        <el-table-column prop="companyName" label="公司名称" min-width="120" align="center"/>
        <el-table-column prop="protocolVersion" label="协议名称" min-width="80" align="center"/>
        <el-table-column prop="testStartTime" label="测试开始时间" min-width="200" align="center"/>
        <el-table-column prop="testEndTime" label="测试结束时间" min-width="200" align="center"/>
        <el-table-column prop="testTime" label="测试时间" min-width="80" align="center"/>

        <el-table-column label="操作" width="190px" align="center" :resizable="false" fixed="right">
          <template slot-scope="{row}">
            <el-link @click="openEdit(row)" icon="el-icon-edit" type="primary" :underline="false" v-if="permission.includes('sys:debugdata:update')">修改</el-link>
            <el-popconfirm title="确定要删除此城市吗？" @confirm="remove(row)" class="ele-action">
              <el-link slot="reference" icon="el-icon-delete" type="danger" :underline="false" v-if="permission.includes('sys:debugdata:delete')">删除</el-link>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 编辑弹窗 -->
    <debug-data-edit
      :data="current"
      :visible.sync="showEdit"
      @done="query"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DebugDataEdit from './debugdata-edit';

export default {
  name: 'SystemDebugData',
  components: {DebugDataEdit},
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      loading: true,  // 加载状态
      data: [],  // 列表数据
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
  mounted() {
    this.query();
  },
  methods: {
    /* 查询 */
    query() {
      this.loading = true;
      // 城市名称
      var name = this.where.name !== undefined ? this.where.name : ""
      this.$http.get('/city/list?name=' + name).then(res => {
        this.loading = false;
        if (res.data.code === 0) {
          this.data = this.$util.toTreeData(res.data.data, 'id', 'pid');
        } else {
          this.$message.error(res.data.msg || '获取数据失败');
        }
      }).catch(e => {
        this.loading = false;
        this.$message.error(e.message);
      });
    },
    /**
     * 异步加载数据
     */
    load(tree, treeNode, resolve) {
      this.where['pid'] = tree.id;
      this.$http.get('/city/list', {params: this.where}).then(res => {
        if (res.data.code === 0) {
          resolve(res.data.data)
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        this.$message.error(e.message);
      });
    },
    /* 重置搜索 */
    reset() {
      this.where = {};
      this.query();
    },
    /* 显示编辑 */
    openEdit(row, parentId) {
      if (!row) {
        // 添加
        this.current = Object.assign({
        level: 1,
        pid: parentId
      }, row);
      this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http.get('/city/detail/' + row.id).then((res) => {
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
      if (row.children && row.children.length > 0) {
        this.$message.error('请先删除子节点');
        return;
      }
      const loading = this.$loading({lock: true});
      this.$http.delete('/city/delete/' + row.id).then(res => {
        loading.close();
        if (res.data.code === 0) {
          this.$message.success(res.data.msg);
          this.query();
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(e => {
        loading.close();
        this.$message.error(e.message);
      });
    },
    /* 展开全部 */
    expandAll() {
      this.$refs.table.data.forEach(d => {
        this.$refs.table.toggleRowExpansion(d, true);
      });
    },
    /* 折叠全部 */
    foldAll() {
      this.$refs.table.data.forEach(d => {
        this.$refs.table.toggleRowExpansion(d, false);
      });
    },
  }
}
</script>

<style scoped>
</style>
