<template>
    <div class="ele-body">
      <el-card shadow="never">
        <!-- 搜索表单 -->
        <el-form
          :model="where"
          label-width="100px"
          class="ele-form-search"
          @keyup.enter.native="reload"
          @submit.native.prevent>
          <el-row :gutter="15">
            <el-col :lg="6" :md="12" >
              <el-form-item label="查询:">
                <el-input
                  style="width: 270px;"
                  clearable
                  v-model="where.keyword"
                  placeholder="单号、客户名称、产品名称"
                  @clear="clearSearchHandle"/>
              </el-form-item>
            </el-col>

            <el-col :lg="6" :md="12">
              <el-date-picker
                v-model="selectDateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="至"
                start-placeholder="订单日期开始日期"
                end-placeholder="订单日期结束日期"
                format="yyyy 年 MM 月 dd 日"
                value-format="yyyy-MM-dd"
                :picker-options="pickerOptions"
                @change="dateRangeHandleSelect">
              </el-date-picker>
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
              :parseData="parseData"
              height="calc(100vh - 315px)">
              <!-- 表头工具栏 -->
              <template slot="toolbar">
                 
                <el-button
                  size="small"
                  type="primary"
                  icon="el-icon-plus"
                  class="ele-btn-icon"
                  @click="openEdit(null)"
                  v-if="permission.includes('sys:shipmentreport:add')">添加
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  icon="el-icon-delete"
                  class="ele-btn-icon"
                  @click="removeBatch"
                  v-if="permission.includes('sys:shipmentreport:dall')">删除
                </el-button>
                <!-- <el-button
                  @click="showImport=true"
                  icon="el-icon-upload2"
                  class="ele-btn-icon"
                  size="small"
                  type="warning">导入
                </el-button> -->
                <el-button
                  size="small"
                  type="success"
                  icon="el-icon-download"
                  class="ele-btn-icon"
                  @click="exportToExcel"
                  v-if="permission.includes('sys:shipmentreport:export')">导出
                </el-button>
                 <el-date-picker
                v-model="selectDate"
                style="width: 160px; margin-left: 336px;"
                type="month"
                format="yyyy 年 MM 月"
                placeholder="选择年月"
                @change="yearAndMonthHandleSelect"
                >
              </el-date-picker>

              <el-select 
              v-model="where.product_module" 
              style="width: 120px; margin-left: 20px"
              clearable 
              placeholder="成品或模块"
              @change="productOrModuleHandleSelect">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                  </el-option>
                </el-select>

                <el-statistic
                group-separator=","
                :value="items_total"
                title="总数量"
                style="padding-left: 200px; font-weight: bold;"
              ></el-statistic>
      
              </template>
              <!-- 附件列 -->
              <template slot="attachment" slot-scope="{row}">
                <el-link v-for="(attachment, index) in row.fileNameList" :key="index"
                @click=" downloadFile(`${preUrl}/${encodeURIComponent(row.attachmentList[index])}`, attachment)" >
                  {{ attachment }}
                </el-link>
              </template>
              <!-- 操作列 -->
              <template slot="action" slot-scope="{row}">
                <el-link
                  type="primary"
                  :underline="false"
                  icon="el-icon-edit"
                  @click="openEdit(row)"
                  v-if="permission.includes('sys:shipmentreport:update')">修改
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
                    v-if="permission.includes('sys:shipmentreport:delete')">删除
                  </el-link>
                </el-popconfirm>
              </template>
              <!-- 状态列 -->
              <!-- <template slot="status" slot-scope="{row}">
                <el-switch
                  v-model="row.status"
                  @change="editStatus(row)"
                  :active-value="1"
                  :inactive-value="2"/>
              </template> -->
               <!-- 成品模块列 -->
              <template slot="product_module" slot-scope="{row}">
                <el-tag v-if="row.product_module === 1" type="success" size="medium">成品</el-tag>
                <el-tag v-if="row.product_module === 2" size="medium">模块</el-tag>
              </template>

            </ele-pro-table>
      </el-card>
      <!-- 编辑弹窗 -->
    <Shipmentreport-edit
      :data="current"
      :visible.sync="showEdit"
      @done="reload"/>

    <Shipmentimport
      :visible.sync="showImport"
      @done="reload"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import ShipmentreportEdit from './shipmentreport-edit';
  import Shipmentimport from './shipmentimport';
  import XLSX from 'xlsx';
  import { saveAs } from 'file-saver';

  export default {
    name: 'SystemShipmentReport',
    components: {ShipmentreportEdit, Shipmentimport},
    computed: {
      ...mapGetters(["permission"]),
    },
    data() {
      return {
        preUrl:process.env.VUE_APP_API_BASE_URL,
        // 表格数据接口
        url: '/shipmentreport/list',
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
            prop: 'update_delivery_date',
            label: '更改交期',
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
            prop: 'finish_date',
            label: '完成日期',
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
            columnKey: 'attachment',
            label: '附件',
            width: 150,
            align: 'center',
            resizable: false,
            slot: 'attachment',
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
        where: {
          // product_module: '1',
          // year: new Date().getFullYear(),
          // month: new Date().getMonth() + 1,
        },
        // selectDate: new Date(),
        selectDate: '',
        // 表格选中数据
        selection: [],
        // 当前编辑数据
        current: null,
        // 是否显示编辑弹窗
        showEdit: false,
        // 是否显示导入弹窗
        showImport: false,
        // 下拉框筛选成品或模块
        options: [{
          value: '1',
          label: '成品'
        }, {
          value: '2',
          label: '模块'
        }],
        // 查询日期范围的左边栏快捷选项
        pickerOptions: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 3);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近半年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 6);
              picker.$emit('pick', [start, end]);
            }
          }
          , {
            text: '最近一年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 12);
              picker.$emit('pick', [start, end]);
            }
          }
        ]
        },
        // 选择的日期范围
        selectDateRange: '',
        // 查询出来的总数量
        items_total:''

      };
    },
    
    methods: {
      parseData(val) {
      // console.log(val,'返回val=====');
      // 总数量
      this.items_total = val.items_total

      if (val.data.length != null){
        // 遍历每条数据 有附件的再处理
        for (var i = 0; i < val.data.length; i++) {
          if (val.data[i].attachment != null){
            // 分成多个文件
            var attachmentList = val.data[i].attachment.split(",");
            var fileNameList = []
            // 文件路径提取出文件名
            for (var j = 0; j < attachmentList.length; j++){   
              var filePath = attachmentList[j];
              var fileNameTemp = filePath.substring(filePath.lastIndexOf("/") + 1);
              var fileName = fileNameTemp.substring(fileNameTemp.indexOf("_") + 1);
              fileNameList.push(fileName)
            }

            val.data[i].attachmentList = attachmentList
            val.data[i].fileNameList = fileNameList
            // console.log(fileNameList);
          }
          
        }
      }
      return val
      },

      // 选择日期范围查询
      dateRangeHandleSelect(){
        this.where.year = null
        this.where.month = null
        this.selectDate = null
        if (this.selectDateRange != null){
          this.where.selectStartDate = this.selectDateRange[0]
          this.where.selectEndDate = this.selectDateRange[1]
        }else{
          this.where.selectStartDate = null
          this.where.selectEndDate = null
          this.$refs.table.reload({page: 1, where: this.where});
        }
      },
      // 选择年月
      yearAndMonthHandleSelect() {
        this.selectDateRange = null
        this.where.selectStartDate = null
        this.where.selectEndDate = null
        this.where.year = null
        this.where.month = null
        if (this.selectDate != null){
          this.where.year = this.selectDate.getFullYear();
          // getMonth 方法返回的月份是从 0 开始计数的，即 0 表示一月
          this.where.month = this.selectDate.getMonth() + 1;
        }
        this.$refs.table.reload({page: 1, where: this.where});
      },
      // 下拉选择成品或模块
      productOrModuleHandleSelect() {
        this.$refs.table.reload({page: 1, where: this.where});
      },
      // 清除搜索框
      clearSearchHandle(){
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 刷新表格 */
      reload() {
        this.$refs.table.reload({page: 1, where: this.where});
      },
      /* 重置搜索 */
      reset() {
        this.selectDateRange = null
        this.selectDate = null
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
          this.$http.get('/shipmentreport/detail/' + row.id).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.current = Object.assign({fileNameList: row.fileNameList, attachmentList:row.attachmentList}, res.data.data);
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
        this.$http.delete('/shipmentreport/delete/' + row.id).then(res => {
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
          this.$http.delete('/shipmentreport/delete/' + this.selection.map(d => d.id).join(",")).then(res => {
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
      // 数据导出
      async exportToExcel() {
        // 创建 Excel 文件
        const workbook = XLSX.utils.book_new();
        //去除不需要的字段，这里我不希望显示id，所以id不返回
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
        this.selection = this.selection.map(({ id,attachment, ...rest }) => rest);

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
          .slice(1, -2) // 排除排除第一列和最后两列,这里我排除的是我的id列、附件列和操作列
          .map(column => column.label);

        // 获取要导出的数据（排除第一列和最后两列）
        const data = this.selection.map(row =>
          this.columns
            .slice(1, -2) 
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
        const fileName = '排期表单.xlsx';
        
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
      // 附件下载
      downloadFile(fileUrl, fileName){
        console.log(fileUrl)
        this.$http.get(fileUrl, { responseType: 'blob' }).then(response => {
          saveAs(response.data, fileName);
        })
        .catch(error => {
          console.error(fileName+'文件下载失败', error);
        });
      },
    
    
    }
  }
  </script>
  
  <style scoped>
  </style>
  
  