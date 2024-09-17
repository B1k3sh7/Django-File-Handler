from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('retrieve/<int:pk>/', views.retrieve_content, name='retrieve_content'),
    path('modify/<int:pk>/', views.modify_content, name='modify_content'),
]
