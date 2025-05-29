from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
    def validate_name(self, value):
        """
        Check that company name is not empty and has reasonable length
        """
        if not value.strip():
            raise serializers.ValidationError("Company name cannot be empty.")
        return value
        
    def validate_economic_sector(self, value):
        """
        Validate economic sector
        """
        if not value.strip():
            raise serializers.ValidationError("Economic sector cannot be empty.")
        return value


class CompanyListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing companies (without full description)
    """
    class Meta:
        model = Company
        fields = ['id', 'name', 'country_of_origin', 'economic_sector']
