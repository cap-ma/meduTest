from rest_framework import serializers

from .models import (
    OrderTestInfo,
    Test,
    TestCategory,
    OrderTestPack,
    OrderTestInfoAssignStudent,
    OrderTestPackResultsOfStudent,
)


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        extra_kwargs = {"answer": {"write_only": True}}


class OrderTestInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestInfo
        fields = "__all__"


class OrderTestPackGetSerializer(serializers.ModelSerializer):
    order_test_info = OrderTestInfoSerializers(required=True)
    test = TestSerializers(required=True)

    class Meta:
        model = OrderTestPack
        fields = ["test", "teacher", "order_test_info"]


class OrderTestPackStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTestPackResultsOfStudent
        fields = "__all__"


class OrderTestInfoStudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestInfoAssignStudent
        fields = "__all__"


class OrderTestPackSerializers(serializers.ModelSerializer):
    test = TestSerializers(required=True)

    class Meta:
        model = OrderTestPack
        fields = "__all__"


class OrderTestPackSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestPack
        fields = "__all__"


class OrderTestPackResponseSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestPack
        fields = ["test", "order_test_info"]


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = "__all__"
        extra_kwargs = {"answer": {"write_only": True}}
