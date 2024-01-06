
from django.urls import path
from . import views


urlpatterns=[
    path("",views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room',views.createroom,name="create-room"),
    path('update-room/<str:pk>/',views.updateroom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteroom,name="delete-room"),

    path('login/',views.login_page,name="login"),
    path('logout/',views.logoutuser,name="logout"),


]