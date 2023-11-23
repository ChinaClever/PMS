import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q

from application.weldingreport import forms
from application.weldingreport.models import Welding
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询分页数据
from utils.utils import uid


def WeldingList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 查询数据
    query = Welding.objects.filter(is_delete=False)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(client_name__icontains=keyword) |
            Q(product_name__icontains=keyword) |
            Q(work_order__icontains=keyword) |
            Q(shape__icontains=keyword)
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
        welding_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        welding_list = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        welding_list = paginator.page(paginator.num_pages)
    # 遍历数据源
    result = []
    if len(welding_list) > 0:
        for item in welding_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'order_time': str(item.order_time.strftime('%Y-%m-%d')),
                'client_name': item.client_name,
                'shape': item.shape,
                'product_name': item.product_name,
                'product_count': item.product_count,
                'submit_time': str(item.submit_time.strftime('%Y-%m-%d')),
                'start_time': str(item.start_time.strftime('%Y-%m-%d')),
                'finish_time': str(item.finish_time.strftime('%Y-%m-%d')),
                'work_hours': item.work_hours,
                'instruction': item.instruction,
                'remark': item.remark,
                'create_time': str(item.create_time.strftime('%Y-%m-%d')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d')) if item.create_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

# 根据ID查询详情
def WeldingDetail(welding_id):
    # 根据ID查询
    welding = Welding.objects.filter(is_delete=False, id=welding_id).first()
    # 查询结果判空
    if not welding:
        return None

    # 声明结构体
    data = {
        'id': welding.id,
        'work_order': welding.work_order,
        'order_time': str(welding.order_time.strftime('%Y-%m-%d')),
        'client_name': welding.client_name,
        'shape': welding.shape,
        'product_name': welding.product_name,
        'product_count': welding.product_count,
        'submit_time': str(welding.submit_time.strftime('%Y-%m-%d')),
        'start_time': str(welding.start_time.strftime('%Y-%m-%d')),
        'finish_time': str(welding.finish_time.strftime('%Y-%m-%d')),
        'work_hours': welding.work_hours,
        'instruction': welding.instruction,
        'remark': welding.remark,
        'create_time': str(welding.create_time.strftime('%Y-%m-%d')),
        'update_time': str(welding.update_time.strftime('%Y-%m-%d')),
    }
    # 返回结果
    return data


def WeldingAdd(request):
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
    form = forms.WeldingForm(dict_data)
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 下单日期
        order_time = form.cleaned_data.get('order_time')
        # 客户名称
        client_name = form.cleaned_data.get('client_name')
        # 规格型号
        shape = form.cleaned_data.get('shape')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 数量
        product_count = form.cleaned_data.get('product_count')
        # 交期
        submit_time = form.cleaned_data.get('submit_time')
        # 开始日期
        start_time = form.cleaned_data.get('start_time')
        # 完成日期
        finish_time = form.cleaned_data.get('finish_time')
        # 所用工时
        work_hours = form.cleaned_data.get('work_hours')
        # 具体说明
        instruction = form.cleaned_data.get('instruction')
        # 备注
        remark = form.cleaned_data.get('remark')
        # 创建数据
        Welding.objects.create(
            work_order=work_order,
            order_time=order_time,
            client_name=client_name,
            shape=shape,
            product_name=product_name,
            product_count=product_count,
            submit_time=submit_time,
            start_time=start_time,
            finish_time=finish_time,
            work_hours=work_hours,
            instruction=instruction if instruction else None,
            remark=remark if remark else None,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

# 更新
def WeldingUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # ID
        welding_id = dict_data.get('id')
        # ID判空
        if not welding_id or int(welding_id) <= 0:
            return R.failed("ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.WeldingForm(dict_data)
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 下单日期
        order_time = form.cleaned_data.get('order_time')
        # 客户名称
        client_name = form.cleaned_data.get('client_name')
        # 规格型号
        shape = form.cleaned_data.get('shape')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 数量
        product_count = form.cleaned_data.get('product_count')
        # 交期
        submit_time = form.cleaned_data.get('submit_time')
        # 开始日期
        start_time = form.cleaned_data.get('start_time')
        # 完成日期
        finish_time = form.cleaned_data.get('finish_time')
        # 所用工时
        work_hours = form.cleaned_data.get('work_hours')
        # 具体说明
        instruction = form.cleaned_data.get('instruction')
        # 备注
        remark = form.cleaned_data.get('remark')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

 # 根据ID查询
    welding = Welding.objects.only('id').filter(id=welding_id, is_delete=False).first()
    # 查询结果判断
    if not welding:
        return R.failed("数据不存在")
# 对象赋值
    welding.work_order = work_order
    welding.order_time = order_time
    welding.client_name = client_name
    welding.shape = shape
    welding.product_name = product_name
    welding.product_count = product_count
    welding.submit_time = submit_time
    welding.start_time = start_time
    welding.finish_time = finish_time
    welding.work_hours = work_hours
    welding.instruction = instruction
    welding.remark = remark
    welding.update_user = uid(request)
    # 更新数据
    welding.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除
def WeldingDelete(welding_id):
    # 记录ID为空判断
    if not welding_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = welding_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            welding = Welding.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not welding:
                return R.failed("数据不存在")
            # 设置删除标识
            welding.is_delete = True
            # 更新记录
            welding.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
