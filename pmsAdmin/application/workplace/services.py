from application.shipmentreport.models import Shipment #出货统计--工单号查询
from application.inspectreport.models import Inspectreport #质检报表
from application.debugreport.models import Debug    #调试报表
from application.debugdata.models import Debugdata  #调试数据
from application.testdata.models import Testdata    #质检数据
from django.db.models import Sum
from datetime import timedelta, datetime

from utils import R, regular

#查询生产总数量（模块和成品）--出货统计-出货报表
def ShipmentAll():
    total_time = timedelta()
    #模块数量总计
    shipmentModelQuantity = Shipment.objects.filter(is_delete=False, product_module='2'
                                                    ).aggregate(shipmentModelQuantity=Sum('product_count'))['shipmentModelQuantity']
    if not shipmentModelQuantity:
        return None

    ##计算模块的总的效率
    GetAllModelDatas = Shipment.objects.filter(is_delete=False, product_module='2')

    for GetAllModelData in GetAllModelDatas:
        total_time += GetAllModelData.delivery_date -  GetAllModelData.order_date
    ModelTotalEfficiency = 0
    if total_time.days > 0:
        ModelTotalEfficiency = shipmentModelQuantity / total_time.days


    #成品数量总计
    shipmentFinishedlQuantity = Shipment.objects.filter(is_delete=False,product_module='1'
                                                        ).aggregate(shipmentFinishedlQuantity=Sum('product_count'))['shipmentFinishedlQuantity']
    if not shipmentFinishedlQuantity:
        return None
    # 计算成品的总的效率
    GetAllFinishedDatas = Shipment.objects.filter(is_delete=False, product_module='1')
    for GetAllFinishedData in GetAllFinishedDatas:
        total_time += GetAllFinishedData.delivery_date -  GetAllFinishedData.order_date
    FinishedTotalEfficiency = 0
    if total_time.days > 0:
        FinishedTotalEfficiency = shipmentModelQuantity / total_time.days

    data = {
            'AllShipmentModelQuantity': shipmentModelQuantity,  #总模块数量
            'AllShipmentFinishedQuantity': shipmentFinishedlQuantity,   #总成品数量
            'ModelTotalEfficiency':ModelTotalEfficiency,    #总模块效率
            'FinishedTotalEfficiency':FinishedTotalEfficiency,  #总成品效率
        }
    return data



#总成品合格率----质检表   总半成品合格率----调试表  模块与成品
def AllPass():
#1.模块的成品合格率计算   使用质检表格内的数据
    #质检模块数量总计
    ModelAllInspectQuantity = Inspectreport.objects.filter(is_delete=False, product_module='2').aggregate(ModelAllInspectQuantity=Sum('examine_an_amount'))['ModelAllInspectQuantity']
    if not ModelAllInspectQuantity:
        return None
    #获取质检模块所有数据
    ModelInspectData = Inspectreport.objects.filter(is_delete=False, product_module='2')
    #质检所有时间
    ModelAllInspectTime = 0
    for inspect in ModelInspectData:
        InspectDuration = inspect.end_time - inspect.start_time
        ModelAllInspectTime += InspectDuration.days

    #计算模块的成品合格率
    ModelTotalAllPass = ModelAllInspectQuantity / ModelAllInspectTime

#2.模块的半成品合格率计算    使用调试表格内的数据
    # 调试模块数量总计
    ModelAllDebugQuantity = Debug.objects.filter(is_delete=False,
                                                 product_module='2').aggregate(ModelAllDebugQuantity=Sum('product_count'))['ModelAllDebugQuantity']
    if not ModelAllDebugQuantity:
        return None

    # 调试模块所有时间
    ModelAllDebugTime = Debug.objects.filter(is_delete=False,
                                             product_module='2').aggregate(ModelAllDebugTime=Sum('work_hours'))['ModelAllDebugTime']
    if not ModelAllDebugTime:
        return None

    # 计算模块总半成品合格率
    ModelTotalHalfPass = ModelAllDebugQuantity / ModelAllDebugTime.days


#3.成品的成品合格率计算  使用质检表格内的数据
    #质检成品数量总计
    FinishedAllInspectQuantity = Inspectreport.objects.filter(is_delete=False,
                                                product_module='1'
                                                ).aggregate(FinishedAllInspectQuantity=Sum('examine_an_amount'))['FinishedAllInspectQuantity']
    if not FinishedAllInspectQuantity:
        return None
    #获取质检成品所有数据
    FinishedInspectData = Inspectreport.objects.filter(is_delete=False, product_module='1')
    #质检所有时间
    FinishedAllInspectTime = 0
    for inspect in FinishedInspectData:
        InspectDuration = inspect.end_time - inspect.start_time
        FinishedAllInspectTime += InspectDuration.days

    #计算成品的成品合格率
    FinishedTotalAllPass = FinishedAllInspectQuantity / FinishedAllInspectTime

