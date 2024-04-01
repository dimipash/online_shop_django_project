from django.urls import path
from . import views
from .views import LogoutView, DashboardView, MyOrdersView, RegisterView, LoginView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),    
    path('my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),    
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]