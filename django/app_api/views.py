from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from app_auth import models as AuthModels
from app_api import serializers
from manager import models as ManagerModels
from payments import models as PaymentModels

import os
import openai
import re

openai.api_key = os.environ.get("OPENAIKEY")


# class UserDetialsViews(generics.RetrieveAPIView):
#     serializer_class = serializers.UserSerializer
#     queryset = AuthModels.User.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

class UserDetialsViews(APIView):
    def get(self, request, *args, **kwargs):
        response = dict()
        
        response = {
            # "email" : user.email,
            "subscription" : PaymentModels.PaypalSubscription.objects.filter(user=request.user).first().plan.name,
            "user" : request.user.username,
        }   

        return Response(response)

class TemplateList(generics.ListAPIView):
    serializer_class = serializers.TemplateSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Template.objects.filter(user=user)

class TemplateCreate(generics.CreateAPIView):
    serializer_class = serializers.TemplateSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Template.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TemplateUpdate(generics.UpdateAPIView):
    serializer_class = serializers.TemplateSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Template.objects.filter(user=user)

class TemplateDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.TemplateSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Template.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# class TemplateListCreateView(generics.ListCreateAPIView):
#     serializer_class = serializers.TemplateSerializer
#     queryset = ManagerModels.Templates.objects.all()

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class TaskListCreateView(generics.ListCreateAPIView):
#     serializer_class = serializers.TaskSerializer
#     queryset = ManagerModels.Task.objects.all()

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


class TaskList(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Task.objects.filter(user=user)

class TaskCreate(generics.CreateAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Task.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskUpdate(generics.UpdateAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Task.objects.filter(user=user)

    def put(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Task.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class MemoList(generics.ListAPIView):
    serializer_class = serializers.MemoSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Memo.objects.filter(user=user)

class MemoCreate(generics.CreateAPIView):
    serializer_class = serializers.MemoSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Memo.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MemoUpdate(generics.UpdateAPIView):
    serializer_class = serializers.MemoSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Memo.objects.filter(user=user)

class MemoDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.MemoSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Memo.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class AlarmList(generics.ListAPIView):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Alarm.objects.filter(user=user)

class AlarmCreate(generics.CreateAPIView):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Alarm.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlarmUpdate(generics.UpdateAPIView):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Alarm.objects.filter(user=user)

class AlarmDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.Alarm.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class BlockedSiteList(generics.ListAPIView):
    serializer_class = serializers.BlockedSiteSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.BlockedSite.objects.filter(user=user)

class BlockedSiteCreate(generics.CreateAPIView):
    serializer_class = serializers.BlockedSiteSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.BlockedSite.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlockedSiteUpdate(generics.UpdateAPIView):
    serializer_class = serializers.BlockedSiteSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.BlockedSite.objects.filter(user=user)

class BlockedSiteDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.BlockedSiteSerializer

    def get_queryset(self):
        user = self.request.user
        return ManagerModels.BlockedSite.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class AIView(APIView):
    def get(self, request, user_message, reply_tone):
        response = dict()
        
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"suggest 3 replies to this message: {user_message}. {reply_tone}",
                max_tokens=80,
        )

        replies = re.split(r'\d+\.', response.choices[0].text.replace('\n', ''))

        replies = [ reply.strip() for reply in replies if reply.strip()]
        
        response = {
            "replies" : replies
        }   

        return Response(response)