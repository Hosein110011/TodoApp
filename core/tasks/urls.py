from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'tasks'


router = DefaultRouter()
router.register('task', views.TaskModelViewSet, basename='task')
router.register('category', views.CategoryModelViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
]
