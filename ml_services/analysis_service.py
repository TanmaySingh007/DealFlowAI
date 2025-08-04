"""
Enhanced Analysis service for DealFlowAI using advanced ML and Hugging Face models
"""

import re
import json
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
from transformers import pipeline, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
from textblob import TextBlob
import spacy
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EnhancedInvestmentAnalysisService:
    """Enhanced service for analyzing investment theses and company matching using advanced AI"""
    
    def __init__(self):
        """Initialize the enhanced analysis service with Hugging Face models"""
        try:
            # Initialize Hugging Face models
            self.sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
            self.text_classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn-samsum")
            
            # Initialize sentence transformer for embeddings
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load spaCy for advanced NLP
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Download if not available
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")
            
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=2000,
                stop_words='english',
                ngram_range=(1, 3)
            )
            
            # Enhanced industry keywords with confidence scores
            self.industry_keywords = {
                'software': {
                    'keywords': ['software', 'saas', 'platform', 'application', 'enterprise', 'cloud', 'api', 'microservices'],
                    'confidence': 0.9
                },
                'fintech': {
                    'keywords': ['fintech', 'financial', 'banking', 'payment', 'blockchain', 'crypto', 'insurtech', 'wealthtech'],
                    'confidence': 0.85
                },
                'healthcare': {
                    'keywords': ['healthcare', 'medical', 'health', 'biotech', 'pharma', 'telemedicine', 'digital health'],
                    'confidence': 0.9
                },
                'energy': {
                    'keywords': ['energy', 'renewable', 'solar', 'wind', 'clean', 'sustainability', 'carbon', 'green'],
                    'confidence': 0.8
                },
                'education': {
                    'keywords': ['education', 'edtech', 'learning', 'training', 'online learning', 'skill development'],
                    'confidence': 0.85
                },
                'retail': {
                    'keywords': ['retail', 'ecommerce', 'consumer', 'marketplace', 'omnichannel', 'd2c'],
                    'confidence': 0.8
                },
                'logistics': {
                    'keywords': ['logistics', 'supply chain', 'transportation', 'warehouse', 'fulfillment', 'last mile'],
                    'confidence': 0.85
                },
                'cybersecurity': {
                    'keywords': ['cybersecurity', 'security', 'privacy', 'threat', 'zero trust', 'identity', 'compliance'],
                    'confidence': 0.9
                },
                'ai_ml': {
                    'keywords': ['ai', 'machine learning', 'artificial intelligence', 'ml', 'deep learning', 'neural networks'],
                    'confidence': 0.95
                },
            }
            
            # Revenue range mapping with fuzzy matching
            self.revenue_ranges = {
                'under_1m': {'range': (0, 1), 'keywords': ['under 1m', 'less than 1m', 'early stage']},
                '1_5m': {'range': (1, 5), 'keywords': ['1m to 5m', '1-5m', 'growth stage']},
                '5_20m': {'range': (5, 20), 'keywords': ['5m to 20m', '5-20m', 'scale up']},
                '20_100m': {'range': (20, 100), 'keywords': ['20m to 100m', '20-100m', 'mature']},
                '100m_plus': {'range': (100, float('inf')), 'keywords': ['100m+', 'enterprise', 'large scale']},
            }
            
            # Funding stage progression with market context
            self.funding_stages = {
                'seed': {'stage': 1, 'keywords': ['seed', 'pre-seed', 'angel'], 'market_context': 'early'},
                'series_a': {'stage': 2, 'keywords': ['series a', 'series-a'], 'market_context': 'growth'},
                'series_b': {'stage': 3, 'keywords': ['series b', 'series-b'], 'market_context': 'scale'},
                'series_c': {'stage': 4, 'keywords': ['series c', 'series-c'], 'market_context': 'expansion'},
                'series_d': {'stage': 5, 'keywords': ['series d', 'series-d'], 'market_context': 'late'},
                'ipo': {'stage': 6, 'keywords': ['ipo', 'public offering'], 'market_context': 'exit'},
                'public': {'stage': 7, 'keywords': ['public', 'listed'], 'market_context': 'public'},
            }
            
            logger.info("Enhanced Investment Analysis Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing enhanced analysis service: {e}")
            # Fallback to basic initialization
            self._initialize_basic()
    
    def _initialize_basic(self):
        """Fallback initialization for basic functionality"""
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.industry_keywords = {
            'software': ['software', 'saas', 'platform'],
            'fintech': ['fintech', 'financial', 'banking'],
            'healthcare': ['healthcare', 'medical', 'health'],
            'ai_ml': ['ai', 'machine learning', 'artificial intelligence'],
        }
        self.revenue_ranges = {
            'under_1m': (0, 1),
            '1_5m': (1, 5),
            '5_20m': (5, 20),
            '20_100m': (20, 100),
            '100m_plus': (100, float('inf')),
        }
    
    async def analyze_thesis_advanced(self, thesis_text: str) -> Dict[str, Any]:
        """
        Advanced thesis analysis using multiple AI models
        
        Args:
            thesis_text: Investment thesis text
            
        Returns:
            Comprehensive analysis results
        """
        try:
            # Parallel processing for different analysis types
            tasks = [
                self._extract_criteria_advanced(thesis_text),
                self._analyze_sentiment(thesis_text),
                self._generate_summary(thesis_text),
                self._extract_entities(thesis_text),
                self._calculate_risk_score(thesis_text)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            criteria, sentiment, summary, entities, risk_score = results
            
            # Generate embedding
            embedding = self.sentence_transformer.encode(thesis_text)
            
            analysis = {
                'criteria': criteria,
                'sentiment': sentiment,
                'summary': summary,
                'entities': entities,
                'risk_score': risk_score,
                'embedding': embedding.tolist(),
                'confidence_score': self._calculate_confidence_score(criteria, sentiment),
                'market_timing': self._analyze_market_timing(thesis_text),
                'competitive_landscape': self._analyze_competitive_landscape(thesis_text),
                'timestamp': datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in advanced thesis analysis: {e}")
            return self._fallback_analysis(thesis_text)
    
    async def _extract_criteria_advanced(self, thesis_text: str) -> Dict[str, Any]:
        """Extract investment criteria using advanced NLP"""
        try:
            doc = self.nlp(thesis_text.lower())
            
            # Extract industries with confidence scores
            industries = []
            for industry, data in self.industry_keywords.items():
                keyword_matches = sum(1 for keyword in data['keywords'] 
                                   if keyword in thesis_text.lower())
                if keyword_matches > 0:
                    confidence = min(keyword_matches / len(data['keywords']), 1.0) * data['confidence']
                    industries.append({
                        'industry': industry,
                        'confidence': confidence,
                        'keywords_found': keyword_matches
                    })
            
            # Extract revenue ranges with fuzzy matching
            revenue_ranges = []
            for range_key, data in self.revenue_ranges.items():
                for keyword in data['keywords']:
                    if keyword in thesis_text.lower():
                        revenue_ranges.append({
                            'range': range_key,
                            'confidence': 0.8,
                            'keywords_found': [keyword]
                        })
                        break
            
            # Extract funding stages with context
            funding_stages = []
            for stage_key, data in self.funding_stages.items():
                for keyword in data['keywords']:
                    if keyword in thesis_text.lower():
                        funding_stages.append({
                            'stage': stage_key,
                            'confidence': 0.9,
                            'market_context': data['market_context'],
                            'keywords_found': [keyword]
                        })
                        break
            
            # Extract business models using classification
            business_models = self._extract_business_models(thesis_text)
            
            # Extract geographic preferences
            geographic_preferences = self._extract_geographic_preferences(thesis_text)
            
            return {
                'industries': industries,
                'revenue_ranges': revenue_ranges,
                'funding_stages': funding_stages,
                'business_models': business_models,
                'geographic_preferences': geographic_preferences,
                'thesis_text': thesis_text
            }
            
        except Exception as e:
            logger.error(f"Error in advanced criteria extraction: {e}")
            return self._extract_thesis_criteria_basic(thesis_text)
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Hugging Face models"""
        try:
            # Analyze overall sentiment
            sentiment_result = self.sentiment_analyzer(text[:512])[0]
            
            # Analyze specific aspects
            aspects = {
                'market_optimism': self._analyze_aspect_sentiment(text, ['growth', 'opportunity', 'potential']),
                'risk_aversion': self._analyze_aspect_sentiment(text, ['risk', 'caution', 'concern']),
                'confidence': self._analyze_aspect_sentiment(text, ['confidence', 'certainty', 'conviction'])
            }
            
            return {
                'overall_sentiment': sentiment_result['label'],
                'confidence': sentiment_result['score'],
                'aspects': aspects,
                'sentiment_score': self._calculate_sentiment_score(sentiment_result, aspects)
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {'overall_sentiment': 'neutral', 'confidence': 0.5}
    
    async def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate summary using Hugging Face summarization"""
        try:
            if len(text) > 100:
                summary_result = self.summarizer(text[:1024], max_length=150, min_length=50)[0]
                return {
                    'summary': summary_result['summary_text'],
                    'confidence': 0.8
                }
            else:
                return {
                    'summary': text,
                    'confidence': 1.0
                }
        except Exception as e:
            logger.error(f"Error in summary generation: {e}")
            return {'summary': text[:200] + '...', 'confidence': 0.5}
    
    async def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities using spaCy"""
        try:
            doc = self.nlp(text)
            entities = {
                'organizations': [],
                'locations': [],
                'dates': [],
                'money': [],
                'percentages': []
            }
            
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'].append(ent.text)
                elif ent.label_ == 'GPE':
                    entities['locations'].append(ent.text)
                elif ent.label_ == 'DATE':
                    entities['dates'].append(ent.text)
                elif ent.label_ == 'MONEY':
                    entities['money'].append(ent.text)
                elif ent.label_ == 'PERCENT':
                    entities['percentages'].append(ent.text)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error in entity extraction: {e}")
            return {'organizations': [], 'locations': [], 'dates': [], 'money': [], 'percentages': []}
    
    async def _calculate_risk_score(self, text: str) -> Dict[str, Any]:
        """Calculate risk score based on thesis content"""
        try:
            risk_keywords = [
                'high risk', 'volatile', 'uncertain', 'unproven', 'experimental',
                'early stage', 'unregulated', 'competitive', 'saturated market'
            ]
            
            risk_score = 0.0
            risk_factors = []
            
            text_lower = text.lower()
            for keyword in risk_keywords:
                if keyword in text_lower:
                    risk_score += 0.1
                    risk_factors.append(keyword)
            
            # Normalize risk score
            risk_score = min(risk_score, 1.0)
            
            return {
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error in risk score calculation: {e}")
            return {'risk_score': 0.5, 'risk_factors': [], 'risk_level': 'medium'}
    
    def _extract_business_models(self, text: str) -> List[Dict[str, Any]]:
        """Extract business models using classification"""
        try:
            business_model_categories = [
                "B2B SaaS",
                "B2C Marketplace", 
                "Subscription Model",
                "Platform as a Service",
                "Freemium Model",
                "Transaction-based",
                "Licensing Model"
            ]
            
            models = []
            for category in business_model_categories:
                # Simple keyword matching for now
                keywords = category.lower().replace(' ', '').replace('-', '')
                if any(keyword in text.lower() for keyword in keywords.split()):
                    models.append({
                        'model': category,
                        'confidence': 0.8
                    })
            
            return models
            
        except Exception as e:
            logger.error(f"Error extracting business models: {e}")
            return []
    
    def _extract_geographic_preferences(self, text: str) -> List[Dict[str, Any]]:
        """Extract geographic preferences"""
        try:
            regions = {
                'North America': ['us', 'usa', 'united states', 'canada', 'north america'],
                'Europe': ['europe', 'eu', 'uk', 'germany', 'france'],
                'Asia Pacific': ['asia', 'china', 'india', 'japan', 'singapore'],
                'Latin America': ['latin america', 'brazil', 'mexico', 'argentina'],
                'Middle East': ['middle east', 'uae', 'saudi arabia', 'israel']
            }
            
            preferences = []
            for region, keywords in regions.items():
                if any(keyword in text.lower() for keyword in keywords):
                    preferences.append({
                        'region': region,
                        'confidence': 0.8
                    })
            
            return preferences
            
        except Exception as e:
            logger.error(f"Error extracting geographic preferences: {e}")
            return []
    
    def _analyze_aspect_sentiment(self, text: str, aspect_keywords: List[str]) -> Dict[str, Any]:
        """Analyze sentiment for specific aspects"""
        try:
            aspect_texts = []
            for keyword in aspect_keywords:
                if keyword in text.lower():
                    # Extract sentences containing the keyword
                    sentences = [s.strip() for s in text.split('.') if keyword in s.lower()]
                    aspect_texts.extend(sentences)
            
            if aspect_texts:
                combined_text = '. '.join(aspect_texts[:3])  # Limit to 3 sentences
                result = self.sentiment_analyzer(combined_text[:512])[0]
                return {
                    'sentiment': result['label'],
                    'confidence': result['score']
                }
            else:
                return {'sentiment': 'neutral', 'confidence': 0.5}
                
        except Exception as e:
            logger.error(f"Error in aspect sentiment analysis: {e}")
            return {'sentiment': 'neutral', 'confidence': 0.5}
    
    def _calculate_sentiment_score(self, overall_result: Dict, aspects: Dict) -> float:
        """Calculate overall sentiment score"""
        try:
            # Convert sentiment labels to scores
            sentiment_map = {'positive': 1.0, 'neutral': 0.5, 'negative': 0.0}
            
            overall_score = sentiment_map.get(overall_result['label'], 0.5)
            
            # Weight different aspects
            aspect_scores = []
            for aspect_name, aspect_result in aspects.items():
                aspect_score = sentiment_map.get(aspect_result['sentiment'], 0.5)
                aspect_scores.append(aspect_score)
            
            # Calculate weighted average
            if aspect_scores:
                final_score = (overall_score * 0.6 + sum(aspect_scores) / len(aspect_scores) * 0.4)
            else:
                final_score = overall_score
            
            return final_score
            
        except Exception as e:
            logger.error(f"Error calculating sentiment score: {e}")
            return 0.5
    
    def _calculate_confidence_score(self, criteria: Dict, sentiment: Dict) -> float:
        """Calculate overall confidence score for the analysis"""
        try:
            confidence_factors = []
            
            # Criteria confidence
            if criteria.get('industries'):
                confidence_factors.append(0.8)
            if criteria.get('revenue_ranges'):
                confidence_factors.append(0.7)
            if criteria.get('funding_stages'):
                confidence_factors.append(0.7)
            
            # Sentiment confidence
            if sentiment.get('confidence'):
                confidence_factors.append(sentiment['confidence'])
            
            if confidence_factors:
                return sum(confidence_factors) / len(confidence_factors)
            else:
                return 0.5
                
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _analyze_market_timing(self, text: str) -> Dict[str, Any]:
        """Analyze market timing indicators"""
        try:
            timing_indicators = {
                'early_adopter': ['early', 'pioneer', 'first mover', 'emerging'],
                'growth_phase': ['growth', 'scaling', 'expansion', 'momentum'],
                'mature_market': ['mature', 'established', 'consolidation', 'saturated'],
                'recession_resistant': ['recession', 'downturn', 'resilient', 'defensive']
            }
            
            timing_analysis = {}
            for timing_type, keywords in timing_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in text.lower())
                timing_analysis[timing_type] = {
                    'indicated': matches > 0,
                    'confidence': min(matches / len(keywords), 1.0)
                }
            
            return timing_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing market timing: {e}")
            return {}
    
    def _analyze_competitive_landscape(self, text: str) -> Dict[str, Any]:
        """Analyze competitive landscape indicators"""
        try:
            competitive_indicators = {
                'high_competition': ['competitive', 'crowded', 'saturated', 'many players'],
                'low_competition': ['unique', 'niche', 'unserved', 'blue ocean'],
                'barriers_to_entry': ['barriers', 'moat', 'proprietary', 'patent'],
                'network_effects': ['network', 'platform', 'ecosystem', 'community']
            }
            
            competitive_analysis = {}
            for indicator_type, keywords in competitive_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in text.lower())
                competitive_analysis[indicator_type] = {
                    'indicated': matches > 0,
                    'confidence': min(matches / len(keywords), 1.0)
                }
            
            return competitive_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing competitive landscape: {e}")
            return {}
    
    def _fallback_analysis(self, thesis_text: str) -> Dict[str, Any]:
        """Fallback analysis when advanced models fail"""
        return {
            'criteria': self._extract_thesis_criteria_basic(thesis_text),
            'sentiment': {'overall_sentiment': 'neutral', 'confidence': 0.5},
            'summary': {'summary': thesis_text[:200] + '...', 'confidence': 0.5},
            'entities': {'organizations': [], 'locations': [], 'dates': [], 'money': [], 'percentages': []},
            'risk_score': {'risk_score': 0.5, 'risk_factors': [], 'risk_level': 'medium'},
            'embedding': [],
            'confidence_score': 0.5,
            'market_timing': {},
            'competitive_landscape': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_thesis_criteria_basic(self, thesis_text: str) -> Dict[str, Any]:
        """Basic criteria extraction as fallback"""
        thesis_lower = thesis_text.lower()
        
        industries = []
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in thesis_lower for keyword in keywords):
                industries.append(industry)
        
        revenue_ranges = []
        for range_key, (min_val, max_val) in self.revenue_ranges.items():
            if any(str(val) in thesis_lower for val in range(min_val, min(max_val, 100))):
                revenue_ranges.append(range_key)
        
        return {
            'industries': industries,
            'revenue_ranges': revenue_ranges,
            'funding_stages': [],
            'business_models': [],
            'geographic_preferences': [],
            'thesis_text': thesis_text
        }
    
    async def find_matching_companies_advanced(self, thesis_text: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Find companies matching the investment thesis using advanced AI
        
        Args:
            thesis_text: Investment thesis text
            top_k: Number of top matches to return
            
        Returns:
            List of matching companies with detailed analysis
        """
        try:
            from deals.models import Company
            
            # Get advanced analysis
            analysis = await self.analyze_thesis_advanced(thesis_text)
            criteria = analysis['criteria']
            
            # Get all active companies
            companies = Company.objects.filter(is_active=True)
            
            matches = []
            
            for company in companies:
                # Calculate advanced fit score
                fit_score = await self._calculate_advanced_fit_score(company, analysis)
                
                if fit_score > 0.1:  # Only include companies with some fit
                    # Generate detailed analysis
                    detailed_analysis = await self._generate_company_analysis(company, analysis)
                    
                    matches.append({
                        'company': company,
                        'fit_score': fit_score,
                        'analysis': detailed_analysis,
                        'recommendation': self._generate_recommendation(fit_score, detailed_analysis),
                        'risk_assessment': self._assess_company_risk(company, analysis),
                        'market_opportunity': self._assess_market_opportunity(company, analysis)
                    })
            
            # Sort by fit score and return top k
            matches.sort(key=lambda x: x['fit_score'], reverse=True)
            return matches[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding matching companies: {e}")
            return []
    
    async def _calculate_advanced_fit_score(self, company, analysis: Dict[str, Any]) -> float:
        """Calculate advanced fit score using multiple factors"""
        try:
            score = 0.0
            weights = {
                'industry': 0.25,
                'revenue': 0.20,
                'funding': 0.20,
                'sentiment': 0.15,
                'risk': 0.10,
                'market_timing': 0.10
            }
            
            criteria = analysis.get('criteria', {})
            sentiment = analysis.get('sentiment', {})
            
            # Industry match with confidence
            thesis_industries = [ind['industry'] for ind in criteria.get('industries', [])]
            if company.industry in thesis_industries:
                score += weights['industry']
            elif any(industry in company.industry for industry in thesis_industries):
                score += weights['industry'] * 0.7
            
            # Revenue range match
            thesis_revenue_ranges = [rng['range'] for rng in criteria.get('revenue_ranges', [])]
            if company.revenue_range in thesis_revenue_ranges:
                score += weights['revenue']
            
            # Funding stage match
            thesis_funding_stages = [stage['stage'] for stage in criteria.get('funding_stages', [])]
            if company.funding_stage in thesis_funding_stages:
                score += weights['funding']
            
            # Sentiment alignment
            sentiment_score = sentiment.get('sentiment_score', 0.5)
            if sentiment_score > 0.6:  # Positive sentiment
                score += weights['sentiment']
            elif sentiment_score < 0.4:  # Negative sentiment
                score += weights['sentiment'] * 0.3
            
            # Risk alignment
            risk_score = analysis.get('risk_score', {}).get('risk_score', 0.5)
            if risk_score < 0.4:  # Low risk thesis
                score += weights['risk']
            elif risk_score > 0.7:  # High risk thesis
                score += weights['risk'] * 0.5
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating advanced fit score: {e}")
            return 0.0
    
    async def _generate_company_analysis(self, company, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed analysis for a company"""
        try:
            return {
                'industry_match': company.industry in [ind['industry'] for ind in analysis.get('criteria', {}).get('industries', [])],
                'revenue_match': company.revenue_range in [rng['range'] for rng in analysis.get('criteria', {}).get('revenue_ranges', [])],
                'funding_match': company.funding_stage in [stage['stage'] for stage in analysis.get('criteria', {}).get('funding_stages', [])],
                'sentiment_alignment': analysis.get('sentiment', {}).get('sentiment_score', 0.5),
                'risk_alignment': analysis.get('risk_score', {}).get('risk_score', 0.5),
                'market_timing_alignment': self._check_market_timing_alignment(company, analysis),
                'competitive_position': self._assess_competitive_position(company, analysis)
            }
            
        except Exception as e:
            logger.error(f"Error generating company analysis: {e}")
            return {}
    
    def _generate_recommendation(self, fit_score: float, analysis: Dict[str, Any]) -> str:
        """Generate investment recommendation"""
        if fit_score > 0.8:
            return "Strong Buy"
        elif fit_score > 0.6:
            return "Buy"
        elif fit_score > 0.4:
            return "Hold"
        elif fit_score > 0.2:
            return "Review"
        else:
            return "Pass"
    
    def _assess_company_risk(self, company, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess company-specific risk factors"""
        try:
            risk_factors = []
            risk_score = 0.5
            
            # Early stage companies are higher risk
            if company.funding_stage in ['seed', 'series_a']:
                risk_factors.append('Early stage')
                risk_score += 0.2
            
            # Low revenue companies are higher risk
            if company.revenue_range in ['under_1m', '1_5m']:
                risk_factors.append('Low revenue')
                risk_score += 0.15
            
            # New companies are higher risk
            if company.founding_year and company.founding_year > 2020:
                risk_factors.append('New company')
                risk_score += 0.1
            
            return {
                'risk_score': min(risk_score, 1.0),
                'risk_factors': risk_factors,
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error assessing company risk: {e}")
            return {'risk_score': 0.5, 'risk_factors': [], 'risk_level': 'medium'}
    
    def _assess_market_opportunity(self, company, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market opportunity for the company"""
        try:
            opportunity_score = 0.5
            
            # Factors that increase opportunity
            if company.industry in ['ai_ml', 'fintech', 'healthcare']:
                opportunity_score += 0.2
            
            if company.funding_stage in ['series_a', 'series_b']:
                opportunity_score += 0.15
            
            if company.revenue_range in ['5_20m', '20_100m']:
                opportunity_score += 0.1
            
            return {
                'opportunity_score': min(opportunity_score, 1.0),
                'market_size': 'Large' if opportunity_score > 0.7 else 'Medium' if opportunity_score > 0.4 else 'Small',
                'growth_potential': 'High' if opportunity_score > 0.7 else 'Medium' if opportunity_score > 0.4 else 'Low'
            }
            
        except Exception as e:
            logger.error(f"Error assessing market opportunity: {e}")
            return {'opportunity_score': 0.5, 'market_size': 'Medium', 'growth_potential': 'Medium'}
    
    def _check_market_timing_alignment(self, company, analysis: Dict[str, Any]) -> bool:
        """Check if company aligns with market timing indicators"""
        try:
            market_timing = analysis.get('market_timing', {})
            
            # Check if company stage aligns with market timing
            if market_timing.get('early_adopter', {}).get('indicated', False):
                return company.funding_stage in ['seed', 'series_a']
            elif market_timing.get('growth_phase', {}).get('indicated', False):
                return company.funding_stage in ['series_a', 'series_b', 'series_c']
            elif market_timing.get('mature_market', {}).get('indicated', False):
                return company.funding_stage in ['series_c', 'series_d', 'ipo']
            
            return True  # Default to aligned if no specific timing indicators
            
        except Exception as e:
            logger.error(f"Error checking market timing alignment: {e}")
            return True
    
    def _assess_competitive_position(self, company, analysis: Dict[str, Any]) -> str:
        """Assess competitive position of the company"""
        try:
            competitive_landscape = analysis.get('competitive_landscape', {})
            
            if competitive_landscape.get('low_competition', {}).get('indicated', False):
                return "Blue Ocean"
            elif competitive_landscape.get('high_competition', {}).get('indicated', False):
                return "Red Ocean"
            elif competitive_landscape.get('barriers_to_entry', {}).get('indicated', False):
                return "Protected"
            else:
                return "Standard"
                
        except Exception as e:
            logger.error(f"Error assessing competitive position: {e}")
            return "Standard"


# Backward compatibility
InvestmentAnalysisService = EnhancedInvestmentAnalysisService 