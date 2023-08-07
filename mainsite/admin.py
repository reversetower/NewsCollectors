from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import UdnFin, UdnTech, Orphan

#UdnFin資料表在admin主控台顯示的欄位
class UdnFinAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(UdnFin, UdnFinAdmin)

#UdnTech資料表在admin主控台顯示的欄位
class UdnTechAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(UdnTech, UdnTechAdmin)

#Orphan資料表在admin主控台顯示的欄位
class OrphanAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(Orphan, OrphanAdmin)

#User資料表在admin主控台顯示的欄位, 自訂display_groups欄位將有加入的群組都顯示出來
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "display_groups", "password", "is_staff", "is_active", "date_joined")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = "Groups"

#先將已註冊User取消再依自訂控制重新註冊
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#Group資料表在admin主控台顯示的欄位, 自訂display_members欄位將有加入此群組的會員都顯示出來
class CustomGroupAdmin(GroupAdmin):
    list_display = ("name", "display_members")

    def display_members(self, obj):
        members = User.objects.filter(groups=obj)
        return ", ".join([member.username for member in members])

#先將已註冊Group取消再依自訂控制重新註冊
admin.site.unregister(Group)
admin.site.register(Group,CustomGroupAdmin)