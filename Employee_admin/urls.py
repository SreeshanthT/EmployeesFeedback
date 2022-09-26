from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.login_view,name='login-page' ), 
    path('logout',views.logout_view,name='logout-page' ),
     
    path('',views.dashboard,name='dashboard' ),
]