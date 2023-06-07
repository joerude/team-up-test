from rest_framework import serializers
from .models import Test, IQTestResult, EQTestResult


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['login']


class IQTestResultSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y')

    class Meta:
        model = IQTestResult
        fields = ['score', 'timestamp']


class EQTestResultSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y')

    class Meta:
        model = EQTestResult
        fields = ['answers', 'timestamp']
