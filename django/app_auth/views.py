from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import auth
from app_auth.models import User
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib import messages
import random

class ExtensionTasksViews(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            # if a user is authenticated, this view is for process of the extension to get the user logged in
            refresh = RefreshToken.for_user(request.user)
            # create cookies
            response = redirect(reverse("manager:home"))
            response.set_cookie('refresh', str(refresh))
            response.set_cookie('access', str(refresh.access_token))
            response.delete_cookie('user_logged_out')
            return response
        return redirect(reverse("app_auth:login"))
        
            

class loginUserView(View):
    template_name = "account/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("manager:home"))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # if not user.is_phone_activated and not user.is_username_activated:
            #     messages.add_message(request, messages.ERROR, 'Verify Phone Number or username to Proceed')
            #     return redirect(reverse("app_auth:login"))

            auth.login(request, user)
            return redirect(reverse("app_auth:extension_tasks"))
            
        messages.add_message(request, messages.ERROR, 'Account Not Found.')
        return redirect(reverse("app_auth:login"))

class RegisterUserView(View):
    template_name = "account/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('manager:home'))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        country_code = request.POST.get("country_code", "")
        phone_number = request.POST.get("mobile_user", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password == confirm_password:
            if not User.objects.filter(username=username):

                verify_code = "".join([ str(i) for i in random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6)])

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    country_code=country_code,
                    phone_number=phone_number,
                    verify_code = verify_code,
                    is_active = False
                )

                if user:
                    response = redirect(reverse("app_auth:login"))
                    return response

                    
                messages.add_message(request, messages.ERROR, 'An Error Occured. Try Again.')
                return redirect(reverse("app_auth:register"))
            else:
                messages.add_message(request, messages.ERROR, 'username not available.')
                return redirect(reverse("app_auth:register"))
        else:
                messages.add_message(request, messages.ERROR, 'Passwords entered do not match.')
                return redirect(reverse("app_auth:register"))

        return render(request, self.template_name)


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'User Logged out')
    response = redirect(reverse("app_auth:login"))
    response.delete_cookie('refresh')
    response.delete_cookie('access')
    response.set_cookie('user_logged_out', True)
    return response
