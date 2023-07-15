from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'accounts'



router = DefaultRouter()
router.register('users', views.UserListModelViewSet, basename='user')


urlpatterns = [
    # Api Root
    path('', include(router.urls)),
    # Registration
    path('registration', views.RegistrationApiView.as_view(), name='registration'),
    # loging and get a token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name= 'login'),
    # loging out and deleting the token
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='logout'),
    
]




