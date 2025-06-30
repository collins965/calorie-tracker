from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),                               # Landing + tracking view
    path('login/', views.login_view, name="login"),                    # Login page
    path('signup/', views.signup_view, name="signup"),                 # Signup page
    path('dashboard/', views.dashboard_view, name="dashboard"),        # User dashboard
    path('home/', views.home_view, name="home"),                       # Redirect to index
    path('logout/', views.logout_view, name='logout'),                 # Logout
    path('delete/<int:item_id>/', views.delete_item, name="delete_item"),  # Delete item
    path('edit/<int:item_id>/', views.edit_item, name="edit_item"),        # Edit item
]
