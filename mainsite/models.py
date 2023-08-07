from django.db import models

#�w�qUdn�]�g���s�D��ƪ����
class UdnFin(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx

#�w�qUdn������s�D��ƪ����
class UdnTech(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx

#�w�q����������ƪ����
class Orphan(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx
