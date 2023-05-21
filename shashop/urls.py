from django.urls import path
from . import views
from .views import ProductCommentsAPIView

urlpatterns = [
    path('order/item/create/list/', views.OrderItemCreateAPIView.as_view()),

    path('order/create/list/', views.OrderCreateListAPIView.as_view()),
    path('order/update/delete/<int:pk>/', views.OrderRetrieveUpdateDestroyAPIView.as_view()),

    path('comment/list/create/', views.CommentListCreateAPIView.as_view()),
    path('comment/update/delete/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),

    path('like/list/create/', views.LikeListCreateAPIView.as_view()),
    path('like/update/delete/<int:pk>/', views.LikeRetrieveUpdateDestroyAPIView.as_view()),

    path('product/create/', views.ProductCreateAPIView.as_view()),
    path('product/list/', views.ProductListAPIView.as_view()),
    path('product/update/delete/<int:pk>/', views.ProductUpdateDeleteAPIView.as_view()),

    path('category/create/list/', views.CategoryCreateListAPIView.as_view()),

    path('favorites/list/create/', views.FavoritesListCreateAPIView.as_view()),
    path('Favorites/update/delete/<int:pk>/', views.FavoritesRetrieveUpdateDestroyAPIView.as_view()),

    path('products/<int:product_id>/comments/', ProductCommentsAPIView.as_view()),

]
