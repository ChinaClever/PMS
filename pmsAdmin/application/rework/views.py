from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
import time

from application.constants import NOTICE_SOURCE_LIST
from application.rework import services
from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

# 渲染通知公告首页
from utils import R
@method_decorator(check_login, name="get")
class ReworkListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:rework:list",)

    # 接收GET请求
    def get(self, request):

        # 调用查询质检报表分页数据方法
        result = services.ReworkList(request)

        # 返回结果
        return result

@method_decorator(check_login, name="post")
class ReworkAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:rework:add",)

    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加质检报表服务方法
        result = services.ReworkAdd(request)
        # 返回结果
        return result

@method_decorator(check_login, name="get")
class ReworkDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:rework:detail",)

    # GET请求渲染HTML模板
    def get(self, request, Rework_id):
        # 调用查询质检报表详情服务方法
        data = services.ReworkDetail(Rework_id)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name="put")
class ReworkUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:rework:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新质检报表服务方法
        result = services.ReworkUpdate(request)
        # 返回结果
        return result

@method_decorator(check_login, name="delete")
class ReworkDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:suggestion:delete',)

    # 接收DELETE请求
    def delete(self, request, Rework_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除通知公告服务方法
        result = services.ReworkDelete(Rework_id)
        # 返回结果
        return result

@method_decorator(check_login, name="get")
class ReworkListOfTotalView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:rework:list",)

    # 接收GET请求
    def get(self, request):

        # 调用查询质检报表分页数据方法
        result = services.ReworkListOfTotal(request)

        # 返回结果
        return result