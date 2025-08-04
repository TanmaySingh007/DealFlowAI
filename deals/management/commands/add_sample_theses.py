from django.core.management.base import BaseCommand
from deals.models import InvestmentThesis
from django.contrib.auth.models import User
import json


class Command(BaseCommand):
    help = 'Add sample investment thesis data'

    def handle(self, *args, **options):
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dealflowai.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        sample_theses = [
            {
                'text': 'We are looking to invest in B2B SaaS companies with strong unit economics, proven product-market fit, and recurring revenue models. Target companies should be in the $5M-$50M ARR range with 100%+ net revenue retention and positive unit economics. We prefer companies with experienced management teams and clear competitive moats.',
                'analysis_summary': 'Focus on B2B SaaS with strong unit economics and proven PMF',
                'extracted_criteria': {
                    'industries': ['software', 'saas'],
                    'revenue_ranges': ['5_20m', '20_100m'],
                    'funding_stages': ['series_a', 'series_b', 'series_c'],
                    'keywords': ['b2b', 'saas', 'unit economics', 'product-market fit', 'recurring revenue']
                },
                'sentiment_score': 0.85,
                'confidence_score': 0.90
            },
            {
                'text': 'Seeking investments in fintech companies disrupting traditional banking and payment systems. Focus on companies with innovative technology, regulatory compliance, and strong customer acquisition. Target companies in Series A-C stages with $10M-$100M revenue.',
                'analysis_summary': 'Fintech companies disrupting traditional banking with innovative technology',
                'extracted_criteria': {
                    'industries': ['fintech'],
                    'revenue_ranges': ['5_20m', '20_100m'],
                    'funding_stages': ['series_a', 'series_b', 'series_c'],
                    'keywords': ['fintech', 'banking', 'payments', 'regulatory compliance', 'customer acquisition']
                },
                'sentiment_score': 0.78,
                'confidence_score': 0.82
            },
            {
                'text': 'Looking for healthcare technology companies that improve patient outcomes and reduce costs. Focus on AI/ML applications in diagnostics, telemedicine, and healthcare management. Target companies with FDA approval or clear regulatory pathway.',
                'analysis_summary': 'Healthcare tech companies improving patient outcomes with AI/ML',
                'extracted_criteria': {
                    'industries': ['healthcare', 'ai_ml'],
                    'revenue_ranges': ['1_5m', '5_20m', '20_100m'],
                    'funding_stages': ['series_a', 'series_b'],
                    'keywords': ['healthcare', 'ai', 'ml', 'patient outcomes', 'fda', 'telemedicine']
                },
                'sentiment_score': 0.92,
                'confidence_score': 0.88
            },
            {
                'text': 'Investing in cybersecurity companies that protect against emerging threats. Focus on companies with innovative security solutions, strong technical teams, and proven market demand. Target companies in growth stage with $5M-$50M revenue.',
                'analysis_summary': 'Cybersecurity companies protecting against emerging threats',
                'extracted_criteria': {
                    'industries': ['cybersecurity'],
                    'revenue_ranges': ['5_20m', '20_100m'],
                    'funding_stages': ['series_b', 'series_c'],
                    'keywords': ['cybersecurity', 'security', 'threats', 'protection', 'technical teams']
                },
                'sentiment_score': 0.80,
                'confidence_score': 0.85
            },
            {
                'text': 'Seeking AI/ML companies that solve real business problems with scalable technology. Focus on companies with proprietary algorithms, strong data moats, and clear commercial applications. Target companies in Series A-C with proven product-market fit.',
                'analysis_summary': 'AI/ML companies solving business problems with scalable technology',
                'extracted_criteria': {
                    'industries': ['ai_ml', 'software'],
                    'revenue_ranges': ['1_5m', '5_20m', '20_100m'],
                    'funding_stages': ['series_a', 'series_b', 'series_c'],
                    'keywords': ['ai', 'ml', 'algorithms', 'data', 'scalable', 'business problems']
                },
                'sentiment_score': 0.88,
                'confidence_score': 0.92
            }
        ]
        
        created_count = 0
        for thesis_data in sample_theses:
            thesis, created = InvestmentThesis.objects.get_or_create(
                text=thesis_data['text'][:100],  # Use first 100 chars as unique identifier
                defaults={
                    'text': thesis_data['text'],
                    'analysis_summary': thesis_data['analysis_summary'],
                    'extracted_criteria': thesis_data['extracted_criteria'],
                    'sentiment_score': thesis_data['sentiment_score'],
                    'confidence_score': thesis_data['confidence_score'],
                    'created_by': user,
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created thesis: {thesis_data["analysis_summary"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample theses')
        ) 