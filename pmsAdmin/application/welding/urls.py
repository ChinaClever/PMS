from django.urls import path  # 导入路径相关配置

from application.welding import views


urlpatterns = [
    path('list', views.WeldingListView.as_view()),

    path('detail/<int:welding_id>', views.WeldingDetailView.as_view()),

    path('add', views.WeldingAddView.as_view()),

    path('update', views.WeldingUpdateView.as_view()),

    path('delete/<str:welding_id>', views.WeldingDeleteView.as_view()),
]
