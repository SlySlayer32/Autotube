"""
Audio Similarity Matching using OpenL3 embeddings.

This module provides functionality for finding similar audio clips
using OpenL3 deep audio embeddings and various similarity metrics.
"""

import logging
import os
from typing import Dict, List, Tuple, Optional, Union
import numpy as np
from pathlib import Path

try:
    import openl3
    import soundfile as sf
    from sklearn.metrics.pairwise import cosine_similarity
    from scipy.spatial.distance import euclidean, cdist
    SIMILARITY_AVAILABLE = True
except ImportError as e:
    SIMILARITY_AVAILABLE = False
    logging.warning(f"Audio similarity dependencies not available: {e}")

logger = logging.getLogger(__name__)


class AudioSimilarityMatcher:
    """
    Audio similarity matching using OpenL3 embeddings.
    
    This class provides methods to:
    - Extract audio embeddings using OpenL3
    - Find similar audio clips based on semantic content
    - Cache embeddings for efficient similarity computations
    """
    
    def __init__(
        self,
        content_type: str = "env",
        input_repr: str = "mel128",
        embedding_size: int = 512,
        cache_embeddings: bool = True
    ):
        """
        Initialize the AudioSimilarityMatcher.
        
        Args:
            content_type: "music" or "env" (environmental sounds)
            input_repr: "mel128", "mel256", or "linear" 
            embedding_size: 512 or 6144 (smaller is faster)
            cache_embeddings: Whether to cache embeddings for reuse
        """
        if not SIMILARITY_AVAILABLE:
            raise RuntimeError(
                "Audio similarity matching requires OpenL3, soundfile, and scikit-learn. "
                "Install with: pip install openl3 soundfile scikit-learn"
            )
        
        self.content_type = content_type
        self.input_repr = input_repr
        self.embedding_size = embedding_size
        self.cache_embeddings = cache_embeddings
        
        # Load OpenL3 model
        try:
            self.model = openl3.models.load_audio_embedding_model(
                input_repr=input_repr,
                content_type=content_type,
                embedding_size=embedding_size
            )
            logger.info(f"OpenL3 model loaded: {content_type}/{input_repr}/{embedding_size}")
        except Exception as e:
            logger.error(f"Failed to load OpenL3 model: {e}")
            raise
        
        # Embedding cache
        self.embedding_cache: Dict[str, np.ndarray] = {}
        
    def extract_embedding(
        self, 
        audio_path: Union[str, Path], 
        pooling_method: str = "mean"
    ) -> np.ndarray:
        """
        Extract audio embedding for a single file.
        
        Args:
            audio_path: Path to audio file
            pooling_method: "mean", "max", or "median" for time-pooling
            
        Returns:
            numpy array of audio embedding
        """
        audio_path = str(audio_path)
        
        # Check cache first
        if self.cache_embeddings and audio_path in self.embedding_cache:
            return self.embedding_cache[audio_path]
        
        try:
            # Load audio file
            audio, sr = sf.read(audio_path)
            
            # Handle stereo by taking first channel
            if audio.ndim > 1:
                audio = audio[:, 0]
            
            # Extract embeddings
            emb, ts = openl3.get_audio_embedding(
                audio, sr, 
                model=self.model,
                verbose=0
            )
            
            # Pool embeddings across time
            if pooling_method == "mean":
                embedding = np.mean(emb, axis=0)
            elif pooling_method == "max":
                embedding = np.max(emb, axis=0)
            elif pooling_method == "median":
                embedding = np.median(emb, axis=0)
            else:
                raise ValueError(f"Unknown pooling method: {pooling_method}")
            
            # Cache the result
            if self.cache_embeddings:
                self.embedding_cache[audio_path] = embedding
                
            logger.debug(f"Extracted embedding for {audio_path}: shape {embedding.shape}")
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to extract embedding for {audio_path}: {e}")
            raise
    
    def compute_similarity(
        self, 
        embedding1: np.ndarray, 
        embedding2: np.ndarray,
        metric: str = "cosine"
    ) -> float:
        """
        Compute similarity between two embeddings.
        
        Args:
            embedding1: First audio embedding
            embedding2: Second audio embedding  
            metric: "cosine", "euclidean", or "manhattan"
            
        Returns:
            Similarity score (higher = more similar for cosine)
        """
        if metric == "cosine":
            # Cosine similarity (0-1, higher is more similar)
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return float(similarity)
        elif metric == "euclidean":
            # Euclidean distance (lower is more similar)
            distance = euclidean(embedding1, embedding2)
            return float(distance)
        elif metric == "manhattan":
            # Manhattan distance (lower is more similar)
            distance = np.sum(np.abs(embedding1 - embedding2))
            return float(distance)
        else:
            raise ValueError(f"Unknown similarity metric: {metric}")
    
    def find_similar_clips(
        self,
        query_path: Union[str, Path],
        candidate_paths: List[Union[str, Path]], 
        top_k: int = 5,
        metric: str = "cosine"
    ) -> List[Tuple[str, float]]:
        """
        Find most similar audio clips to a query clip.
        
        Args:
            query_path: Path to query audio file
            candidate_paths: List of candidate audio file paths
            top_k: Number of most similar clips to return
            metric: Similarity metric to use
            
        Returns:
            List of (file_path, similarity_score) tuples, sorted by similarity
        """
        # Extract query embedding
        query_embedding = self.extract_embedding(query_path)
        
        # Compute similarities
        similarities = []
        for candidate_path in candidate_paths:
            try:
                candidate_embedding = self.extract_embedding(candidate_path)
                similarity = self.compute_similarity(
                    query_embedding, candidate_embedding, metric
                )
                similarities.append((str(candidate_path), similarity))
            except Exception as e:
                logger.warning(f"Skipping {candidate_path}: {e}")
                continue
        
        # Sort by similarity
        if metric == "cosine":
            # Higher cosine similarity = more similar
            similarities.sort(key=lambda x: x[1], reverse=True)
        else:
            # Lower distance = more similar  
            similarities.sort(key=lambda x: x[1])
        
        return similarities[:top_k]
    
    def find_similar_in_categories(
        self,
        query_path: Union[str, Path],
        categories: Dict[str, List[str]],
        top_k_per_category: int = 3,
        metric: str = "cosine"
    ) -> Dict[str, List[Tuple[str, float]]]:
        """
        Find similar clips within each category.
        
        Args:
            query_path: Path to query audio file
            categories: Dict of category_name -> list of file paths
            top_k_per_category: Number of similar clips per category
            metric: Similarity metric to use
            
        Returns:
            Dict of category_name -> list of (file_path, similarity_score)
        """
        results = {}
        
        for category_name, file_paths in categories.items():
            try:
                similar_clips = self.find_similar_clips(
                    query_path, file_paths, top_k_per_category, metric
                )
                results[category_name] = similar_clips
                logger.info(f"Found {len(similar_clips)} similar clips in {category_name}")
            except Exception as e:
                logger.error(f"Error processing category {category_name}: {e}")
                results[category_name] = []
        
        return results
    
    def batch_extract_embeddings(
        self, 
        file_paths: List[Union[str, Path]],
        batch_size: int = 32
    ) -> Dict[str, np.ndarray]:
        """
        Extract embeddings for multiple files efficiently.
        
        Args:
            file_paths: List of audio file paths
            batch_size: Number of files to process at once
            
        Returns:
            Dict of file_path -> embedding
        """
        embeddings = {}
        
        for i in range(0, len(file_paths), batch_size):
            batch_paths = file_paths[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(file_paths)-1)//batch_size + 1}")
            
            for file_path in batch_paths:
                try:
                    embedding = self.extract_embedding(file_path)
                    embeddings[str(file_path)] = embedding
                except Exception as e:
                    logger.warning(f"Failed to process {file_path}: {e}")
                    continue
        
        return embeddings
    
    def save_embeddings_cache(self, cache_path: Union[str, Path]) -> None:
        """Save embedding cache to disk."""
        if not self.embedding_cache:
            logger.warning("No embeddings to save")
            return
            
        try:
            np.savez_compressed(cache_path, **self.embedding_cache)
            logger.info(f"Saved {len(self.embedding_cache)} embeddings to {cache_path}")
        except Exception as e:
            logger.error(f"Failed to save embeddings cache: {e}")
    
    def load_embeddings_cache(self, cache_path: Union[str, Path]) -> None:
        """Load embedding cache from disk."""
        try:
            data = np.load(cache_path)
            self.embedding_cache = {key: data[key] for key in data.files}
            logger.info(f"Loaded {len(self.embedding_cache)} embeddings from {cache_path}")
        except Exception as e:
            logger.error(f"Failed to load embeddings cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the embedding cache."""
        return {
            "cached_files": len(self.embedding_cache),
            "embedding_size": self.embedding_size,
            "memory_usage_mb": sum(
                emb.nbytes for emb in self.embedding_cache.values()
            ) / (1024 * 1024)
        }


def create_similarity_matcher(content_type: str = "env") -> AudioSimilarityMatcher:
    """
    Factory function to create a pre-configured similarity matcher.
    
    Args:
        content_type: "env" for environmental sounds, "music" for music
        
    Returns:
        Configured AudioSimilarityMatcher instance
    """
    return AudioSimilarityMatcher(
        content_type=content_type,
        input_repr="mel128",
        embedding_size=512,  # Faster computation
        cache_embeddings=True
    )
