import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q

from application.debugreport import forms
from application.debugreport.models import Debug
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询分页数据
from utils.utils import uid


def DebugList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 查询数据
    query = Debug.objects.filter(is_delete=False)
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
        debug_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        debug_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        debug_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    # 遍历数据源
    result = []
    if len(debug_list) > 0:
        for item in debug_list:
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
                'product_module': item.product_module,
                'create_time': str(item.create_time.strftime('%Y-%m-%d')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d')) if item.create_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

# 根据ID查询详情
def DebugDetail(debug_id):
    # 根据ID查询
    debug = Debug.objects.filter(is_delete=False, id=debug_id).first()
    # 查询结果判空
    if not debug:
        return None

    # 声明结构体
    data = {
        'id': debug.id,
        'work_order': debug.work_order,
        'order_time': str(debug.order_time.strftime('%Y-%m-%d')),
        'client_name': debug.client_name,
        'shape': debug.shape,
        'product_name': debug.product_name,
        'product_count': debug.product_count,
        'submit_time': str(debug.submit_time.strftime('%Y-%m-%d')),
        'start_time': str(debug.start_time.strftime('%Y-%m-%d')),
        'finish_time': str(debug.finish_time.strftime('%Y-%m-%d')),
        'work_hours': debug.work_hours,
        'instruction': debug.instruction,
        'remark': debug.remark,
        'product_module': debug.product_module,
        'create_time': str(debug.create_time.strftime('%Y-%m-%d')),
        'update_time': str(debug.update_time.strftime('%Y-%m-%d')),
    }
    # 返回结果
    return data


def DebugAdd(request):
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
    form = forms.DebugForm(dict_data)
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
        product_module = form.cleaned_data.get('product_module')
        # 创建数据
        Debug.objects.create(
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
            product_module=product_module,
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
def DebugUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # ID
        debug_id = dict_data.get('id')
        # ID判空
        if not debug_id or int(debug_id) <= 0:
            return R.failed("ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.DebugForm(dict_data)
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
        # 成品/模块
        product_module = form.cleaned_data.get('product_module')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

 # 根据ID查询
    debug = Debug.objects.only('id').filter(id=debug_id, is_delete=False).first()
    # 查询结果判断
    if not debug:
        return R.failed("数据不存在")
# 对象赋值
    debug.work_order = work_order
    debug.order_time = order_time
    debug.client_name = client_name
    debug.shape = shape
    debug.product_name = product_name
    debug.product_count = product_count
    debug.submit_time = submit_time
    debug.start_time = start_time
    debug.finish_time = finish_time
    debug.work_hours = work_hours
    debug.instruction = instruction
    debug.remark = remark
    debug.product_module = product_module
    debug.update_user = uid(request)
    # 更新数据
    debug.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除
def DebugDelete(debug_id):
    # 记录ID为空判断
    if not debug_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = debug_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            debug = Debug.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not debug:
                return R.failed("数据不存在")
            # 设置删除标识
            debug.is_delete = True
            # 更新记录
            debug.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
