from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from manager import models as ManagerModels
from payments import models as PaymentModels
import json


def get_social_user(request):
    try:
        if request.user.socialaccount_set.all().filter(user=request.user):
            social_user = request.user.socialaccount_set.all().filter(user=request.user).first()
        else:
            social_user = None

        return social_user
    except:
        return redirect(reverse("app_auth:login"))

class HomePageView(View):
    template_name = "manager/index.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not (request.COOKIES.get('refresh') and request.COOKIES.get('access')):
                return redirect(reverse("app_auth:extension_tasks"))

            context_data = {
                "social_user" : get_social_user(request),
                "page_msg": f"Welcome Back, {request.user.username if request.user.username else request.user.email}."
            }
            
            return render(request, template_name=self.template_name, context=context_data)
        return redirect(reverse("app_auth:login"))

class PricingView(View):
    template_name = "manager/pricings.html"
    def get(self, request, *args, **kwargs):
        context_data = {
            "social_user" : get_social_user(request),
            "page_msg": f"Get the best for your money.",
            "pricings": PaymentModels.PaypalPlan.objects.all(),
            "features": PaymentModels.Feature.objects.all(),
        }
        return render(request, template_name=self.template_name, context=context_data)


class AccountView(View):
    template_name = "manager/profile.html"
    def get(self, request, *args, **kwargs):
        context_data = {
            "social_user" : get_social_user(request),
            "page_msg": f"",
            "subscriptions": PaymentModels.PaypalSubscription.objects.filter(
                user=request.user.id
            ).order_by("-id")
        }
        
        return render(request, template_name=self.template_name, context=context_data)


class WhatsappView(View):
    template_name = "whatsapp/index.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context_data = {
                "social_user" : get_social_user(request),
                "page_msg": f"",
                "subscriptions": PaymentModels.PaypalSubscription.objects.filter(
                    user=request.user.id
                ).order_by("-id")
            }
            
            return render(request, template_name=self.template_name, context=context_data)
        return redirect(reverse("app_auth:login"))


@csrf_exempt
def WhatsappSchedulerView(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Request Forbidden'})

        data = json.loads(request.body)
        task = ManagerModels.Task.objects.create(data=data, user=request.user)
        return JsonResponse({'status': 'success', 'message': 'Message Scheduled', "data": data})
    elif request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Request Forbidden'})

        data = []
        tasks = ManagerModels.Task.objects.filter(user=request.user)
        for task in tasks:
            data.append(task.data)
        
        return JsonResponse({'status': 'success', "data": data})