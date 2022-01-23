from atexit import register
from django.conf import settings
from rest_framework import  viewsets
from .serializers import  NurseSerializer, VisitSerializer, UserLogoutSerializer,UserLoginSerializer
from .models import  Nurse, Visit
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  
from .task import task_send_email
import json
from django.core.mail import send_mail
from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.db.models import Q
from django.core.exceptions import ValidationError
from uuid import uuid4

class Login(generics.GenericAPIView):
    # get method handler
    queryset = Nurse.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return render(request, "signin.html",{'data':serializer_class.data})#Response(serializer_class.data, status=HTTP_200_OK)
        else:
            messages.info(request, 'Username OR password is incorrect')
        return render(request, "signin.html",{})#Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
        

        #     return render(request, "signin.html",{'data': serializer_class.data})#Response(serializer_class.data, status=HTTP_200_OK)
        # return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
    
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password =request.POST.get('password')
        print(email)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user  = None
            # if the email has been passed
        if '@' in email:
            user = Nurse.objects.filter(Q(email=email) & Q(password=password)).distinct()
            if not user.exists():
                messages.info(request, 'Username OR password is incorrect')
                return  render(request, 'signin.html', {})
            user = Nurse.objects.get(email=email)
        else:
            user = Nurse.objects.filter(Q(username=email) & Q(password=password)).distinct()
            if not user.exists():
                messages.info(request, 'Username OR password is incorrect')
                return  render(request, 'signin.html', {})
            user = Nurse.objects.get(username=email)
        user.token = uuid4()
        user.save()
        return render(request, 'stronka.html', {})
    return render(request, 'signin.html', {})


class Logout(generics.GenericAPIView):
    queryset = Nurse.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


#nie dziala
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class NurseViews(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    authentication_classes = []
    serializer_class = NurseSerializer
    # permission_classes = [permissions.IsAuthenticated]'


class VisitViews(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    authentication_classes = []
    serializer_class = VisitSerializer

    # def get_queryset(self):
    #     spec_id = self.request.query_params.get('spec_id')
    #     return Visit.objects.filter(doctor__specialization__id = spec_id).distinct()

def widok(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return HttpResponse("<h1>Widok <br> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</h1>")

    


def template(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "signin.html",{})




   