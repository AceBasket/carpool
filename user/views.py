from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
import pyotp
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserSerializer
from user.models import User
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='Register',
            fields={
                'email': serializers.EmailField(),
                'password': serializers.CharField(),
            }
        ),
        responses={
            201: inline_serializer(
                name='Register-success',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
            400: inline_serializer(
                name='Register-badrequest',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
            409: inline_serializer(
                name='Register-conflict',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "success", 'message': "Registered successfully, please login"}, status=status.HTTP_201_CREATED)
            except:
                return Response({"status": "fail", "message": "User with that email already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GenerateOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='GenerateOTP',
            fields={
                'user_id': serializers.IntegerField(),
                'email': serializers.EmailField(),
            }
        ),
        responses={
            200: inline_serializer(
                name='GenerateOTP-success',
                fields={
                    'base32': serializers.CharField(),
                    'otpauth_url': serializers.URLField(),
                }
            ),
            404: inline_serializer(
                name='GenerateOTP-error',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
        }
    )
    def post(self, request):
        data = request.data
        user_id = data.get('user_id', None)
        email = data.get('email', None)

        user = User.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="ManuelAndSarah")

        user.otp_auth_url = otp_auth_url
        user.otp_base32 = otp_base32
        user.save()

        return Response({'base32': otp_base32, "otpauth_url": otp_auth_url})


class VerifyOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='VerifyOTP',
            fields={
                'user_id': serializers.IntegerField(),
                'token': serializers.CharField(min_length=6, max_length=6),
            }
        ),
        responses={
            200: inline_serializer(
                name='VerifyOTP-success',
                fields={
                    'otp_verified': serializers.BooleanField(),
                    'user': UserSerializer(),
                    'token': inline_serializer(
                        name='Token',
                        fields={
                            'refresh': serializers.CharField(),
                            'access': serializers.CharField(),
                        }
                    ),
                }
            ),
            400: inline_serializer(
                name='VerifyOTP-badrequest',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
            404: inline_serializer(
                name='VerifyOTP-error',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
        }
    )
    def post(self, request):
        message = "Token is invalid or user doesn't exist"
        data = request.data
        user_id = data.get('user_id', None)
        otp_token = data.get('token', None)
        user = User.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token):
            return Response({"status": "fail", "message": message}, status=status.HTTP_400_BAD_REQUEST)
        user.otp_enabled = True
        user.otp_verified = True
        user.save()
        serializer = self.serializer_class(user)

        refresh_token = RefreshToken.for_user(user)

        return Response({'otp_verified': True, "user": serializer.data, "token": {"refresh": str(refresh_token), "access": str(refresh_token.access_token)}}, status=status.HTTP_200_OK)


class ValidateOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='ValidateOTP',
            fields={
                'user_id': serializers.IntegerField(),
                'token': serializers.CharField(min_length=6, max_length=6),
            }
        ),
        responses={
            200: inline_serializer(
                name='ValidateOTP-success',
                fields={
                    'otp_valid': serializers.BooleanField(),
                    'token': inline_serializer(
                        name='Token',
                        fields={
                            'refresh': serializers.CharField(),
                            'access': serializers.CharField(),
                        }
                    ),
                }
            ),
            400: inline_serializer(
                name='ValidateOTP-badrequest',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
            404: inline_serializer(
                name='ValidateOTP-error',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
        }
    )
    def post(self, request):
        message = "Token is invalid or user doesn't exist"
        data = request.data
        user_id = data.get('user_id', None)
        otp_token = data.get('token', None)
        user = User.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.otp_verified:
            return Response({"status": "fail", "message": "OTP must be verified first"}, status=status.HTTP_404_NOT_FOUND)

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token, valid_window=1):
            return Response({"status": "fail", "message": message}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(user)

        return Response({'otp_valid': True, "token": {"refresh": str(refresh_token), "access": str(refresh_token.access_token)}}, status=status.HTTP_200_OK)


class DisableOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='DisableOTP',
            fields={
                'user_id': serializers.IntegerField(),
            }
        ),
        responses={
            200: inline_serializer(
                name='DisableOTP-success',
                fields={
                    'otp_disabled': serializers.BooleanField(),
                    'user': UserSerializer(),
                }
            ),
            404: inline_serializer(
                name='DisableOTP-error',
                fields={
                    'status': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            ),
        }
    )
    def post(self, request):
        data = request.data
        user_id = data.get('user_id', None)

        user = User.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        user.otp_enabled = False
        user.otp_verified = False
        user.otp_base32 = None
        user.otp_auth_url = None
        user.save()
        serializer = self.serializer_class(user)

        return Response({'otp_disabled': True, 'user': serializer.data})
