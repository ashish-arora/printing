from django.shortcuts import render
from .models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, ParseError
from rest_framework.exceptions import APIException
from printapp.utils.json_response import JSONResponse
from rest_framework.views import APIView
import time, traceback, json
from utils import log
from utils.helper import process_signup, process_user_query, process_user_response, hire_user
from mongoengine.errors import NotUniqueError
from mongoengine.errors import DoesNotExist
import base64, os
from models import User, UserRequest, UserResponse
from serializers import UserRequestSerializer, UserResponseSerializer, UserSerializer
# Create your views here.
#from models import VALID_REQUEST_STATUS, VALID_RESPONSE_STATUS
from models import USER_TYPES
from mongoengine.errors import DoesNotExist
from datetime import datetime, timedelta
from printapp.utils.helper import authenticate_user
#from utils.helpers import QueueRequests
#from school.settings import NOTIFICATION_QUEUE, SMS_QUEUE
from rest_framework.views import APIView
from django.core.cache import cache
import bson, base64, random, os
BASE64_URLSAFE="-_"
from school.settings import REDIS_CONN as cache
from collections import deque


logger = log.Logger.get_logger(__file__)

# Create your views here

class AccountSignUp(APIView):

    def post(self, request):
        """
        Account Sign Up
        You need to give name, msisdn, type:1/2/3/4 (ADMIN/TEACHER/PARENT/STUDENT), organization_id, group_id
        ---
        # YAML (must be separated by `---`)

        type:
            name:
                required: true
                type: string
            msisdn:
                required: true
                type: string
            type:
                required: true
                type: integer
            organization_id:
                required: true
                type: string
            group_id:
                required: true
                type: string

        serializer: UserSerializer
        omit_serializer: True

        parameters_strategy: merge
        omit_parameters:
            - path

        responseMessages:
            - code: 200
              message: Successfully Signed up
            - code: 400
              message: Bad Request
        """
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            msisdn = request.data.get('msisdn')
            type = int(request.data.get('type'))
            business_name = request.data.get('business_name','')
            description = request.data.get('description','')
            country=request.data.get('country')
            city = request.data.get('city')
            password = request.data.get('password')
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error":"Required parameter were not there"})

        try:
            process_signup(name=name, email=email, msisdn=msisdn, type=type, business_name=business_name,
                       description=description, city=city, country=country, password=password)
        except ValidationError as ex:
            logger.error("AccountSignUp: %s" % str(ex))
            return JSONResponse({"error":str(ex)})
        except Exception as ex:
            logger.error("AccountSignUp: %s" % str(ex))
            logger.error(traceback.format_exc())
            return JSONResponse({"error":str(ex)})

        logger.debug("Successfully signed up for msisdn: %s" %(msisdn))
        return JSONResponse({"stat":"ok"})

class AccountLogin(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        try:
            user = User.objects.get(email=email, password=password)
        except Exception, ex:
            raise AuthenticationFailed("Invalid credentials,email:%s" % email)

class UserRequestApi(APIView):

    @authenticate_user
    def get(self, request_id, request):
        user_request = UserRequest.objects.get(id=request_id)
        serializer = UserRequestSerializer(user_request)
        return JSONResponse(serializer.data, status=200)


    @authenticate_user
    def post(self, request):
        try:
            type = request.data.get('type')
            paper_size = request.data.get('size')
            quantity = request.data.get('quantity')
            paper = request.data.get('paper_type')
            binding = request.data.get('binding')
            time = request.data.get('time')
            design = request.data.get('design', '')
            description = request.data.get('description', '')
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        try:
            process_user_query(user=request.user, type=type, paper_size=paper_size, quantity=quantity, paper=paper, binding=binding, time=time, design=design, description=description)
        except ValidationError as ex:
            logger.error("AccountSignUp: %s" % str(ex))
            return JSONResponse({"error":str(ex)})
        except Exception as ex:
            logger.error("AccountSignUp: %s" % str(ex))
            logger.error(traceback.format_exc())
            return JSONResponse({"error":str(ex)})

        logger.debug("Successfully posted the query for email: %s" %(email))
        return JSONResponse({"stat":"ok"})


class UserResponseApi(APIView):

    @authenticate_user
    def get(self, response_id, request):
        user_response = UserResponse.objects.get(id=response_id)
        serializer = UserResponseSerializer(user_response)
        return JSONResponse(serializer.data, status=200)

    @authenticate_user
    def post(self, request):
        try:
            description = request.data.get('description', '')
            quote = request.data.get('quote')
            request_id = request.data.get('request_id')
            response_id = request.data.get('response_id')
            time = request.data.get('time', '')
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        try:
            process_user_response(user=request.user,  quote=quote, request_id=request_id, response_id=response_id, time=time, description=description)
        except ValidationError as ex:
            logger.error("UserResponse: %s" % str(ex))
            return JSONResponse({"error":str(ex)})
        except Exception as ex:
            logger.error("UserResponse: %s" % str(ex))
            logger.error(traceback.format_exc())
            return JSONResponse({"error":str(ex)})

        logger.debug("Successfully posted the response for user: %s" %(request.user.email))
        return JSONResponse({"stat":"ok"})

class UserResponseMulti(APIView):

    @authenticate_user
    def get(self, request):
        """try:
            response_ids = request.data.get("response_ids")
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        if isinstance(response_ids, list):
            return JSONResponse({"error": "Required parameter were not there"})
        """
        user_responses = UserResponse.objects.filter(user=request.user)
        serializer = UserResponseSerializer(user_responses, many=True)
        return JSONResponse(serializer.data, status=200)

class UserRequestMulti(APIView):

    @authenticate_user
    def get(self, request):
        """try:
            response_ids = request.data.get("response_ids")
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        if isinstance(response_ids, list):
            return JSONResponse({"error": "Required parameter were not there"})
        """
        user_requests = UserRequest.objects.filter(user=request.user)
        serializer = UserRequestSerializer(user_requests, many=True)
        return JSONResponse(serializer.data, status=200)



class HireUser(APIView):

    @authenticate_user
    def post(self, request):
        try:
            request_id = request.data.get('request_id')
            response_id = request.data.get('response_id')
            user_id = request.data.get('user_id')
        except Exception, ex:
            logger.error("Error: %s" %(str(ex)))
            return JSONResponse({"error": "Required parameter were not there"})

        try:
            hire_user(user=request.user,  hired_user_id=user_id, request_id=request_id, response_id=response_id)
        except ValidationError as ex:
            logger.error("HireUserResponse: %s" % str(ex))
            return JSONResponse({"error":str(ex)})
        except Exception as ex:
            logger.error("HireUserResponse: %s" % str(ex))
            logger.error(traceback.format_exc())
            return JSONResponse({"error":str(ex)})

        logger.debug("Successfully hired the %s ->: %s" %(request.user.email, user_id))
        return JSONResponse({"stat":"ok"})