#4.成品的半成品合格率计算 使用调试表格内的数据
    # 调试成品数量总计
    FinishedAllDebugQuantity = Debug.objects.filter(is_delete=False,
                                                 product_module='1').aggregate(FinishedAllDebugQuantity=Sum('product_count'))['FinishedAllDebugQuantity']
    if not FinishedAllDebugQuantity:
        return None

    # 调试成品所有时间
    FinishedAllDebugTime = Debug.objects.filter(is_delete=False,
                                             product_module='1').aggregate(FinishedAllDebugTime=Sum('work_hours'))['FinishedAllDebugTime']
    if not FinishedAllDebugTime:
        return None

    # 计算成品总半成品合格率
    FinishedTotalHalfPass = FinishedAllDebugQuantity / FinishedAllDebugTime.days

    data = {
        'ModelTotalAllPass':ModelTotalAllPass,          #模块的成品合格率
        'ModelTotalHalfPass':ModelTotalHalfPass,        #模块总半成品合格率
        'FinishedTotalAllPass':FinishedTotalAllPass,    #成品的成品合格率
        'FinishedTotalHalfPass':FinishedTotalHalfPass   #成品总半成品合格率
    }
    return data

#总工具使用时常  质检测试表格  调试测试表格
def AllUseToolTime():
    #质检测试工具所用时长
    UseInspectToolTime = Testdata.objects.filter(is_delete=False).aggregate(UseInspectToolTime=Sum('testTime'))['UseInspectToolTime']
    if not UseInspectToolTime:
        return None
    UseInspectToolTimeHours = UseInspectToolTime / 3600 #转成小时

    #调试工具所用时长
    UseDebugToolTime = Debugdata.objects.filter(is_delete=False).aggregate(UseDebugToolTime=Sum('testTime'))['UseDebugToolTime']
    if not UseDebugToolTime:
        return None
    UseDebugToolTimeHours = UseDebugToolTime / 3600 #转成小时

    #总的工具使用时常
    AllUseToolTimeHours = UseInspectToolTimeHours + UseDebugToolTimeHours

    data = {
        'AllUseToolTimeHours':AllUseToolTimeHours
    }
    return data

