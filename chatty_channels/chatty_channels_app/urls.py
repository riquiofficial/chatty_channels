from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.signout, name="signout"),
    path("login/", views.signin, name="login"),
    path("signup/", views.signup, name="signup")
]