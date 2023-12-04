from django.utils.decorators import method_decorator
from django.views import View

from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from utils import R
from . import services


@method_decorator(check_login, name='dispatch')
class ShipmentReportListView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:list',)

    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.ShipmentReportList(request)
        # 返回结果
        return result

# 查询详情
@method_decorator(check_login, name='dispatch')
class ShipmentReportDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:shipmentreport:detail',)

    # GET请求渲染HTML模板
    def get(self, request, shipment_id):
        # 调用查询职级详情服务方法
        data = services.ShipmentReportDetail(shipment_id)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name='dispatch')
class ShipmentReportAddView(PermissionRequired, View):

    permission_required = ('sys:shipmentreport:add',)
    def post(self, request):

        result = services.ShipmentReportAdd(request)

        return result


@method_decorator(check_login, name='dispatch')
class ProductDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:shipmentreport:detail',)

    # GET请求渲染HTML模板
    def get(self, request, product_code):
        # 调用查询职级详情服务方法
        data = services.ProdcutDetail(product_code)
        # 返回结果
        return R.ok(data=data)


@method_decorator(check_login, name='dispatch')
class ProductListView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:list',)

    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.ProductList(request)
        # 返回结果
        return result