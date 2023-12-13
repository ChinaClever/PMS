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
    if shipmentModelQuantity == None:
        shipmentModelQuantity = 0

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
    if shipmentFinishedlQuantity == None:
        shipmentFinishedlQuantity = 0
    # 计算成品的总的效率
    GetAllFinishedDatas = Shipment.objects.filter(is_delete=False, product_module='1')
    for GetAllFinishedData in GetAllFinishedDatas:
        total_time += GetAllFinishedData.delivery_date -  GetAllFinishedData.order_date
    FinishedTotalEfficiency = 0
    if total_time.days > 0:
        FinishedTotalEfficiency = shipmentFinishedlQuantity / total_time.days

    ModelTotalEfficiency = round(ModelTotalEfficiency, 2)
    FinishedTotalEfficiency = round(FinishedTotalEfficiency, 2)
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
    if ModelAllInspectQuantity == None:
        ModelAllInspectQuantity = 0
    #获取质检模块所有数据
    ModelInspectData = Inspectreport.objects.filter(is_delete=False, product_module='2')
    if not ModelInspectData:
        return None

    #质检所有时间
    ModelAllInspectTime = 0
    for inspect in ModelInspectData:
        InspectDuration = inspect.end_time - inspect.start_time
        ModelAllInspectTime += InspectDuration.days

    #计算模块的成品合格率
    ModelTotalAllPass = ModelAllInspectQuantity / ModelAllInspectTime if ModelAllInspectTime > 0 else 0

#2.模块的半成品合格率计算    使用调试表格内的数据
    # 调试模块数量总计
    ModelAllDebugQuantity = Debug.objects.filter(is_delete=False,
                                                 product_module='2').aggregate(ModelAllDebugQuantity=Sum('product_count'))['ModelAllDebugQuantity']
    if ModelAllDebugQuantity == None:
        ModelAllDebugQuantity = 0

    # 调试模块所有时间
    ModelAllDebugTime = Debug.objects.filter(is_delete=False,
                                             product_module='2').aggregate(ModelAllDebugTime=Sum('work_hours'))['ModelAllDebugTime']
    if not ModelAllDebugTime:
        return None

    ModelAllDebugTime = round(ModelAllDebugTime/24.0, 2)
    # 计算模块总半成品合格率
    ModelTotalHalfPass = ModelAllDebugQuantity / ModelAllDebugTime if ModelAllDebugTime > 0 else 0
    ModelTotalHalfPass = round(ModelTotalHalfPass, 2)

#3.成品的成品合格率计算  使用质检表格内的数据
    #质检成品数量总计
    FinishedAllInspectQuantity = Inspectreport.objects.filter(is_delete=False,
                                                product_module='1'
                                                ).aggregate(FinishedAllInspectQuantity=Sum('examine_an_amount'))['FinishedAllInspectQuantity']
    # print(f"质检成品数量总计{FinishedAllInspectQuantity}")
    if FinishedAllInspectQuantity == None:
        FinishedAllInspectQuantity = 0
    #获取质检成品所有数据
    FinishedInspectData = Inspectreport.objects.filter(is_delete=False, product_module='1')
    if not FinishedInspectData:
        return None

    #质检所有时间
    FinishedAllInspectTime = 0
    for inspect in FinishedInspectData:
        InspectDuration = inspect.end_time - inspect.start_time
        FinishedAllInspectTime += InspectDuration.days

    #计算成品的成品合格率
    FinishedTotalAllPass = FinishedAllInspectQuantity / FinishedAllInspectTime if FinishedAllInspectTime > 0 else 0

#4.成品的半成品合格率计算 使用调试表格内的数据
    # 调试成品数量总计
    FinishedAllDebugQuantity = Debug.objects.filter(is_delete=False,
                                                 product_module='1').aggregate(FinishedAllDebugQuantity=Sum('product_count'))['FinishedAllDebugQuantity']
    if FinishedAllDebugQuantity == None:
        FinishedAllDebugQuantity = 0

    # 调试成品所有时间
    FinishedAllDebugTime = Debug.objects.filter(is_delete=False,
                                             product_module='1').aggregate(FinishedAllDebugTime=Sum('work_hours'))['FinishedAllDebugTime']
    if FinishedAllDebugTime == None:
        FinishedAllDebugTime = 0

    # 计算成品总半成品合格率
    FinishedTotalHalfPass = FinishedAllDebugQuantity / FinishedAllDebugTime if FinishedAllDebugTime > 0 else 0
    FinishedTotalHalfPass = round(FinishedTotalHalfPass, 2)

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
    if UseInspectToolTime == None:
        UseInspectToolTime = 0
    UseInspectToolTimeHours = UseInspectToolTime / 3600 if UseInspectToolTime > 0 else 0#转成小时

    #调试工具所用时长
    UseDebugToolTime = Debugdata.objects.filter(is_delete=False).aggregate(UseDebugToolTime=Sum('testTime'))['UseDebugToolTime']
    if UseDebugToolTime == None:
        UseDebugToolTime = 0

    UseDebugToolTimeHours = UseDebugToolTime / 3600 if UseDebugToolTime > 0 else 0 #转成小时


    #总的工具使用时常
    AllUseToolTimeHours = UseInspectToolTimeHours + UseDebugToolTimeHours
    AllUseToolTimeHours = round(AllUseToolTimeHours, 3)
    data = {
        'AllUseToolTimeHours':AllUseToolTimeHours
    }

    return data

