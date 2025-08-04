"""
URL configuration for deals app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'theses', views.InvestmentThesisViewSet)
router.register(r'deals', views.DealViewSet)

# API URL patterns
api_patterns = [
    path('api/', include(router.urls)),
    path('api/analyze-thesis/', views.analyze_thesis, name='analyze_thesis'),
    path('api/create-deal/', views.create_deal_from_thesis, name='create_deal'),
    path('api/deals/<int:deal_id>/analysis/', views.get_deal_analysis, name='deal_analysis'),
    path('api/update-embeddings/', views.update_embeddings, name='update_embeddings'),
    path('api/dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/thesis-history/', views.thesis_history, name='thesis_history'),
    path('api/thesis/<int:thesis_id>/details/', views.get_thesis_details, name='thesis_details'),
    path('api/advanced-analytics/', views.advanced_analytics, name='advanced_analytics'),
    path('api/company-performance/', views.company_performance, name='company_performance'),
    path('api/deal-pipeline-analysis/', views.deal_pipeline_analysis, name='deal_pipeline_analysis'),
    path('api/advanced-visualizations/', views.advanced_visualizations, name='advanced_visualizations'),
]

# HTML URL patterns
html_patterns = [
    path('', views.home, name='home'),
    path('test/', views.test_view, name='test'),
    path('thesis-analyzer/', views.thesis_analyzer, name='thesis_analyzer'),
    path('dashboard/', views.deal_dashboard, name='deal_dashboard'),
    path('thesis-details/', views.thesis_details_view, name='thesis_details_view'),
    path('test-api/', views.test_api_view, name='test_api'),
]

urlpatterns = api_patterns + html_patterns 