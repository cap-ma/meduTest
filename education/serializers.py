from rest_framework import serializers

from .models import (
    OrderTestInfo,
    Test,
    TestCategory,
    OrderTestPack,
    OrderTestInfoStudent,
)


class OrderTestInfoStudentsSerializers(serializers.ModelSerializer):
    class Meta:
        models = OrderTestInfoStudent
        fields = "__all__"


class OrderTestPackSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestPack
        fields = "__all__"


class OrderTestPackResponseSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestPack
        fields = ["test", "order_test_info"]


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
