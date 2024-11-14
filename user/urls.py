from django.urls import path

from user.views import CreateUserView, LoginUserView

app_name = 'user'

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path('login/', LoginUserView.as_view(), name="taken_token"),
]