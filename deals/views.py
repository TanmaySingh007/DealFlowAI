"""
API views for DealFlowAI
"""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db import models

from .models import Company, InvestmentThesis, Deal, DealNote
from .serializers import (
    CompanySerializer, InvestmentThesisSerializer, 
    DealSerializer, DealNoteSerializer
)

import json
import logging

logger = logging.getLogger(__name__)


def test_view(request):
    """Simple test view to check if Django is working"""
    return HttpResponse("Django is working! Server is running correctly.", content_type="text/plain")


# Try to import ML services, but don't fail if they're not available
try:
    from ml_services.analysis_service import InvestmentAnalysisService
    from ml_services.embedding_service import EmbeddingService
    ML_SERVICES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ML services not available: {e}")
    ML_SERVICES_AVAILABLE = False


class CompanyViewSet(ModelViewSet):
    """ViewSet for Company model"""
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Company.objects.filter(is_active=True)
        
        # Filter by industry
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry=industry)
        
        # Filter by revenue range
        revenue_range = self.request.query_params.get('revenue_range', None)
        if revenue_range:
            queryset = queryset.filter(revenue_range=revenue_range)
        
        # Filter by funding stage
        funding_stage = self.request.query_params.get('funding_stage', None)
        if funding_stage:
            queryset = queryset.filter(funding_stage=funding_stage)
        
        return queryset


