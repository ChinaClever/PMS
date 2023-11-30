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
from django.core.paginator import Paginator
from django.db.models import Q

from constant.constants import PAGE_LIMIT
from application.mac import forms
from application.mac.models import mac
from utils import R, regular


# 查询数据列表
def MacList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 分页查询
    query = mac.objects.filter(is_delete=False)
    # 角色名称模糊筛选
    keyword = request.GET.get('keyword')
    if keyword:
        query = query.filter(Q(name__contains=keyword) | Q(work_order=keyword))
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
                'name': item.name,
                'code': item.code,
                'serial_id':item.serial_id,
                'mac_address': item.mac_address,
                'create_time': str(item.create_time.strftime('%Y-%m-%d ')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d ')) if item.update_time else None,
            }
            # 加入数组对象
            result.append(data)
            # 返回结果
    return R.ok(data=result, count=count)


# 根据ID获取详情
def MacDetail(mac_id):
    # 根据ID查询客户
    user = mac.objects.filter(is_delete=False, id=mac_id).first()
    # 查询结果判空
    if not user:
        return None
    # 声明结构体
    data = {
        'id': user.id,
        'work_order': user.work_order,
        'name': user.name,
        'code': user.code,
        'serial_id': user.serial_id,
        'mac_address': user.mac_address,

    }
    # 返回结果
    return data


# 添加客户
def MacAdd(request):
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
    # 表单验证
    form = forms.MacForm(dict_data)
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 客户名称
        name = form.cleaned_data.get('name')
        # 产品类型
        code = form.cleaned_data.get('code')
        # 序列号
        serial_id = form.cleaned_data.get('serial_id')
        # mac地址
        mac_address = form.cleaned_data.get('mac_address')
        obj = mac.objects.filter(mac_address=mac_address)
        if obj:
            return R.failed('mac地址不能重复')
        # 创建数据
        else:
            mac.objects.create(
                work_order=work_order,
                name=name,
                code= code,
                serial_id=serial_id,
                mac_address=mac_address,
            )
            # 返回结果
            return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        print(err_msg)
        # 返回错误信息
        return R.failed(err_msg)


# 更新客户
def MacUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 客户ID
        mac_id = dict_data.get('id')
        # 客户ID判空
        if not mac_id or int(mac_id) <= 0:
            return R.failed("客户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.MacForm(dict_data)
    if form.is_valid():
        work_order = form.cleaned_data.get('work_order')
        # 客户名称
        name = form.cleaned_data.get('name')
        # 产品类型
        code = form.cleaned_data.get('code')
        # 序列号
        serial_id = form.cleaned_data.get('serial_id')
        # mac地址
        mac_address = form.cleaned_data.get('mac_address')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询客户
    user = mac.objects.only('id').filter(id=mac_id, is_delete=False).first()
    # 查询结果判断
    if not user:
        return R.failed("客户不存在")

    # 对象赋值
    user.work_order = work_order
    user.name = name
    user.code = code
    user.serial_id = serial_id
    user.mac_address= mac_address

    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")

# 删除客户
def MacDelete(mac_id):
    # 记录ID为空判断
    if not mac_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = mac_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            user = mac.objects.only('id').filter(id=int(id), is_delete=False).first()
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
