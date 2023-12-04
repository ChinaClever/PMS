from django.urls import path
from application.shipmentreport import views

urlpatterns = [
    path('list', views.ShipmentReportListView.as_view()),

    path('detail/<int:shipment_id>', views.ShipmentReportDetailView.as_view()),
    #
    path('add', views.ShipmentReportAddView.as_view()),
    #
    # path('update', views.ShipmentReportUpdateView.as_view()),
    #
    # path('delete/<str:welding_id>', views.ShipmentReportDeleteView.as_view()),

    path('product/detail/<str:product_code>', views.ProductDetailView.as_view()),

    path('product/list', views.ProductListView.as_view()),

]
