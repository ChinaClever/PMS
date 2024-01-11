from django.urls import path  # 导入路径相关配置

from application.debugreport import views


urlpatterns = [
    path('list', views.DebugListView.as_view()),

    path('detail/<int:debug_id>', views.DebugDetailView.as_view()),

    path('add', views.DebugAddView.as_view()),

    path('update', views.DebugUpdateView.as_view()),

    path('delete/<str:debug_id>', views.DebugDeleteView.as_view()),
    # 查询统计维修报表柱状图
    path('listOf', views.DebugreportListOfTotalView1.as_view()),
    #查询调试看板表格数据
    path('listOf1', views.DebugreportListOf1TotalView1.as_view()),
]