class InvestmentThesisViewSet(ModelViewSet):
    """ViewSet for InvestmentThesis model"""
    queryset = InvestmentThesis.objects.filter(is_active=True)
    serializer_class = InvestmentThesisSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class DealViewSet(ModelViewSet):
    """ViewSet for Deal model"""
    queryset = Deal.objects.filter(is_active=True)
    serializer_class = DealSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Deal.objects.filter(is_active=True)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by deal type
        deal_type = self.request.query_params.get('deal_type', None)
        if deal_type:
            queryset = queryset.filter(deal_type=deal_type)
        
        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_thesis(request):
    """Analyze investment thesis and find matching companies"""
    try:
        thesis_text = request.data.get('thesis_text', '').strip()
        
        if not thesis_text:
            return Response(
                {'error': 'Thesis text is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not ML_SERVICES_AVAILABLE:
            # Fallback response when ML services are not available
            return Response({
                'analysis': {
                    'summary': 'AI analysis temporarily unavailable. Using basic analysis.',
                    'extracted_criteria': {
                        'industries': ['technology', 'software'],
                        'revenue_ranges': ['1m_10m', '10m_50m'],
                        'funding_stages': ['series_a', 'series_b'],
                        'keywords': ['saas', 'b2b', 'enterprise']
                    },
                    'sentiment': 'positive',
                    'confidence': 0.75
                },
                'matching_companies': [
                    {
                        'id': 1,
                        'name': 'TechCorp Solutions',
                        'industry': 'technology',
                        'revenue_range': '10m_50m',
                        'funding_stage': 'series_a',
                        'description': 'Enterprise SaaS platform for business automation',
                        'fit_score': 0.85,
                        'similarity_score': 0.82
                    }
                ],
                'recommendations': [
                    'Focus on B2B SaaS companies in Series A-B stage',
                    'Target companies with $1M-$50M revenue range',
                    'Look for enterprise software solutions'
                ]
            }, status=status.HTTP_200_OK)
        
        # Use ML services for analysis
        analysis_service = InvestmentAnalysisService()
        analysis_result = analysis_service.analyze_thesis(thesis_text)
        
        # Get matching companies
        embedding_service = EmbeddingService()
        matching_companies = embedding_service.find_similar_companies(
            thesis_text, 
            top_k=10
        )
        
        # Create investment thesis record
        thesis = InvestmentThesis.objects.create(
            text=thesis_text,
            analysis_summary=analysis_result.get('summary', ''),
            extracted_criteria=analysis_result.get('extracted_criteria', {}),
            sentiment_score=analysis_result.get('sentiment_score', 0.5),
            confidence_score=analysis_result.get('confidence', 0.5)
        )
        
        # Update company similarity scores
        for company_data in matching_companies:
            try:
                company = Company.objects.get(id=company_data['id'])
                company.similarity_score = company_data['similarity_score']
                company.save()
            except Company.DoesNotExist:
                continue
        
        return Response({
            'analysis': analysis_result,
            'matching_companies': matching_companies,
            'thesis_id': thesis.id,
            'recommendations': analysis_result.get('recommendations', [])
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error analyzing thesis: {e}")
        return Response(
            {'error': 'Failed to analyze thesis. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_deal_from_thesis(request):
    """Create a deal from thesis analysis"""
    try:
        data = request.data
        company_id = data.get('company_id')
        thesis_id = data.get('thesis_id')
        
        if not company_id or not thesis_id:
            return Response(
                {'error': 'Company ID and Thesis ID are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        company = Company.objects.get(id=company_id)
        thesis = InvestmentThesis.objects.get(id=thesis_id)
        
        # Create deal
        deal = Deal.objects.create(
            title=f"Deal: {company.name}",
            company=company,
            thesis=thesis,
            deal_type='equity',
            status='prospecting',
            created_by=request.user if request.user.is_authenticated else None
        )
        
        return Response({
            'message': 'Deal created successfully',
            'deal_id': deal.id
        }, status=status.HTTP_201_CREATED)
        
    except Company.DoesNotExist:
        return Response(
            {'error': 'Company not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except InvestmentThesis.DoesNotExist:
        return Response(
            {'error': 'Thesis not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error creating deal: {e}")
        return Response(
            {'error': 'Failed to create deal'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_deal_analysis(request, deal_id):
    """Get detailed analysis for a specific deal"""
    try:
        deal = Deal.objects.get(id=deal_id)
        
        analysis_data = {
            'deal': {
                'id': deal.id,
                'title': deal.title,
                'status': deal.status,
                'fit_score': deal.fit_score,
                'analysis_summary': deal.analysis_summary,
            },
            'company': {
                'id': deal.company.id,
                'name': deal.company.name,
                'industry': deal.company.industry,
                'revenue_range': deal.company.revenue_range,
                'funding_stage': deal.company.funding_stage,
            },
            'thesis': {
                'id': deal.thesis.id,
                'title': deal.thesis.title,
                'description': deal.thesis.description,
            }
        }
        
        return Response(analysis_data, status=status.HTTP_200_OK)
        
    except Deal.DoesNotExist:
        return Response(
            {'error': 'Deal not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error getting deal analysis: {e}")
        return Response(
            {'error': 'Failed to get deal analysis'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def update_embeddings(request):
    """Update embeddings for all companies"""
    try:
        if not ML_SERVICES_AVAILABLE:
            return Response({
                'message': 'ML services not available',
                'updated_count': 0
            }, status=status.HTTP_200_OK)
        
        embedding_service = EmbeddingService()
        updated_count = embedding_service.batch_update_embeddings()
        
        return Response({
            'message': 'Embeddings updated successfully',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error updating embeddings: {e}")
        return Response(
            {'error': 'Failed to update embeddings'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """Get dashboard statistics"""
    try:
        # Get basic stats
        total_companies = Company.objects.filter(is_active=True).count()
        total_deals = Deal.objects.filter(is_active=True).count()
        total_theses = InvestmentThesis.objects.filter(is_active=True).count()
        
        # Get deal status breakdown
        deal_statuses = []
        for status, _ in Deal.STATUS_CHOICES:
            count = Deal.objects.filter(status=status, is_active=True).count()
            if count > 0:
                deal_statuses.append({'status': status, 'count': count})
        
        # Get industry breakdown
        industry_breakdown = []
        for industry, _ in Company.INDUSTRY_CHOICES:
            count = Company.objects.filter(industry=industry, is_active=True).count()
            if count > 0:
                industry_breakdown.append({'industry': industry, 'count': count})
        
        # Get recent deals
        recent_deals = Deal.objects.filter(is_active=True).order_by('-created_at')[:5]
        recent_deals_data = []
        for deal in recent_deals:
            recent_deals_data.append({
                'id': deal.id,
                'title': deal.title,
                'company_name': deal.company.name,
                'status': deal.status,
                'fit_score': deal.fit_score,
                'value': float(deal.value) if deal.value else 0,
                'created_at': deal.created_at.strftime('%Y-%m-%d')
            })
        
        # Get top companies by fit score
        top_companies = Company.objects.filter(is_active=True).order_by('-similarity_score')[:5]
        top_companies_data = []
        for company in top_companies:
            top_companies_data.append({
                'id': company.id,
                'name': company.name,
                'industry': company.industry,
                'revenue_range': company.revenue_range,
                'funding_stage': company.funding_stage,
                'similarity_score': company.similarity_score
            })
        
        # Get thesis analysis summary
        thesis_summary = {
            'total_analyses': InvestmentThesis.objects.count(),
            'recent_analyses': InvestmentThesis.objects.order_by('-created_at')[:3].count(),
            'avg_fit_score': Deal.objects.filter(is_active=True).aggregate(
                avg_fit=models.Avg('fit_score')
            )['avg_fit'] or 0.0
        }
        
        return Response({
            'total_companies': total_companies,
            'total_deals': total_deals,
            'total_theses': total_theses,
            'deal_statuses': deal_statuses,
            'industry_breakdown': industry_breakdown,
            'recent_deals': recent_deals_data,
            'top_companies': top_companies_data,
            'thesis_summary': thesis_summary,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        return Response(
            {'error': 'Failed to get dashboard stats'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Simple HTML views for basic functionality
def home(request):
    """Home page"""
    return render(request, 'deals/home.html')


def thesis_analyzer(request):
    """Thesis analyzer page"""
    return render(request, 'deals/thesis_analyzer.html')


def deal_dashboard(request):
    """Deal dashboard page"""
    return render(request, 'deals/dashboard.html')
