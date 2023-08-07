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

#post: 將新聞依來源及類別分別寫入資料庫. 權限: managers
class NewsCollectorsAPI(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagers]

    #依類別選擇序列器
    def get_serializer_class(self):
        if self.request.data.get("news_cate") == "fin":
            return UdnFinSerializer
        elif self.request.data.get("news_cate") == "tech":
            return UdnTechSerializer
        else:
            return OrphanSerializer
    
    #檢查news_title是否重複, 若無則寫入資料庫, 重複返回208
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.check_title(request.data.get("news_title")):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "News is already exist!"}, status=status.HTTP_208_ALREADY_REPORTED)

    #依類別檢查news_title是否重複, 返回布林值
    def check_title(self, title):
        if self.request.data.get("news_cate") == "fin":
            return UdnFin.objects.filter(news_title=title).exists()
        elif self.request.data.get("news_cate") == "tech":
            return UdnTech.objects.filter(news_title=title).exists()
        else:
            return Orphan.objects.filter(news_title=title).exists()

#get: 依網址後附帶參數cate選擇類別讀取新聞列表. 權限: managers
class GetNewsListAPI(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagers]

    #改寫get_serializer依網址附帶參數cate選擇序列器
    def get_serializer(self, cate, *args, **kwargs):
        serializer_class = self.get_serializer_class(cate)
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
    
    #改寫get_serializer_class依網址附帶參數cate選擇序列器
    def get_serializer_class(self, cate):
        if cate == "fin":
            return UdnFinSerializer
        elif cate == "tech":
            return UdnTechSerializer
        else:
            return OrphanSerializer

    #依網址後附帶參數cate選擇類別讀取新聞列表
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

#post: 使用者註冊. 權限: 無
class RegisterAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(serializer.validated_data["username"], serializer.validated_data["email"], serializer.validated_data["password"])
        return Response(serializer.data, status= status.HTTP_201_CREATED)

#post: 使用者登入. 權限: 無
class LoginAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    #使用authenticate驗證, 驗證成功返回此user物件, 以login登入自動控制sesson
    def create(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login Successful!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

#post: 使用者登出. 權限: 已登入使用者
class Logout(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        logout(request)
        return Response({"message": "Logout Successful!"}, status=status.HTTP_200_OK)

#get, put, delete: 使用者資料修改及刪除. 權限: 已登入使用者本人
class UserDataEdit(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]
    lookup_field = 'pk'

    #post not allowed.
    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #get: 以pk取得資料庫裡的使用者資料
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #get: 以request裡的User資料來取得資料庫裡的使用者資料
    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #put: 依使用者更新的欄位資料並將password加密後存入資料庫
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = make_password(request.data["password"])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    #delete: 刪除使用者資料
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
