from django.urls import path

from . import views
from . import consumers

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.signout, name="signout"),
    path("login/", views.signin, name="login"),
    path("signup/", views.signup, name="signup"),
    path('room/<pk>', views.room, name="room"),
]

websocket_url_patterns = [
    path('ws/chat/<room>/', consumers.ChatConsumer.as_asgi()),
]
