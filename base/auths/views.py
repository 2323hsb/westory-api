from django.shortcuts import render

from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException

from google.oauth2 import id_token
from google.auth.transport import requests

from apis.models import User

import json

HTTP_ACCEPT = 'HTTP_ACCEPT'
CLIENT_ID = '877944658856-1tr4gmmtc8nm4ur7m1p3jv2e9omm8fo3.apps.googleusercontent.com'

class SignUpWithGoogle(ObtainAuthToken):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        print("tetst")
        token_data = json.loads(request.body)
        user_id_token = token_data['id_token']
        try:
            idinfo = id_token.verify_oauth2_token(
                user_id_token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                json_response = {
                    'status': 'fail',
                    'message': 'invalid id',
                }
                return Response(json_response)

            google_id = idinfo['sub']
            google_email = idinfo['email']
            google_name = idinfo['name']
            google_profile_img_url = idinfo['picture']

            

            if User.objects.filter(google_id=google_id):
                json_response = {
                    'status': 'fail',
                    'message': 'user already exists',
                }
                return Response(json_response)
            else:
                json_response = {
                    'status': 'success',
                    'message': 'create new user',
                }
                newUser = User(email=google_email,
                               username=google_name, google_id=google_id, profile_img=google_profile_img_url)
                newUser.save()
                return Response(json_response)

        except ValueError:
            json_response = {
                'status': 'fail',
                'message': 'invalid id',
            }
            return Response(json_response)


class SignIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        user_id_token = request_data['id_token']

        try:
            idinfo = id_token.verify_oauth2_token(
                user_id_token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise APIException('Some Error')

            google_id = idinfo['sub']
            try:
                user = User.objects.get(google_id=google_id)
                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    'status': 'success',
                    'access_token': token.key
                })
            except User.DoesNotExist:
                json_response = {
                    'status': 'new',
                    'message': 'user does not exist',
                }
                return Response(json_response)
        except ValueError:
            raise APIException('Some Error')