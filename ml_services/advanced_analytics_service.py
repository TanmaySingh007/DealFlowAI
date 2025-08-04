import logging
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import spacy
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class AdvancedAnalyticsService:
    """
    Advanced analytics service using Langchain and ML libraries for sophisticated thesis analysis
    """
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def analyze_thesis_advanced(self, thesis_text: str, companies_data: List[Dict]) -> Dict:
        """
        Advanced thesis analysis using multiple ML techniques
        """
        try:
            # 1. Sentiment analysis
            sentiment_scores = self._analyze_sentiment(thesis_text)
            
            # 2. Entity extraction
            entities = self._extract_entities(thesis_text)
            
            # 3. Advanced company matching
            matched_companies = self._advanced_company_matching(thesis_text, companies_data)
            
            # 4. Risk assessment
            risk_assessment = self._assess_risk(thesis_text, entities, sentiment_scores)
            
            # 5. Market opportunity analysis
            market_opportunity = self._analyze_market_opportunity(thesis_text, entities)
            
            # 6. Investment thesis scoring
            thesis_score = self._calculate_thesis_score(
                sentiment_scores, risk_assessment, market_opportunity
            )
            
            return {
                'sentiment_analysis': sentiment_scores,
                'entities': entities,
                'matched_companies': matched_companies,
                'risk_assessment': risk_assessment,
                'market_opportunity': market_opportunity,
                'thesis_score': thesis_score,
                'confidence_score': self._calculate_confidence_score(thesis_text),
                'recommendations': self._generate_advanced_recommendations(
                    thesis_score, risk_assessment, market_opportunity
                )
            }
            
        except Exception as e:
            logger.error(f"Error in advanced thesis analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Advanced sentiment analysis using multiple approaches"""
        try:
            # TextBlob sentiment
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment.polarity
            
            # HuggingFace sentiment
            hf_result = self.sentiment_analyzer(text[:512])[0]
            hf_sentiment = 1.0 if hf_result['label'] == 'POSITIVE' else -1.0
            
            # Combined sentiment score
            combined_sentiment = (textblob_sentiment + hf_sentiment) / 2
            
            return {
                'overall_sentiment': combined_sentiment,
                'textblob_sentiment': textblob_sentiment,
                'huggingface_sentiment': hf_sentiment,
                'sentiment_label': self._get_sentiment_label(combined_sentiment)
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {'overall_sentiment': 0, 'sentiment_label': 'neutral'}
    
    def _get_sentiment_label(self, score: float) -> str:
        if score > 0.1:
            return 'positive'
        elif score < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract named entities and key information"""
        try:
            doc = self.nlp(text)
            
            entities = {
                'organizations': [],
                'industries': [],
                'technologies': [],
                'locations': [],
                'financial_terms': [],
                'market_segments': []
            }
            
            # Extract named entities
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'].append(ent.text)
                elif ent.label_ == 'GPE':
                    entities['locations'].append(ent.text)
            
            # Extract industries and technologies using patterns
            industry_patterns = [
                r'\b(?:AI|artificial intelligence|machine learning|ML|blockchain|fintech|healthtech|edtech|proptech|insurtech)\b',
                r'\b(?:SaaS|software|cloud|mobile|web|e-commerce|marketplace)\b',
                r'\b(?:biotech|pharmaceutical|healthcare|medical|diagnostic)\b',
                r'\b(?:energy|renewable|solar|wind|battery|EV|electric vehicle)\b'
            ]
            
            for pattern in industry_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities['industries'].extend(matches)
            
            # Extract financial terms
            financial_patterns = [
                r'\b(?:revenue|ARR|MRR|LTV|CAC|churn|burn rate|runway|valuation|funding|Series [A-Z])\b',
                r'\b(?:growth|scaling|expansion|market share|competitive advantage)\b'
            ]
            
            for pattern in financial_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities['financial_terms'].extend(matches)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error in entity extraction: {str(e)}")
            return {'organizations': [], 'industries': [], 'technologies': [], 'locations': [], 'financial_terms': [], 'market_segments': []}
    
    def _advanced_company_matching(self, thesis_text: str, companies_data: List[Dict]) -> List[Dict]:
        """Advanced company matching using embeddings and similarity"""
        try:
            if not companies_data:
                return []
            
            # Create embeddings for thesis and companies
            thesis_embedding = self.embeddings.embed_query(thesis_text)
            
            matched_companies = []
            
            for company in companies_data:
                company_text = f"{company.get('name', '')} {company.get('industry', '')} {company.get('description', '')}"
                company_embedding = self.embeddings.embed_query(company_text)
                
                # Calculate similarity
                similarity = cosine_similarity([thesis_embedding], [company_embedding])[0][0]
                
                # Additional matching criteria
                industry_match = self._check_industry_match(thesis_text, company.get('industry', ''))
                stage_match = self._check_stage_match(thesis_text, company.get('funding_stage', ''))
                
                # Combined score
                combined_score = (similarity * 0.6 + industry_match * 0.3 + stage_match * 0.1)
                
                if combined_score > 0.3:  # Threshold for matching
                    matched_companies.append({
                        'company': company,
                        'similarity_score': similarity,
                        'industry_match': industry_match,
                        'stage_match': stage_match,
                        'combined_score': combined_score,
                        'fit_score': min(combined_score * 100, 100)
                    })
            
            # Sort by combined score
            matched_companies.sort(key=lambda x: x['combined_score'], reverse=True)
            return matched_companies[:10]  # Top 10 matches
            
        except Exception as e:
            logger.error(f"Error in advanced company matching: {str(e)}")
            return []
    
    def _check_industry_match(self, thesis_text: str, company_industry: str) -> float:
        """Check industry match between thesis and company"""
        try:
            thesis_lower = thesis_text.lower()
            industry_lower = company_industry.lower()
            
            # Simple keyword matching
            if industry_lower in thesis_lower or any(word in thesis_lower for word in industry_lower.split()):
                return 1.0
            
            # Industry synonyms
            industry_synonyms = {
                'ai': ['artificial intelligence', 'machine learning', 'ml'],
                'fintech': ['financial technology', 'banking', 'payments'],
                'healthtech': ['healthcare', 'medical', 'biotech'],
                'edtech': ['education', 'learning', 'edtech'],
                'proptech': ['real estate', 'property', 'proptech']
            }
            
            for industry, synonyms in industry_synonyms.items():
                if industry_lower in industry or any(syn in industry_lower for syn in synonyms):
                    if any(syn in thesis_lower for syn in synonyms):
                        return 0.8
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error in industry match: {str(e)}")
            return 0.0
    
    def _check_stage_match(self, thesis_text: str, company_stage: str) -> float:
        """Check funding stage match"""
        try:
            thesis_lower = thesis_text.lower()
            stage_lower = company_stage.lower()
            
            stage_keywords = {
                'seed': ['seed', 'early stage', 'startup'],
                'series a': ['series a', 'growth', 'scaling'],
                'series b': ['series b', 'expansion', 'growth'],
                'series c': ['series c', 'mature', 'established'],
                'public': ['public', 'ipo', 'listed']
            }
            
            for stage, keywords in stage_keywords.items():
                if stage in stage_lower:
                    if any(keyword in thesis_lower for keyword in keywords):
                        return 1.0
            
            return 0.5  # Default neutral score
            
        except Exception as e:
            logger.error(f"Error in stage match: {str(e)}")
            return 0.0
    
    def _assess_risk(self, thesis_text: str, entities: Dict, sentiment_scores: Dict) -> Dict:
        """Assess investment risk based on thesis analysis"""
        try:
            risk_factors = {
                'market_risk': 0.0,
                'technology_risk': 0.0,
                'competition_risk': 0.0,
                'regulatory_risk': 0.0,
                'execution_risk': 0.0
            }
            
            text_lower = thesis_text.lower()
            
            # Market risk assessment
            market_risk_keywords = ['saturated', 'competitive', 'declining', 'recession', 'economic']
            risk_factors['market_risk'] = sum(1 for keyword in market_risk_keywords if keyword in text_lower) * 0.2
            
            # Technology risk assessment
            tech_risk_keywords = ['unproven', 'experimental', 'beta', 'prototype', 'early stage']
            risk_factors['technology_risk'] = sum(1 for keyword in tech_risk_keywords if keyword in text_lower) * 0.2
            
            # Competition risk
            competition_keywords = ['competition', 'competitor', 'rival', 'market leader', 'established']
            risk_factors['competition_risk'] = sum(1 for keyword in competition_keywords if keyword in text_lower) * 0.2
            
            # Regulatory risk
            regulatory_keywords = ['regulation', 'compliance', 'legal', 'government', 'policy']
            risk_factors['regulatory_risk'] = sum(1 for keyword in regulatory_keywords if keyword in text_lower) * 0.2
            
            # Execution risk (based on sentiment)
            risk_factors['execution_risk'] = max(0, -sentiment_scores['overall_sentiment']) * 0.5
            
            # Overall risk score
            overall_risk = sum(risk_factors.values()) / len(risk_factors)
            
            return {
                'risk_factors': risk_factors,
                'overall_risk': min(overall_risk, 1.0),
                'risk_level': self._get_risk_level(overall_risk)
            }
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {str(e)}")
            return {'risk_factors': {}, 'overall_risk': 0.5, 'risk_level': 'medium'}
    
    def _get_risk_level(self, risk_score: float) -> str:
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def _analyze_market_opportunity(self, thesis_text: str, entities: Dict) -> Dict:
        """Analyze market opportunity based on thesis"""
        try:
            opportunity_score = 0.5  # Base score
            
            # Market size indicators
            market_size_keywords = ['large market', 'growing market', 'billion dollar', 'trillion dollar', 'massive opportunity']
            if any(keyword in thesis_text.lower() for keyword in market_size_keywords):
                opportunity_score += 0.2
            
            # Growth indicators
            growth_keywords = ['growth', 'expanding', 'increasing', 'rising', 'trending']
            growth_count = sum(1 for keyword in growth_keywords if keyword in thesis_text.lower())
            opportunity_score += min(growth_count * 0.05, 0.2)
            
            # Technology advantage
            tech_advantage_keywords = ['unique', 'proprietary', 'patent', 'innovation', 'breakthrough']
            if any(keyword in thesis_text.lower() for keyword in tech_advantage_keywords):
                opportunity_score += 0.15
            
            # Market timing
            timing_keywords = ['timing', 'right time', 'market ready', 'mature market']
            if any(keyword in thesis_text.lower() for keyword in timing_keywords):
                opportunity_score += 0.1
            
            return {
                'opportunity_score': min(opportunity_score, 1.0),
                'market_size': 'large' if opportunity_score > 0.7 else 'medium' if opportunity_score > 0.4 else 'small',
                'growth_potential': 'high' if opportunity_score > 0.6 else 'medium' if opportunity_score > 0.3 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error in market opportunity analysis: {str(e)}")
            return {'opportunity_score': 0.5, 'market_size': 'medium', 'growth_potential': 'medium'}
    
    def _calculate_thesis_score(self, sentiment_scores: Dict, risk_assessment: Dict, market_opportunity: Dict) -> float:
        """Calculate overall thesis score"""
        try:
            # Weighted scoring
            sentiment_weight = 0.3
            risk_weight = 0.3
            opportunity_weight = 0.4
            
            sentiment_score = (sentiment_scores['overall_sentiment'] + 1) / 2  # Normalize to 0-1
            risk_score = 1 - risk_assessment['overall_risk']  # Invert risk
            opportunity_score = market_opportunity['opportunity_score']
            
            final_score = (
                sentiment_score * sentiment_weight +
                risk_score * risk_weight +
                opportunity_score * opportunity_weight
            )
            
            return min(max(final_score, 0), 1)  # Ensure 0-1 range
            
        except Exception as e:
            logger.error(f"Error in thesis score calculation: {str(e)}")
            return 0.5
    
    def _calculate_confidence_score(self, thesis_text: str) -> float:
        """Calculate confidence in the analysis"""
        try:
            # Factors that increase confidence
            confidence_factors = 0.5  # Base confidence
            
            # Length factor
            if len(thesis_text) > 500:
                confidence_factors += 0.1
            if len(thesis_text) > 1000:
                confidence_factors += 0.1
            
            # Specificity factor
            specific_terms = ['revenue', 'market', 'technology', 'team', 'competition', 'growth']
            specificity_score = sum(1 for term in specific_terms if term in thesis_text.lower()) / len(specific_terms)
            confidence_factors += specificity_score * 0.2
            
            # Structure factor
            if any(section in thesis_text.lower() for section in ['problem', 'solution', 'market', 'team', 'financial']):
                confidence_factors += 0.1
            
            return min(confidence_factors, 1.0)
            
        except Exception as e:
            logger.error(f"Error in confidence calculation: {str(e)}")
            return 0.5
    
    def _generate_advanced_recommendations(self, thesis_score: float, risk_assessment: Dict, market_opportunity: Dict) -> List[str]:
        """Generate advanced investment recommendations"""
        try:
            recommendations = []
            
            if thesis_score > 0.7:
                recommendations.append("Strong investment thesis with high potential for returns")
                recommendations.append("Consider leading or co-leading the investment round")
            elif thesis_score > 0.5:
                recommendations.append("Moderate investment thesis with balanced risk-reward")
                recommendations.append("Consider participating in the investment round")
            else:
                recommendations.append("Weak investment thesis with significant risks")
                recommendations.append("Consider passing or requiring significant changes")
            
            # Risk-based recommendations
            if risk_assessment['overall_risk'] > 0.7:
                recommendations.append("High risk investment - consider smaller position size")
                recommendations.append("Implement strict monitoring and milestone requirements")
            
            # Market opportunity recommendations
            if market_opportunity['opportunity_score'] > 0.7:
                recommendations.append("Large market opportunity - consider aggressive investment strategy")
            elif market_opportunity['opportunity_score'] < 0.3:
                recommendations.append("Limited market opportunity - consider smaller investment or pass")
            
            # General recommendations
            recommendations.append("Conduct thorough due diligence on team and technology")
            recommendations.append("Monitor market conditions and competitive landscape")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in recommendation generation: {str(e)}")
            return ["Conduct thorough analysis before making investment decision"]
    
    def _get_fallback_analysis(self) -> Dict:
        """Fallback analysis when advanced analysis fails"""
        return {
            'sentiment_analysis': {'overall_sentiment': 0, 'sentiment_label': 'neutral'},
            'entities': {'organizations': [], 'industries': [], 'technologies': [], 'locations': [], 'financial_terms': [], 'market_segments': []},
            'matched_companies': [],
            'risk_assessment': {'risk_factors': {}, 'overall_risk': 0.5, 'risk_level': 'medium'},
            'market_opportunity': {'opportunity_score': 0.5, 'market_size': 'medium', 'growth_potential': 'medium'},
            'thesis_score': 0.5,
            'confidence_score': 0.5,
            'recommendations': ["Conduct manual analysis due to processing limitations"]
        }
    
    def update_dashboard_analytics(self, thesis_history: List[Dict]) -> Dict:
        """Update dashboard with advanced analytics based on thesis history"""
        try:
            if not thesis_history:
                return self._get_empty_dashboard_analytics()
            
            # Analyze trends over time
            trend_analysis = self._analyze_trends(thesis_history)
            
            # Performance metrics
            performance_metrics = self._calculate_performance_metrics(thesis_history)
            
            # Predictive analytics
            predictions = self._generate_predictions(thesis_history)
            
            return {
                'trend_analysis': trend_analysis,
                'performance_metrics': performance_metrics,
                'predictions': predictions,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in dashboard analytics update: {str(e)}")
            return self._get_empty_dashboard_analytics()
    
    def _analyze_trends(self, thesis_history: List[Dict]) -> Dict:
        """Analyze trends in thesis analysis over time"""
        try:
            # Extract scores and dates
            scores = []
            dates = []
            sentiments = []
            
            for thesis in thesis_history:
                if 'thesis_score' in thesis:
                    scores.append(thesis['thesis_score'])
                    dates.append(datetime.fromisoformat(thesis.get('created_at', datetime.now().isoformat())))
                
                if 'sentiment_analysis' in thesis:
                    sentiments.append(thesis['sentiment_analysis'].get('overall_sentiment', 0))
            
            if not scores:
                return {'trend': 'stable', 'score_trend': 0, 'sentiment_trend': 0}
            
            # Calculate trends
            score_trend = np.polyfit(range(len(scores)), scores, 1)[0] if len(scores) > 1 else 0
            sentiment_trend = np.polyfit(range(len(sentiments)), sentiments, 1)[0] if len(sentiments) > 1 else 0
            
            # Determine trend direction
            if score_trend > 0.01:
                trend = 'improving'
            elif score_trend < -0.01:
                trend = 'declining'
            else:
                trend = 'stable'
            
            return {
                'trend': trend,
                'score_trend': score_trend,
                'sentiment_trend': sentiment_trend,
                'average_score': np.mean(scores),
                'score_volatility': np.std(scores)
            }
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {str(e)}")
            return {'trend': 'stable', 'score_trend': 0, 'sentiment_trend': 0}
    
    def _calculate_performance_metrics(self, thesis_history: List[Dict]) -> Dict:
        """Calculate performance metrics from thesis history"""
        try:
            if not thesis_history:
                return {'total_analyses': 0, 'average_score': 0, 'success_rate': 0}
            
            scores = [thesis.get('thesis_score', 0.5) for thesis in thesis_history]
            sentiments = [thesis.get('sentiment_analysis', {}).get('overall_sentiment', 0) for thesis in thesis_history]
            
            # Calculate metrics
            total_analyses = len(thesis_history)
            average_score = np.mean(scores)
            average_sentiment = np.mean(sentiments)
            success_rate = len([s for s in scores if s > 0.6]) / total_analyses
            
            # Risk distribution
            risk_levels = [thesis.get('risk_assessment', {}).get('risk_level', 'medium') for thesis in thesis_history]
            risk_distribution = {
                'low': risk_levels.count('low'),
                'medium': risk_levels.count('medium'),
                'high': risk_levels.count('high')
            }
            
            return {
                'total_analyses': total_analyses,
                'average_score': average_score,
                'average_sentiment': average_sentiment,
                'success_rate': success_rate,
                'risk_distribution': risk_distribution,
                'score_volatility': np.std(scores),
                'sentiment_volatility': np.std(sentiments)
            }
            
        except Exception as e:
            logger.error(f"Error in performance metrics: {str(e)}")
            return {'total_analyses': 0, 'average_score': 0, 'success_rate': 0}
    
    def _generate_predictions(self, thesis_history: List[Dict]) -> Dict:
        """Generate predictions based on historical data"""
        try:
            if len(thesis_history) < 5:
                return {'next_score_prediction': 0.5, 'confidence': 0.5}
            
            # Extract time series data
            scores = [thesis.get('thesis_score', 0.5) for thesis in thesis_history]
            dates = [datetime.fromisoformat(thesis.get('created_at', datetime.now().isoformat())) for thesis in thesis_history]
            
            # Sort by date
            sorted_data = sorted(zip(dates, scores), key=lambda x: x[0])
            sorted_scores = [score for date, score in sorted_data]
            
            # Simple linear prediction
            if len(sorted_scores) > 1:
                trend = np.polyfit(range(len(sorted_scores)), sorted_scores, 1)
                next_prediction = trend[0] * len(sorted_scores) + trend[1]
                next_prediction = max(0, min(1, next_prediction))  # Clamp to 0-1
                
                # Calculate confidence based on trend consistency
                residuals = [abs(sorted_scores[i] - (trend[0] * i + trend[1])) for i in range(len(sorted_scores))]
                confidence = 1 - min(np.mean(residuals), 1)
                
                return {
                    'next_score_prediction': next_prediction,
                    'confidence': confidence,
                    'trend_direction': 'up' if trend[0] > 0 else 'down' if trend[0] < 0 else 'stable'
                }
            
            return {'next_score_prediction': 0.5, 'confidence': 0.5}
            
        except Exception as e:
            logger.error(f"Error in prediction generation: {str(e)}")
            return {'next_score_prediction': 0.5, 'confidence': 0.5}
    
    def _get_empty_dashboard_analytics(self) -> Dict:
        """Return empty dashboard analytics structure"""
        return {
            'trend_analysis': {'trend': 'stable', 'score_trend': 0, 'sentiment_trend': 0},
            'performance_metrics': {'total_analyses': 0, 'average_score': 0, 'success_rate': 0},
            'predictions': {'next_score_prediction': 0.5, 'confidence': 0.5},
            'last_updated': datetime.now().isoformat()
        } 