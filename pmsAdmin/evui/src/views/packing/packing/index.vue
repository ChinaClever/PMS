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
              <el-form-item label="查询:">
                <el-input
                  clearable
                  v-model="where.keyword"
                  @clear="clearSearchHandle"
                  placeholder="单号、客户名称或产品名称"/>
              </el-form-item>
            </el-col>

            <el-col :lg="6" :md="12" :offset="3" :pull="3">
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
              v-if="permission.includes('sys:packing:add')">添加
            </el-button>
            <el-button
              size="small"
              type="primary"
              icon="el-icon-plus"
              class="ele-btn-icon"
              @click="openBatchAddPage"
              v-if="permission.includes('sys:packing:add')">批量添加
            </el-button>
            <el-button
              size="small"
              type="danger"
              icon="el-icon-delete"
              class="ele-btn-icon"
              @click="removeBatch"
              v-if="permission.includes('sys:packing:dall')">删除
            </el-button>
            <el-button
              size="small"
              type="success"
              icon="el-icon-download"
              class="ele-btn-icon"
              @click="exportToExcel"
              v-if="permission.includes('sys:packing:export')">导出
            </el-button>
          </template>
          <!-- 操作列 -->
          <template slot="action" slot-scope="{row}">
            <el-link
              type="primary"
              :underline="false"
              icon="el-icon-edit"
              @click="openEdit(row)"
              v-if="permission.includes('sys:packing:update')">修改
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
                v-if="permission.includes('sys:weldingreport:delete')">删除
              </el-link>
            </el-popconfirm>
          </template>
           <!-- 成品模块列 -->
        <template slot="product_module" slot-scope="{row}">
          <el-tag v-if="row.product_module === 1" type="success" size="medium">成品</el-tag>
          <el-tag v-if="row.product_module === 2" size="medium">模块</el-tag>
        </template>
       
        </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
    <Packing-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import PackingEdit from './packing-edit';
  import XLSX from 'xlsx';
  import { saveAs } from 'file-saver';

  export default {
    name: 'ShipmentPacking',
    components: {PackingEdit},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        // 表格数据接口
        url: '/packing/list',
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
            prop: 'packing_finish_time',
            label: '打包完成日期',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'packing_count',
            label: '打包数量',
            showOverflowTooltip: true,
            minWidth: 100,
            align: 'center',
          },
          {
            prop: 'work_hours',
            label: '工时',
            showOverflowTooltip: true,
            minWidth: 80,
            align: 'center',
          },
          {
            prop: 'work_order',
            label: '单号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'client_name',
            label: '客户名称',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_code',
            label: '成品编码',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_name',
            label: '产品名称',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'shape',
            label: '规格型号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
            prop: 'product_count',
            label: '数量',
            showOverflowTooltip: true,
            minWidth: 60,
            align: 'center',
          },
          {
            prop: 'order_date',
            label: '订单日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'delivery_date',
            label: '交货日期',
            showOverflowTooltip: true,
            minWidth: 120,
            align: 'center',
            sortable: 'custom',
            order: '', 
            sortableMethod: ()=> {
            this.where.order = this.order;
            this.reload();
            }
          },
          {
            prop: 'SO_RQ_id',
            label: 'SO/RQ号',
            showOverflowTooltip: true,
            minWidth: 200,
            align: 'center',
          },
          {
          prop: 'product_module',
          label: '成品/模块',
          minWidth: 100,
          align: 'center',
          resizable: false,
          slot: 'product_module',
          },
          {
            prop: 'remark',
            label: '备注',
            showOverflowTooltip: true,
            minWidth: 200,
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
          this.current = null;
          this.showEdit = true;
        } else {
          // 编辑
          this.loading = true;
          this.$http.get('/packing/detail/' + row.id).then((res) => {
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
        this.$http.delete('/packing/delete/' + row.id).then(res => {
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
          this.$http.delete('/packing/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      // 清除搜索框
      clearSearchHandle(){
        this.$refs.table.reload({page: 1, where: this.where});
      },
      // 数据导出
      async exportToExcel() {
        // 创建 Excel 文件
        const workbook = XLSX.utils.book_new();     
        let temp = this.selection;
        if(this.selection.length == 0){
          await this.$http.get(this.url,{ params : {...this.where} }).then((res) => {
            if (res.data.code === 0) {
              // eslint-disable-next-line
              this.selection = res.data.data;
            } else {
              this.$message.error(res.data.msg);
            }
          }).catch((e) => {
            this.$message.error(e.message);
          });
        } 
        // eslint-disable-next-line
        this.selection = this.selection.map(({ id, ...rest }) => rest);

        this.selection = this.selection.map(obj => {
          if (obj.product_module === 2) {
            return { ...obj, product_module: '模块' };
          } else if (obj.product_module === 1) {
            return { ...obj, product_module: '成品' };
          }
          return obj;
        });

        // 获取字段名称（中文）
        const header = this.columns
          .slice(1, -1) // 排除排除第一列和最后两列,这里我排除的是我的id列和操作列
          .map(column => column.label);

        // 获取要导出的数据（排除第一列和最后两列）
        const data = this.selection.map(row =>
          this.columns
            .slice(1, -1) 
            .map(column => row[column.prop])
        );
        const worksheet = XLSX.utils.json_to_sheet(data);
        // 将字段名称添加到 Excel 文件中
        XLSX.utils.sheet_add_aoa(worksheet, [header], { origin: 'A1' });

        // 将数据添加到 Excel 文件中
        XLSX.utils.sheet_add_aoa(worksheet, data, { origin: 'A2' });

        // 将工作表添加到工作簿中
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

        // 保存 Excel 文件
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
        // 导出的文件名,下面代码在后面加了时间，如果不加可以直接saveAs(blob, fileName);
        const fileName = '打包记录表.xlsx';
        
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const date = String(currentDate.getDate()).padStart(2, '0');
        const hours = String(currentDate.getHours()).padStart(2, '0');
        const minutes = String(currentDate.getMinutes()).padStart(2, '0');
        const seconds = String(currentDate.getSeconds()).padStart(2, '0');

        const formattedDate = `${year}年${month}月${date}日${hours}时${minutes}分${seconds}秒`;
        const newFileName = `${fileName.split('.')[0]}_${formattedDate}.${fileName.split('.')[1]}`;

        saveAs(blob, newFileName); 
        this.selection = temp;
      },

      // 跳转批量添加界面
      openBatchAddPage(){
        this.$router.push("/packing/batchadd")
      }

    }
  }
  </script>
  
  <style scoped>
  </style>
  
  