from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = get_user_model().objects.get(username=username)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token),
                             "refresh": str(refresh)},
                             status=status.HTTP_200_OK)
        return Response({"invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)