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
]

# HTML URL patterns
html_patterns = [
    path('', views.home, name='home'),
    path('test/', views.test_view, name='test'),
    path('thesis-analyzer/', views.thesis_analyzer, name='thesis_analyzer'),
    path('dashboard/', views.deal_dashboard, name='deal_dashboard'),
]

urlpatterns = api_patterns + html_patterns 