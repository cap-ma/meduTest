from rest_framework import serializers

from .models import OrderTestInfo, Test, TestCategory


class OrderTestInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestInfo
        fields = "__all__"


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = "__all__"
