from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserRegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            return render(request, 'login.html', {'errors': 'Invalid credentials'})
        return render(request, 'login.html', {'errors': serializer.errors})

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except ObjectDoesNotExist:
            pass
        logout(request)
        return redirect('/')

