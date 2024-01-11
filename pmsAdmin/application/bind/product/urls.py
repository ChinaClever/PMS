from django.urls import path  # 导入路径相关配置

from application.bind.product import views


urlpatterns = [

    path('list', views.ProductListView.as_view()),

    path('detail/<int:product_id>', views.ProductDetailView.as_view()),

    path('add', views.ProductAddView.as_view()),

    path('update', views.ProductUpdateView.as_view()),

    path('delete/<str:product_id>', views.ProductDeleteView.as_view()),

]
