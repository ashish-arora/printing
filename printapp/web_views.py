__author__ = 'ashish'
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from printapp.utils.helper import process_signup, user_login, process_user_query2
from printapp.utils.helper import is_valid_type, get_type_id, process_user_response
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from printapp.models import User, USER_MAP, UserRequest, UserResponse
from time import gmtime, strftime, time
import ipdb

class IndexView(View):
    template_name='index.html'

    def get(self, request):
        # <view logic>
        return render(request, self.template_name, {})

class RequestView(View):
    template_name = 'index.html'

    def post(self, request):
        request_type = request.POST.get('request_type')
        #print self.kwards['path']
        if request_type == "visiting-card":
            data = request.POST.dict()
            if data.has_key('csrfmiddlewaretoken'):
                del data['csrfmiddlewaretoken']
            process_user_query2(request.user, request_type, data)

        return render(request, self.template_name, {"message":"You request has been successfully submitted"})

    def get(self, request):
        user_requests = UserRequest.objects.all()
        return render(request, self.template_name, {"user_requests": user_requests})


class SingleRequestView(View):
    template_name = 'user_request.html'

    def get(self, request, request_id):
        user_request = UserRequest.objects.get(id=request_id)
        UserResponse.objects.get(request=user_request, user=request.user)
        return render(request, self.template_name, {"user_request": user_request})

    def post(self, request, request_id):
        pass

class ResponseView(View):
    template_name = 'user_request.html'

    def post(self, request, request_id):
        quote = request.POST.get("quote")
        comment = request.POST.get("comment")
        user_request, user_response = process_user_response(request.user, quote, request_id, comment)
        return render(request, self.template_name, {"user_response": user_response, "user_request": user_request})


class SignUpView(View):
    template_name = 'signup.html'

    def post(self, request):
        ipdb.set_trace()
        error=[]
        username = request.POST.get('username')
        email = request.POST.get('email')
        msisdn = request.POST.get('msisdn')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        looking_for = request.POST.get('looking_for')
        business_name = request.POST.get('business_name')
        city = request.POST.get('city')
        description = request.POST.get('description')
        country = request.POST.get('country')

        if not (username and email and password and confirm_password):
            return render(request, self.template_name, {'error':"required paramters is not there"})

        if not is_valid_type(looking_for):
            return render(request, self.template_name, {'error':"type is not valid"})

        if password != confirm_password:
            return render(request, self.template_name, {'error':""})
        user_type = USER_MAP.get(looking_for)
        try:
            user = process_signup(username, email, msisdn, password, user_type, business_name, description, city, country)
            if not user:
                raise Exception("User is none")
            user.set_password(password)
            user.save()
        except Exception as ex:
            error = str(ex)
            return render(request, self.template_name, {'error': error})
        if not user:
            return render(request, self.template_name, {'error': "Some error occurred while signup, Please try it again"})
        user_login(request, user)
        return redirect('/index')

    def get(self, request):
        return render(request, self.template_name, {})

class LoginView(View):
    template_name='index.html'

    def get(self, request):
        app_path=request.get_full_path()
        return render(request, "login.html", {"app_path":app_path})

    def post(self, request):
        redirect_to = request.POST.get('next')
        try:
            password =request.POST.get("password")
            user = User.objects.get(username=request.POST.get('username'))
            if user.check_password(password):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                login(request, user)
                request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                return HttpResponseRedirect('/index')
            else:
                return render(request, self.template_name, {'error': "user crendentials are not valid"})
        except Exception, ex:
            return render(request, self.template_name, {'error': "user does not exist"})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        user_requests = UserRequest.objects.all().order_by('-ts')
        for user_request in user_requests:
            user_request.date = strftime("%d %b", gmtime(user_request.ts))
        return render(request, self.template_name, {'user_requests': user_requests})







