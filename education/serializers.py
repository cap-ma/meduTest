from rest_framework import serializers

from .models import (
    OrderTestInfo,
    Test,
    TestCategory,
    OrderTestPack,
    OrderTestInfoAssignStudent,
    OrderTestPackResultsOfStudent,
)


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = "__all__"


class TestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id", "question", "a", "b", "c", "d", "level", "answer"]


class TestSerializers(serializers.ModelSerializer):
    category = TestCategorySerializer()

    class Meta:
        model = Test
        fields = [
            "id",
            "question",
            "a",
            "b",
            "c",
            "d",
            "answer",
            "level",
            "teacher",
            "category",
        ]


class TestSerializersForTeacherWithAnswer(serializers.ModelSerializer):
    category = TestCategorySerializer()

    class Meta:
        model = Test
        fields = [
            "id",
            "question",
            "a",
            "b",
            "c",
            "d",
            "level",
            "answer",
            "teacher",
            "category",
        ]


class FilterTestInfoSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data=data.filter(level=2,edition__hide=False)
        return super(FilterTestInfoSerializer,self).to_representation(data)
    

class OrderTestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = OrderTestInfo
        list_serailizer_class=FilterTestInfoSerializer
        fields = "__all__"

class OrderTestInfoAssignedStudentSerializer(serializers.ModelSerializer):
    order_test_info=OrderTestInfoSerializer()

    class Meta:
        model=OrderTestInfoAssignStudent
        fields=["submitted","created_at","order_test_info"]




class OrderTestPackGetSerializer(serializers.ModelSerializer):
    order_test_info = OrderTestInfoSerializer(required=True)
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
