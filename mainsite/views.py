from importlib import machinery
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import UdnFin, UdnTech, Orphan
from .serializers import UdnFinSerializer, UdnTechSerializer, OrphanSerializer, UserSerializer, GroupSerializer
from .permissions import IsPosterOrReadOnly, IsManagers, IsUser
from mainsite import serializers

#post: �N�s�D�̨ӷ������O���O�g�J��Ʈw. �v��: managers
class NewsCollectorsAPI(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagers]

    #�����O��ܧǦC��
    def get_serializer_class(self):
        if self.request.data.get("news_cate") == "fin":
            return UdnFinSerializer
        elif self.request.data.get("news_cate") == "tech":
            return UdnTechSerializer
        else:
            return OrphanSerializer
    
    #�ˬdnews_title�O�_����, �Y�L�h�g�J��Ʈw, ���ƪ�^208
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.check_title(request.data.get("news_title")):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "News is already exist!"}, status=status.HTTP_208_ALREADY_REPORTED)

    #�����O�ˬdnews_title�O�_����, ��^���L��
    def check_title(self, title):
        if self.request.data.get("news_cate") == "fin":
            return UdnFin.objects.filter(news_title=title).exists()
        elif self.request.data.get("news_cate") == "tech":
            return UdnTech.objects.filter(news_title=title).exists()
        else:
            return Orphan.objects.filter(news_title=title).exists()

#get: �̺��}����a�Ѽ�cate������OŪ���s�D�C��. �v��: managers
class GetNewsListAPI(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagers]

    #��gget_serializer�̺��}���a�Ѽ�cate��ܧǦC��
    def get_serializer(self, cate, *args, **kwargs):
        serializer_class = self.get_serializer_class(cate)
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
    
    #��gget_serializer_class�̺��}���a�Ѽ�cate��ܧǦC��
    def get_serializer_class(self, cate):
        if cate == "fin":
            return UdnFinSerializer
        elif cate == "tech":
            return UdnTechSerializer
        else:
            return OrphanSerializer

    #�̺��}����a�Ѽ�cate������OŪ���s�D�C��
    def list(self, request, cate):
        if cate == "fin":
            self.get_serializer(cate)
            self.queryset = UdnFin.objects.all()
            serializer = UdnFinSerializer(self.queryset, many=True)
        elif cate == "tech":
            self.get_serializer(cate)
            self.queryset = UdnTech.objects.all()
            serializer = UdnTechSerializer(self.queryset, many=True)
        else:
            self.get_serializer(cate)
            self.queryset = Orphan.objects.all()
            serializer = OrphanSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#post: �ϥΪ̵��U. �v��: �L
class RegisterAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(serializer.validated_data["username"], serializer.validated_data["email"], serializer.validated_data["password"])
        return Response(serializer.data, status= status.HTTP_201_CREATED)

#post: �ϥΪ̵n�J. �v��: �L
class LoginAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    #�ϥ�authenticate����, ���Ҧ��\��^��user����, �Hlogin�n�J�۰ʱ���sesson
    def create(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login Successful!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

#post: �ϥΪ̵n�X. �v��: �w�n�J�ϥΪ�
class Logout(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        logout(request)
        return Response({"message": "Logout Successful!"}, status=status.HTTP_200_OK)

#get, put, delete: �ϥΪ̸�ƭק�ΧR��. �v��: �w�n�J�ϥΪ̥��H
class UserDataEdit(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]
    lookup_field = 'pk'

    #post not allowed.
    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #get: �Hpk���o��Ʈw�̪��ϥΪ̸��
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #get: �Hrequest�̪�User��ƨӨ��o��Ʈw�̪��ϥΪ̸��
    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #put: �̨ϥΪ̧�s������ƨñNpassword�[�K��s�J��Ʈw
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = make_password(request.data["password"])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    #delete: �R���ϥΪ̸��
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
