from django.urls import path  # 导入路径相关配置
from application.analysis import views

# 模块路由
urlpatterns = [
    #获取维修数据
    path('RepairData', views.RepairDataView.as_view()),
    #获取维修总数量数据
    path('RepairnumberData', views.RepairnumberDataView.as_view()),
    #获取原因
    path('ResultData', views.ResultDataView.as_view()),
]