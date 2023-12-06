from django.urls import path  # 导入路径相关配置
from application.workplace import views

# 模块路由
urlpatterns = [
    #获取总生产总数(模块和成品)，生产效率
    path('ShipmentAllQuantity', views.ShipmentAllView.as_view()),

    #获取总合格率
    path('AllPass', views.AllPassView.as_view()),

    #获取总的工具使用时长
    path('AllUseToolTime', views.AllUseToolTimeView.as_view()),

    #获取所有生产模块的数据
    path('AllModelsData', views.AllModelsDataView.as_view()),

    #获取所有生产成品的数据
    path('AllFinishedData', views.AllFinishedDataView.as_view()),

    #获取工具使用时长
    path('GetToolUseTime', views.GetToolUseTimeView.as_view()),
]