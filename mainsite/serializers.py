from .models import UdnFin, UdnTech, Orphan
from django.contrib.auth.models import User, Group
from rest_framework import serializers

#UdnFin的序列器
class UdnFinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdnFin
        fields = "__all__"

#UdnTech的序列器
class UdnTechSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdnTech
        fields = "__all__"

#Orphan的序列器
class OrphanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orphan
        fields = "__all__"

#User的序列器, password附加屬性write only讀取的序列化會被忽略. groups附加屬性read only寫入的反序列化會被忽略.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "groups"]
        extra_kwargs = {"password": {"write_only": True}, "groups": {"read_only": True}}

#Group的序列器
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"