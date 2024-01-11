import errno
import json
import logging
import socket
import time

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from application.bind.module import services
from application.bind.product.models import ProductBind
from application.bind.module.models import Module
from constant.constants import PAGE_LIMIT
from utils import R, regular
from datetime import datetime


from utils.utils import uid

# udp 接收调试数据
# @csrf_exempt
# def receive_udp_data():
#     # 创建 UDP socket
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 
#     # 绑定 IP 地址和端口
#     ip_address = '0.0.0.0'  # 监听所有可用的网络接口
#     port = 1236  # 指定要监听的端口号
# 
#     try:
#         # 尝试绑定地址和端口
#         udp_socket.bind((ip_address, port))
#     except socket.error as e:
#         # 判断地址和端口被占用的错误码
#         if e.errno == errno.EADDRINUSE:
#             # 地址和端口被占用，执行处理操作（例如直接返回或其他处理）
#             return
#         else:
#             # 其他错误，抛出异常或执行其他错误处理
#             raise
#     buffer_size = 1024  # 缓冲区大小
#     try:
#         while True:
#             data, address = udp_socket.recvfrom(buffer_size)
#             json_data = data.decode()
#             # 将接收到的 JSON 数据解析为 Python 字典
#             dict_data = json.loads(json_data)
# 
#             softwareType = dict_data.get('softwareType')
#             productType = dict_data.get('productType')
#             productSN = dict_data.get('productSN')
#             macAddress = dict_data.get('macAddress')
#             result = dict_data.get('result')
#             softwareVersion = dict_data.get('softwareVersion')
#             work_order = dict_data.get('work_order')
#             companyName = dict_data.get('companyName')
#             protocolVersion = dict_data.get('protocolVersion')
#             testStartTime = dict_data.get('testStartTime')
#             testEndTime = dict_data.get('testEndTime')
#             testTime = dict_data.get('testTime')
#             module = dict_data.get('module')
# 
#             with transaction.atomic():
#                 # 创建数据
#                 product = Product.objects.create(
#                     softwareType=softwareType,
#                     productType=productType,
#                     productSN=productSN,
#                     macAddress=macAddress,
#                     result=result,
#                     softwareVersion=softwareVersion,
#                     work_order=work_order,
#                     companyName=companyName,
#                     protocolVersion=protocolVersion,
#                     testStartTime=testStartTime,
#                     testEndTime=testEndTime,
#                     testTime=testTime
#                 )
#                 # 获取 Debugdata 对象的 ID
#                 product_id = product.id
#                 # 存id和teststep数据
#                 for item in module:
#                     Module.objects.create(
#                         product_id=product_id,
#                         no=item.get('no'),
#                         name=item.get('name'),
#                         result=item.get('result'),
#                     )
#     finally:
#         udp_socket.close()

# 查询分页数据
def ProductList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 查询数据
    query = ProductBind.objects.filter(is_delete=False)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(module_SN__icontains=keyword)
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
        product_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        product_list = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        product_list = paginator.page(paginator.num_pages)
    # 遍历数据源
    result = []
    if len(product_list) > 0:
        for item in product_list:
            module_list = services.getModuleList(item.id)
            data = {
                'id': item.id,
                'key': item.goods_SN,
                'module': module_list,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

# 根据ID查询详情
def ProductDetail(product_id):
    # 根据ID查询
    product = ProductBind.objects.filter(is_delete=False, id=product_id).first()
    # 查询结果判空
    if not product:
        return None

    module_list = services.getModuleList(product_id)
    # 声明结构体
    data = {
        'id': product.id,
        'key': product.goods_SN,
        'module': module_list,
    }
    # 返回结果
    return data


@transaction.atomic
def ProductAdd(request):

    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)

        goods_SN = dict_data.get('goods_SN')
        module_SN = dict_data.get('module_SN')
        # 创建数据
        product = ProductBind.objects.create(
            goods_SN=goods_SN,
        )

        for item in module_SN:
            Module.objects.create(
            product_id=product.id,
            module_SN=item.get('module_SN'),
            )
        # 返回结果
        return R.ok(msg="创建成功")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        print(e)
        return R.failed("参数错误")


@transaction.atomic
def ProductUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # ID
        product_id = dict_data.get('id')
        # ID判空
        if not product_id or int(product_id) <= 0:
            return R.failed("ID不能为空")

        key = dict_data.get('key')
        module = dict_data.get('module')
        # 根据ID查询
        product = ProductBind.objects.only('id').filter(id=product_id, is_delete=False).first()

        # 查询结果判断
        if not product:
            return R.failed("数据不存在")
        # 对象赋值
        product.module_SN = key
        product.update_user = uid(request)
        product.update_time = datetime.now()


        # 更新数据
        product.save()
        # 更新testdata_teststep表
        Module.objects.filter(product_id=product_id).delete()
        for item in module:
            Module.objects.create(
            product_id=product.id,
            module_SN=item.get('key')
            )
        # 返回结果
        return R.ok(msg="更新成功")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        print(e)
        return R.failed("参数错误")


def ProductDelete(product_id):
    # 记录ID为空判断
    if not product_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = product_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源django_debugdata
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            tetdata = ProductBind.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not tetdata:
                return R.failed("数据不存在")
            # 设置删除标识
            tetdata.is_delete = True
            # 更新记录
            tetdata.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
