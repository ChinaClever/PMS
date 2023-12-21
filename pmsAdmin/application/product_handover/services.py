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
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from constant.constants import PAGE_LIMIT
from application.product_handover import forms
from application.product_handover.models import product_handover
from utils import R, regular


# 查询客户数据列表
def Product_handoverList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = request.GET.get('limit')
    if limit:
        limit = int(request.GET.get('limit'))
    else:
        limit = 65535000;
    # 分页查询
    query = product_handover.objects.filter(is_delete=False)
    # 角色名称模糊筛选
    keyword = request.GET.get('keyword')
    if keyword:
        query = query.filter(Q(name__contains=keyword) | Q(work_order=keyword))

    # 筛选年月范围
    selectStartDate = request.GET.get('selectStartDate')
    selectEndDate = request.GET.get('selectEndDate')
    if selectStartDate and selectEndDate:
        start_date = datetime.strptime(selectStartDate, "%Y-%m-%d")
        end_date = datetime.strptime(selectEndDate, "%Y-%m-%d")
        query = query.filter(order_time__gte=start_date, order_time__lte=end_date)

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
                'time':str(item.time.strftime('%Y-%m-%d ')) if item.time else None,
                'work_order':item.work_order,
                'name': item.name,
                'code': item.code,
                'remark': item.remark,
                'delivery_time': str(item.delivery_time.strftime('%Y-%m-%d ')) if item.delivery_time else None,
                'quantity': item.quantity,
                'control_version': item.control_version,
                'execute_version': item.execute_version,
                'create_time': str(item.create_time.strftime('%Y-%m-%d ')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d ')) if item.update_time else None,
            }
            # 加入数组对象
            result.append(data)
            # 返回结果
    return R.ok(data=result, count=count)


# 根据ID获取详情
def Product_handoverDetail(product_handover_id):
    # 根据ID查询客户
    user = product_handover.objects.filter(is_delete=False, id=product_handover_id).first()
    # 查询结果判空
    if not user:
        return None
    # 声明结构体
    data = {
        'id': user.id,
        'time': str(user.time.strftime('%Y-%m-%d ')) if user.time else None,
        'work_order': user.work_order,
        'name': user.name,
        'code': user.code,
        'remark': user.remark,
        'delivery_time': str(user.delivery_time.strftime('%Y-%m-%d ')) if user.delivery_time else None,
        'quantity': user.quantity,
        'control_version':user.control_version,
        'execute_version': user.execute_version,
    }
    # 返回结果
    return data


# 添加客户
def Product_handoverAdd(request):
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
    # 日期
    time = dict_data.get('time')
    # 工单号
    work_order = dict_data.get('work_order')
    # 客户名称
    name = dict_data.get('name')
    # 规格型号
    code = dict_data.get('code')
    # 安数
    remark = dict_data.get('remark')
    # 交货日期
    delivery_time = dict_data.get('delivery_time')
    # 数量
    quantity = dict_data.get('quantity')
    # 主控板版本号
    control_version = dict_data.get('control_version')
    # 执行板版本号
    execute_version = dict_data.get('execute_version')
    # 创建数据
    product_handover.objects.create(
        time=time,
        work_order=work_order,
        name=name,
        code= code,
        remark=remark,
        delivery_time=delivery_time,
        quantity=quantity,
        control_version= control_version,
        execute_version= execute_version,
    )
    # 返回结果
    return R.ok(msg="创建成功")



# 更新客户
def Product_handoverUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 客户ID
        product_handover_id = dict_data.get('id')
        # 客户ID判空
        if not product_handover_id or int(product_handover_id) <= 0:
            return R.failed("客户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 日期
    time = dict_data.get('time')
    time = datetime.strptime(time, '%Y-%m-%d')


    # 单号
    work_order = dict_data.get('work_order')
    # 客户名称
    name = dict_data.get('name')
    # 规格型号
    code = dict_data.get('code')
    # 安数
    remark = dict_data.get('remark')
    # 交货日期
    delivery_time = dict_data.get('delivery_time')
    delivery_time = datetime.strptime(delivery_time, '%Y-%m-%d')
    # 数量
    quantity = dict_data.get('quantity')
    # 主控板版本号
    control_version = dict_data.get('control_version')
   # 执行板版本号
    execute_version = dict_data.get('execute_version')

    # 根据ID查询客户
    user = product_handover.objects.only('id').filter(id=product_handover_id, is_delete=False).first()
    # 查询结果判断
    if not user:
        return R.failed("客户不存在")

    current_time = datetime.now()
    # 对象赋值
    user.time = time
    user.work_order = work_order
    user.name = name
    user.code = code
    user.remark = remark
    user.delivery_time = delivery_time
    user. quantity =  quantity
    user.control_version = control_version
    user.execute_version = execute_version
    user.update_time = current_time

    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除客户
def Product_handoverDelete(product_handover_id):
    # 记录ID为空判断
    if not product_handover_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = product_handover_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            user = product_handover.objects.only('id').filter(id=int(id), is_delete=False).first()
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
