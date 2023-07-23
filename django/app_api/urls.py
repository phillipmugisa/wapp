from django.urls import path, include
from app_api import views as ApiViews

from rest_framework.routers import DefaultRouter

app_name = "app_api"

urlpatterns = [
    path("user/details/", ApiViews.UserDetialsViews.as_view(), name="user_detials_api"),
    # path("data/templates/", ApiViews.TemplateListCreateView.as_view(), name="templates"),
    # path("data/tasks/", ApiViews.TaskListCreateView.as_view(), name="tasks"),
    path("ai/<str:user_message>/<str:reply_tone>/", ApiViews.AIView.as_view(), name="ai"),

    path('templates/', ApiViews.TemplateList.as_view(), name='template-list'),
    path('templates/create/', ApiViews.TemplateCreate.as_view(), name='template-create'),
    path('templates/<int:pk>/update/', ApiViews.TemplateUpdate.as_view(), name='template-update'),
    path('templates/<int:pk>/delete/', ApiViews.TemplateDeleteView.as_view(), name='template-delete'),

    path('tasks/', ApiViews.TaskList.as_view(), name='task-list'),
    path('tasks/create/', ApiViews.TaskCreate.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', ApiViews.TaskUpdate.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', ApiViews.TaskDeleteView.as_view(), name='task-delete'),

    path('memos/', ApiViews.MemoList.as_view(), name='memo-list'),
    path('memos/create/', ApiViews.MemoCreate.as_view(), name='memo-create'),
    path('memos/<int:pk>/update/', ApiViews.MemoUpdate.as_view(), name='memo-update'),
    path('memos/<int:pk>/delete/', ApiViews.MemoDeleteView.as_view(), name='memo-delete'),

    path('alarms/', ApiViews.AlarmList.as_view(), name='alarm-list'),
    path('alarms/create/', ApiViews.AlarmCreate.as_view(), name='alarm-create'),
    path('alarms/<int:pk>/update/', ApiViews.AlarmUpdate.as_view(), name='alarm-update'),
    path('alarms/<int:pk>/delete/', ApiViews.AlarmDeleteView.as_view(), name='alarm-delete'),

    path('blockedsite/', ApiViews.BlockedSiteList.as_view(), name='blockedsite-list'),
    path('blockedsite/create/', ApiViews.BlockedSiteCreate.as_view(), name='blockedsite-create'),
    path('blockedsite/<int:pk>/update/', ApiViews.BlockedSiteUpdate.as_view(), name='blockedsite-update'),
    path('blockedsite/<int:pk>/delete/', ApiViews.BlockedSiteDeleteView.as_view(), name='blockedsite-delete'),
]