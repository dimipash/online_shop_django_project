from django.urls import path
from . import views
from .views import LogoutView, DashboardView, MyOrdersView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]