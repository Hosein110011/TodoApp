from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import SubTaskSerializer
from .models import SubTask


"""Showing a list of each subtasks's information in general and detail
"""
class SubTaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()
    lookup_field = 'id'

