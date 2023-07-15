from rest_framework import viewsets
from .serializers import UserListSerializer, RegistrationSerializer, CustomAuthTokenSerializer
from .models import User
from rest_framework import generics, mixins
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

"""This class is used to register and create serializer for a new user
""" 
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if  serializer.is_valid():
            serializer.save()
            data = {
                'email':serializer.validated_data['email']
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""""This class is created for loging in the user, creating a serializer along with a new token that is assigned to the user.
"""
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer._validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.id,
            'email':user.email
        })
    

"""Loging out / token cancellation
"""
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

""""Showing a list of each user's information in general and detail
"""
class UserListModelViewSet(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'base.html'
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    
