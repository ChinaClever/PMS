from django.urls import path
from application.shipmentreport import views

urlpatterns = [
    path('list', views.ShipmentReportListView.as_view()),

    path('detail/<int:shipment_id>', views.ShipmentReportDetailView.as_view()),

    path('add', views.ShipmentReportAddView.as_view()),

    path('update', views.ShipmentReportUpdateView.as_view()),

    path('delete/<str:shipment_id>', views.ShipmentReportDeleteView.as_view()),
    # 获取全部工单号
    path('work_order/list', views.WorkOrderListView.as_view()),
    # 根据工单号查详情
    path('detail/<str:work_order>', views.ShipmentDetailView.as_view()),

    path('product/detail/<str:product_code>', views.ProductDetailView.as_view()),

    path('product/list', views.ProductListView.as_view()),

]
