from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import (
    UserRegisterationSerializer,
    UserLoginSerializer)


class UserRegisterationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        token =RefreshToken.for_user(user)
        data = serializer.data
        data['token'] = {"access":str(token.access_token),"refresh":str(token)}
        return Response(data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data
        token =RefreshToken.for_user(user)
        data = serializer.data
        data['token'] = {"access":str(token.access_token),"refresh":str(token)}
        return Response(data, status=status.HTTP_200_OK)
    
class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,*args,**kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            # request.user.auth_token.delete()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
