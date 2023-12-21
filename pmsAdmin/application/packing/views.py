from django.utils.decorators import method_decorator
from django.views import View

from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from utils import R
from . import services

@method_decorator(check_login, name='dispatch')
class PackingListView(PermissionRequired, View):
    permission_required = ('sys:packing:list',)
    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.PackingList(request)
        # 返回结果
        return result

# 查询详情
@method_decorator(check_login, name='dispatch')
class PackingDetailView(PermissionRequired, View):
    permission_required = ('sys:packing:detail',)
    def get(self, request, packing_id):
        # 调用查询职级详情服务方法
        data = services.PackingDetail(packing_id)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name='dispatch')
class PackingAddView(PermissionRequired, View):
    permission_required = ('sys:packing:add',)
    def post(self, request):
        result = services.PackingAdd(request)
        return result

@method_decorator(check_login, name="put")
class PackingUpdateView(PermissionRequired, View):
    permission_required = ('sys:packing:update',)
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新服务方法
        result = services.PackingUpdate(request)
        # 返回结果
        return result

@method_decorator(check_login, name="delete")
class PackingDeleteView(PermissionRequired, View):
    permission_required = ('sys:packing:delete',)
    def delete(self, request, packing_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除用户服务方法
        result = services.PackingDelete(packing_id)
        # 返回结果
        return result