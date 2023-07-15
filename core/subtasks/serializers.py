from rest_framework import serializers
from .models import SubTask



class SubTaskSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_url')
    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'url', 'created_time', 'updated_time']

    
    
        
    
    def get_url(self, obj):
        request = self.context.get('request')
        # return urllib.parse.unquote(urllib.parse.unquote(request.build_absolute_uri(obj.title)).replace(" ",""))
        return request.build_absolute_uri(obj.id)
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('id'):
            rep.pop('url', None)
            rep.pop('created_time')
            rep.pop('updated_time', None)
        rep['task'] = instance.task.title
        
        return rep
        

    def validate(self, attrs):
        if attrs.get('task').user != self.context.get('request').user:
            raise serializers.ValidationError({"detail":"user doesnt have any task with this title"})
        return super().validate(attrs)
        