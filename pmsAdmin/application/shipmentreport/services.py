import logging
import json
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import transaction
from django.db.models import Q
from application.shipmentreport.models import Shipment
from application.shipmentreport.models import Product
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
@transaction.atomic
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
    # 将新的product_name存储到Product表中
    product_name_list= ProductNameList(request)
    if not product_name_list:
        return R.failed('无法获取产品名字列表')

    if product_name not in [item['value'] for item in product_name_list]:
        Product.objects.create(
            product_code=product_code,
            product_name=product_name,
            shape=shape,
            product_module=product_module,
        )

    return R.ok(msg="创建成功")


@transaction.atomic
def ShipmentReportUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # ID
        shipment_id = dict_data.get('id')
        # ID判空
        if not shipment_id or int(shipment_id) <= 0:
            return R.failed("ID不能为空")

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

        # 根据ID查询
        shipment = Shipment.objects.only('id').filter(id=shipment_id, is_delete=False).first()
        # 查询结果判断
        if not shipment:
            return R.failed("数据不存在")
        # 保存原先的product_code 方便更新product表
        origin_product_code = shipment.product_code
        # 对象赋值
        shipment.work_order = work_order
        shipment.client_name = client_name
        shipment.product_code = product_code
        shipment.product_name = product_name
        shipment.shape = shape
        shipment.order_date = order_date
        shipment.delivery_date = delivery_date
        shipment.finish_date = finish_date
        shipment.product_count = product_count
        shipment.SO_RQ_id = SO_RQ_id
        shipment.remark = remark
        shipment.product_module = product_module
        shipment.update_user = uid(request)
        shipment.save()
        # 更新product表 用原先的product_code查
        product = Product.objects.filter(is_delete=False, product_code=origin_product_code).first()
        # 查询结果判断
        if not product:
            return R.failed("product数据不存在")
        product.product_code = product_code
        product.product_name = product_name
        product.shape = shape
        product.product_module = product_module
        product.update_user = uid(request)
        product.save()
        # 返回结果
        return R.ok(msg="更新成功")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        print(e)
        return R.failed("参数错误")

def ShipmentReportDelete(shipment_id):
    if not shipment_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = shipment_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            shipment = Shipment.objects.only('id').filter(id=int(id), is_delete=False).first()
            if not shipment:
                return R.failed("数据不存在")
            # 设置删除标识
            shipment.is_delete = True
            # 更新记录
            shipment.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 根据产品编码查产品名称 规格
def SelectProdcutDetailByProductCode(product_code):
    product = Product.objects.filter(is_delete=False, product_code=product_code).first()
    if not product:
        return None

    data = {
        'id': product.id,
        'product_code': product.product_code,
        'product_name': product.product_name,
        'shape': product.shape,
        'product_module': product.product_module,
    }
    return data

# 获取所有产品名称
def ProductNameList(request):
    productNameList = Product.objects.filter(is_delete=False)
    result = []
    existing_names = set()  # 存储已存在的product_name值
    if len(productNameList) > 0:
        for item in productNameList:
            product_name = item.product_name
            if product_name not in existing_names:
                data = {
                    'value': product_name,
                }
                result.append(data)
                existing_names.add(product_name)
    # 返回结果
    return result


