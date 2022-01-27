from django.urls import path
from payment import views
app_name = 'payment'
urlpatterns = [
   path('store/checkout.html', views.CheckoutTemplateView.as_view(), name='checkout'),
]
