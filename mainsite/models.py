from django.db import models

#定義Udn財經類新聞資料表欄位
class UdnFin(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx

#定義Udn科技類新聞資料表欄位
class UdnTech(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx

#定義未知分類資料表欄位
class Orphan(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_idx
