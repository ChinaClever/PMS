from django.urls import path  # 导入路径相关配置

from application.testdata import views


urlpatterns = [

    path('list', views.TestDataListView.as_view()),

    path('detail/<int:testdata_id>', views.TestDataDetailView.as_view()),

    path('add', views.TestDataAddView.as_view()),

    # path('update', views.DebugDataUpdateView.as_view()),
    #
    # path('delete/<str:debugdata_id>', views.DebugDataDeleteView.as_view()),
]
