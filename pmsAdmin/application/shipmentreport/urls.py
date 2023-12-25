from django.urls import path
from application.shipmentreport import views

urlpatterns = [
    path('list', views.ShipmentReportListView.as_view()),

    path('details/<int:shipment_id>', views.ShipmentReportDetailView.as_view()),

    path('add', views.ShipmentReportAddView.as_view()),

    path('update', views.ShipmentReportUpdateView.as_view()),

    path('delete/<str:shipment_id>', views.ShipmentReportDeleteView.as_view()),
    # 获取所有工单号
    path('work_order/list', views.WorkOrderListView.as_view()),
    # 根据工单号查详情
    path('detail/<str:work_order>', views.ShipmentDetailView.as_view()),
    # 根据产品编码查产品详情
    path('product/detail/<str:product_code>', views.ProductDetailView.as_view()),
    # 获取所有产品名(不重复)
    path('product/list', views.ProductListView.as_view()),
    #  导入功能
    path('importfile', views.uploadFileView.as_view()),


    # 获取所有产品名称表的数据
    path('productname/list', views.ProductNameListView.as_view()),

    path('productname/detail/<int:product_id>', views.ProductNameDetailView.as_view()),

    path('productname/add', views.ProductNameAddView.as_view()),

    path('productname/update', views.ProductNameUpdateView.as_view()),

    path('productname/delete/<str:product_id>', views.ProductNameDeleteView.as_view()),
]
