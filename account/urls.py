from django.urls import path
from . import views


urlpatterns = [
    path('user/create/', views.UserCreate.as_view()),
    path('user/login/', views.UserAuthorization.as_view()),
    path('user/logout/', views.UserLogout.as_view()),
]

