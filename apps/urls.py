from django.urls import path

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('products/search/', views.search),
    path('products/<str:category_slug>/<str:product_slug>/',
         views.ProductDetail.as_view(), name='product-detail'),
    path('products/<str:category_slug>/',
         views.CategoryDetail.as_view(), name='category-detail'),
    path('checkout/', views.checkout),
    path('orders/', views.OrderList.as_view()),
]
