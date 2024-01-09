import json

from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import transaction
from django.db.models import Q
from application.packing.models import Packing
from application.testdata.models import Testdata
from constant.constants import PAGE_LIMIT
from utils import R
from utils.utils import uid

def PackingList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 查询数据
    query = Packing.objects.filter(is_delete=False)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(work_order__icontains=keyword) |
            Q(product_name__icontains=keyword) |
            Q(client_name__icontains=keyword)
        )
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
        productname_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        productname_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        productname_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    # 遍历数据源
    result = []
    if len(productname_list) > 0:
        for item in productname_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'client_name': item.client_name,
                'product_code': item.product_code,
                'product_name': item.product_name,
                'shape': item.shape,
                'order_date': str(item.order_date.strftime('%Y-%m-%d')),
                'delivery_date': str(item.delivery_date.strftime('%Y-%m-%d')),
                'packing_finish_time': str(item.packing_finish_time.strftime('%Y-%m-%d %H:%M:%S')) if item.packing_finish_time else None,
                'product_count': item.product_count,
                'remark': item.remark if item.remark else None,
                'SO_RQ_id': item.SO_RQ_id if item.SO_RQ_id else None,
                'product_module': item.product_module,
                'work_hours': item.work_hours,
                'packing_count': item.packing_count,
                'goods_SN': item.goods_SN
                         }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

def PackingDetail(packing_id):
    # 根据ID查询
    packing = Packing.objects.filter(is_delete=False, id=packing_id).first()
    # 查询结果判空
    if not packing:
        return None
    # 声明结构体
    data = {
        'id': packing.id,
        'work_order': packing.work_order,
        'client_name': packing.client_name,
        'product_code': packing.product_code,
        'product_name': packing.product_name,
        'shape': packing.shape,
        'order_date': str(packing.order_date.strftime('%Y-%m-%d')),
        'delivery_date': str(packing.delivery_date.strftime('%Y-%m-%d')),
        'product_count': packing.product_count,
        'SO_RQ_id': packing.SO_RQ_id,
        'product_module': packing.product_module,
        'remark': packing.remark if packing.remark else None,
        'packing_finish_time': str(packing.packing_finish_time.strftime('%Y-%m-%d %H:%M:%S')) if packing.packing_finish_time else None,
        'work_hours': packing.work_hours,
        'packing_count': packing.packing_count,
        'goods_SN': packing.goods_SN
    }
    # 返回结果
    return data

def PackingUpdate(request):
    # 接收请求参数
    json_data = request.body.decode()
    # 参数为空判断
    if not json_data:
        return R.failed("参数不能为空")
    # 数据类型转换
    dict_data = json.loads(json_data)

    id = dict_data.get('id')
    packing_finish_time = dict_data.get('packing_finish_time')
    work_hours = dict_data.get('work_hours')
    packing_count = dict_data.get('packing_count')
    goods_SN = dict_data.get('goods_SN')
    # 根据ID查询
    packing = Packing.objects.only('id').filter(id=id, is_delete=False).first()
    # 对象赋值
    packing.packing_finish_time = packing_finish_time
    packing.work_hours = work_hours
    packing.packing_count = packing_count
    packing.goods_SN = goods_SN
    packing.update_time = datetime.now()
    packing.update_user = uid(request)
    # 更新数据
    packing.save()
    # 返回结果
    return R.ok(msg="更新成功")

def PackingAdd(request):
    # 接收请求参数
    json_data = request.body.decode()
    # 参数为空判断
    if not json_data:
        return R.failed("参数不能为空")
        # 数据类型转换
    dict_data = json.loads(json_data)

    work_order = dict_data.get('work_order')
    client_name = dict_data.get('client_name')
    product_code = dict_data.get('product_code')
    product_module = dict_data.get('product_module')
    shape = dict_data.get('shape')
    order_date = dict_data.get('order_date')
    product_name = dict_data.get('product_name')
    delivery_date = dict_data.get('delivery_date')
    product_count = dict_data.get('product_count')
    SO_RQ_id = dict_data.get('SO_RQ_id')
    remark = dict_data.get('remark')
    packing_finish_time = dict_data.get('packing_finish_time')
    work_hours = dict_data.get('work_hours')
    packing_count = dict_data.get('packing_count')
    goods_SN = dict_data.get('goods_SN')
    Packing.objects.create(
        work_order=work_order,
        client_name = client_name,
        product_code = product_code,
        product_module = product_module,
        shape = shape,
        order_date = order_date,
        product_name = product_name,
        delivery_date =delivery_date,
        product_count = product_count,
        SO_RQ_id = SO_RQ_id,
        packing_finish_time = packing_finish_time,
        remark=remark if remark else None,
        work_hours = work_hours,
        packing_count = packing_count,
        goods_SN = goods_SN,
        create_user=uid(request)
    )

    # 返回结果
    return R.ok(msg="创建成功")

def PackingDelete(packing_id):
    # 记录ID为空判断
    if not packing_id:
        return R.failed("ID不存在")
    # 分裂字符串
    list = packing_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            packing = Packing.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not packing:
                return R.failed("数据不存在")
            # 设置删除标识
            packing.is_delete = True
            # 更新记录
            packing.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


def SNisRepeat(goods_SN):
    packing = Packing.objects.filter(is_delete=False, goods_SN=goods_SN).first()
    testdata = Testdata.objects.filter(is_delete=False, goods_SN=goods_SN).first()
    if packing:
        return R.failed("SN码" + goods_SN + "重复")
    elif not testdata:
        return R.ok(code=2, msg="SN码" + goods_SN + "未在测试数据内绑定")
    else:
        return R.ok(msg="验证通过")
