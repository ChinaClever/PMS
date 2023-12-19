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

# 根据产品名称查询所需要的数据
def RepairData(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Dict.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        # sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = ("SELECT t1.id, t1.name, sum(t1.repair_number) AS repair_total, sum(t2.product_count) AS total "
               "FROM django_repairreport AS t1 "
               "Join django_shipmentreport AS t2 ON t1.name = t2.product_name "
               "WHERE t1.is_delete = 0 AND t2.is_delete=0 and t1.repair_time >= %s AND t1.repair_time <= %s AND t2.order_date >= %s AND t2.order_date <= %s "
               "GROUP BY name ")
        query = Dict.objects.raw(sql, [startTime, endTime,startTime, endTime])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        endTime = datetime.now().date()
        startTime = endTime - timedelta(days=365)

        sql = ("SELECT t1.id, t1.name, sum(t1.repair_number) AS repair_total, sum(t2.product_count) AS total "
               "FROM django_repairreport AS t1 "
               "Join django_shipmentreport AS t2 ON t1.name = t2.product_name "
               "WHERE t1.is_delete = 0 and t2.is_delete = 0 and t1.repair_time >= %s AND t1.repair_time <= %s AND t2.order_date >= %s AND t2.order_date <= %s "
               "GROUP BY name ")
        query = Dict.objects.raw(sql,[startTime,endTime,startTime, endTime])
        paginator = Paginator(query, limit)

    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0 and len(producerecord_list) < 20:
        for item in producerecord_list:
            item.rate = item.repair_total/item.total
            item.rate = round(item.rate,2)
            data = {
                'product_name': item.name,  #客户名
                'repair_total': item.repair_total,  #维修总数
                'total': item.total,  #产品总数量
                'rate': item.rate,   #百分比
            }
            result.append(data)
    # 返回结果
    print(f"{result}")
    return R.ok(data=result, count=count)


def ResultData(request):

    endTime = datetime.now().date()
    startTime = endTime-timedelta(days=365)
    if startTime and endTime:
        # sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = ("SELECT id, analysis, count(analysis) AS num "
               "FROM django_repairreport "
               "WHERE is_delete = 0  AND repair_time >= %s AND repair_time <= %s "
               "GROUP BY analysis ")
        query = Dict.objects.raw(sql, [startTime, endTime])

    else:
        sql =("SELECT id, analysis, count(analysis) AS num "
               "FROM django_repairreport "
               "WHERE is_delete = 0  "
               "GROUP BY analysis ")
        query = Dict.objects.raw(sql)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(query) > 0 :
        for item in query:
            data = {
                'name': item.analysis, #原因
                'value': item.num,  #数量
            }
            result.append(data)

    # 返回结果
    return R.ok(data=result)