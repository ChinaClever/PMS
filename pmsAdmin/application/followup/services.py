import json
import logging

from django.core.paginator import Paginator

from application.constants import NOTICE_SOURCE_LIST
from application.followup import forms
from application.followup.models import Followup
from application.user.services import UserDetail
from config.env import IMAGE_URL
from constant.constants import PAGE_LIMIT
from utils import R, regular
from django.db.models import Q
from datetime import datetime

from utils.utils import saveEditContent, uid

def FollowupList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = request.GET.get("limit", PAGE_LIMIT)
    if limit:
        limit = int(limit)
    else:
        limit = 655350000
    # 实例化查询对象
    query = Followup.objects.filter(is_delete=False)
    # 按关键字查询
    keyword = request.GET.get('keyword')
    if keyword:
        query = query.filter(
            Q(commit_user__icontains=keyword) |  # commit_user字段包含关键字
            Q(item_number__icontains=keyword) |  # item_number字段包含关键字
            Q(work_order__icontains=keyword)  # work_order字段包含关键字
        )
    # 信号
    signal = request.GET.get('signal')
    if signal:
        query = query.filter(signal=signal)
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
                'start_time': str(item.start_time.strftime('%Y-%m-%d %H:%M')) if item.create_time else None,
                'end_time': str(item.end_time.strftime('%Y-%m-%d %H:%M')) if item.create_time else None,
                'commit_user': item.commit_user,
                'item_number': item.item_number,
                'qty_obj_hour': item.qty_obj_hour,
                'qty_prod_hour': item.qty_prod_hour,
                'cumul_qty_obj': item.cumul_qty_obj,
                'cumul_qty_prod': item.cumul_qty_prod,
                'loss_time': item.loss_time,
                'changeover_time': item.changeover_time,
                'signal': item.signal,
                'problems': item.problem,
                'actions': item.action,
                'remark':item.remark,
                'work_hours':item.work_hours,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