#获取所有模块的数据
def AllModelsData(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('start_date')
    vueEndTime = request.GET.get('end_date')

    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year' and vueStartTime == None and vueEndTime == None:
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_year
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'month'and vueStartTime == None and vueEndTime == None:
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_month
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'week'and vueStartTime == None and vueEndTime == None:
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_week
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'today'and vueStartTime == None and vueEndTime == None:
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime
        getDifferenceDays = ((now - now_day).days + (now - now_day).seconds )/86400
        getDifferenceDay = round(getDifferenceDays)

    else:
        start_date =datetime.fromisoformat(vueStartTime)
        end_date = datetime.fromisoformat(vueEndTime)
        getDifferenceDay = (end_date - start_date).total_seconds()/86400

    #获取所有产品的名字
    GetproductNames = Shipment.objects.filter(is_delete=False, product_module='2')
    data = set()

    for GetProductName in GetproductNames:
        productName = GetProductName.product_name

        # 获取出货表同产品名字的总生产数量
        shipmentModelQuantity = Shipment.objects.filter(is_delete=False,
                                                        product_module='2',
                                                        product_name=productName,
                                                        delivery_date__range=(start_date, end_date)
                                                    ).aggregate(shipmentModelQuantity=Sum('product_count'))['shipmentModelQuantity']
        if shipmentModelQuantity == None:
            shipmentModelQuantity = 0


        # 获取调试表单内按照产品名字筛选获取到的数量   半成品
        total_quantity_Debug = Debug.objects.filter(is_delete=False,
                                                 product_module='2',
                                                 product_name=productName,
                                                 submit_time__range=(start_date, end_date)
                                                 ).aggregate(total_quantity_Debug=Sum('product_count'))['total_quantity_Debug']
        if total_quantity_Debug == None:
            total_quantity_Debug = 0


        # 获取质检表单内按照产品名字筛选获取到的数量   成品
        total_quantity_Inspect = Inspectreport.objects.filter(is_delete=False,
                                                     product_module='2',
                                                     product_name=productName,
                                                     end_time__range=(start_date, end_date)
                                                              ).aggregate(total_quantity_Inspect=Sum('examine_an_amount'))['total_quantity_Inspect']

        if total_quantity_Inspect == None:
            total_quantity_Inspect = 0

        # 计算每个产品的生产效率

        efficiency = shipmentModelQuantity / getDifferenceDay if getDifferenceDay > 0 else 0
        efficiency = round(efficiency, 2)
        # 计算模块的半成品合格率
        Model_HalfPass = total_quantity_Debug / shipmentModelQuantity if shipmentModelQuantity > 0 else 0
        Model_HalfPass = round(Model_HalfPass, 3)
        # 计算模块的成品合格率
        Model_AllPass = total_quantity_Inspect / shipmentModelQuantity if shipmentModelQuantity > 0 else 0
        Model_AllPass = round(Model_AllPass, 3)

        product_data = {
            'product_name': productName,  # 模块产品名字
            'ModelData':shipmentModelQuantity, #模块产品的所有生产数量
            'efficiency': efficiency,  # 模块产品的生产效率
            'Model_HalfPass': Model_HalfPass,  # 模块的半成品合格率
            'Model_AllPass': Model_AllPass  # 模块的成品合格率
        }
        data.add(tuple(product_data.items()))
    SendData = [dict(item) for item in data]
    return SendData

#获取所有成品的数据
def AllFinishedData(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('start_date')
    vueEndTime = request.GET.get('end_date')

    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year' and vueStartTime == None and vueEndTime == None:
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_year
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'month'and vueStartTime == None and vueEndTime == None:
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_month
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'week'and vueStartTime == None and vueEndTime == None:
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay
        getDifferenceDays = now - now_week
        getDifferenceDay = getDifferenceDays.days

    elif tag == 'today'and vueStartTime == None and vueEndTime == None:
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime
        getDifferenceDays = ((now - now_day).days + (now - now_day).seconds )/86400
        getDifferenceDay = round(getDifferenceDays)

    else:
        start_date =datetime.fromisoformat(vueStartTime)
        end_date = datetime.fromisoformat(vueEndTime)
        getDifferenceDay = (end_date - start_date).total_seconds()/86400

    #获取所有产品的名字
    GetproductNames = Shipment.objects.filter(is_delete=False, product_module='1')
    data = set()

    for GetProductName in GetproductNames:
        productName = GetProductName.product_name
        #获取出货表同产品名字的总生产数量
        FinishedData = (Shipment.objects.filter(is_delete=False,
                                              product_module='1',
                                              product_name=productName,
                                              delivery_date__range=(start_date, end_date))
                        .aggregate(total_quantity_Shipment=Sum('product_count')))['total_quantity_Shipment']
        if FinishedData == None:
            FinishedData = 0
        # 获取调试表单内按照产品名字筛选获取到的数量   半成品
        GetDebugQuantity = (Debug.objects.filter(is_delete=False,
                                                 product_module='1',
                                                 product_name__in=productName,
                                                 submit_time__range=(start_date, end_date))
                            .aggregate(total_quantity_Debug=Sum('product_count')))['total_quantity_Debug']
        if GetDebugQuantity == None:
            GetDebugQuantity = 0

        # 获取质检表单内按照产品名字筛选获取到的数量   成品
        GetInspectQuantity = (Inspectreport.objects.filter(is_delete=False,
                                                     product_module='1',
                                                     product_name__in=productName,
                                                     end_time__range=(start_date, end_date))
                              .aggregate(total_quantity_Inspect=Sum('examine_an_amount')))['total_quantity_Inspect']
        if GetInspectQuantity == None:
            GetInspectQuantity = 0

        #计算每个产品的生产效率
        efficiency = FinishedData / getDifferenceDay if getDifferenceDay > 0 else 0
        efficiency = round(efficiency, 2)
        #计算成品的半成品合格率
        Finished_HalfPass = GetDebugQuantity / FinishedData if FinishedData > 0 else 0
        Finished_HalfPass = round(Finished_HalfPass, 2)
        #计算成品的成品合格率
        Finished_AllPass = GetInspectQuantity / FinishedData if FinishedData > 0 else 0
        Finished_AllPass = round(Finished_AllPass, 2)

        product_data = {
            'product_name':productName, #成品产品名字
            'FinishedData':FinishedData,#成品全部生产数量
            'efficiency':efficiency,    #成品产品的生产效率
            'Finished_HalfPass':Finished_HalfPass,  #成品的半成品合格率
            'Finished_AllPass':Finished_AllPass #成品的成品合格率
        }
        data.add(tuple(product_data.items()))
    SendData = [dict(item) for item in data]
    # print(f"成品的全部数据SendData{SendData}")
    return SendData

def GetToolUseTime(request):
    tag = request.GET.get('tag')
    vueStartTime = request.GET.get('start_date')
    vueEndTime = request.GET.get('end_date')

    now = datetime.now()
    now_strDay = datetime.strftime(now, "%Y-%m-%d")
    now_strTime = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

    if tag == 'year' and vueStartTime == None and vueEndTime == None:
        now_year = datetime(now.year, 1, 1)
        start_date = datetime.strftime(now_year, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'month' and vueStartTime == None and vueEndTime == None:
        now_month = datetime(now.year, now.month, 1)
        start_date = datetime.strftime(now_month, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'week' and vueStartTime == None and vueEndTime == None:
        now_week = now - timedelta(days=now.weekday())
        start_date = datetime.strftime(now_week, "%Y-%m-%d")
        end_date = now_strDay

    elif tag == 'today' and vueStartTime == None and vueEndTime == None:
        now_day = datetime(now.year, now.month, now.day)
        start_date = datetime.strftime(now_day, "%Y-%m-%d %H:%M:%S")
        end_date = now_strTime

    else:
        start_date = datetime.fromisoformat(vueStartTime)
        end_date = datetime.fromisoformat(vueEndTime)


    # 获取工具使用时长
    GetUseToolTimeDebugQuantityTime = (Debugdata.objects.filter(is_delete=False,
                                                            testEndTime__range=(start_date, end_date))
                                   .aggregate(GetUseToolTimeDebugQuantityTime=Sum('testTime')))['GetUseToolTimeDebugQuantityTime']
    if GetUseToolTimeDebugQuantityTime == None:
        GetUseToolTimeDebugQuantityTime = 0

    # 转成小时
    GetUseToolTimeDebugQuantity = GetUseToolTimeDebugQuantityTime / 3600
    GetUseToolTimeDebugQuantity = round(GetUseToolTimeDebugQuantity, 2)

    GetUseToolTimeTestQuantityTime = (Testdata.objects.filter(is_delete=False,
                                                            testEndTime__range=(start_date, end_date))
                                   .aggregate(GetUseToolTimeTestQuantityTime=Sum('testTime')))['GetUseToolTimeTestQuantityTime']
    if GetUseToolTimeTestQuantityTime == None:
        GetUseToolTimeTestQuantityTime = 0

    GetUseToolTimeTestQuantity = GetUseToolTimeTestQuantityTime / 3600
    GetUseToolTimeTestQuantity = round(GetUseToolTimeTestQuantity, 2)

    GetUseToolTimeQuantity = GetUseToolTimeDebugQuantity + GetUseToolTimeTestQuantity
    GetUseToolTimeQuantity = round(GetUseToolTimeQuantity, 2)

    data = {
        'GetUseToolTimeDebugQuantity':GetUseToolTimeDebugQuantity,#调试时间
        'GetUseToolTimeTestQuantity':GetUseToolTimeTestQuantity,#质检时间
        'GetUseToolTimeQuantity':GetUseToolTimeQuantity#总时间
    }

    return data