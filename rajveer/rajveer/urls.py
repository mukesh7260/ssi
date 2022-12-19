
from django.contrib import admin
from django.urls import path
from rajapp import views
from rajapp.serializers import EmployeeSerializer , ProductSerializer 
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView

router = DefaultRouter()
router.register('register',views.RegisterViewset,basename='register')
router.register('table',views.EmployeeView,basename='table')
router.register('product',views.ProductView, basename='product')
router.register('login', views.LogiViewset,basename='login')


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', views.login),
    #path('logout/', views.logout),
   # path('register/',views.register),
  #  path('factauth/',views.ValidatePhoneSendOTP.as_view()),
   # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verifyotp/',views.VerifyOtpViewSet.as_view(),name = 'verify_otp'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    path("logout/",views.LogoutAPIView.as_view(), name="logout_view"),
    path("logoutt/",views.LogoutApiview.as_view(), name="logout_view"),
    path("cpassword/",views.ChangePasswordView.as_view, name = "change_password"),

    
]+router.urls
