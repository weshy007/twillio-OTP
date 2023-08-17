from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login/",views.login_view, name="login"),
    path("verifyNumber/",views.verify_number, name="verify-number"),
    path("verify/<str:phone_no>/",views.verify, name="verify"),

]