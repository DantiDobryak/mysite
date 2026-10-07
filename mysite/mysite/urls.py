from django.contrib import admin
from django.urls import path
from diary import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('knights/', views.get_knights, name='knights_list'),
    path('login/', views.user_login, name='login'),
    path('artifacts/', views.get_artifacts, name='artifacts'),
    path('admin/', admin.site.urls),
    path('api/artifacts/', views.ArtifactListAPIView.as_view(), name='api_artifact'),
    path('api/knights/', views.KnightListAPIView.as_view(), name='api_knight'),
]
