from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from .models import UdnFin, UdnTech, Orphan
from django.urls import reverse


class UserTest(APITestCase):
    
    #�e�m�ǳƫإ�managers�s��, �s�ؤ@�ӨϥΪ�test001�å[�Jmanagers�s��
    def setUp(self):
        Group.objects.create(name="managers")
        data = {"username": "test001", "email": "test001@mail.com", "password": "qoo123456"}
        User.objects.create_user(**data)
        user = User.objects.get(username="test001")
        group = Group.objects.get(name="managers")
        user.groups.set([group])
    
    #����RegisterAPI
    def test_registerapi(self):
        #�e�m�ϥΪ�test001�O�_���\�إ�
        self.assertEqual(User.objects.filter(username="test001").exists(), True)
        url = "/registerapi/"
        data1 = {"username": "test001", "email": "test001@mail.com", "password": "qoo123456"}
        data2 = {"username": "test002", "email": "test002@mail.com", "password": "qoo123456"}
        data3 = {"username": "", "email": "test001@mail.com", "password": ""}
        #���ճz�LRegisterAPI�إߨϥΪ�
        response1 = self.client.post(url, data2)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(username="test002").exists(), True)
        #���իإ߭��ƪ��ϥΪ̦W
        response2 = self.client.post(url, data1)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        #���իإߨϥΪ̦W�αK�X�ů�
        response3 = self.client.post(url, data3)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    #����LoginAPI, LogoutAPI
    def test_loginapi_logoutapi(self):
        url1 = "/loginapi/"
        url2 = "/logoutapi/"
        data1 = {"username": "test999",  "password": "tgb987456"}
        data2 = {"username": "test001",  "password": "tgb987456"}
        data3 = {"username": "test001", "password": "qoo123456"}
        #���յn�J�ϥΪ̦W�αK�X���~
        response1 = self.client.post(url1, data1)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        #���յn�J�K�X���~
        response2 = self.client.post(url1, data2)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        #���ըϥΪ̵n�J
        response3 = self.client.post(url1, data3)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        #���ըϥΪ̵n�X
        response4 = self.client.post(url2)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
    
    #����NewsCollectorsAPI
    def test_newscollectorsapi(self):
        url = "/newscollectorsapi/"
        data1 = {"news_source": "udn", "news_cate": "fin", "news_title": "test fin news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data2 = {"news_source": "udn", "news_cate": "tech", "news_title": "test tech news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data3 = {"news_source": "udn", "news_cate": "unknow", "news_title": "test unknow news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        #�j��n�J�ϥΪ�test001����
        user = User.objects.get(username="test001")
        self.client.force_authenticate(user=user)
        #���ը̤����U�s�ؤ@�h�s�D
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

    #����GetNewsListAPI
    def test_get_news_list(self):
        #�s�@���a�Ѽƪ����}
        url1 = reverse("getnewslistapi", args=["fin"])
        url2 = reverse("getnewslistapi", args=["tech"])
        url3 = reverse("getnewslistapi", args=["unknow"])
        #�b�U�����s�ؤ@�h�s�D
        data1 = {"news_source": "udn", "news_cate": "fin", "news_title": "test fin news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data2 = {"news_source": "udn", "news_cate": "tech", "news_title": "test tech news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        data3 = {"news_source": "udn", "news_cate": "unknow", "news_title": "test unknow news one", "news_date": "20230806", "news_url": "http://www.udn.com.tw"}
        UdnFin.objects.create(**data1)
        UdnTech.objects.create(**data2)
        Orphan.objects.create(**data3)
        #�j��n�J�ϥΪ�test001����
        user = User.objects.get(username="test001")
        self.client.force_authenticate(user=user)
        #���ը̺��}�Ϊ��a�Ѽƨ��o�U�����s�D�C��
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)
        response3 = self.client.get(url3)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
