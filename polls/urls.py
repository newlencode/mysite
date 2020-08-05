from django.urls import path,include
from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login',views.login),
    path('register',views.register),
    path('logout', views.logout),
    path('captcha/', include('captcha.urls')),
    path('confirm/', views.user_confirm),
]
