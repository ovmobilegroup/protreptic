from sentence_transformers import SentenceTransformer
import faiss
import json
import os
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import time

# Global model cache to avoid reloading
_model_cache = {}

# Global flag to indicate if dependencies are available
SEMANTIC_DEPS_AVAILABLE = True

class SemanticSearchEngine:
    """Semantic search engine using BGE-m3 + FAISS."""
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        index_path: Optional[str] = None,
        data_path: Optional[str] = None,
        device: str = "cpu"
    ):
        if not SEMANTIC_DEPS_AVAILABLE:
            raise RuntimeError(
                "Semantic search dependencies not installed. "
                "Install with: pip install sentence-transformers faiss-cpu"
            )
        
        self.model_name = model_name
        self.device = device
        self.index_path = index_path if index_path else "<repo>/api/data/semantic_index.faiss"
        self.data_path = data_path if data_path else "<repo>/api/data/scenarios_zh.json"
        self.metadata_path = self.index_path.replace(".faiss", "_metadata.pkl")
        
        # Initialize FAISS index
        self.index = None
        self.scenarios = []  # List of scenario dicts
        self.code_to_idx = {}  # code -> index mapping
        self.model = None
        
        # Load or build index
        self._load_or_build_index()
    
    def _load_or_build_index(self):
        """Load existing index or build new one."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print(f"Loading existing index from {self.index_path}")
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                self.scenarios = metadata['scenarios']
                self.code_to_idx = metadata['code_to_idx']
            print(f"Loaded {len(self.scenarios)} scenarios")
            
            # Load model from cache if available
            model_key = f"{self.model_name}_{self.device}"
            if model_key in _model_cache:
                self.model = _model_cache[model_key]
                self.embedding_dim = self.model.get_embedding_dimension()
            else:
                print(f"Loading model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name, device=self.device)
                _model_cache[model_key] = self.model
                self.embedding_dim = self.model.get_embedding_dimension()
        else:
            print("Building new semantic index...")
            self._build_index()
    
    def _build_index(self):
        """Build FAISS index from scenario data."""
        # Load scenario data from tools directory which contains all 421 scenarios
        tools_zh_path = Path("<repo>/tools/scenarios_zh.json")
        tools_en_path = Path("<repo>/tools/scenarios_en.json")
        
        if tools_zh_path.exists() and tools_en_path.exists():
            print(f"Loading from tools directory with all 421 scenarios")
            with open(tools_zh_path, 'r', encoding='utf-8') as f:
                scenarios_zh = json.load(f)
            with open(tools_en_path, 'r', encoding='utf-8') as f:
                scenarios_en = json.load(f)
        else:
            # Fallback to the configured data path if tools directory doesn't exist
            print(f"Tools directory not found, falling back to configured path: {self.data_path}")
            with open(self.data_path, 'r', encoding='utf-8') as f:
                scenarios_zh = json.load(f)
            with open(self.data_path.replace('zh', 'en'), 'r', encoding='utf-8') as f:
                scenarios_en = json.load(f)
        
        print(f"Building full index with {len(scenarios_zh)} scenarios")
        
        # Prepare texts for embedding
        texts = []
        self.scenarios = []
        
        for code, zh_data in scenarios_zh.items():
            en_data = scenarios_en.get(code, {})
            
            # Combine fields for embedding
            text_parts = [
                zh_data.get('name', ''),
                zh_data.get('description', ''),
                zh_data.get('reason', ''),
            ]
            text = " ".join(filter(None, text_parts))
            
            texts.append(text)
            
            scenario = {
                'code': code,
                'name': zh_data.get('name', ''),
                'name_en': en_data.get('name', ''),
                'description': zh_data.get('description', ''),
                'description_en': en_data.get('description', ''),
                'reason': zh_data.get('reason', ''),
                'reason_en': en_data.get('reason', ''),
                'modes': zh_data.get('modes', []),
            }
            self.scenarios.append(scenario)
        
        print(f"Encoding {len(texts)} scenarios...")
        
        # Load model if not already cached
        model_key = f"{self.model_name}_{self.device}"
        if model_key not in _model_cache:
            print(f"Loading model: {self.model_name}")
            _model_cache[model_key] = SentenceTransformer(self.model_name, device=self.device)
        self.model = _model_cache[model_key]
        
        self.embedding_dim = self.model.get_embedding_dimension()
        
        # Use optimized batch size for speed
        start_time = time.time()
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # For cosine similarity
        )
        encoding_time = time.time() - start_time
        print(f"Encoding completed in {encoding_time:.2f}s ({len(texts)} texts)")
        
        # Build FAISS index (Inner Product for cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings.astype(np.float32))
        
        # Build code to index mapping
        self.code_to_idx = {s['code']: i for i, s in enumerate(self.scenarios)}
        
        # Save index and metadata
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump({
                'scenarios': self.scenarios,
                'code_to_idx': self.code_to_idx,
            }, f)
        
        print(f"Built full index with {len(self.scenarios)} scenarios, dim={self.embedding_dim}")
    
    def search(self, query: str, top_k: int = 10, lang: str = "zh") -> tuple[List[Dict[str, Any]], float]:
        """Search for similar scenarios."""
        if self.index is None:
            raise RuntimeError("Index not loaded")
        
        # Encode query
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True
        ).astype(np.float32)
        
        # Search
        start_time = time.time()
        scores, indices = self.index.search(query_embedding, top_k)
        search_time = time.time() - start_time
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.scenarios):
                scenario = self.scenarios[idx]
                result = {
                    'code': scenario['code'],
                    'name': scenario['name'] if lang == 'zh' else scenario['name_en'],
                    'description': scenario['description'] if lang == 'zh' else scenario['description_en'],
                    'reason': scenario['reason'] if lang == 'zh' else scenario['reason_en'],
                    'modes': scenario['modes'],
                    'score': float(score),
                }
                results.append(result)
        
        return results, search_time
    
    def get_similar(self, code: str, top_k: int = 5, lang: str = "zh") -> tuple[List[Dict[str, Any]], float]:
        """Find scenarios similar to a given code."""
        if code not in self.code_to_idx:
            raise ValueError(f"Code {code} not found in index")
        
        idx = self.code_to_idx[code]
        # Get the vector for this code
        vector = self.index.reconstruct(idx).reshape(1, -1)
        
        # Search (exclude self by searching top_k+1)
        start_time = time.time()
        scores, indices = self.index.search(vector, top_k + 1)
        search_time = time.time() - start_time
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != self.code_to_idx[code] and idx < len(self.scenarios):
                scenario = self.scenarios[idx]
                results.append({
                    'code': scenario['code'],
                    'name': scenario['name'] if lang == 'zh' else scenario['name_en'],
                    'description': scenario['description'] if lang == 'zh' else scenario['description_en'],
                    'reason': scenario['reason'] if lang == 'zh' else scenario['reason_en'],
                    'modes': scenario['modes'],
                    'score': float(score),
                })
                if len(results) >= top_k:
                    break
        
        return results, search_time
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            'total_scenarios': len(self.scenarios),
            'embedding_dim': self.embedding_dim,
            'model': self.model_name,
            'index_type': type(self.index).__name__,
            'device': self.device,
            'index_path': self.index_path,
            'metadata_path': self.metadata_path,
        }


def create_semantic_search_engine(
    model_name: str = "BAAI/bge-m3",
    index_path: Optional[str] = None,
    data_path: Optional[str] = None,
    device: str = "cpu"
) -> SemanticSearchEngine:
    """Factory function to create semantic search engine."""
    base_dir = Path(__file__).parent.parent
    default_index = base_dir / "api" / "data" / "semantic_index.faiss"
    
    # Use the provided data path if available, otherwise use the api/data path
    if data_path is None:
        default_data = base_dir / "api" / "data" / "scenarios_zh.json"
    else:
        default_data = Path(data_path)
    
    return SemanticSearchEngine(
        model_name=model_name,
        index_path=index_path or str(default_index),
        data_path=str(default_data),
        device=device
    )