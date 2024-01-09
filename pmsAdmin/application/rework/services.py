import json
import logging

from django.core.paginator import Paginator

from application.constants import NOTICE_SOURCE_LIST
from application.rework import forms
from application.rework.models import Rework
from application.user.services import UserDetail
from config.env import IMAGE_URL
from constant.constants import PAGE_LIMIT
from utils import R, regular
from django.db.models import Q
from datetime import datetime

from utils.utils import saveEditContent, uid

def ReworkList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = request.GET.get("limit", PAGE_LIMIT)
    if limit:
        limit = int(limit)
    else:
        limit = 655350000
    # 实例化查询对象
    query = Rework.objects.filter(is_delete=False)
    # 按关键字查询
    keyword = request.GET.get('keyword')
    if keyword:
        query = query.filter(
            Q(item_number__icontains=keyword) |  # item_number字段包含关键字
            Q(work_order__icontains=keyword)  # work_order字段包含关键字
        )
    # 返工原因
    rw_reason = request.GET.get('rw_reason')
    if rw_reason:
        query = query.filter(rw_reason=rw_reason)
    # 时间
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        query = query.filter(start_time__gte=startTime).filter(start_time__lte=endTime)
    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by("-id")

    # 设置分页
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0:
        for item in producerecord_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'product_name' : item.product_name,
                'product_module' : item.product_module,
                'respon': item.respon,
                'item_number': item.item_number,
                'rw_qty': item.rw_qty,
                'loss_material_qty': item.loss_material_qty,
                'loss_material_name': item.loss_material_name,
                'rw_reason': item.rw_reason,
                'loss_time':item.loss_time,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


def ReworkAdd(request):
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
    form = forms.ReworkForm(dict_data);
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 责任归属人
        respon = form.cleaned_data.get('respon')
        # 成品/模块
        product_module = form.cleaned_data.get('product_module')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 产品型号
        item_number = form.cleaned_data.get('item_number')
        # 返工数量
        rw_qty = form.cleaned_data.get('rw_qty')
        # 损耗材料数量
        loss_material_qty = form.cleaned_data.get('loss_material_qty')
        # 损耗材料名称
        loss_material_name = form.cleaned_data.get('loss_material_name')
        # 返工原因
        rw_reason = form.cleaned_data.get('rw_reason')
        # 损耗工时
        loss_time = form.cleaned_data.get('loss_time')

        Rework.objects.create(
            product_name=product_name,
            respon=respon,
            work_order=work_order,
            product_module=product_module,
            item_number=item_number,
            rw_qty=rw_qty,
            loss_material_qty=loss_material_qty,
            loss_material_name=loss_material_name,
            rw_reason=rw_reason,
            loss_time=loss_time,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

def ReworkDetail(Rework_id):
    # 根据ID查询质检报表
    item = Rework.objects.filter(is_delete=False, id=Rework_id).first()
    # 查询结果判空
    if not item:
        return None

    # 声明结构体
    data = {
        'id': item.id,
        'work_order': item.work_order,
        'product_name' : item.product_name,
        'product_module' : item.product_module,
        'respon': item.respon,
        'item_number': item.item_number,
        'rw_qty': item.rw_qty,
        'loss_material_qty': item.loss_material_qty,
        'loss_material_name': item.loss_material_name,
        'rw_reason': item.rw_reason,
        'loss_time':item.loss_time,
    }
    # 返回结果
    return data
#
def ReworkUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 质检报表ID
        rework_id = dict_data.get('id')
        # 质检报表ID判空
        if not rework_id or int(rework_id) <= 0:
            return R.failed("质检报表ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.ReworkForm(dict_data);
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 责任归属人
        respon = form.cleaned_data.get('respon')
        # 成品/模块
        product_module = form.cleaned_data.get('product_module')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 产品型号
        item_number = form.cleaned_data.get('item_number')
        # 返工数量
        rw_qty = form.cleaned_data.get('rw_qty')
        # 损耗材料数量
        loss_material_qty = form.cleaned_data.get('loss_material_qty')
        # 损耗材料名称
        loss_material_name = form.cleaned_data.get('loss_material_name')
        # 返工原因
        rw_reason = form.cleaned_data.get('rw_reason')
        # 损耗工时
        loss_time = form.cleaned_data.get('loss_time')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询通知公告
    rework = Rework.objects.only('id').filter(id=rework_id, is_delete=False).first()
    # 查询结果判断
    if not rework:
        return R.failed("质检报表不存在")

    # 对象赋值
    rework.work_order = work_order
    rework.respon = respon
    rework.product_module = product_module
    rework.product_name = product_name
    rework.loss_time = loss_time
    rework.item_number = item_number
    rework.rw_qty = rw_qty
    rework.loss_material_qty = loss_material_qty
    rework.loss_material_name = loss_material_name
    rework.rw_reason = rw_reason
    rework.update_user = uid(request)
    rework.update_time = datetime.now()

    # 更新数据
    rework.save()
    # 返回结果
    return R.ok(msg="更新成功")
#
def ReworkDelete(Rework_id):
    # 记录ID为空判断
    if not Rework_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = Rework_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            rework = Rework.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not rework:
                return R.failed("意见反馈不存在")
            # 设置删除标识
            rework.is_delete = True
            # 更新记录
            rework.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))

def ReworkListOfTotal(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Rework.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        #sql = 'SELECT item_number,sum(rw_qty) AS total,sum(loss_material_qty) AS badtotal FROM django_rework WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,item_number, sum(rw_qty) AS total, sum(loss_material_qty) AS badtotal FROM django_rework WHERE is_delete = 0 AND start_time >= %s AND end_time <= %s GROUP BY item_number LIMIT %s"
        query = Rework.objects.raw(sql,[startTime, endTime, limit])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        sql = "SELECT id,item_number, sum(rw_qty) AS total, sum(loss_material_qty) AS badtotal FROM django_rework WHERE is_delete = 0 GROUP BY item_number LIMIT %s"
        query = Rework.objects.raw(sql,[ limit])
        paginator = Paginator(query, limit)

    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0:
        for item in producerecord_list:
            item.target_actual_pass_rate = int(((item.total - item.badtotal) / item.total) * 100)
            data = {
                'id': item.id,
                'item_number': item.item_number,
                'loss_material_name': item.total,
                'examine_bad_total_amount': item.badtotal,
                'target_actual_pass_rate': item.target_actual_pass_rate,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)