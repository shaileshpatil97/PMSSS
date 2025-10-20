from rest_framework import serializers
from .models import SAG


class SAGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAG
        fields = '__all__'
