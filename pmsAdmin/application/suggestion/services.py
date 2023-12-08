import json
import logging

from django.core.paginator import Paginator

from application.constants import NOTICE_SOURCE_LIST
from application.suggestion import forms
from application.suggestion.models import Suggestion
from config.env import IMAGE_URL
from constant.constants import PAGE_LIMIT
from utils import R, regular

from utils.utils import saveEditContent, uid

def SuggestionList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Suggestion.objects.filter(is_delete=False)
    # 提交者
    commit_user = request.GET.get('commit_user')
    if commit_user:
        query = query.filter(commit_user__contains=commit_user)
    # 类型
    type = request.GET.get('type')
    if type:
        query = query.filter(type=type)
    # 状态
    status = request.GET.get('status')
    if status:
        query = query.filter(status=status)
    #优先级
    priority = request.GET.get('priority')
    if priority:
        query = query.filter(priority=priority)
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
                'content': item.content,
                'commit_user': item.commit_user,
                'status': item.status,
                'feedback': item.feedback,
                'priority': item.priority,
                'type': item.type,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


def SuggestionAdd(request):
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
    form = forms.SuggestionForm(dict_data);
    if form.is_valid():
        # 提交人
        commit_user = form.cleaned_data.get('commit_user')
        # 类型
        type = form.cleaned_data.get('type')
        # 处理状态
        status = form.cleaned_data.get('status')
        # 优先级
        priority = form.cleaned_data.get('priority')
        # 内容
        content = form.cleaned_data.get('content')
        # 反馈
        feedback = form.cleaned_data.get('feedback')

        # 处理富文本内容
        content = saveEditContent(content, commit_user, "suggestion")
        feedback = saveEditContent(feedback, commit_user, "suggestion")

        # 创建数据
        Suggestion.objects.create(
            commit_user=commit_user,
            type=type,
            status=status,
            priority=priority,
            content=content,
            feedback=feedback,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

def SuggestionDetail(suggestion_id):
    # 根据ID查询通知公告
    suggestion = Suggestion.objects.filter(is_delete=False, id=suggestion_id).first()
    # 查询结果判空
    if not suggestion:
        return None

    # 声明结构体
    data = {
        'id': suggestion.id,
        'commit_user': suggestion.commit_user,
        'type': suggestion.type,
        'status': suggestion.status,
        'priority': suggestion.priority,
        'content': suggestion.content,
        'feedback': suggestion.feedback,
    }
    # 返回结果
    return data

def SuggestionUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 通知公告ID
        suggestion_id = dict_data.get('id')
        # 通知公告ID判空
        if not suggestion_id or int(suggestion_id) <= 0:
            return R.failed("通知公告ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.SuggestionForm(dict_data);
    if form.is_valid():
        # 提交人
        commit_user = form.cleaned_data.get('commit_user')
        # 类型
        type = form.cleaned_data.get('type')
        # 处理状态
        status = form.cleaned_data.get('status')
        # 优先级
        priority = form.cleaned_data.get('priority')
        # 内容
        content = form.cleaned_data.get('content')
        # 反馈
        feedback = form.cleaned_data.get('feedback')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询通知公告
    suggestion = Suggestion.objects.only('id').filter(id=suggestion_id, is_delete=False).first()
    # 查询结果判断
    if not suggestion:
        return R.failed("意见反馈不存在")
    if suggestion.content != content:
        status = 1;

    # 处理富文本内容
    content = saveEditContent(content, commit_user, "suggestion")
    feedback = saveEditContent(feedback, commit_user, "suggestion")

    # 对象赋值
    suggestion.commit_user = commit_user
    suggestion.type = type
    suggestion.priority = priority
    suggestion.status = status
    suggestion.feedback = feedback
    suggestion.content = content
    suggestion.update_user = uid(request)

    # 更新数据
    suggestion.save()
    # 返回结果
    return R.ok(msg="更新成功")

def SuggestionDelete(suggestion_id):
    # 记录ID为空判断
    if not suggestion_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = suggestion_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            suggestion = Suggestion.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not suggestion:
                return R.failed("意见反馈不存在")
            # 设置删除标识
            suggestion.is_delete = True
            # 更新记录
            suggestion.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
