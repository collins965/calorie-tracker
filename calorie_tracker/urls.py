from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),               # Landing page
    path('login/', views.login_view, name="login"),         # ✅ Fixes /login/ redirect
    path('index/', views.index, name="index"),
    path('delete/<int:item_id>/', views.delete_item, name="delete_item"),
    path('signup/', views.signup_view, name="signup"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout_view, name='logout'),
]
