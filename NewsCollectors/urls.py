from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from mainsite import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#drf_yasg設定
schema_view = get_schema_view(
    openapi.Info(
        title="NewsCollectors API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://google.com/policies/terms/",
        contact=openapi.Contact(email="st72x500y@gmail.com"),
        license=openapi.License(name="BSD License"),
        ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    )

#API網址路徑設定
router = DefaultRouter()
router.register(r"registerapi", views.RegisterAPI, basename="registerapi")
router.register(r"loginapi", views.LoginAPI, basename="loginapi")
router.register(r"logoutapi", views.Logout, basename="logoutapi")
router.register(r"userdataeditapi", views.UserDataEdit, basename="userdataeditapi")
router.register(r"newscollectorsapi", views.NewsCollectorsAPI, basename="newscollectorsapi")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    #依分類取得新聞列表的網址及附帶參數設定
    path(r"getnewslistapi/<str:cate>", views.GetNewsListAPI.as_view({'get': 'list'}), name="getnewslistapi"),
    #drf_yasg路徑設定
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]