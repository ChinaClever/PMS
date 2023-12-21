from django.utils.decorators import method_decorator
from django.views import View

from config.env import DEBUG
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
    permission_required = ('sys:shipmentreport:detail',)

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

@method_decorator(check_login, name="dispatch")
class ShipmentReportUpdateView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:update',)
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新服务方法
        result = services.ShipmentReportUpdate(request)
        # 返回结果
        return result

@method_decorator(check_login, name="delete")
class ShipmentReportDeleteView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:delete',)
    def delete(self, request, shipment_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除用户服务方法
        result = services.ShipmentReportDelete(shipment_id)
        # 返回结果
        return result

# 获取全部工单号
@method_decorator(check_login, name='dispatch')
class WorkOrderListView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:list',)
    def get(self, request):
        # 调用查询职级分页数据服务方法
        data = services.WorkOrderList(request)
        # 返回结果
        return R.ok(data=data)

# 根据工单号查详情
@method_decorator(check_login, name='dispatch')
class ShipmentDetailView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:detail',)
    def get(self, request, work_order):
        # 调用查询职级详情服务方法
        data = services.SelectShipmentDetailByWorkOrder(work_order)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name='dispatch')
class ProductDetailView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:detail',)
    def get(self, request, product_code):
        # 调用查询职级详情服务方法
        data = services.SelectProdcutDetailByProductCode(product_code)
        # 返回结果
        return R.ok(data=data)


@method_decorator(check_login, name='dispatch')
class ProductListView(PermissionRequired, View):
    permission_required = ('sys:shipmentreport:list',)
    def get(self, request):
        # 调用查询职级分页数据服务方法
        data = services.ProductList(request)
        # 返回结果
        return R.ok(data=data)



# -----------------------产品名称模块-----------------------------------
#####################################################################
@method_decorator(check_login, name='dispatch')
class ProductNameListView(PermissionRequired, View):
    permission_required = ('sys:productname:list',)

    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.ProductNameList(request)
        # 返回结果
        return result

# 查询详情
@method_decorator(check_login, name='dispatch')
class ProductNameDetailView(PermissionRequired, View):
    permission_required = ('sys:productname:detail',)

    def get(self, request, product_id):
        # 调用查询职级详情服务方法
        data = services.ProductNameDetail(product_id)
        # 返回结果
        return R.ok(data=data)

@method_decorator(check_login, name='dispatch')
class ProductNameAddView(PermissionRequired, View):
    permission_required = ('sys:productname:add',)
    def post(self, request):
        result = services.ProductNameAdd(request)
        return result

@method_decorator(check_login, name="put")
class ProductNameUpdateView(PermissionRequired, View):
    permission_required = ('sys:productname:update',)
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新服务方法
        result = services.ProductNameUpdate(request)
        # 返回结果
        return result

@method_decorator(check_login, name="delete")
class ProductNameDeleteView(PermissionRequired, View):
    permission_required = ('sys:productname:delete',)
    def delete(self, request, product_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除用户服务方法
        result = services.ProductNameDelete(product_id)
        # 返回结果
        return result