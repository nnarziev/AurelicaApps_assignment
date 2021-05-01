from django.urls import path

from . import views

urlpatterns = [
    path('category/list', views.CategoriesView.as_view(), name="category_list"),
    path('category', views.ProductCategoryView.as_view(), name='product_category'),
    path('product/list', views.ProductsView.as_view(), name="products_list"),
    path('product/details', views.ProductView.as_view(), name="product_details"),
]
