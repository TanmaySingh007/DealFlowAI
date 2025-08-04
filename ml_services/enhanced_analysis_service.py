"""
Simplified Analysis service for DealFlowAI
"""

import re
import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SimplifiedInvestmentAnalysisService:
    """Simplified service for analyzing investment theses and company matching"""
    
    def __init__(self):
        """Initialize the simplified analysis service"""
        try:
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Industry keywords with confidence scores
            self.industry_keywords = {
                'software': {
                    'keywords': ['software', 'saas', 'platform', 'application', 'enterprise', 'cloud', 'api'],
                    'confidence': 0.9
                },
                'fintech': {
                    'keywords': ['fintech', 'financial', 'banking', 'payment', 'blockchain', 'crypto'],
                    'confidence': 0.85
                },
                'healthcare': {
                    'keywords': ['healthcare', 'medical', 'health', 'biotech', 'pharma', 'telemedicine'],
                    'confidence': 0.9
                },
                'energy': {
                    'keywords': ['energy', 'renewable', 'solar', 'wind', 'clean', 'sustainability'],
                    'confidence': 0.8
                },
                'education': {
                    'keywords': ['education', 'edtech', 'learning', 'training', 'online learning'],
                    'confidence': 0.85
                },
                'ai_ml': {
                    'keywords': ['ai', 'machine learning', 'artificial intelligence', 'ml', 'deep learning'],
                    'confidence': 0.95
                },
            }
            
            # Revenue range mapping
            self.revenue_ranges = {
                'under_1m': {'range': (0, 1), 'keywords': ['under 1m', 'less than 1m', 'early stage']},
                '1_5m': {'range': (1, 5), 'keywords': ['1m to 5m', '1-5m', 'growth stage']},
                '5_20m': {'range': (5, 20), 'keywords': ['5m to 20m', '5-20m', 'scale up']},
                '20_100m': {'range': (20, 100), 'keywords': ['20m to 100m', '20-100m', 'mature']},
                '100m_plus': {'range': (100, float('inf')), 'keywords': ['100m+', 'enterprise', 'large scale']},
            }
            
            # Funding stage progression
            self.funding_stages = {
                'seed': {'stage': 1, 'keywords': ['seed', 'pre-seed', 'angel']},
                'series_a': {'stage': 2, 'keywords': ['series a', 'series-a']},
                'series_b': {'stage': 3, 'keywords': ['series b', 'series-b']},
                'series_c': {'stage': 4, 'keywords': ['series c', 'series-c']},
                'series_d': {'stage': 5, 'keywords': ['series d', 'series-d']},
                'ipo': {'stage': 6, 'keywords': ['ipo', 'public offering']},
            }
            
            logger.info("Simplified Investment Analysis Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing simplified analysis service: {e}")
            self._initialize_basic()
    
    def _initialize_basic(self):
        """Fallback initialization for basic functionality"""
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
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
    
    def analyze_thesis(self, thesis_text: str) -> Dict[str, Any]:
        """
        Analyze investment thesis using simplified methods
        
        Args:
            thesis_text: Investment thesis text
            
        Returns:
            Analysis results
        """
        try:
            # Extract criteria
            criteria = self._extract_criteria_simple(thesis_text)
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment_simple(thesis_text)
            
            # Generate summary
            summary = self._generate_summary_simple(thesis_text)
            
            # Calculate confidence
            confidence = self._calculate_confidence_simple(criteria, sentiment)
            
            return {
                'criteria': criteria,
                'sentiment': sentiment,
                'summary': summary,
                'confidence_score': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in thesis analysis: {e}")
            return self._fallback_analysis(thesis_text)
    
    def _extract_criteria_simple(self, thesis_text: str) -> Dict[str, Any]:
        """Extract investment criteria using simple keyword matching"""
        try:
            thesis_lower = thesis_text.lower()
            
            # Extract industries
            industries = []
            for industry, data in self.industry_keywords.items():
                if isinstance(data, dict):
                    keywords = data['keywords']
                    confidence = data['confidence']
                else:
                    keywords = data
                    confidence = 0.8
                
                keyword_matches = sum(1 for keyword in keywords 
                                   if keyword in thesis_lower)
                if keyword_matches > 0:
                    industries.append({
                        'industry': industry,
                        'confidence': min(keyword_matches / len(keywords), 1.0) * confidence,
                        'keywords_found': keyword_matches
                    })
            
            # Extract revenue ranges
            revenue_ranges = []
            for range_key, data in self.revenue_ranges.items():
                if isinstance(data, dict):
                    keywords = data['keywords']
                else:
                    keywords = [range_key.replace('_', ' ')]
                
                for keyword in keywords:
                    if keyword in thesis_lower:
                        revenue_ranges.append({
                            'range': range_key,
                            'confidence': 0.8,
                            'keywords_found': [keyword]
                        })
                        break
            
            # Extract funding stages
            funding_stages = []
            for stage_key, data in self.funding_stages.items():
                keywords = data['keywords']
                for keyword in keywords:
                    if keyword in thesis_lower:
                        funding_stages.append({
                            'stage': stage_key,
                            'confidence': 0.9,
                            'keywords_found': [keyword]
                        })
                        break
            
            return {
                'industries': industries,
                'revenue_ranges': revenue_ranges,
                'funding_stages': funding_stages,
                'thesis_text': thesis_text
            }
            
        except Exception as e:
            logger.error(f"Error in criteria extraction: {e}")
            return {
                'industries': [{'industry': 'software', 'confidence': 0.8}],
                'revenue_ranges': [{'range': '1_5m', 'confidence': 0.7}],
                'funding_stages': [{'stage': 'series_a', 'confidence': 0.8}],
                'thesis_text': thesis_text
            }
    
    def _analyze_sentiment_simple(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using simple keyword matching"""
        try:
            positive_keywords = [
                'growth', 'opportunity', 'potential', 'strong', 'excellent',
                'innovative', 'leading', 'successful', 'profitable', 'scalable'
            ]
            
            negative_keywords = [
                'risk', 'concern', 'challenge', 'difficult', 'uncertain',
                'volatile', 'declining', 'weak', 'struggling', 'failing'
            ]
            
            text_lower = text.lower()
            
            positive_count = sum(1 for word in positive_keywords if word in text_lower)
            negative_count = sum(1 for word in negative_keywords if word in text_lower)
            
            total_sentiment_words = positive_count + negative_count
            
            if total_sentiment_words == 0:
                sentiment_score = 0.5
                sentiment_label = 'neutral'
            else:
                sentiment_score = positive_count / total_sentiment_words
                if sentiment_score > 0.6:
                    sentiment_label = 'positive'
                elif sentiment_score < 0.4:
                    sentiment_label = 'negative'
                else:
                    sentiment_label = 'neutral'
            
            return {
                'sentiment_label': sentiment_label,
                'sentiment_score': sentiment_score,
                'positive_words': positive_count,
                'negative_words': negative_count,
                'confidence': min(total_sentiment_words / 10, 1.0)
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                'sentiment_label': 'neutral',
                'sentiment_score': 0.5,
                'confidence': 0.5
            }
    
    def _generate_summary_simple(self, text: str) -> Dict[str, Any]:
        """Generate simple summary"""
        try:
            # Extract key sentences (first and last sentences)
            sentences = text.split('.')
            if len(sentences) > 1:
                summary = sentences[0].strip() + '. ' + sentences[-1].strip()
            else:
                summary = text[:200] + '...' if len(text) > 200 else text
            
            return {
                'summary': summary,
                'confidence': 0.8
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                'summary': text[:200] + '...' if len(text) > 200 else text,
                'confidence': 0.5
            }
    
    def _calculate_confidence_simple(self, criteria: Dict, sentiment: Dict) -> float:
        """Calculate overall confidence score"""
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
    
    def _fallback_analysis(self, thesis_text: str) -> Dict[str, Any]:
        """Fallback analysis when main analysis fails"""
        return {
            'criteria': {
                'industries': [{'industry': 'software', 'confidence': 0.8}],
                'revenue_ranges': [{'range': '1_5m', 'confidence': 0.7}],
                'funding_stages': [{'stage': 'series_a', 'confidence': 0.8}],
                'thesis_text': thesis_text
            },
            'sentiment': {
                'sentiment_label': 'neutral',
                'sentiment_score': 0.5,
                'confidence': 0.5
            },
            'summary': {
                'summary': thesis_text[:200] + '...' if len(thesis_text) > 200 else thesis_text,
                'confidence': 0.5
            },
            'confidence_score': 0.5,
            'timestamp': datetime.now().isoformat()
        }
    
    def find_matching_companies(self, thesis_text: str, companies: List[Dict], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Find companies matching the investment thesis
        
        Args:
            thesis_text: Investment thesis text
            companies: List of company dictionaries
            top_k: Number of top matches to return
            
        Returns:
            List of matching companies with scores
        """
        try:
            matches = []
            
            for company in companies:
                # Calculate similarity score
                similarity = self._calculate_company_similarity(thesis_text, company)
                
                if similarity > 0.1:  # Only include companies with some similarity
                    matches.append({
                        'id': company.get('id'),
                        'name': company.get('name'),
                        'industry': company.get('industry'),
                        'revenue_range': company.get('revenue_range'),
                        'funding_stage': company.get('funding_stage'),
                        'description': company.get('description'),
                        'fit_score': min(similarity + 0.2, 0.95),  # Boost score
                        'similarity_score': similarity
                    })
            
            # Sort by fit score and return top k
            matches.sort(key=lambda x: x['fit_score'], reverse=True)
            return matches[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding matching companies: {e}")
            return []
    
    def _calculate_company_similarity(self, thesis_text: str, company: Dict) -> float:
        """Calculate similarity between thesis and company"""
        try:
            thesis_lower = thesis_text.lower()
            company_text = f"{company.get('name', '')} {company.get('description', '')} {company.get('industry', '')}".lower()
            
            # Simple keyword matching
            thesis_words = set(thesis_lower.split())
            company_words = set(company_text.split())
            
            common_words = thesis_words & company_words
            similarity = len(common_words) / max(len(thesis_words), 1)
            
            return min(similarity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating company similarity: {e}")
            return 0.0


# Backward compatibility
InvestmentAnalysisService = SimplifiedInvestmentAnalysisService 