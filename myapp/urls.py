from django.urls import path
from . import views 

urlpatterns = [
  path("", views.index, name="index"),
  path("signup",views.signup,name="signup"),
  path("login",views.login_view,name="login"),
  path('logout',views.logout_view,name='logout' ),
  path('home/<str:id_string>/', views.home, name='home'),
  path('profile/<str:id_string>/', views.profile, name='profile'),
  path('affiliatecode/<str:id_string>/' ,views.affiliatecode,name="affiliatecode"),
  path('packages/<str:id_string>/',views.packages,name="packages"),
  path('earnings/<str:id_string>/',views.earnings,name="earnings"),
  path("withdraw/<str:id_string>/",views.withdraw,name="withdraw"),
  path("success", views.success, name="success"),
  path("confirmdetail",views.confirmdetail,name="comfirmdetail"),
  path('newpassword/<str:id_string>/',views.newpassword, name='newpassword'),
  path('basic/<str:id_string>/', views.basic, name='basic'),
  path('gold/<str:id_string>/', views.gold, name='gold'),
  path('checkout/<str:plan>/', views.checkout, name='checkout'),
  path('receipt/<str:user_id>/<int:amount>/<str:acc_no>/', views.receipt, name='receipt'),

]