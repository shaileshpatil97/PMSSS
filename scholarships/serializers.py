from rest_framework import serializers
from .models import Scheme, Application, ApplicationDocument


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['id', 'doc_type', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ApplicationSerializer(serializers.ModelSerializer):
    documents = ApplicationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
    fields = '__all__'