#获取所有模块的数据
def AllModelsData(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('startDate')
    vueEndTime = request.GET.get('endDate')
    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year':
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_year
        getDifferenceDay = getDifferenceDays

    elif tag == 'month':
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_month
        getDifferenceDay = getDifferenceDays

    elif tag == 'week':
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_week
        getDifferenceDay = getDifferenceDays

    elif tag == 'today':
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime
        getDifferenceDays = ((now - now_day).days + (now - now_day).seconds )/86400
        getDifferenceDays = "{:.4f}".format(getDifferenceDays)
        getDifferenceDay = getDifferenceDays

    else:
        start_date = vueStartTime
        end_date = vueEndTime
        getDifferenceDay = None

    #获取所有产品的名字
    GetproductNames = Shipment.objects.filter(is_delete=False, product_module='2')
    data = []

    for GetProductName in GetproductNames:
        productName = GetProductName.product_name
        # 获取出货表同产品名字的总生产数量
        ModelData = (Shipment.objects.filter(is_delete=False,
                                                product_module='2',
                                                product_name=productName,
                                                elivery_date__range=(start_date, end_date))
                        .aggregate(total_quantity_Shipment=Sum('product_count')))['total_quantity_Shipment']
        if not ModelData:
            return None
        # 获取调试表单内按照产品名字筛选获取到的数量   半成品
        GetDebugQuantity = (Debug.objects.filter(is_delete=False,
                                                 product_module='2',
                                                 product_name__in=productName,
                                                 submit_time__range=(start_date, end_date))
                            .aggregate(total_quantity_Debug=Sum('product_count')))['total_quantity_Debug']
        if not GetDebugQuantity:
            return None

        # 获取质检表单内按照产品名字筛选获取到的数量   成品
        GetInspectQuantity = (Inspectreport.objects.filter(is_delete=False,
                                                     product_module='2',
                                                     product_name__in=productName,
                                                     end_time__range=(start_date, end_date))
                              .aggregate(total_quantity_Inspect=Sum('examine_an_amount')))['total_quantity_Inspect']
        if not GetInspectQuantity:
            return None

        # 计算每个产品的生产效率
        efficiency = ModelData / getDifferenceDay
        # 计算模块的半成品合格率
        Model_HalfPass = GetDebugQuantity / ModelData if ModelData > 0 else 0
        # 计算模块的成品合格率
        Model_AllPass = GetInspectQuantity / ModelData if ModelData > 0 else 0

        product_data = {
            'product_name': productName,  # 模块产品名字
            'ModelData':ModelData, #模块产品的所有生产数量
            'efficiency': efficiency,  # 模块产品的生产效率
            'Model_HalfPass': Model_HalfPass,  # 模块的半成品合格率
            'Model_AllPass': Model_AllPass  # 模块的成品合格率
        }
        data.append(product_data)

    return R.ok(data=data)

#获取所有成品的数据
def AllFinishedData(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('startDate')
    vueEndTime = request.GET.get('endDate')

    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year':
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_year
        getDifferenceDay = getDifferenceDays

    elif tag == 'month':
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_month
        getDifferenceDay = getDifferenceDays

    elif tag == 'week':
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_week
        getDifferenceDay = getDifferenceDays

    elif tag == 'today':
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime
        getDifferenceDays = ((now - now_day).days + (now - now_day).seconds )/86400
        getDifferenceDays = "{:.4f}".format(getDifferenceDays)
        getDifferenceDay = getDifferenceDays

    else:
        start_date = vueStartTime
        end_date = vueEndTime
        getDifferenceDay = None

    #获取所有产品的名字
    GetproductNames = Shipment.objects.filter(is_delete=False, product_module='1')
    data = []

    for GetProductName in GetproductNames:
        productName = GetProductName.product_name
        #获取出货表同产品名字的总生产数量
        FinishedData = (Shipment.objects.filter(is_delete=False,
                                              product_module='1',
                                              product_name=productName,
                                              elivery_date__range=(start_date, end_date))
                        .aggregate(total_quantity_Shipment=Sum('product_count')))['total_quantity_Shipment']
        if not FinishedData:
            return None
        # 获取调试表单内按照产品名字筛选获取到的数量   半成品
        GetDebugQuantity = (Debug.objects.filter(is_delete=False,
                                                 product_module='1',
                                                 product_name__in=productName,
                                                 submit_time__range=(start_date, end_date))
                            .aggregate(total_quantity_Debug=Sum('product_count')))['total_quantity_Debug']
        if not GetDebugQuantity:
            return None

        # 获取质检表单内按照产品名字筛选获取到的数量   成品
        GetInspectQuantity = (Inspectreport.objects.filter(is_delete=False,
                                                     product_module='1',
                                                     product_name__in=productName,
                                                     end_time__range=(start_date, end_date))
                              .aggregate(total_quantity_Inspect=Sum('examine_an_amount')))['total_quantity_Inspect']
        if not GetInspectQuantity:
            return None

        #计算每个产品的生产效率
        efficiency = FinishedData / getDifferenceDay
        #计算成品的半成品合格率
        Finished_HalfPass = GetDebugQuantity / FinishedData if FinishedData > 0 else 0
        #计算成品的成品合格率
        Finished_AllPass = GetInspectQuantity / FinishedData if FinishedData > 0 else 0

        product_data = {
            'product_name':productName, #成品产品名字
            'FinishedData':FinishedData,#成品全部生产数量
            'efficiency':efficiency,    #成品产品的生产效率
            'Finished_HalfPass':Finished_HalfPass,  #成品的半成品合格率
            'Finished_AllPass':Finished_AllPass #成品的成品合格率
        }
        data.append(product_data)

    return R.ok(data=data)

def GetToolUseTime(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('startDate')
    vueEndTime = request.GET.get('endDate')

    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year':
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'month':
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'week':
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'today':
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime

    else:
        start_date = vueStartTime
        end_date = vueEndTime

    # 获取工具使用时长
    GetUseToolTimeDebugQuantity = (Debugdata.objects.filter(is_delete=False,
                                                            testEndTime__range=(start_date, end_date))
                                   .aggregate(total_quantity_time=Sum('testTime')))['total_quantity_time']
    if not GetUseToolTimeDebugQuantity:
        return None

    # 转成小时
    GetUseToolTimeDebugQuantity = GetUseToolTimeDebugQuantity / 3600

    GetUseToolTimeTestQuantity = (Testdata.objects.filter(is_delete=False,
                                                            testEndTime__range=(start_date, end_date))
                                   .aggregate(total_quantity_time=Sum('testTime')))['total_quantity_time']
    if not GetUseToolTimeTestQuantity:
        return None

    GetUseToolTimeTestQuantity = GetUseToolTimeTestQuantity / 3600

    GetUseToolTimeQuantity = GetUseToolTimeDebugQuantity + GetUseToolTimeTestQuantity
    data = {
        'GetUseToolTimeDebugQuantity':GetUseToolTimeQuantity,
    }
    return R.ok(data=data)