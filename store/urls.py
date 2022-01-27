from django.urls import path
from store import views

app_name = 'store'
urlpatterns = [
    # path('home/', views.home, name='home'),
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
]
