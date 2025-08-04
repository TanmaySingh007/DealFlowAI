"""
Admin configuration for deals app
"""

from django.contrib import admin
from .models import Company, InvestmentThesis, Deal, DealNote


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin configuration for Company model"""
    list_display = [
        'name', 'industry', 'revenue_range', 'funding_stage', 
        'employee_count', 'similarity_score', 'is_active', 'created_at'
    ]
    list_filter = [
        'industry', 'revenue_range', 'funding_stage', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'description', 'headquarters']
    readonly_fields = ['created_at', 'updated_at', 'similarity_score']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'website', 'headquarters')
        }),
        ('Business Details', {
            'fields': ('industry', 'revenue_range', 'funding_stage', 'founding_year', 'employee_count', 'total_funding')
        }),
        ('ML/AI Data', {
            'fields': ('embedding_vector', 'similarity_score'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvestmentThesis)
class InvestmentThesisAdmin(admin.ModelAdmin):
    """Admin configuration for InvestmentThesis model"""
    list_display = [
        'title', 'created_by', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Investment Criteria', {
            'fields': ('investment_criteria', 'target_industries', 'target_revenue_ranges', 'target_funding_stages')
        }),
        ('ML Data', {
            'fields': ('embedding_vector',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Admin configuration for Deal model"""
    list_display = [
        'title', 'company', 'deal_type', 'status', 'value', 
        'fit_score', 'risk_score', 'created_by', 'created_at'
    ]
    list_filter = [
        'deal_type', 'status', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'company__name', 'analysis_summary']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'thesis', 'created_by')
        }),
        ('Deal Details', {
            'fields': ('deal_type', 'status', 'value', 'equity_percentage')
        }),
        ('Analysis', {
            'fields': ('fit_score', 'risk_score', 'analysis_summary')
        }),
        ('Metadata', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DealNote)
class DealNoteAdmin(admin.ModelAdmin):
    """Admin configuration for DealNote model"""
    list_display = [
        'deal', 'note_type', 'created_by', 'created_at'
    ]
    list_filter = ['note_type', 'created_at']
    search_fields = ['content', 'deal__title']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Note Information', {
            'fields': ('deal', 'content', 'note_type', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
