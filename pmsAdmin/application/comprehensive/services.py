from application.shipmentreport.models import Shipment #出货统计--工单号查询
from application.inspectreport.models import Inspectreport #质检报表
from application.debugreport.models import Debug    #调试报表
from application.burning.models import burning #烧录报表
from application.repairreport.models import Dict #维修报表
from datetime import timedelta, datetime
from constant.constants import PAGE_LIMIT
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from utils import R, regular

# 根据工单查询所需要的数据
def DetailAll(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    query = Shipment.objects.filter(is_delete=False)
    if not query:
        return R.failed("数据不存在")

    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by("-priority","-id")
    # 分页设置
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # # 分页查询
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

    data = []

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
                             .aggregate(burningReport=Sum('burning_quantity')))['burningReport']
            if burningReport == None:
                burningReport = 0

            # 维修报表的数量
            repair_bad_number = (Dict.objects.filter(is_delete=False, work_order=workId)
                            .aggregate(repairReport=Sum('bad_number')))['repairReport']
            if repair_bad_number == None:
                repair_bad_number = 0

            Alldata = {
                'work_order_id': workId,
                'name': shipmentReport.client_name,
                'model': shipmentReport.shape,
                'deliveryDate': str(shipmentReport.delivery_date.strftime('%Y-%m-%d')),
                'startDate': str(shipmentReport.order_date.strftime('%Y-%m-%d')),
                'endDate': str(shipmentReport.finish_date.strftime('%Y-%m-%d')) if shipmentReport.finish_date else None,
                'product_count':shipmentReport.product_count,

                'inspect_quantity':inspectReport, #质检数量
                'debug_quantity':debugReport, #调试数量
                'burning_quantity':burningReport,  #烧录数量
                'repair_quantity':repair_bad_number,  #维修数量
                'inspect_duration_days': shipmentReport.inspect_duration_days,  ## 质检所需天数
                'debug_duration_days': shipmentReport.debug_duration_days,  # 调试所需天数
                'burning_duration_days': shipmentReport.burning_duration_days,  # 烧录所需天数
            }
            data.append(Alldata)
    #         data.add(tuple(Alldata.items()))
    # SendData = [dict(item) for item in data]
    # print(f"根据工单查询所需要的数据{data}")
    return R.ok(data=data, count=count)

# 获取出货表的数据
def getShipmentData(request):
    today = timezone.now().date()
    start_date = today.replace(day=1)
    if start_date.month == 12:
        end_date = start_date.replace(day=1, month=1, year=start_date.year+1) - timezone.timedelta(days=1)
    else:
        end_date = start_date.replace(day=1, month=start_date.month+1) - timezone.timedelta(days=1)

    #按照范围时间来选择
    shipmentReportS = Shipment.objects.filter(is_delete=False, delivery_date__range=(start_date, end_date))
    if not shipmentReportS:
        return R.failed("数据不存在")
    data = []
    if len(shipmentReportS) > 0 or len(shipmentReportS) < 20:
        for shipmentReport in shipmentReportS:
            Alldata = {
                'name': shipmentReport.client_name,#客户名字
                'product_count': shipmentReport.product_count, #数量
            }
            data.append(Alldata)
    #         data.add(tuple(Alldata.items()))
    # SendData = [dict(item) for item in data]
    return R.ok(data=data)