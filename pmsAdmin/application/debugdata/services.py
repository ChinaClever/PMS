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

from application.debugdata_teststep import services
from application.debugdata.models import Debugdata
from application.debugdata_teststep.models import DebugDataTestStep
from constant.constants import PAGE_LIMIT
from utils import R, regular


from utils.utils import uid

# udp 接收调试数据
# @csrf_exempt
def receive_udp_data():
    # 创建 UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定 IP 地址和端口
    ip_address = '0.0.0.0'  # 监听所有可用的网络接口
    port = 1234  # 指定要监听的端口号

    try:
        # 尝试绑定地址和端口
        udp_socket.bind((ip_address, port))
    except socket.error as e:
        # 判断地址和端口被占用的错误码
        if e.errno == errno.EADDRINUSE:
            # 地址和端口被占用，执行处理操作（例如直接返回或其他处理）
            return
        else:
            # 其他错误，抛出异常或执行其他错误处理
            raise
    buffer_size = 1024  # 缓冲区大小
    try:
        while True:
            data, address = udp_socket.recvfrom(buffer_size)
            json_data = data.decode()
            # 将接收到的 JSON 数据解析为 Python 字典
            dict_data = json.loads(json_data)

            softwareType = dict_data.get('softwareType')
            productType = dict_data.get('productType')
            productSN = dict_data.get('productSN')
            macAddress = dict_data.get('macAddress')
            result = dict_data.get('result')
            softwareVersion = dict_data.get('softwareVersion')
            clientName = dict_data.get('clientName')
            companyName = dict_data.get('companyName')
            protocolVersion = dict_data.get('protocolVersion')
            testStartTime = dict_data.get('testStartTime')
            testEndTime = dict_data.get('testEndTime')
            testTime = dict_data.get('testTime')
            testStep = dict_data.get('testStep')

            with transaction.atomic():
                # 创建数据
                debugdata = Debugdata.objects.create(
                    softwareType=softwareType,
                    productType=productType,
                    productSN=productSN,
                    macAddress=macAddress,
                    result=result,
                    softwareVersion=softwareVersion,
                    clientName=clientName,
                    companyName=companyName,
                    protocolVersion=protocolVersion,
                    testStartTime=testStartTime,
                    testEndTime=testEndTime,
                    testTime=testTime
                )
                # 获取 Debugdata 对象的 ID
                debugdata_id = debugdata.id
                # 存id和teststep数据
                for item in testStep:
                    DebugDataTestStep.objects.create(
                        debugdata_id=debugdata_id,
                        no=item.get('no'),
                        name=item.get('name'),
                        result=item.get('result'),
                    )
    finally:
        udp_socket.close()

