"""
Embedding service for DealFlowAI using sentence-transformers
"""

import numpy as np
import json
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the embedding service
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Initialized embedding service with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of float values representing the embedding
        """
        try:
            embedding = self.model.encode(text)
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
            embeddings = self.model.encode(texts)
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
    
    def find_similar_companies(self, query_embedding: List[float], 
                             company_embeddings: List[Dict[str, Any]], 
                             top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find companies similar to a query embedding
        
        Args:
            query_embedding: Query embedding vector
            company_embeddings: List of company data with embeddings
            top_k: Number of top results to return
            
        Returns:
            List of similar companies with scores
        """
        try:
            results = []
            
            for company_data in company_embeddings:
                company_embedding = company_data.get('embedding_vector')
                if company_embedding:
                    # Parse JSON string if needed
                    if isinstance(company_embedding, str):
                        company_embedding = json.loads(company_embedding)
                    
                    similarity = self.calculate_similarity(query_embedding, company_embedding)
                    
                    results.append({
                        'company_id': company_data.get('id'),
                        'company_name': company_data.get('name'),
                        'similarity_score': similarity,
                        'company_data': company_data
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