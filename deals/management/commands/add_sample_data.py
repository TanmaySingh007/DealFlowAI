#!/usr/bin/env python
"""
Management command to add sample data for testing
"""
import os
import sys
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from deals.models import Company, InvestmentThesis, Deal
from ml_services.embedding_service import EmbeddingService

class Command(BaseCommand):
    help = 'Add sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample data...')
        
        try:
            with transaction.atomic():
                # Create sample companies
                companies_data = [
                    # Technology Companies
                    {'name': 'TechFlow Solutions', 'industry': 'technology', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered workflow automation platform for small businesses'},
                    {'name': 'CloudSync Pro', 'industry': 'technology', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Enterprise cloud synchronization and backup solutions'},
                    {'name': 'DataViz Analytics', 'industry': 'technology', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Advanced data visualization and business intelligence platform'},
                    {'name': 'SecureNet Systems', 'industry': 'technology', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Cybersecurity solutions for enterprise networks'},
                    {'name': 'MobileFirst Apps', 'industry': 'technology', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Mobile-first SaaS applications for productivity'},
                    {'name': 'AI Insights Corp', 'industry': 'technology', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Machine learning analytics for business intelligence'},
                    {'name': 'BlockChain Solutions', 'industry': 'technology', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Blockchain infrastructure for enterprise applications'},
                    {'name': 'IoT Connect', 'industry': 'technology', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Internet of Things connectivity platform'},
                    {'name': 'Quantum Computing Inc', 'industry': 'technology', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Quantum computing solutions for complex problems'},
                    {'name': 'VR Experience Labs', 'industry': 'technology', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'Virtual reality experiences for training and entertainment'},
                    
                    # Healthcare Companies
                    {'name': 'MedTech Innovations', 'industry': 'healthcare', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Medical device technology for patient monitoring'},
                    {'name': 'HealthAI Platform', 'industry': 'healthcare', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered healthcare diagnostics and treatment planning'},
                    {'name': 'TeleMed Solutions', 'industry': 'healthcare', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Telemedicine platform for remote healthcare delivery'},
                    {'name': 'PharmaTech Labs', 'industry': 'healthcare', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Pharmaceutical technology and drug discovery platform'},
                    {'name': 'Mental Health AI', 'industry': 'healthcare', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'AI-powered mental health assessment and therapy'},
                    {'name': 'Genomics Data Corp', 'industry': 'healthcare', 'revenue_range': '10m_50m', 'funding_stage': 'series_b', 'description': 'Genomic data analysis for personalized medicine'},
                    {'name': 'Wearable Health Tech', 'industry': 'healthcare', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Wearable health monitoring devices and apps'},
                    {'name': 'Clinical Trial AI', 'industry': 'healthcare', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'AI-optimized clinical trial management platform'},
                    {'name': 'Medical Imaging AI', 'industry': 'healthcare', 'revenue_range': '10m_50m', 'funding_stage': 'series_b', 'description': 'AI-powered medical imaging analysis'},
                    {'name': 'Health Data Analytics', 'industry': 'healthcare', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Healthcare data analytics and insights platform'},
                    
                    # Finance Companies
                    {'name': 'FinTech Solutions', 'industry': 'finance', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Digital banking and payment solutions'},
                    {'name': 'Crypto Trading Pro', 'industry': 'finance', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Cryptocurrency trading and investment platform'},
                    {'name': 'InsurTech AI', 'industry': 'finance', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered insurance underwriting and claims processing'},
                    {'name': 'Wealth Management AI', 'industry': 'finance', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Automated wealth management and investment advisory'},
                    {'name': 'RegTech Compliance', 'industry': 'finance', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Regulatory technology for financial compliance'},
                    {'name': 'Peer-to-Peer Lending', 'industry': 'finance', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'P2P lending platform with AI risk assessment'},
                    {'name': 'Digital Asset Management', 'industry': 'finance', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Digital asset custody and management solutions'},
                    {'name': 'Fraud Detection AI', 'industry': 'finance', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'AI-powered fraud detection for financial transactions'},
                    {'name': 'Credit Scoring AI', 'industry': 'finance', 'revenue_range': '10m_50m', 'funding_stage': 'series_b', 'description': 'Alternative credit scoring using AI and big data'},
                    {'name': 'Financial Planning AI', 'industry': 'finance', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'AI-powered financial planning and budgeting tools'},
                    
                    # E-commerce Companies
                    {'name': 'E-Commerce Platform Pro', 'industry': 'ecommerce', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Complete e-commerce platform for online stores'},
                    {'name': 'Dropshipping AI', 'industry': 'ecommerce', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered dropshipping automation platform'},
                    {'name': 'Inventory Management AI', 'industry': 'ecommerce', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Smart inventory management for e-commerce'},
                    {'name': 'Customer Service AI', 'industry': 'ecommerce', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered customer service for online stores'},
                    {'name': 'Price Optimization AI', 'industry': 'ecommerce', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Dynamic pricing optimization for e-commerce'},
                    {'name': 'Social Commerce Platform', 'industry': 'ecommerce', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Social media integrated e-commerce platform'},
                    {'name': 'Mobile Commerce App', 'industry': 'ecommerce', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Mobile-first e-commerce application'},
                    {'name': 'Subscription Box AI', 'industry': 'ecommerce', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered subscription box curation'},
                    {'name': 'Marketplace Platform', 'industry': 'ecommerce', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Multi-vendor marketplace platform'},
                    {'name': 'E-commerce Analytics', 'industry': 'ecommerce', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'Advanced analytics for e-commerce businesses'},
                    
                    # Education Companies
                    {'name': 'EdTech Learning Platform', 'industry': 'education', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Online learning platform with AI personalization'},
                    {'name': 'Language Learning AI', 'industry': 'education', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered language learning application'},
                    {'name': 'Virtual Classroom Pro', 'industry': 'education', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Virtual classroom and remote learning platform'},
                    {'name': 'Skill Assessment AI', 'industry': 'education', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered skill assessment and certification'},
                    {'name': 'Corporate Training AI', 'industry': 'education', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Corporate training and development platform'},
                    {'name': 'Student Success AI', 'industry': 'education', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered student success and retention platform'},
                    {'name': 'Educational Content AI', 'industry': 'education', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-generated educational content and curriculum'},
                    {'name': 'Tutoring Platform AI', 'industry': 'education', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered tutoring and homework help platform'},
                    {'name': 'Campus Management AI', 'industry': 'education', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Campus management and administration platform'},
                    {'name': 'Learning Analytics AI', 'industry': 'education', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'Learning analytics and performance tracking'},
                    
                    # Manufacturing Companies
                    {'name': 'Smart Manufacturing AI', 'industry': 'manufacturing', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered smart manufacturing solutions'},
                    {'name': 'Quality Control AI', 'industry': 'manufacturing', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered quality control and inspection'},
                    {'name': 'Supply Chain AI', 'industry': 'manufacturing', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Supply chain optimization and management'},
                    {'name': 'Predictive Maintenance AI', 'industry': 'manufacturing', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Predictive maintenance for manufacturing equipment'},
                    {'name': '3D Printing Solutions', 'industry': 'manufacturing', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'Advanced 3D printing technology and services'},
                    {'name': 'Robotics Automation', 'industry': 'manufacturing', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Industrial robotics and automation solutions'},
                    {'name': 'Digital Twin Technology', 'industry': 'manufacturing', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Digital twin technology for manufacturing processes'},
                    {'name': 'Energy Management AI', 'industry': 'manufacturing', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Energy management and optimization for manufacturing'},
                    {'name': 'Inventory Optimization AI', 'industry': 'manufacturing', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered inventory optimization'},
                    {'name': 'Manufacturing Analytics', 'industry': 'manufacturing', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Manufacturing analytics and insights platform'},
                    
                    # Real Estate Companies
                    {'name': 'PropTech Solutions', 'industry': 'real_estate', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Property technology platform for real estate management'},
                    {'name': 'Virtual Tours AI', 'industry': 'real_estate', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered virtual property tours and visualization'},
                    {'name': 'Property Valuation AI', 'industry': 'real_estate', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered property valuation and appraisal'},
                    {'name': 'Real Estate Analytics', 'industry': 'real_estate', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Real estate market analytics and insights'},
                    {'name': 'Property Management AI', 'industry': 'real_estate', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered property management platform'},
                    {'name': 'Mortgage Processing AI', 'industry': 'real_estate', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Automated mortgage processing and approval'},
                    {'name': 'Tenant Screening AI', 'industry': 'real_estate', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered tenant screening and background checks'},
                    {'name': 'Real Estate Investment AI', 'industry': 'real_estate', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered real estate investment analysis'},
                    {'name': 'Facility Management AI', 'industry': 'real_estate', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Smart facility management and maintenance'},
                    {'name': 'Commercial Real Estate AI', 'industry': 'real_estate', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Commercial real estate analytics and insights'},
                    
                    # Transportation Companies
                    {'name': 'Autonomous Vehicle Tech', 'industry': 'transportation', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Autonomous vehicle technology and solutions'},
                    {'name': 'Fleet Management AI', 'industry': 'transportation', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered fleet management and optimization'},
                    {'name': 'Logistics Optimization AI', 'industry': 'transportation', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Logistics and route optimization platform'},
                    {'name': 'Ride-Sharing AI', 'industry': 'transportation', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered ride-sharing and mobility platform'},
                    {'name': 'Traffic Management AI', 'industry': 'transportation', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Smart traffic management and optimization'},
                    {'name': 'Electric Vehicle Charging', 'industry': 'transportation', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Electric vehicle charging infrastructure and services'},
                    {'name': 'Drone Delivery AI', 'industry': 'transportation', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered drone delivery and logistics'},
                    {'name': 'Public Transit AI', 'industry': 'transportation', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Smart public transit management and optimization'},
                    {'name': 'Parking Management AI', 'industry': 'transportation', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered parking management and optimization'},
                    {'name': 'Transportation Analytics', 'industry': 'transportation', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Transportation analytics and insights platform'},
                    
                    # Energy Companies
                    {'name': 'Renewable Energy AI', 'industry': 'energy', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered renewable energy optimization'},
                    {'name': 'Smart Grid Technology', 'industry': 'energy', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Smart grid technology and energy management'},
                    {'name': 'Energy Storage AI', 'industry': 'energy', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered energy storage and battery optimization'},
                    {'name': 'Carbon Trading Platform', 'industry': 'energy', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Carbon trading and offset platform'},
                    {'name': 'Energy Efficiency AI', 'industry': 'energy', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered energy efficiency optimization'},
                    {'name': 'Solar Energy AI', 'industry': 'energy', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered solar energy optimization and management'},
                    {'name': 'Wind Energy Analytics', 'industry': 'energy', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Wind energy analytics and optimization'},
                    {'name': 'Nuclear Energy AI', 'industry': 'energy', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered nuclear energy safety and optimization'},
                    {'name': 'Energy Trading AI', 'industry': 'energy', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered energy trading and market analysis'},
                    {'name': 'Microgrid Solutions', 'industry': 'energy', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Microgrid technology and energy management'},
                    
                    # Entertainment Companies
                    {'name': 'Gaming AI Platform', 'industry': 'entertainment', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered gaming platform and experiences'},
                    {'name': 'Content Creation AI', 'industry': 'entertainment', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered content creation and media production'},
                    {'name': 'Streaming Analytics AI', 'industry': 'entertainment', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Streaming analytics and content optimization'},
                    {'name': 'Virtual Reality Gaming', 'industry': 'entertainment', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Virtual reality gaming and entertainment'},
                    {'name': 'Music AI Platform', 'industry': 'entertainment', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered music creation and recommendation'},
                    {'name': 'Sports Analytics AI', 'industry': 'entertainment', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered sports analytics and performance tracking'},
                    {'name': 'Live Event AI', 'industry': 'entertainment', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered live event management and optimization'},
                    {'name': 'Film Production AI', 'industry': 'entertainment', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered film production and post-production'},
                    {'name': 'Podcast Analytics AI', 'industry': 'entertainment', 'revenue_range': '5m_20m', 'funding_stage': 'series_a', 'description': 'AI-powered podcast analytics and optimization'},
                    {'name': 'Social Media AI', 'industry': 'entertainment', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered social media content and engagement'},
                    
                    # Food & Agriculture Companies
                    {'name': 'AgTech Solutions', 'industry': 'food_agriculture', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Agricultural technology and precision farming'},
                    {'name': 'Food Safety AI', 'industry': 'food_agriculture', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered food safety monitoring and compliance'},
                    {'name': 'Vertical Farming AI', 'industry': 'food_agriculture', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered vertical farming and urban agriculture'},
                    {'name': 'Crop Monitoring AI', 'industry': 'food_agriculture', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered crop monitoring and yield optimization'},
                    {'name': 'Food Delivery AI', 'industry': 'food_agriculture', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'AI-powered food delivery and logistics'},
                    {'name': 'Livestock Management AI', 'industry': 'food_agriculture', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered livestock monitoring and health management'},
                    {'name': 'Supply Chain Food AI', 'industry': 'food_agriculture', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Food supply chain optimization and traceability'},
                    {'name': 'Plant-Based Food Tech', 'industry': 'food_agriculture', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Plant-based food technology and alternatives'},
                    {'name': 'Food Waste AI', 'industry': 'food_agriculture', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered food waste reduction and management'},
                    {'name': 'Agricultural Robotics', 'industry': 'food_agriculture', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Agricultural robotics and automation solutions'},
                    
                    # Additional Companies for Diversity
                    {'name': 'LegalTech AI', 'industry': 'legal', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered legal research and document analysis'},
                    {'name': 'Marketing Automation AI', 'industry': 'marketing', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'AI-powered marketing automation and optimization'},
                    {'name': 'HR Tech Solutions', 'industry': 'human_resources', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'AI-powered HR technology and recruitment'},
                    {'name': 'Environmental Monitoring AI', 'industry': 'environmental', 'revenue_range': '1m_10m', 'funding_stage': 'seed', 'description': 'AI-powered environmental monitoring and conservation'},
                    {'name': 'Space Technology Corp', 'industry': 'aerospace', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Space technology and satellite solutions'},
                    {'name': 'Biotech Innovations', 'industry': 'biotechnology', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Biotechnology innovations and research platform'},
                    {'name': 'Nanotech Solutions', 'industry': 'nanotechnology', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'Nanotechnology applications and research'},
                    {'name': 'Quantum Tech Labs', 'industry': 'quantum_computing', 'revenue_range': '20m_100m', 'funding_stage': 'series_c', 'description': 'Quantum computing technology and applications'},
                    {'name': 'Robotics Automation Pro', 'industry': 'robotics', 'revenue_range': '10m_50m', 'funding_stage': 'series_a', 'description': 'Advanced robotics and automation solutions'},
                    {'name': 'IoT Platform Solutions', 'industry': 'internet_of_things', 'revenue_range': '5m_20m', 'funding_stage': 'series_b', 'description': 'IoT platform and connectivity solutions'},
                ]
                
                # Create companies
                companies = []
                for company_data in companies_data:
                    company = Company.objects.create(
                        name=company_data['name'],
                        industry=company_data['industry'],
                        revenue_range=company_data['revenue_range'],
                        funding_stage=company_data['funding_stage'],
                        description=company_data['description'],
                        is_active=True
                    )
                    companies.append(company)
                
                # Create sample investment thesis
                thesis = InvestmentThesis.objects.create(
                    text="We are looking to invest in B2B SaaS companies in the technology sector with Series A-B funding, focusing on enterprise software solutions with $1M-$50M revenue range.",
                    analysis_summary="Focus on B2B SaaS technology companies",
                    extracted_criteria={
                        'industries': ['technology'],
                        'revenue_ranges': ['1m_10m', '10m_50m'],
                        'funding_stages': ['series_a', 'series_b'],
                        'keywords': ['saas', 'b2b', 'enterprise', 'software']
                    },
                    sentiment_score=0.8,
                    confidence_score=0.85
                )
                
                # Create sample deals
                sample_deals = [
                    {
                        'title': 'TechFlow Solutions Investment',
                        'company': companies[0],
                        'thesis': thesis,
                        'status': 'prospecting',
                        'value': 5000000,
                        'fit_score': 0.85
                    },
                    {
                        'title': 'CloudSync Pro Partnership',
                        'company': companies[1],
                        'thesis': thesis,
                        'status': 'qualification',
                        'value': 8000000,
                        'fit_score': 0.78
                    },
                    {
                        'title': 'DataViz Analytics Deal',
                        'company': companies[2],
                        'thesis': thesis,
                        'status': 'proposal',
                        'value': 12000000,
                        'fit_score': 0.92
                    }
                ]
                
                for deal_data in sample_deals:
                    Deal.objects.create(
                        title=deal_data['title'],
                        company=deal_data['company'],
                        thesis=deal_data['thesis'],
                        status=deal_data['status'],
                        value=deal_data['value'],
                        fit_score=deal_data['fit_score'],
                        is_active=True
                    )
                
                # Update embeddings for all companies
                embedding_service = EmbeddingService()
                embedding_service.update_embeddings()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added {len(companies)} companies, 1 thesis, and {len(sample_deals)} deals!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error adding sample data: {e}')
            )
            raise 