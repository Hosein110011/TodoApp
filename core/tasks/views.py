from rest_framework import viewsets
from .serializers import TaskListSerializer, CategorySerializer
from .models import Task, Category
from rest_framework.filters import SearchFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


""""Showing a list of each task's information in general and detail
"""
class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    lookup_field = 'id'


"""Showing a list of each categorie's information in general and detail
"""
class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'




