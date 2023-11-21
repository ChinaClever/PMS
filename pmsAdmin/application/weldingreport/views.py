from django.utils.decorators import method_decorator
from django.views import View

from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from . import services
from utils import R

# 为全部请求方法添加装饰器
from .models import Welding


# 查询分页数据
# 为全部请求方法添加装饰器
@method_decorator(check_login, name='dispatch')
class WeldingListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:weldingreport:list',)

    # POST查询分页数据
    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.WeldingList(request)
        # 返回结果
        return result


# 查询详情
@method_decorator(check_login, name='dispatch')
class WeldingDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:weldingreport:detail',)

    # GET请求渲染HTML模板
    def get(self, request, welding_id):
        # 调用查询职级详情服务方法
        data = services.WeldingDetail(welding_id)
        # 返回结果
        return R.ok(data=data)


# 添加
@method_decorator(check_login, name='dispatch')
class WeldingAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:weldingreport:add',)

    # 接收POST网络请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加职级服务
        result = services.WeldingAdd(request)
        # 返回结果
        return result

# 更新
@method_decorator(check_login, name="put")
class WeldingUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:weldingreport:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新服务方法
        result = services.WeldingUpdate(request)
        # 返回结果
        return result

# 删除
@method_decorator(check_login, name="delete")
class WeldingDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:weldingreport:delete',)

    # 接收DELETE请求
    def delete(self, request, welding_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除用户服务方法
        result = services.WeldingDelete(welding_id)
        # 返回结果
        return result
