import logging
import json
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q
from application.shipmentreport.models import Shipment
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询分页数据
from utils.utils import uid


def ShipmentReportList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 筛选成品 模块
    product_module = request.GET.get('product_module')
    # 查询数据(前端默认展示1成品)
    if product_module:
        query = Shipment.objects.filter(is_delete=False, product_module = product_module)
    else:
        query = Shipment.objects.filter(is_delete=False, product_module=1)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(client_name__icontains=keyword) |
            Q(product_name__icontains=keyword) |
            Q(product_code__icontains=keyword) |
            Q(work_order__icontains=keyword) |
            Q(SO_RQ_id__icontains=keyword)
        )
    # 筛选年份(前端默认展示当前年)
    year = request.GET.get('year')
    if year:
        query = query.filter(delivery_date__year=int(year))
    else:
        current_year = datetime.now().year
        query = query.filter(delivery_date__year=current_year)
    # 筛选月份(前端默认展示成品的一月份)
    month = request.GET.get('month')
    if month:
        query = query.filter(delivery_date__month=int(month))
    else:
        query = query.filter(delivery_date__month=1)

    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by("-id")
    # 分页设置
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    try:
        shipmentreport_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        shipmentreport_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        shipmentreport_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    # 遍历数据源
    result = []
    if len(shipmentreport_list) > 0:
        for item in shipmentreport_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'client_name': item.client_name,
                'product_code': item.product_code,
                'product_name': item.product_name,
                'shape': item.shape,
                'order_date': str(item.order_date.strftime('%Y-%m-%d')),
                'delivery_date': str(item.delivery_date.strftime('%Y-%m-%d')),
                'update_delivery_date': str(item.update_delivery_date.strftime('%Y-%m-%d')) if item.update_delivery_date else None,
                'finish_date': str(item.finish_date.strftime('%Y-%m-%d')) if item.finish_date else None,
                'product_count': item.product_count,
                'SO_RQ_id': item.SO_RQ_id if item.SO_RQ_id else None,
                'remark': item.remark if item.remark else None,
                'product_module': item.product_module,
                'attachment': item.attachment if item.attachment else None,
                'create_time': str(item.create_time.strftime('%Y-%m-%d')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d')) if item.create_time else None,

            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


def ShipmentReportDetail(shipment_id):
    # 根据ID查询
    shipment = Shipment.objects.filter(is_delete=False, id=shipment_id).first()
    # 查询结果判空
    if not shipment:
        return None
    # 声明结构体
    data = {
        'id': shipment.id,
        'work_order': shipment.work_order,
        'client_name': shipment.client_name,
        'product_code': shipment.product_code,
        'product_name': shipment.product_name,
        'shape': shipment.shape,
        'order_date': str(shipment.order_date.strftime('%Y-%m-%d')),
        'delivery_date': str(shipment.delivery_date.strftime('%Y-%m-%d')),
        'update_delivery_date': str(shipment.update_delivery_date.strftime('%Y-%m-%d')) if shipment.update_delivery_date else None,
        'finish_date': str(shipment.finish_date.strftime('%Y-%m-%d')) if shipment.finish_date else None,
        'product_count': shipment.product_count,
        'SO_RQ_id': shipment.SO_RQ_id,
        'remark': shipment.remark if shipment.remark else None,
        'product_module': shipment.product_module,
        'attachment': shipment.attachment if shipment.attachment else None,

    }
    # 返回结果
    return data

def ShipmentReportAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    work_order = dict_data.get('work_order')
    client_name = dict_data.get('client_name')
    product_code = dict_data.get('product_code')
    product_name = dict_data.get('product_name')
    shape = dict_data.get('shape')
    order_date = dict_data.get('order_date')
    delivery_date = dict_data.get('delivery_date')
    finish_date = dict_data.get('finish_date')
    product_count = dict_data.get('product_count')
    SO_RQ_id = dict_data.get('SO_RQ_id')
    remark = dict_data.get('remark')
    product_module = dict_data.get('product_module')
    # 创建数据
    Shipment.objects.create(
        work_order=work_order,
        client_name=client_name,
        product_code=product_code,
        product_name=product_name,
        shape=shape,
        order_date=order_date,
        delivery_date=delivery_date,
        finish_date=finish_date if remark else None,
        product_count=product_count,
        SO_RQ_id=SO_RQ_id,
        product_module=product_module,
        remark=remark if remark else None,
        create_user=uid(request)
        )
    # 返回结果
    return R.ok(msg="创建成功")
