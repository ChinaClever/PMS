from django.urls import path  # 导入路径相关配置
from application.comprehensive import views

# 模块路由
urlpatterns = [
    #获取所有数据
    path('DetailAll', views.DetailAllView.as_view()),

    path('ShipmentData', views.getShipmentDataView.as_view()),
]