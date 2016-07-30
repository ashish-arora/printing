__author__ = 'ashish'
from mongoengine.errors import *
from printapp.models import User, UserRequest, UserResponse
from printapp.models import USER_TYPES, VALID_COUNTRY, VALID_CITIES, VALID_PRODUCT_TYPES
import base64, os, json
from printapp.models import OPEN, RESPONSE_RECEIVED, CLOSED, PRINTER, CLIENT
from django.contrib.auth import authenticate, login

def authenticate_user(func):
    """
    this will be called when the user has to be authenticated

    """
    def inner(self, request):
        username = self.request.data.get("username", None)
        password = self.request.data.get("password", None)
        try:
            user = User.objects.get(username=username, password=password)
        except DoesNotExist:
            raise ValidationError("User does not exist")
        else:
            request.user = user
            return func(self, request)
    return inner

def process_signup(username, email, msisdn, password, user_type, business_name, description, city, country):
    import ipdb;ipdb.set_trace()
    if user_type not in USER_TYPES:
        raise ValidationError("Not valid user type")

    city=1

    if msisdn and msisdn.startswith("+"):
        if len(msisdn[1:]) != 12 or not msisdn[1:].isdigit():
            raise ValidationError("Invalid msisdn:%s" % msisdn)
        elif msisdn[:3] not in VALID_COUNTRY:
            raise ValidationError("Invalid country in msisdn: %s" % msisdn)
    elif msisdn and (not msisdn.isdigit() or not len(msisdn) == 10):
        raise ValidationError("Invalid country in msisdn: %s" % msisdn)

    token = base64.urlsafe_b64encode(os.urandom(8))
    msisdn='+919811665296'
    return User.objects.create(username=username, email=email, msisdn=msisdn,
                        type=user_type, business_name=business_name, description=description, city=city)


def user_login(request, user):
    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
    login(request, user)
    request.session.set_expiry(60 * 60 * 1)
    return user


def get_targetted_printers_in_specified_area(location):
    return User.objects.filter(type=PRINTER, city = location)\
        .order_by('-order_processed', '-rating').limit(15)

def send_request_to_targetted_users(users, user_request):
    import ipdb; ipdb.set_trace()
    user_responses=[]
    for user in users:
        user_responses.append(UserResponse(user=user, request=user_request, status=OPEN))
    UserResponse.objects.insert(user_responses)

def process_user_query(user, type, paper_size, quantity, paper='', time='', binding='', design='', description=''):
    if type not in dict(VALID_PRODUCT_TYPES):
        raise ValidationError("Not valid product type")
    request_data = {"paper_size":paper_size, "quantity":quantity, "paper":paper, "time":time, "binding":binding, "design":design, 'description':description}
    user_request = UserRequest.objects.create(user_id=user, status=OPEN, description=request_data)
    users = get_targetted_printers_in_specified_area(user.city)
    send_request_to_targetted_users(users, user_request)


def process_user_query2(user, request_type, request_data):
    import ipdb;ipdb.set_trace()
    #if type not in dict(VALID_PRODUCT_TYPES):
    #    raise ValidationError("Not valid product type")
    #request_data = {"paper_size":paper_size, "quantity":quantity, "paper":paper, "time":time, "binding":binding, "design":design, 'description':description}
    user_request = UserRequest.objects.create(user=user, status=OPEN, type=request_type, description=request_data)
    users = get_targetted_printers_in_specified_area(user.city)
    send_request_to_targetted_users(users, user_request)


def process_user_response(user, quote, request_id, description=''):
    user_request = UserRequest.objects.get(id=request_id)
    user_response = UserResponse.objects.create(user=user, request=user_request, status=RESPONSE_RECEIVED, response_data = description, quote=quote)
    #user_response.delivery_hours = time
    return user_request, user_response

def hire_user(user,  hired_user_id, request_id, response_id):
    hired_user = User.objects.get(id=hired_user_id)
    user_request = UserRequest.objects.get(id=request_id)
    user_response = UserResponse.objects.get(id=response_id)
    user_request.hired_user = hired_user
    user_request.status=CLOSED
    user_request.save()
    user_response.status=CLOSED
    user_response.save()
    hired_user.update_one(inc__orders_completed=1)

def is_valid_type(type):
    if type not in ["Worker", "Employer"]:
        return False
    else:
        return True

def get_type_id(type):
    if type == "Worker":
        return PRINTER
    else:
        return CLIENT


def is_user_logged_in(func):
    """
    this will be called when the user is logged in

    """
    def inner(self, request):
        username = self.request.data.get("username", None)
        password = self.request.data.get("password", None)
        try:
            user = User.objects.get(username=username, password=password)
        except DoesNotExist:
            raise ValidationError("User does not exist")
        else:
            request.user = user
            return func(self, request)
    return inner





