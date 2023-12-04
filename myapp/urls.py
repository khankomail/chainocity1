from django.urls import path
from . import views 

urlpatterns = [
  path("", views.index, name="index"),
  path("signup",views.signup,name="signup"),
  path("login",views.login,name="login"),
  path("home",views.home,name="home"),
  path("profile",views.profile,name="profile"),
  path("affiliatecode",views.affiliatecode,name="affiliatecode"),
  path("packages",views.packages,name="packages"),
  path("earnings",views.earnings,name="earnings"),
  path("withdraw",views.withdraw,name="withdraw"),
  path("success",views.success,name="success"),
  path("confirmdetail",views.confirmdetail,name="comfirmdetail"),
  path("newpassword",views.newpassword,name="newpassword"),
]