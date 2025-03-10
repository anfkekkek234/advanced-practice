import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage as DjangoEmailMessage  # تغییر نام
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from mail_templated import EmailMessage as TemplatedEmailMessage  # تغییر نام
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile
from ..utils import EmailThread
from .serializers import (
    ActivationResendSerializer,
    ChangePasswordSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    RegisterationSerializer,
)

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            html_content = render_to_string(
                "email/activation_email.tpl", {"token": token}
            )
            email_obj = DjangoEmailMessage(
                subject="Account Activation",
                body=html_content,
                from_email="admin@gmail.com",
                to=[email],
            )
            email_obj.content_subtype = "html"
            email_obj.send()
            data = {"email": email}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})        # noqa: E501


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):      # noqa: E501
                return Response(
                    {"old_password": ["wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)


class TestEmailSend(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = "al.ko.0179.611@gmail.com"
        try:
            user_obj = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise NotFound("User not found")

        token = self.get_tokens_for_user(user_obj)
        html_content = render_to_string("email/heloo.tpl", {"token": token})

        email_obj = DjangoEmailMessage(
            subject="Account Activation",
            body=html_content,
            from_email="a@gmail.com",
            to=[self.email],
        )
        email_obj.content_subtype = "html"
        email_obj.send()

        return Response("Email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])       # noqa: E501
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response({"details": "your account has already been verified"})       # noqa: E501
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account have been verified and activated successfully"}     # noqa: E501
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = TemplatedEmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@gmail.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
