# +----------------------------------------------------------------------
# | DjangoAdmin敏捷开发框架 [ 赋能开发者，助力企业发展 ]
# +----------------------------------------------------------------------
# | 版权所有 2021~2023 北京DjangoAdmin研发中心
# +----------------------------------------------------------------------
# | Licensed LGPL-3.0 DjangoAdmin并不是自由软件，未经许可禁止去掉相关版权
# +----------------------------------------------------------------------
# | 官方网站: https://www.djangoadmin.cn
# +----------------------------------------------------------------------
# | 作者: @一米阳光 团队荣誉出品
# +----------------------------------------------------------------------
# | 版权和免责声明:
# | 本团队对该软件框架产品拥有知识产权（包括但不限于商标权、专利权、著作权、商业秘密等）
# | 均受到相关法律法规的保护，任何个人、组织和单位不得在未经本团队书面授权的情况下对所授权
# | 软件框架产品本身申请相关的知识产权，禁止用于任何违法、侵害他人合法权益等恶意的行为，禁
# | 止用于任何违反我国法律法规的一切项目研发，任何个人、组织和单位用于项目研发而产生的任何
# | 意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其造成的损失 (包括但不限于直接、间接、
# | 附带或衍生的损失等)，本团队不承担任何法律责任，本软件框架禁止任何单位和个人、组织用于
# | 任何违法、侵害他人合法利益等恶意的行为，如有发现违规、违法的犯罪行为，本团队将无条件配
# | 合公安机关调查取证同时保留一切以法律手段起诉的权利，本软件框架只能用于公司和个人内部的
# | 法律所允许的合法合规的软件产品研发，详细声明内容请阅读《框架免责声明》附件；
# +----------------------------------------------------------------------

import json
import logging
import re
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from constant.constants import PAGE_LIMIT
from application.safety import forms
from application.safety.models import safety
from utils import R, regular


# 查询数据列表
def SafetyList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = request.GET.get('limit')
    if limit:
        limit = int(request.GET.get('limit'))
    else:
        limit = 65535000;
    # 分页查询
    query = safety.objects.filter(is_delete=False)
    # 角色名称模糊筛选
    keyword = request.GET.get('keyword')
    if keyword:
        query = query.filter(work_order=keyword)
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by('-id')
    # 分页设置
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 查询分页数据
    role_list = paginator.page(page)
    # 实例化返回对象
    result = []
    # 遍历数据源
    if len(role_list) > 0:
        for item in role_list:
            data = {
                'id': item.id,
                'work_order':item.work_order,
                'softwareType': item.softwareType,
                'productType': item.productType,
                'productSN':item.productSN,
                'Gnd':item.Gnd,
                'Ir':item.Ir,
                'Dcw':item.Dcw,
                'Acw':item.Acw,
                'result':item.result,
                'safety_address': item.safety_address,
                'create_time': str(item.create_time.strftime('%Y-%m-%d ')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d ')) if item.update_time else None,
            }
            # 加入数组对象
            result.append(data)
            # 返回结果
    return R.ok(data=result, count=count)


# 根据ID获取详情
def SafetyDetail(safety_id):
    # 根据ID查询客户
    user = safety.objects.filter(is_delete=False, id=safety_id).first()
    # 查询结果判空
    if not user:
        return None
    # 声明结构体
    data = {
                'id': user.id,
                'work_order':user.work_order,
                'softwareType': user.softwareType,
                'productType': user.productType,
                'productSN':user.productSN,
                'Gnd':user.Gnd,
                'Ir':user.Ir,
                'Dcw':user.Dcw,
                'Acw':user.Acw,
                'result':user.result,
                'safety_address': user.safety_address,
                'create_time': str(user.create_time.strftime('%Y-%m-%d ')) if user.create_time else None,
                'update_time': str(user.update_time.strftime('%Y-%m-%d ')) if user.update_time else None,

    }
    # 返回结果
    return data


# 添加客户
def SafetyAdd(request):
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
    softwareType = dict_data.get('softwareType')
    productType = dict_data.get('productType')
    productSN = dict_data.get('productSN')
    Gnd = dict_data.get('Gnd')
    Ir = dict_data.get('Ir')
    Dcw = dict_data.get('Dcw')
    Acw = dict_data.get('Acw')
    result = dict_data.get('result')
    softwareVersion = dict_data.get('softwareVersion')
    companyName = dict_data.get('companyName')
    protocolVersion = dict_data.get('protocolVersion')
    testStartTime = dict_data.get('testStartTime')
    testEndTime = dict_data.get('testEndTime')
    testTime = dict_data.get('testTime')

    safety.objects.create(
        work_order=work_order,
        softwareType=softwareType,
        productType= productType,
        productSN=productSN,
        Gnd=Gnd,
        Ir=Ir,
        Dcw=Dcw,
        Acw=Acw,
        result=result,
        softwareVersion=softwareVersion,
        companyName=companyName,
        protocolVersion=protocolVersion,
        testStartTime=testStartTime,
        testEndTime=testEndTime,
        testTime=testTime,
    )
    # 返回结果
    return R.ok(msg="创建成功")

# 更新客户
def SafetyUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 客户ID
        safety_id = dict_data.get('id')
        # 客户ID判空
        if not safety_id or int(safety_id) <= 0:
            return R.failed("客户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    work_order = dict_data.get('work_order')
    softwareType = dict_data.get('softwareType')
    productType = dict_data.get('productType')
    productSN = dict_data.get('productSN')
    Gnd = dict_data.get('Gnd')
    Ir = dict_data.get('Ir')
    Dcw = dict_data.get('Dcw')
    Acw = dict_data.get('Acw')
    result = dict_data.get('result')
    softwareVersion = dict_data.get('softwareVersion')
    companyName = dict_data.get('companyName')
    protocolVersion = dict_data.get('protocolVersion')
    testStartTime = dict_data.get('testStartTime')
    testEndTime = dict_data.get('testEndTime')
    testTime = dict_data.get('testTime')
    current_time = datetime.now()
    user = safety.objects.filter(id=safety_id,is_delete=False, ).first()
    if user:
        user.work_order = work_order
        user.softwareType = softwareType
        user.productType = productType
        user.productSN = productSN
        user.Gnd = Gnd
        user.Ir = Ir
        user.Dcw = Dcw
        user.Acw = Acw
        user.result = result
        user.softwareVersion = softwareVersion
        user.companyName = companyName
        user.protocolVersion = protocolVersion
        user.testStartTime = testStartTime
        user.testEndTime = testEndTime
        user.testTime = testTime

        user.update_time = current_time
    else:
        return R.failed('safety地址已经存在')


    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")

# 删除客户
def SafetyDelete(safety_id):
    # 记录ID为空判断
    if not safety_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = safety_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            user = safety.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not user:
                return R.failed("不存在")
            # 设置删除标识
            user.is_delete = True
            # 更新记录
            user.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
