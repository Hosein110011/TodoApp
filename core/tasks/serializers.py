from rest_framework import serializers
from .models import Task, Category
from subtasks.models import SubTask



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']




class TaskListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    subtasks = serializers.SerializerMethodField(method_name='get_subtask', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'is_complete', 'category','absolute_url','subtasks', 'created_time', 'updated_time']
        read_only_fields = []

    
    
    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.id)
    
    
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('id'):
            rep.pop('absolute_url', None)
            if rep['subtasks'] == None:
                rep.pop('subtasks', None)
        else:
            rep.pop('subtasks', None)
        rep['category'] = CategorySerializer(instance.category).data
        return rep
    

    def get_subtask(self, obj):
        if SubTask.objects.filter(task=obj).exists():
            return SubTask.objects.filter(task=obj.id).values_list('title', flat=True)
        else:
            return None
    
    """Identify the user automatically"""
    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)        
    




