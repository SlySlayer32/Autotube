"""
Tests for audio similarity matching functionality.
"""

import os
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch

from project_name.core.audio_similarity import AudioSimilarityMatcher, create_similarity_matcher


@pytest.mark.unit
class TestAudioSimilarityMatcher:
    """Test audio similarity matching functionality."""
    
    @pytest.fixture
    def mock_openl3(self):
        """Mock OpenL3 to avoid requiring model downloads in tests."""
        with patch('project_name.core.audio_similarity.openl3') as mock_openl3:
            # Mock model loading
            mock_model = Mock()
            mock_openl3.models.load_audio_embedding_model.return_value = mock_model
            
            # Mock embedding extraction
            mock_embedding = np.random.rand(10, 512)  # 10 time frames, 512 features
            mock_timestamps = np.arange(10) * 0.1
            mock_openl3.get_audio_embedding.return_value = (mock_embedding, mock_timestamps)
            
            yield mock_openl3
    
    @pytest.fixture
    def mock_soundfile(self):
        """Mock soundfile to avoid requiring actual audio files."""
        with patch('project_name.core.audio_similarity.sf') as mock_sf:
            # Mock audio loading - return dummy audio data
            mock_audio = np.random.rand(44100)  # 1 second of dummy audio
            mock_sr = 44100
            mock_sf.read.return_value = (mock_audio, mock_sr)
            yield mock_sf
    
    @pytest.fixture
    def similarity_matcher(self, mock_openl3, mock_soundfile):
        """Create a similarity matcher with mocked dependencies."""
        return AudioSimilarityMatcher(
            content_type="env",
            embedding_size=512,
            cache_embeddings=True
        )
    
    def test_init(self, similarity_matcher):
        """Test similarity matcher initialization."""
        assert similarity_matcher.content_type == "env"
        assert similarity_matcher.embedding_size == 512
        assert similarity_matcher.cache_embeddings is True
        assert similarity_matcher.model is not None
        assert isinstance(similarity_matcher.embedding_cache, dict)
    
    def test_extract_embedding(self, similarity_matcher, tmp_path):
        """Test embedding extraction."""
        # Create a dummy audio file path
        audio_file = tmp_path / "test.wav"
        audio_file.touch()  # Create empty file
        
        # Extract embedding
        embedding = similarity_matcher.extract_embedding(str(audio_file))
        
        # Should return a single embedding vector (mean pooled)
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (512,)  # Should match embedding_size
        
        # Should be cached
        assert str(audio_file) in similarity_matcher.embedding_cache
    
    def test_extract_embedding_pooling_methods(self, similarity_matcher, tmp_path):
        """Test different pooling methods for embedding extraction."""
        audio_file = tmp_path / "test.wav"
        audio_file.touch()
        
        # Test different pooling methods
        for method in ["mean", "max", "median"]:
            embedding = similarity_matcher.extract_embedding(str(audio_file), pooling_method=method)
            assert isinstance(embedding, np.ndarray)
            assert embedding.shape == (512,)
    
    def test_compute_similarity_cosine(self, similarity_matcher):
        """Test cosine similarity computation."""
        emb1 = np.random.rand(512)
        emb2 = np.random.rand(512)
        
        similarity = similarity_matcher.compute_similarity(emb1, emb2, metric="cosine")
        
        assert isinstance(similarity, float)
        assert 0 <= similarity <= 1  # Cosine similarity range
    
    def test_compute_similarity_euclidean(self, similarity_matcher):
        """Test Euclidean distance computation."""
        emb1 = np.random.rand(512)
        emb2 = np.random.rand(512)
        
        distance = similarity_matcher.compute_similarity(emb1, emb2, metric="euclidean")
        
        assert isinstance(distance, float)
        assert distance >= 0  # Distance is non-negative
    
    def test_find_similar_clips(self, similarity_matcher, tmp_path):
        """Test finding similar clips."""
        # Create dummy audio files
        query_file = tmp_path / "query.wav"
        query_file.touch()
        
        candidate_files = []
        for i in range(5):
            candidate_file = tmp_path / f"candidate_{i}.wav"
            candidate_file.touch()
            candidate_files.append(str(candidate_file))
        
        # Find similar clips
        similar_clips = similarity_matcher.find_similar_clips(
            str(query_file), candidate_files, top_k=3
        )
        
        # Should return top 3 similar clips
        assert len(similar_clips) == 3
        
        # Each result should be (file_path, similarity_score)
        for file_path, score in similar_clips:
            assert isinstance(file_path, str)
            assert isinstance(score, float)
    
    def test_find_similar_in_categories(self, similarity_matcher, tmp_path):
        """Test finding similar clips within categories."""
        # Create dummy audio files
        query_file = tmp_path / "query.wav"
        query_file.touch()
        
        categories = {}
        for category in ["rain", "thunder", "nature"]:
            category_files = []
            for i in range(3):
                file_path = tmp_path / f"{category}_{i}.wav"
                file_path.touch()
                category_files.append(str(file_path))
            categories[category] = category_files
        
        # Find similar clips in each category
        results = similarity_matcher.find_similar_in_categories(
            str(query_file), categories, top_k_per_category=2
        )
        
        # Should return results for each category
        assert len(results) == 3
        assert "rain" in results
        assert "thunder" in results
        assert "nature" in results
        
        # Each category should have up to 2 similar clips
        for category, similar_clips in results.items():
            assert len(similar_clips) <= 2
    
    def test_batch_extract_embeddings(self, similarity_matcher, tmp_path):
        """Test batch embedding extraction."""
        # Create dummy audio files
        file_paths = []
        for i in range(5):
            file_path = tmp_path / f"audio_{i}.wav"
            file_path.touch()
            file_paths.append(str(file_path))
        
        # Extract embeddings in batch
        embeddings = similarity_matcher.batch_extract_embeddings(file_paths, batch_size=2)
        
        # Should return embeddings for all files
        assert len(embeddings) == 5
        
        # Each embedding should be correct shape
        for file_path, embedding in embeddings.items():
            assert isinstance(embedding, np.ndarray)
            assert embedding.shape == (512,)
    
    def test_cache_operations(self, similarity_matcher, tmp_path):
        """Test embedding cache save/load operations."""
        # Add some embeddings to cache
        for i in range(3):
            file_path = f"test_{i}.wav"
            embedding = np.random.rand(512)
            similarity_matcher.embedding_cache[file_path] = embedding
        
        # Save cache
        cache_path = tmp_path / "test_cache.npz"
        similarity_matcher.save_embeddings_cache(cache_path)
        assert cache_path.exists()
        
        # Clear cache and reload
        similarity_matcher.embedding_cache.clear()
        assert len(similarity_matcher.embedding_cache) == 0
        
        similarity_matcher.load_embeddings_cache(cache_path)
        assert len(similarity_matcher.embedding_cache) == 3
    
    def test_get_cache_stats(self, similarity_matcher):
        """Test cache statistics."""
        # Add some embeddings to cache
        for i in range(3):
            file_path = f"test_{i}.wav"
            embedding = np.random.rand(512)
            similarity_matcher.embedding_cache[file_path] = embedding
        
        stats = similarity_matcher.get_cache_stats()
        
        assert "cached_files" in stats
        assert "embedding_size" in stats
        assert "memory_usage_mb" in stats
        assert stats["cached_files"] == 3
        assert stats["embedding_size"] == 512


@pytest.mark.unit
def test_create_similarity_matcher():
    """Test factory function for creating similarity matcher."""
    with patch('project_name.core.audio_similarity.AudioSimilarityMatcher') as mock_class:
        create_similarity_matcher(content_type="music")
        
        # Should call constructor with correct parameters
        mock_class.assert_called_once_with(
            content_type="music",
            input_repr="mel128",
            embedding_size=512,
            cache_embeddings=True
        )


@pytest.mark.integration
class TestAudioSimilarityIntegration:
    """Integration tests for audio similarity (requires actual dependencies)."""
    
    @pytest.mark.skipif(
        not os.getenv("RUN_INTEGRATION_TESTS"),
        reason="Integration tests require RUN_INTEGRATION_TESTS environment variable"
    )
    def test_real_openl3_integration(self):
        """Test with real OpenL3 (only runs if explicitly enabled)."""
        try:
            import openl3
            import soundfile as sf
            
            # This test would use real OpenL3 and audio files
            # Only run if integration tests are explicitly enabled
            matcher = create_similarity_matcher()
            assert matcher is not None
            
        except ImportError:
            pytest.skip("OpenL3 or soundfile not available for integration test")
