from rest_framework import serializers
from app_auth import models as AuthModels
from manager import models as ManagerModels
from payments import models as PaymentModels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModels.User
        fields = ['id', 'username', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('context').get('request').user
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["subscription"] = PaymentModels.PaypalSubscription.objects.filter(user=instance).first().plan.name
        return representation

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Template
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Task
        fields = "__all__"


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Memo
        fields = "__all__"

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Alarm
        fields = "__all__"

class BlockedSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.BlockedSite
        fields = "__all__"