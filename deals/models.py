from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Company(models.Model):
    """Company model for storing company information"""
    
    INDUSTRY_CHOICES = [
        ('software', 'Software'),
        ('fintech', 'FinTech'),
        ('healthcare', 'Healthcare'),
        ('energy', 'Energy'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('logistics', 'Logistics'),
        ('cybersecurity', 'Cybersecurity'),
        ('ai_ml', 'AI/ML'),
        ('other', 'Other'),
    ]
    
    REVENUE_CHOICES = [
        ('under_1m', 'Under $1M'),
        ('1_5m', '$1M - $5M'),
        ('5_20m', '$5M - $20M'),
        ('20_100m', '$20M - $100M'),
        ('100m_plus', '$100M+'),
    ]
    
    FUNDING_STAGE_CHOICES = [
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('series_b', 'Series B'),
        ('series_c', 'Series C'),
        ('series_d', 'Series D'),
        ('ipo', 'IPO'),
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    revenue_range = models.CharField(max_length=20, choices=REVENUE_CHOICES)
    funding_stage = models.CharField(max_length=20, choices=FUNDING_STAGE_CHOICES)
    website = models.URLField(blank=True, null=True)
    founding_year = models.IntegerField(blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    headquarters = models.CharField(max_length=200, blank=True)
    total_funding = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    # ML/AI fields
    embedding_vector = models.TextField(blank=True, null=True)  # JSON string
    similarity_score = models.FloatField(default=0.0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_embedding_vector(self):
        """Get embedding vector as list"""
        if self.embedding_vector:
            return json.loads(self.embedding_vector)
        return None
    
    def set_embedding_vector(self, vector):
        """Set embedding vector from list"""
        self.embedding_vector = json.dumps(vector)
    
    def get_company_summary(self):
        """Get a summary of the company"""
        return f"{self.name} - {self.industry} - {self.funding_stage}"


class InvestmentThesis(models.Model):
    """Investment thesis model for storing investment criteria"""
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    investment_criteria = models.JSONField(default=dict)
    target_industries = models.JSONField(default=list)
    target_revenue_ranges = models.JSONField(default=list)
    target_funding_stages = models.JSONField(default=list)
    
    # ML fields
    embedding_vector = models.TextField(blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Investment Theses"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Deal(models.Model):
    """Deal model for tracking investment opportunities"""
    
    STATUS_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('due_diligence', 'Due Diligence'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    DEAL_TYPE_CHOICES = [
        ('equity', 'Equity Investment'),
        ('debt', 'Debt Investment'),
        ('acquisition', 'Acquisition'),
        ('merger', 'Merger'),
        ('partnership', 'Partnership'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals')
    thesis = models.ForeignKey(InvestmentThesis, on_delete=models.CASCADE, related_name='deals')
    
    # Deal details
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospecting')
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    equity_percentage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True, null=True
    )
    
    # Analysis fields
    fit_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.5
    )
    analysis_summary = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.name}"
    
    def get_deal_summary(self):
        """Get a summary of the deal"""
        return f"{self.title} ({self.status}) - {self.company.name}"


class DealNote(models.Model):
    """Notes and comments for deals"""
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    note_type = models.CharField(max_length=50, default='general')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note on {self.deal.title} - {self.created_at.date()}"
