import json
import logging

from django.core.paginator import Paginator

from application.constants import NOTICE_SOURCE_LIST
from application.inspectreport import forms
from application.inspectreport.models import Inspectreport
from application.user.services import UserDetail
from config.env import IMAGE_URL
from constant.constants import PAGE_LIMIT
from utils import R, regular
from django.db.models import Q
from datetime import datetime

from utils.utils import saveEditContent, uid

def InspectreportList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = request.GET.get("limit", PAGE_LIMIT)
    if limit:
        limit = int(limit)
    else:
        limit = 655350000
    # 实例化查询对象
    query = Inspectreport.objects.filter(is_delete=False)
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
                'examine_an_amount': item.examine_an_amount,
                'examine_a_bad_amount': item.examine_a_bad_amount,
                'examine_amount_total_amount': item.examine_amount_total_amount,
                'examine_bad_total_amount': item.examine_bad_total_amount,
                'target_pass_rate': item.target_pass_rate,
                'target_actual_pass_rate': item.target_actual_pass_rate,
                'signal': item.signal,
                'problems': item.problem,
                'actions': item.action,
                'work_hours':item.work_hours,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


def InspectreportAdd(request):
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
    form = forms.InspectreportForm(dict_data);
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
        # 检验数量
        examine_an_amount = form.cleaned_data.get('examine_an_amount')
        # 检验不良数量
        examine_a_bad_amount = form.cleaned_data.get('examine_a_bad_amount')
        # 检验数量累计
        examine_amount_total_amount = form.cleaned_data.get('examine_amount_total_amount')
        # 检验不良累计
        examine_bad_total_amount = form.cleaned_data.get('examine_bad_total_amount')
        # ERP目标合格率
        target_pass_rate = form.cleaned_data.get('target_pass_rate')
        if target_pass_rate:
            None
        else:
            target_pass_rate = 95
        # 问题
        problem = form.cleaned_data.get('problems')
        # 行动
        action = form.cleaned_data.get('actions')
        # 实际合格率
        target_actual_pass_rate = ((examine_amount_total_amount - examine_bad_total_amount) * 100) / examine_amount_total_amount
        # 信号
        signal = 2 if target_actual_pass_rate >= target_pass_rate else 1
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
        Inspectreport.objects.create(
            commit_user=UserDetail(uid(request)).get("realname"),
            product_name=product_name,
            work_order=work_order,
            product_module=product_module,
            start_time=start_time,
            end_time=end_time,
            item_number=item_number,
            examine_an_amount=examine_an_amount,
            examine_a_bad_amount=examine_a_bad_amount,
            examine_amount_total_amount=examine_amount_total_amount,
            examine_bad_total_amount=examine_bad_total_amount,
            target_pass_rate=target_pass_rate,
            target_actual_pass_rate=target_actual_pass_rate,
            signal=signal,
            problem=problem,
            action=action,
            work_hours=work_hours,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

def InspectreportDetail(Inspectreport_id):
    # 根据ID查询质检报表
    item = Inspectreport.objects.filter(is_delete=False, id=Inspectreport_id).first()
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
        'examine_an_amount': item.examine_an_amount,
        'examine_a_bad_amount': item.examine_a_bad_amount,
        'examine_amount_total_amount': item.examine_amount_total_amount,
        'examine_bad_total_amount': item.examine_bad_total_amount,
        'target_pass_rate': item.target_pass_rate,
        'target_actual_pass_rate': item.target_actual_pass_rate,
        'signal': item.signal,
        'problems': item.problem,
        'actions': item.action,
    }
    # 返回结果
    return data
#
def InspectreportUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 质检报表ID
        inspectreport_id = dict_data.get('id')
        # 质检报表ID判空
        if not inspectreport_id or int(inspectreport_id) <= 0:
            return R.failed("质检报表ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.InspectreportForm(dict_data);
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
        # 检验数量
        examine_an_amount = form.cleaned_data.get('examine_an_amount')
        # 检验不良数量
        examine_a_bad_amount = form.cleaned_data.get('examine_a_bad_amount')
        # 检验数量累计
        examine_amount_total_amount = form.cleaned_data.get('examine_amount_total_amount')
        # 检验不良累计
        examine_bad_total_amount = form.cleaned_data.get('examine_bad_total_amount')
        # ERP目标合格率
        target_pass_rate = form.cleaned_data.get('target_pass_rate')
        if target_pass_rate:
            None
        else:
            target_pass_rate = 95
        # 问题
        problem = form.cleaned_data.get('problems')
        # 行动
        action = form.cleaned_data.get('actions')
        # 实际合格率
        target_actual_pass_rate = ((examine_amount_total_amount - examine_bad_total_amount) * 100) / examine_amount_total_amount
        # 信号
        signal = 2 if target_actual_pass_rate >= target_pass_rate else 1
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
    inspectreport = Inspectreport.objects.only('id').filter(id=inspectreport_id, is_delete=False).first()
    # 查询结果判断
    if not inspectreport:
        return R.failed("质检报表不存在")

    # 对象赋值
    inspectreport.work_order = work_order
    inspectreport.product_module = product_module
    inspectreport.product_name = product_name
    inspectreport.start_time = start_time
    inspectreport.end_time = end_time
    inspectreport.item_number = item_number
    inspectreport.examine_an_amount = examine_an_amount
    inspectreport.examine_a_bad_amount = examine_a_bad_amount
    inspectreport.examine_amount_total_amount = examine_amount_total_amount
    inspectreport.examine_bad_total_amount = examine_bad_total_amount
    inspectreport.target_pass_rate = target_pass_rate
    inspectreport.target_actual_pass_rate = target_actual_pass_rate
    inspectreport.signal = signal
    inspectreport.problem = problem
    inspectreport.action = action
    inspectreport.work_hours = round((end_time - start_time).total_seconds() / 3600 + 0.5)
    inspectreport.update_user = uid(request)
    inspectreport.update_time = datetime.now()

    # 更新数据
    inspectreport.save()
    # 返回结果
    return R.ok(msg="更新成功")
#
def InspectreportDelete(Inspectreport_id):
    # 记录ID为空判断
    if not Inspectreport_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = Inspectreport_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            inspectreport = Inspectreport.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not inspectreport:
                return R.failed("意见反馈不存在")
            # 设置删除标识
            inspectreport.is_delete = True
            # 更新记录
            inspectreport.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))

def InspectreportListOfTotal(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Inspectreport.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        #sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,item_number, sum(examine_an_amount) AS total, sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= %s AND end_time <= %s GROUP BY item_number LIMIT %s"
        query = Inspectreport.objects.raw(sql,[startTime, endTime, limit])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        sql = "SELECT id,item_number, sum(examine_an_amount) AS total, sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 GROUP BY item_number LIMIT %s"
        query = Inspectreport.objects.raw(sql,[ limit])
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
                'examine_amount_total_amount': item.total,
                'examine_bad_total_amount': item.badtotal,
                'target_actual_pass_rate': item.target_actual_pass_rate,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)