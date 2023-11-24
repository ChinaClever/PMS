from django.urls import path  # 导入路径相关配置

from application.debugdata import views


urlpatterns = [

    path('list', views.DebugDataListView.as_view()),

    path('detail/<int:debugdata_id>', views.DebugDataDetailView.as_view()),

    path('add', views.DebugDataAddView.as_view()),

    path('update', views.DebugDataUpdateView.as_view()),

    path('delete/<str:debugdata_id>', views.DebugDataDeleteView.as_view()),
]
