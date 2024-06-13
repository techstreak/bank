from django.urls import path
from .views import  show_links, user_logout, register, user_login, account_detail , AddBalanceView, send_money , users

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('account/', account_detail, name='account_detail'),
    path('add-balance/', AddBalanceView.as_view(), name='add_balance'),
    path('users/', users, name='users'),
    path('send-money/', send_money, name='send_money'),
    path('logout/', user_logout, name='logout'),  # Add this line
]

