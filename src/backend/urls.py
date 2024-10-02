"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

from django.urls import path
from . import views

urlpatterns = [
    path('users/access/', views.users_access, name='users_access'),
    path('images/upload/', views.upload_image, name='upload_image'),
    path('images/cropping/', views.images_cropping, name='images_cropping'),
    path('videos/upload/', views.upload_video, name='upload_video'),
    path('videos/upload/count/', views.videos_count, name='videos_count'),
    path('videos/result/generate/', views.videos_generator, name='videos_generator'),
    path('videos/result/<str:user_token>/', views.videos_result, name='videos_result'),
    path('faces/count/', views.faces_count, name='faces_count'),
    path('faces/detect/', views.faces_detect, name='faces_detect'),
    path('faces/reenactment/<int:face_id>/', views.faces_reenactment, name='faces_reenactment'),
    path('environment/cleanup/', views.clean_up, name='clean_up'),
]
