from rest_framework import serializers
from .models import User
from tasks.models import Task
from collections import OrderedDict
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _




class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255 ,write_only = True)
    class Meta:
        model = User
        fields = ['email', 'password', 'password1']
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail':'password doesnt match.'})
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        return super().validate(attrs)
        
    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)
        """We use the same function that we created in user management to save validated user information"""

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Emaill"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class UserListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_abs_url')
    tasks = serializers.SerializerMethodField(method_name='get_tasks')
    completed = serializers.SerializerMethodField(method_name='get_completed')
    completed_tasks = serializers.SerializerMethodField(method_name='get_is_completed')
    not_completed = serializers.SerializerMethodField(method_name='get_not_completed')
    class Meta:
        model = User
        fields = ['id','email', 'tasks','completed_tasks','not_completed','url','completed','created_time', 'updated_time']
        read_only_fields = ['tasks']

    def to_representation(self, instance):
        request = self.context.get('request')        
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('id'):
            if rep['tasks'] == None:
                rep.pop('tasks', None)
            elif rep['completed_tasks'] == None:
                rep.pop('completed_tasks', None)
            elif rep['not_completed'] == None:
                rep.pop('not_completed', None)
            rep.pop('url', None)
        else:
            rep.pop('tasks', None)
            rep.pop('num_of_completed', None)
            rep.pop('completed_tasks', None)
            rep.pop('not_completed', None)
        return rep

    
    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.id)
    
    
    def get_tasks(self, obj):
        if Task.objects.filter(user=obj).exists():
            return Task.objects.filter(user=obj).values_list('title', flat=True)
        else:
            return None
    
    """Calculator of the number of completed tasks"""
    def get_completed(self, obj):
        
        count = obj.task_set.count()
        return count
        # a = []
        # f = []
        # for i in Task.objects.filter(user=obj.id).values():
        #     a.append(i)
        #     for j in a:
        #         if j['user_id']==obj.id:
        #             if j['is_complete']==True:
        #                 f.append(j)  
        # f = OrderedDict((frozenset(item.items()),item) for item in f).values()
        # return len(f)

    
    def get_is_completed(self, obj):
        a = []
        f = []
        t = []
        for i in Task.objects.filter(user=obj.id).values():
            a.append(i)
            for j in a:
                if j['user_id']==obj.id:
                    if j['is_complete']==True:
                        f.append(j)  
        for z in f:
            t.append(z['title'])
        return set(t)
    
    
    def get_not_completed(self, obj):
        a = []
        f = []
        t = []
        for i in Task.objects.filter(user=obj.id).values():
            a.append(i)
            for j in a:
                if j['user_id']==obj.id:
                    if j['is_complete']==False:
                        f.append(j)  
        for z in f:
            t.append(z['title'])
        return set(t)
