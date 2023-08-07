from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import UdnFin, UdnTech, Orphan

#UdnFin��ƪ�badmin�D���x��ܪ����
class UdnFinAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(UdnFin, UdnFinAdmin)

#UdnTech��ƪ�badmin�D���x��ܪ����
class UdnTechAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(UdnTech, UdnTechAdmin)

#Orphan��ƪ�badmin�D���x��ܪ����
class OrphanAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(Orphan, OrphanAdmin)

#User��ƪ�badmin�D���x��ܪ����, �ۭqdisplay_groups���N���[�J���s�ճ���ܥX��
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "display_groups", "password", "is_staff", "is_active", "date_joined")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = "Groups"

#���N�w���UUser�����A�̦ۭq����s���U
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#Group��ƪ�badmin�D���x��ܪ����, �ۭqdisplay_members���N���[�J���s�ժ��|������ܥX��
class CustomGroupAdmin(GroupAdmin):
    list_display = ("name", "display_members")

    def display_members(self, obj):
        members = User.objects.filter(groups=obj)
        return ", ".join([member.username for member in members])

#���N�w���UGroup�����A�̦ۭq����s���U
admin.site.unregister(Group)
admin.site.register(Group,CustomGroupAdmin)