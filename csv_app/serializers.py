from rest_framework import serializers
from .models import User, UserReportData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, data):
        if data['age'] < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        if not data['name']:
            raise serializers.ValidationError("Name cannot be empty.")
        return data
    
class UserReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReportData
        fields = '__all__'