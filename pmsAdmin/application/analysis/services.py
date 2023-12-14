from application.shipmentreport.models import Shipment #出货统计--工单号查询
from application.inspectreport.models import Inspectreport #质检报表
from application.debugreport.models import Debug    #调试报表
from application.burning.models import burning #烧录报表
from application.repairreport.models import Dict #维修报表
from datetime import timedelta, datetime
from constant.constants import PAGE_LIMIT
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

from django.db.models import Sum
from utils import R, regular

# 根据工单查询所需要的数据
def DetailAll(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    shipmentReportS = Shipment.objects.filter(is_delete=False)
    if not shipmentReportS:
        return None
    data = set()
    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        shipmentReportS = shipmentReportS.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        shipmentReportS = shipmentReportS.order_by("-id")
    # 分页设置
    paginator = Paginator(shipmentReportS, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    try:
        shipmentReportS = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        shipmentReportS = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        shipmentReportS = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')

    if len(shipmentReportS) > 0:
        for shipmentReport in shipmentReportS:
            #查询所有的工单号
            workId = shipmentReport.work_order

            # 质检报表查询质检数量
            inspectReport = (Inspectreport.objects.filter(is_delete=False, work_order=workId)
                             .aggregate(inspectReport=Sum('examine_an_amount')))['inspectReport']
            if inspectReport == None:
                inspectReport = 0

            # 调试报表的调试数量
            debugReport = (Debug.objects.filter(is_delete=False, work_order=workId)
                        .aggregate(debugReport=Sum('product_count')))['debugReport']
            if debugReport == None:
                debugReport = 0

            # 烧录报表的数量
            burningReport = (burning.objects.filter(is_delete=False, work_order=workId)
                             .aggregate(burningReport=Sum('quantity')))['burningReport']
            if burningReport == None:
                burningReport = 0

            # 维修报表的数量
            repairReport = (Dict.objects.filter(is_delete=False, work_order=workId)
                            .aggregate(repairReport=Sum('bad_number')))['repairReport']
            if repairReport == None:
                repairReport = 0
            deliveryDate = shipmentReport.delivery_date.strftime("%Y-%m-%d")
            if deliveryDate == None:
                deliveryDate = 'None'

            startDate = shipmentReport.order_date.strftime("%Y-%m-%d")
            if startDate == None:
                startDate = 'None'


            Alldata = {
                'work_order_id': workId,
                'name': shipmentReport.client_name,
                'model': shipmentReport.shape,
                'deliveryDate': deliveryDate,
                'startDate': startDate,
                'endDate': shipmentReport.finish_date,
                'product_count':shipmentReport.product_count,

                'inspect_quantity':inspectReport, #质检数量
                'debug_quantity':debugReport, #调试数量
                'burning_quantity':burningReport,  #烧录数量
                'repair_quantity':repairReport,  #维修数量
            }
            data.add(tuple(Alldata.items()))
    SendData = [dict(item) for item in data]
    # print(f"根据工单查询所需要的数据{SendData}")
    return R.ok(data=SendData, count=count)

def getShipmentData():
    shipmentReportS = Shipment.objects.filter(is_delete=False)
    if not shipmentReportS:
        return None
    data = set()
    if len(shipmentReportS) > 0 or len(shipmentReportS) < 20:
        for shipmentReport in shipmentReportS:
            Alldata = {
                'name': shipmentReport.client_name,
                'product_count': shipmentReport.product_count,
            }
            data.add(tuple(Alldata.items()))
    SendData = [dict(item) for item in data]
    # print(SendData)
    return R.ok(data=SendData)