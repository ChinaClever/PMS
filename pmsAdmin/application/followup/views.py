from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
import time

from application.constants import NOTICE_SOURCE_LIST
from application.followup import services
from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

# 渲染通知公告首页
from utils import R
@method_decorator(check_login, name="get")
class FollowupListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:followup:list",)

    # 接收GET请求
    def get(self, request):

        # 调用查询质检报表分页数据方法
        result = services.FollowupList(request)

        # 返回结果
        return result

@method_decorator(check_login, name="post")
class FollowupAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:followup:add",)

    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加质检报表服务方法
        result = services.FollowupAdd(request)
        # 返回结果
        return result

@method_decorator(check_login, name="get")
class FollowupDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:followup:detail",)

    # GET请求渲染HTML模板
    def get(self, request, Followup_id):
        # 调用查询质检报表详情服务方法
        data = services.FollowupDetail(Followup_id)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name="put")
class FollowupUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:followup:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新质检报表服务方法
        result = services.FollowupUpdate(request)
        # 返回结果
        return result

@method_decorator(check_login, name="delete")
class FollowupDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:suggestion:delete',)

    # 接收DELETE请求
    def delete(self, request, Followup_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除通知公告服务方法
        result = services.FollowupDelete(Followup_id)
        # 返回结果
        return result

@method_decorator(check_login, name="get")
class FollowupListOfTotalView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:followup:list",)

    # 接收GET请求
    def get(self, request):

        # 调用查询质检报表分页数据方法
        result = services.FollowupListOfTotal(request)

        # 返回结果
        return result