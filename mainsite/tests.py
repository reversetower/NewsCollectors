from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from .models import UdnFin, UdnTech, Orphan
from django.urls import reverse


class UserTest(APITestCase):
    
    #前置準備建立managers群組, 新建一個使用者test001並加入managers群組
    def setUp(self):
        Group.objects.create(name="managers")
        data = {"username": "test001", "email": "test001@mail.com", "password": "qoo123456"}
        User.objects.create_user(**data)
        user = User.objects.get(username="test001")
        group = Group.objects.get(name="managers")
        user.groups.set([group])
    
    #測試RegisterAPI
    def test_registerapi(self):
        #前置使用者test001是否成功建立
        self.assertEqual(User.objects.filter(username="test001").exists(), True)
        url = "/registerapi/"
        data1 = {"username": "test001", "email": "test001@mail.com", "password": "qoo123456"}
        data2 = {"username": "test002", "email": "test002@mail.com", "password": "qoo123456"}
        data3 = {"username": "", "email": "test001@mail.com", "password": ""}
        #測試透過RegisterAPI建立使用者
        response1 = self.client.post(url, data2)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(username="test002").exists(), True)
        #測試建立重複的使用者名
        response2 = self.client.post(url, data1)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        #測試建立使用者名及密碼空缺
        response3 = self.client.post(url, data3)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    #測試LoginAPI, LogoutAPI
    def test_loginapi_logoutapi(self):
        url1 = "/loginapi/"
        url2 = "/logoutapi/"
        data1 = {"username": "test999",  "password": "tgb987456"}
        data2 = {"username": "test001",  "password": "tgb987456"}
        data3 = {"username": "test001", "password": "qoo123456"}
        #測試登入使用者名及密碼錯誤
        response1 = self.client.post(url1, data1)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        #測試登入密碼錯誤
        response2 = self.client.post(url1, data2)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        #測試使用者登入
        response3 = self.client.post(url1, data3)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        #測試使用者登出
        response4 = self.client.post(url2)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
    
    #測試NewsCollectorsAPI
    def test_newscollectorsapi(self):
        url = "/newscollectorsapi/"
        data1 = {"news_source": "udn", "news_cate": "fin", "news_title": "test fin news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data2 = {"news_source": "udn", "news_cate": "tech", "news_title": "test tech news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data3 = {"news_source": "udn", "news_cate": "unknow", "news_title": "test unknow news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        #強制登入使用者test001身份
        user = User.objects.get(username="test001")
        self.client.force_authenticate(user=user)
        #測試依分類各新建一則新聞
        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)
        response3 = self.client.post(url, data3)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UdnFin.objects.count(), 1)
        self.assertEqual(UdnFin.objects.filter(news_title="test fin news one").exists(), True)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UdnTech.objects.count(), 1)
        self.assertEqual(UdnTech.objects.filter(news_title="test tech news one").exists(), True)

        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Orphan.objects.count(), 1)
        self.assertEqual(Orphan.objects.filter(news_title="test unknow news one").exists(), True)

    #測試GetNewsListAPI
    def test_get_news_list(self):
        #製作附帶參數的網址
        url1 = reverse("getnewslistapi", args=["fin"])
        url2 = reverse("getnewslistapi", args=["tech"])
        url3 = reverse("getnewslistapi", args=["unknow"])
        #在各分類新建一則新聞
        data1 = {"news_source": "udn", "news_cate": "fin", "news_title": "test fin news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data2 = {"news_source": "udn", "news_cate": "tech", "news_title": "test tech news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data3 = {"news_source": "udn", "news_cate": "unknow", "news_title": "test unknow news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        UdnFin.objects.create(**data1)
        UdnTech.objects.create(**data2)
        Orphan.objects.create(**data3)
        #強制登入使用者test001身份
        user = User.objects.get(username="test001")
        self.client.force_authenticate(user=user)
        #測試依網址及附帶參數取得各分類新聞列表
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)
        response3 = self.client.get(url3)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
