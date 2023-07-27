from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_api import serializers
from manager import models as ManagerModels


@api_view(['GET', 'POST'])
def WhatsappSchedulerView(request):
    if request.method == 'GET':
        tasks = ManagerModels.Task.objects.filter(user=request.user)
        serializer = serializer.TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializer.TaskSerializer(data=request.data, user=request.user.pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
