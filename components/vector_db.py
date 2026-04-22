import uuid
from datetime import datetime
from typing import List, Dict, Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class LongTermMemory:
    def __init__(self):
        """
        Unified Long-Term Memory:
        - FAISS vector DB
        - Sentence embeddings
        - Tool-aware structured memory
        """

        # -------------------------
        # Embedding model
        # -------------------------
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384

        # FAISS index
        self.index = faiss.IndexFlatL2(self.dim)

        # metadata store
        self.store: List[Dict[str, Any]] = []

    # =====================================================
    # 🔹 Build embedding text
    # =====================================================
    def build_embedding_text(self, parsed: dict, query: str) -> str:
        tool_info = []

        for call, res in zip(
            parsed.get("tool_calls", []),
            parsed.get("tool_results", [])
        ):
            tool_info.append(
                f"{call.get('tool_name')}({call.get('args')}) → {res.get('response')}"
            )

        return f"""
            User: {query}

            Answer: {parsed.get('text')}

            Tools Used:
            {chr(10).join(tool_info)}
            """.strip()

    # =====================================================
    # 🔹 Add to memory
    # =====================================================
    def add(self, parsed: dict, query: str):
        """
        Store conversation + tool usage into vector DB
        """

        memory_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        embedding_text = self.build_embedding_text(parsed, query)

        tool_names = [
            t.get("tool_name") for t in parsed.get("tool_calls", [])
        ]

        memory_item = {
            "id": memory_id,
            "timestamp": timestamp,
            "query": query,
            "final_answer": parsed.get("text"),
            "tool_calls": parsed.get("tool_calls", []),
            "tool_results": parsed.get("tool_results", []),
            "embedding_text": embedding_text,
            "meta": {
                "type": "conversation",
                "tools_used": tool_names,
            }
        }

        # -------------------------
        # Vector embedding
        # -------------------------
        vector = self.model.encode([embedding_text])[0]
        vector = np.array([vector]).astype("float32")

        # store in FAISS
        self.index.add(vector)

        # store metadata
        self.store.append(memory_item)

        return memory_item

    # =====================================================
    # 🔹 Search memory
    # =====================================================
    def search(self, query: str, k: int = 3):
        """
        Semantic search over past conversations
        """

        query_vec = self.model.encode([query])[0]
        query_vec = np.array([query_vec]).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_vec, k)

        results = []

        for i in indices[0]:
            if 0 <= i < len(self.store):
                results.append(self.store[i])

        return results


vector_memory = LongTermMemory()