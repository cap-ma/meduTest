from rest_framework import serializers

from .models import OrderTestInfo


class OrderTestInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTestInfo
        fields = "__all__"
