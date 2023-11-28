from django.utils.decorators import method_decorator
from django.views import View

from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from . import services


@method_decorator(check_login, name='dispatch')
class ShipmentReportListView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:list',)

    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.ShipmentReportList(request)
        # 返回结果
        return result

