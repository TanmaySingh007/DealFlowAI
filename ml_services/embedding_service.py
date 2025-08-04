"""
Simplified Embedding service for DealFlowAI
"""

import numpy as np
import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class SimplifiedEmbeddingService:
    """Simplified service for generating and managing embeddings"""
    
    def __init__(self):
        """Initialize the simplified embedding service"""
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.dimension = 1000  # TF-IDF dimension
            logger.info("Initialized simplified embedding service")
        except Exception as e:
            logger.error(f"Failed to initialize embedding service: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using TF-IDF
        
        Args:
            text: Input text to embed
            
        Returns:
            List of float values representing the embedding
        """
        try:
            # Use TF-IDF for simple embeddings
            tfidf_matrix = self.vectorizer.fit_transform([text])
            embedding = tfidf_matrix.toarray()[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * self.dimension
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embeddings
        """
        try:
            # Use TF-IDF for batch embeddings
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            embeddings = tfidf_matrix.toarray()
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            # Return zero vectors as fallback
            return [[0.0] * self.dimension for _ in texts]
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1).reshape(1, -1)
            vec2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(vec1, vec2)[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_similar_companies(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find companies similar to a query text
        
        Args:
            query_text: Query text
            top_k: Number of top results to return
            
        Returns:
            List of similar companies with scores
        """
        try:
            from deals.models import Company
            
            # Get all companies
            companies = Company.objects.filter(is_active=True)
            
            if not companies.exists():
                return []
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query_text)
            
            results = []
            
            for company in companies:
                # Create company text for embedding
                company_text = f"{company.name} {company.description} {company.industry}"
                company_embedding = self.generate_embedding(company_text)
                
                # Calculate similarity
                similarity = self.calculate_similarity(query_embedding, company_embedding)
                
                if similarity > 0.01:  # Only include companies with some similarity
                    results.append({
                        'id': company.id,
                        'name': company.name,
                        'industry': company.industry,
                        'revenue_range': company.revenue_range,
                        'funding_stage': company.funding_stage,
                        'description': company.description,
                        'similarity_score': similarity,
                        'fit_score': min(similarity + 0.2, 0.95)  # Boost score
                    })
            
            # Sort by similarity score and return top k
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar companies: {e}")
            return []
    
    def update_company_embedding(self, company_text: str, company_id: int) -> bool:
        """
        Update embedding for a specific company
        
        Args:
            company_text: Text to generate embedding from
            company_id: Company ID to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from deals.models import Company
            
            embedding = self.generate_embedding(company_text)
            company = Company.objects.get(id=company_id)
            company.set_embedding_vector(embedding)
            company.save()
            
            logger.info(f"Updated embedding for company {company_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating company embedding: {e}")
            return False
    
    def batch_update_embeddings(self) -> int:
        """
        Update embeddings for all companies that don't have embeddings
        
        Returns:
            Number of companies updated
        """
        try:
            from deals.models import Company
            
            companies_without_embeddings = Company.objects.filter(
                embedding_vector__isnull=True
            ).exclude(embedding_vector='')
            
            updated_count = 0
            
            for company in companies_without_embeddings:
                # Create text representation for embedding
                company_text = f"{company.name} {company.description} {company.industry}"
                
                if self.update_company_embedding(company_text, company.id):
                    updated_count += 1
            
            logger.info(f"Updated embeddings for {updated_count} companies")
            return updated_count
            
        except Exception as e:
            logger.error(f"Error in batch update embeddings: {e}")
            return 0


# Backward compatibility
EmbeddingService = SimplifiedEmbeddingService 