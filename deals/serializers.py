"""
Serializers for DealFlowAI
"""

from rest_framework import serializers
from .models import Company, InvestmentThesis, Deal, DealNote


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model"""
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'industry', 'revenue_range',
            'funding_stage', 'website', 'founding_year', 'employee_count',
            'headquarters', 'total_funding', 'similarity_score',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'similarity_score']


class InvestmentThesisSerializer(serializers.ModelSerializer):
    """Serializer for InvestmentThesis model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = InvestmentThesis
        fields = [
            'id', 'title', 'description', 'investment_criteria',
            'target_industries', 'target_revenue_ranges', 'target_funding_stages',
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DealNoteSerializer(serializers.ModelSerializer):
    """Serializer for DealNote model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DealNote
        fields = [
            'id', 'deal', 'content', 'note_type', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DealSerializer(serializers.ModelSerializer):
    """Serializer for Deal model"""
    
    company = CompanySerializer(read_only=True)
    thesis = InvestmentThesisSerializer(read_only=True)
    notes = DealNoteSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Deal
        fields = [
            'id', 'title', 'company', 'thesis', 'deal_type', 'status',
            'value', 'equity_percentage', 'fit_score', 'risk_score',
            'analysis_summary', 'notes', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ThesisAnalysisRequestSerializer(serializers.Serializer):
    """Serializer for thesis analysis requests"""
    thesis_text = serializers.CharField(max_length=10000, required=True)


class DealCreationRequestSerializer(serializers.Serializer):
    """Serializer for deal creation requests"""
    thesis_text = serializers.CharField(max_length=10000, required=True)
    company_id = serializers.IntegerField(required=True)
    deal_title = serializers.CharField(max_length=200, required=False)


class CompanySearchSerializer(serializers.Serializer):
    """Serializer for company search requests"""
    query = serializers.CharField(max_length=500, required=False)
    industry = serializers.CharField(max_length=50, required=False)
    revenue_range = serializers.CharField(max_length=20, required=False)
    funding_stage = serializers.CharField(max_length=20, required=False) 