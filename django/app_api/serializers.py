from rest_framework import serializers
from manager import models as ManagerModels
from app_auth import models as AuthModels

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AuthModels.User.objects.all())
    class Meta:
        model = ManagerModels.Task
        fields = "__all__"
