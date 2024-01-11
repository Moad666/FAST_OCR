from rest_framework import serializers
from .models import OCRResult,OCRTask,OCRTaskk

class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = ('id', 'image', 'text')

class OCRTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRTask
        fields = '__all__'

class OCRTaskkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRTaskk
        fields = '__all__'

