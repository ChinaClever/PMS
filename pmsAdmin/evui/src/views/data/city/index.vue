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
            <el-form-item label="城市名称:">
              <el-input
                clearable
                v-model="where.name"
                placeholder="请输入城市名称"/>
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
      <!-- 数据表格 -->
      <el-table ref="table" :data="data" v-loading="loading" row-key="id" default-expand-all border
                height="calc(100vh - 215px)" highlight-current-row lazy
                :load="load"
                :tree-props="{children: 'children', hasChildren: 'haveChild'}">
        <el-table-column label="编号" type="index" width="60" align="center" fixed="left"/>
        <el-table-column label="城市名称" show-overflow-tooltip min-width="200">
          <template slot-scope="{row}">{{ row.name }}</template>
        </el-table-column>
        <el-table-column prop="city_code" label="城市区号" min-width="150" align="center"/>
        <el-table-column prop="area_code" label="行政编码" min-width="150" align="center"/>
        <el-table-column prop="parent_code" label="父级编码" min-width="150" align="center"/>
        <el-table-column label="城市级别" width="100px" align="center">
          <template slot-scope="{row}">
            <el-tag :type="['primary','success','warning', 'info'][row.level-1]" size="mini">
              {{ ['省份', '城市', '县区', '街道'][row.level - 1] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="zip_code" label="邮政编码" min-width="100" align="center"/>
        <el-table-column prop="short_name" label="城市简称" min-width="150" align="center"/>
        <el-table-column prop="pinyin" label="城市拼音" min-width="150" align="center"/>
        <el-table-column prop="lng" label="经度" min-width="100" align="center"/>
        <el-table-column prop="lat" label="纬度" min-width="100" align="center"/>
        <el-table-column prop="create_time" label="创建时间" show-overflow-tooltip min-width="160" align="center"/>
        <el-table-column label="操作" width="190px" align="center" :resizable="false" fixed="right">
          <template slot-scope="{row}">
            <el-link @click="openEdit(null, row.id)" icon="el-icon-plus" type="primary" :underline="false" v-if="permission.includes('sys:city:addz')">添加</el-link>
            <el-link @click="openEdit(row)" icon="el-icon-edit" type="primary" :underline="false" v-if="permission.includes('sys:city:update')">修改</el-link>
            <el-popconfirm title="确定要删除此城市吗？" @confirm="remove(row)" class="ele-action">
              <el-link slot="reference" icon="el-icon-delete" type="danger" :underline="false" v-if="permission.includes('sys:city:delete')">删除</el-link>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 编辑弹窗 -->
    <city-edit
      :data="current"
      :visible.sync="showEdit"
      @done="query"/>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import CityEdit from './city-edit';

export default {
  name: 'SystemCity',
  components: {CityEdit},
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
