from django.urls import path
from . import views

urlpatterns = [
    path('market/', views.market, name='market'),
    path('coin/<str:coin_id>/', views.coin_detail, name='coin_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