def FollowupAdd(request):
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
    form = forms.FollowupForm(dict_data);
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 成品/模块
        product_module = form.cleaned_data.get('product_module')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 开始时间
        start_time = form.cleaned_data.get('start_time')
        # 结束时间
        end_time = form.cleaned_data.get('end_time')
        # 产品型号
        item_number = form.cleaned_data.get('item_number')
        # ERP目标
        qty_obj_hour = form.cleaned_data.get('qty_obj_hour')
        # 实际产出
        qty_prod_hour = form.cleaned_data.get('qty_prod_hour')
        # ERP目标累计
        cumul_qty_obj = form.cleaned_data.get('cumul_qty_obj')
        # 实际累计
        cumul_qty_prod = form.cleaned_data.get('cumul_qty_prod')
        # 损耗工时
        loss_time = form.cleaned_data.get('loss_time')
        # 换线时间
        changeover_time = form.cleaned_data.get('changeover_time')
        # 问题
        problem = form.cleaned_data.get('problems')
        # 行动
        action = form.cleaned_data.get('actions')
        # 备注
        remark = form.cleaned_data.get('remark')
        # 信号
        signal = 2 if qty_prod_hour >= qty_obj_hour else 1
        # 创建数据
        selectedDate = dict_data.get("selectedDate")
        if selectedDate:
            # 提取 selectedDate 的年月日部分
            selectedDate_date = datetime.strptime(selectedDate, '%Y-%m-%d %H:%M')
            year = selectedDate_date.year
            month = selectedDate_date.month
            day = selectedDate_date.day

            # 提取 start_time 的时分秒部分
            hours = start_time.hour
            minutes = start_time.minute
            seconds = start_time.second

            # 拼接年月日和时分秒
            start_time = datetime(year, month, day, hours, minutes, seconds)

            # 提取 end_time 的时分秒部分
            hours = end_time.hour
            minutes = end_time.minute
            seconds = end_time.second

            # 拼接年月日和时分秒
            end_time = datetime(year, month, day, hours, minutes, seconds)
        work_hours = round((end_time - start_time).total_seconds() / 3600 + 0.5)
        Followup.objects.create(
            commit_user=UserDetail(uid(request)).get("realname"),
            product_name=product_name,
            work_order=work_order,
            product_module=product_module,
            start_time=start_time,
            end_time=end_time,
            item_number=item_number,
            qty_obj_hour=qty_obj_hour,
            qty_prod_hour=qty_prod_hour,
            cumul_qty_obj=cumul_qty_obj,
            cumul_qty_prod=cumul_qty_prod,
            loss_time=loss_time,
            changeover_time=changeover_time,
            signal=signal,
            problem=problem,
            action=action,
            work_hours=work_hours,
            remark=remark,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

def FollowupDetail(Followup_id):
    # 根据ID查询质检报表
    item = Followup.objects.filter(is_delete=False, id=Followup_id).first()
    # 查询结果判空
    if not item:
        return None

    # 声明结构体
    data = {
        'id': item.id,
        'work_order': item.work_order,
        'product_module': item.product_module,
        'product_name':item.product_name,
        'start_time': str(item.start_time.strftime('%Y-%m-%d %H:%M')) if item.create_time else None,
        'end_time': str(item.end_time.strftime('%Y-%m-%d %H:%M')) if item.create_time else None,
        'commit_user': item.commit_user,
        'item_number': item.item_number,
        'qty_obj_hour': item.qty_obj_hour,
        'qty_prod_hour': item.qty_prod_hour,
        'cumul_qty_obj': item.cumul_qty_obj,
        'cumul_qty_prod': item.cumul_qty_prod,
        'loss_time': item.loss_time,
        'changeover_time': item.changeover_time,
        'signal': item.signal,
        'problems': item.problem,
        'actions': item.action,
        'remark': item.remark
    }
    # 返回结果
    return data
#
def FollowupUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 质检报表ID
        followup_id = dict_data.get('id')
        # 质检报表ID判空
        if not followup_id or int(followup_id) <= 0:
            return R.failed("质检报表ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.FollowupForm(dict_data);
    if form.is_valid():
        # 工单号
        work_order = form.cleaned_data.get('work_order')
        # 成品/模块
        product_module = form.cleaned_data.get('product_module')
        # 产品名称
        product_name = form.cleaned_data.get('product_name')
        # 开始时间
        start_time = form.cleaned_data.get('start_time')
        # 结束时间
        end_time = form.cleaned_data.get('end_time')
        # 产品型号
        item_number = form.cleaned_data.get('item_number')
        # ERP目标
        qty_obj_hour = form.cleaned_data.get('qty_obj_hour')
        # 实际产出
        qty_prod_hour = form.cleaned_data.get('qty_prod_hour')
        # ERP目标累计
        cumul_qty_obj = form.cleaned_data.get('cumul_qty_obj')
        # 实际累计
        cumul_qty_prod = form.cleaned_data.get('cumul_qty_prod')
        # 损耗工时
        loss_time = form.cleaned_data.get('loss_time')
        # 换线时间
        changeover_time = form.cleaned_data.get('changeover_time')
        # 问题
        problem = form.cleaned_data.get('problems')
        # 行动
        action = form.cleaned_data.get('actions')
        # 备注
        remark = form.cleaned_data.get('remark')
        # 信号
        signal = 2 if qty_prod_hour >= qty_obj_hour else 1
        selectedDate = dict_data.get("selectedDate")
        if selectedDate:
            # 提取 selectedDate 的年月日部分
            selectedDate_date = datetime.strptime(selectedDate, '%Y-%m-%d %H:%M')
            year = selectedDate_date.year
            month = selectedDate_date.month
            day = selectedDate_date.day

            # 提取 start_time 的时分秒部分
            hours = start_time.hour
            minutes = start_time.minute
            seconds = start_time.second

            # 拼接年月日和时分秒
            start_time = datetime(year, month, day, hours, minutes, seconds)

            # 提取 end_time 的时分秒部分
            hours = end_time.hour
            minutes = end_time.minute
            seconds = end_time.second

            # 拼接年月日和时分秒
            end_time = datetime(year, month, day, hours, minutes, seconds)
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询通知公告
    followup = Followup.objects.only('id').filter(id=followup_id, is_delete=False).first()
    # 查询结果判断
    if not followup:
        return R.failed("质检报表不存在")

    # 对象赋值
    followup.work_order = work_order
    followup.product_module = product_module
    followup.product_name = product_name
    followup.start_time = start_time
    followup.end_time = end_time
    followup.item_number = item_number
    followup.qty_obj_hour = qty_obj_hour
    followup.qty_prod_hour = qty_prod_hour
    followup.cumul_qty_obj = cumul_qty_obj
    followup.cumul_qty_prod = cumul_qty_prod
    followup.loss_time = loss_time
    followup.changeover_time = changeover_time
    followup.signal = signal
    followup.problem = problem
    followup.action = action
    followup.remark = remark
    followup.work_hours = round((end_time - start_time).total_seconds() / 3600 + 0.5)
    followup.update_user = uid(request)
    followup.update_time = datetime.now()

    # 更新数据
    followup.save()
    # 返回结果
    return R.ok(msg="更新成功")
#
def FollowupDelete(Followup_id):
    # 记录ID为空判断
    if not Followup_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = Followup_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            followup = Followup.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not followup:
                return R.failed("记录不存在")
            # 设置删除标识
            followup.is_delete = True
            # 更新记录
            followup.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))

def FollowupListOfTotal(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Followup.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        #sql = 'SELECT item_number,sum(qty_obj_hour) AS total,sum(qty_prod_hour) AS badtotal FROM django_followup WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,item_number, sum(qty_obj_hour) AS total, sum(qty_prod_hour) AS badtotal FROM django_followup WHERE is_delete = 0 AND start_time >= %s AND end_time <= %s GROUP BY item_number LIMIT %s"
        query = Followup.objects.raw(sql,[startTime, endTime, limit])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        sql = "SELECT id,item_number, sum(qty_obj_hour) AS total, sum(qty_prod_hour) AS badtotal FROM django_followup WHERE is_delete = 0 GROUP BY item_number LIMIT %s"
        query = Followup.objects.raw(sql,[ limit])
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
            item.changeover_time = int(((item.total - item.badtotal) / item.total) * 100)
            data = {
                'id': item.id,
                'item_number': item.item_number,
                'cumul_qty_obj': item.total,
                'cumul_qty_prod': item.badtotal,
                'changeover_time': item.changeover_time,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)