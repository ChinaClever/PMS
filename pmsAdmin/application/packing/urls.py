from django.urls import path
from application.packing import views

urlpatterns = [
    path('list', views.PackingListView.as_view()),

    path('detail/<int:packing_id>', views.PackingDetailView.as_view()),

    path('add', views.PackingAddView.as_view()),

    path('update', views.PackingUpdateView.as_view()),

    path('delete/<str:packing_id>', views.PackingDeleteView.as_view()),
]
