from .models import UdnFin, UdnTech, Orphan
from django.contrib.auth.models import User, Group
from rest_framework import serializers

#UdnFin���ǦC��
class UdnFinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdnFin
        fields = "__all__"

#UdnTech���ǦC��
class UdnTechSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdnTech
        fields = "__all__"

#Orphan���ǦC��
class OrphanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orphan
        fields = "__all__"

#User���ǦC��, password���[�ݩ�write onlyŪ�����ǦC�Ʒ|�Q����. groups���[�ݩ�read only�g�J���ϧǦC�Ʒ|�Q����.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "groups"]
        extra_kwargs = {"password": {"write_only": True}, "groups": {"read_only": True}}

#Group���ǦC��
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"