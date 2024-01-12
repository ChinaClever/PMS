<template>
 <div class="container">
    <el-form
        :model="where"
        label-width="77px"
        class="ele-form-search"
        @submit.native.prevent>
        <el-row :gutter="15">
        <el-col :lg="6" :md="12" :sm="16">
            <el-form-item label="扫码:">
            <el-input
                clearable
                v-model="where.keyword"
                placeholder="SN码"
                @keyup.enter.native="handleEnterKey"/>
            </el-form-item>
        </el-col>
        <el-col :lg="2" :md="2" :sm="2">
            <div class="ele-form-actions">
            <el-button
                type="primary"
                icon="el-icon-search"
                class="ele-btn-icon">查询
            </el-button>
            </div>
        </el-col>
        </el-row>
    </el-form>
 </div>
</template>

<script>
export default {
  data(){
    return{
        where:{}
    }
  },
  methods: {
    handleEnterKey(event){
        this.$http.get('/shipmentreport/report/' + event.target.value).then((res) => { 
            console.log(res.data)
        })
    }
  }

}

</script>

<style scoped>
.ele-form-search{
    padding-top: 30px;
}
</style>