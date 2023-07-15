from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'subtasks'


router = DefaultRouter()
router.register('subtask', views.SubTaskModelViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
]