# 查询分页数据
def DebugDataList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 查询数据
    query = Debugdata.objects.filter(is_delete=False)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(result__icontains=keyword) |
            Q(softwareType__icontains=keyword) |
            Q(productType__icontains=keyword)
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
        debugdata_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        debugdata_list = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        debugdata_list = paginator.page(paginator.num_pages)
    # 遍历数据源
    result = []
    if len(debugdata_list) > 0:
        for item in debugdata_list:
            testStep_list = services.getDebugDataTestStepList(item.id)
            data = {
                'id': item.id,
                'softwareType': item.softwareType,
                'productType': item.productType,
                'productSN': item.productSN,
                'macAddress': item.macAddress,
                'result': item.result,
                'softwareVersion': item.softwareVersion,
                'clientName': item.clientName,
                'companyName': item.companyName,
                'protocolVersion': item.protocolVersion,
                'testStartTime': str(item.testStartTime.strftime('%Y-%m-%d %H:%M:%S')) if item.testStartTime else None,
                'testEndTime': str(item.testEndTime.strftime('%Y-%m-%d %H:%M:%S')) if item.testEndTime else None,
                'testTime': item.testTime,
                'testStep': testStep_list,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

# 根据ID查询详情
def DebugDataDetail(debugdata_id):
    # 根据ID查询
    debugdata = Debugdata.objects.filter(is_delete=False, id=debugdata_id).first()
    # 查询结果判空
    if not debugdata:
        return None

    testStep_list = services.getDebugDataTestStepList(debugdata_id)
    # 声明结构体
    data = {
        'id': debugdata.id,
        'softwareType': debugdata.softwareType,
        'productType': debugdata.productType,
        'productSN': debugdata.productSN,
        'macAddress': debugdata.macAddress,
        'result': debugdata.result,
        'softwareVersion': debugdata.softwareVersion,
        'clientName': debugdata.clientName,
        'companyName': debugdata.companyName,
        'protocolVersion': debugdata.protocolVersion,
        'testStartTime': str(debugdata.testStartTime.strftime('%Y-%m-%d %H:%M:%S')) if debugdata.testStartTime else None,
        'testEndTime': str(debugdata.testEndTime.strftime('%Y-%m-%d %H:%M:%S')) if debugdata.testEndTime else None,
        'testTime': debugdata.testTime,
        'testStep': testStep_list,
    }
    # 返回结果
    return data

@transaction.atomic
def DebugDataAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)

        softwareType = dict_data.get('softwareType')
        productType = dict_data.get('productType')
        productSN = dict_data.get('productSN')
        macAddress = dict_data.get('macAddress')
        result = dict_data.get('result')
        softwareVersion = dict_data.get('softwareVersion')
        clientName = dict_data.get('clientName')
        companyName = dict_data.get('companyName')
        protocolVersion = dict_data.get('protocolVersion')
        testStartTime = dict_data.get('testStartTime')
        testEndTime = dict_data.get('testEndTime')
        testTime = dict_data.get('testTime')
        testStep = dict_data.get('testStep')
        # 创建数据
        debugdata = Debugdata.objects.create(
            softwareType=softwareType,
            productType=productType,
            productSN=productSN,
            macAddress=macAddress,
            result=result,
            softwareVersion=softwareVersion,
            clientName=clientName,
            companyName=companyName,
            protocolVersion=protocolVersion,
            testStartTime=testStartTime,
            testEndTime=testEndTime,
            testTime=testTime,
            create_user=uid(request)
        )
        # 存id和teststep数据
        if testStep:
            for item in testStep:
                DebugDataTestStep.objects.create(
                debugdata_id=debugdata.id,
                no=item.get('no'),
                name = item.get('name'),
                result = item.get('result'),
                )
        # 返回结果
        return R.ok(msg="创建成功")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        print(format(e))
        return R.failed("参数错误")

# 更新
@transaction.atomic
def DebugDataUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # ID
        debugdata_id = dict_data.get('id')
        # ID判空
        if not debugdata_id or int(debugdata_id) <= 0:
            return R.failed("ID不能为空")

        softwareType = dict_data.get('softwareType')
        productType = dict_data.get('productType')
        productSN = dict_data.get('productSN')
        macAddress = dict_data.get('macAddress')
        result = dict_data.get('result')
        softwareVersion = dict_data.get('softwareVersion')
        clientName = dict_data.get('clientName')
        companyName = dict_data.get('companyName')
        protocolVersion = dict_data.get('protocolVersion')
        testStartTime = dict_data.get('testStartTime')
        testEndTime = dict_data.get('testEndTime')
        testTime = dict_data.get('testTime')
        testStep = dict_data.get('testStep')
        # 根据ID查询
        debugdata = Debugdata.objects.only('id').filter(id=debugdata_id, is_delete=False).first()
        # 查询结果判断
        if not debugdata:
            return R.failed("数据不存在")
        # 对象赋值
        debugdata.softwareType = softwareType
        debugdata.productType = productType
        debugdata.productSN = productSN
        debugdata.macAddress = macAddress
        debugdata.result = result
        debugdata.softwareVersion = softwareVersion
        debugdata.clientName = clientName
        debugdata.companyName = companyName
        debugdata.protocolVersion = protocolVersion
        debugdata.testStartTime = testStartTime
        debugdata.testEndTime = testEndTime
        debugdata.testTime = testTime
        debugdata.update_user = uid(request)
        # 更新数据
        debugdata.save()
        # 更新debugdata_teststep表
        DebugDataTestStep.objects.filter(debugdata_id=debugdata_id).delete()
        for item in testStep:
            DebugDataTestStep.objects.create(
            debugdata_id=debugdata.id,
            no=item.get('no'),
            name = item.get('name'),
            result = item.get('result'),
            )
        # 返回结果
        return R.ok(msg="更新成功")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

# 删除（不删dabugdata_teststep表）
def DebugDataDelete(debugdata_id):
    # 记录ID为空判断
    if not debugdata_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = debugdata_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            debugdata = Debugdata.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not debugdata:
                return R.failed("数据不存在")
            # 设置删除标识
            debugdata.is_delete = True
            # 更新记录
            debugdata.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
