from django.urls import path
from .views import home, sign_up, log_in, reciept, logout_view, otp,  forgottenpassword, setpassword, chat, article, article_details
from django.contrib.auth import views as auth_views
from .models import dashboard
app_name = "new"

urlpatterns = [
    path('', home, name="home"),
    path('signup/', sign_up, name="signup"),
    path('login/', log_in, name="login"),
    path('OTP/', otp, name="otp"),
    path('resetpassword/', setpassword, name="setpassword"),
    path('forgot-password/', forgottenpassword, name="forgotpassword"),
    path('Dashboard/', dashboard, name="dashboard"),
    path('logout/', logout_view, name="logout"),
    path('reciept/', reciept, name="reciept"),
    path('chat/', chat, name="chat"),
    path('article/', article, name="article"),
    path('article_detail/<int:ID>/', article_details, name="article_detail")
]