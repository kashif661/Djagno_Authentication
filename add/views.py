from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Send email verification link
            verification_url = f"http://localhost:8000/api/verify-email/{token}/"
            send_mail(
                'Verify Your Email',
                f'Click the link to verify your email: {verification_url}',
                'from@example.com',  # Update this with your email address
                [user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            refresh = RefreshToken(token)
            user_id = refresh.payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'message': 'Email successfully verified!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    pass
