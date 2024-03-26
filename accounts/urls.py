from django.urls import path
from . import views
from .views import LogoutView, DashboardView, MyOrdersView, OrderDetailView, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('change_password/', views.change_password, name='change_password'),
]