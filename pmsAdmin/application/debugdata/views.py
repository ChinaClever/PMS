
from django.utils.decorators import method_decorator
from django.views import View
from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from application.debugdata import services
from utils import R


# 查询数据
@method_decorator(check_login, name='dispatch')
class DebugDataListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:debugdata:list',)

    # POST查询分页数据
    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.DebugDataList(request)
        # 返回结果
        return result


# 查询详情
@method_decorator(check_login, name='dispatch')
class DebugDataDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:debugdata:detail',)

    # GET请求渲染HTML模板
    def get(self, request, debugdata_id):
        # 调用查询职级详情服务方法
        data = services.DebugDataDetail(debugdata_id)
        # 返回结果
        return R.ok(data=data)


# 添加
@method_decorator(check_login, name='dispatch')
class DebugDataAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:debugdata:add',)

    # 接收POST网络请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加职级服务
        result = services.DebugDataAdd(request)
        # 返回结果
        return result

# 更新
# @method_decorator(check_login, name="put")
# class DebugDataUpdateView(PermissionRequired, View):
#     # 方法权限标识
#     permission_required = ('sys:debugdata:update',)
#
#     # 接收PUT请求
#     def put(self, request):
#         if DEBUG:
#             return R.failed("演示环境，暂无操作权限")
#         # 调用更新服务方法
#         result = services.DebugDataUpdate(request)
#         # 返回结果
#         return result

# 删除
# @method_decorator(check_login, name="delete")
# class DebugDataDeleteView(PermissionRequired, View):
#     # 方法权限标识
#     permission_required = ('sys:debugdata:delete',)
#
#     # 接收DELETE请求
#     def delete(self, request, debugdata_id):
#         if DEBUG:
#             return R.failed("演示环境，暂无操作权限")
#         # 调用删除用户服务方法
#         result = services.DebugDataDelete(debugdata_id)
#         # 返回结果
#         return result
