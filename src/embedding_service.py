from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class EmbeddingService:
    def __init__(self, collection_name="schema_elements"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.chroma_client.get_or_create_collection(collection_name)

    def embed(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def add_documents(self, docs):
        # docs: list of dicts with 'id' and 'text'
        texts = [doc['text'] for doc in docs]
        ids = [doc['id'] for doc in docs]
        embeddings = self.embed(texts)
        self.collection.add(documents=texts, ids=ids, embeddings=embeddings)

    def semantic_search(self, query, n_results=5):
        embedding = self.embed([query])[0]
        results = self.collection.query(query_embeddings=[embedding], n_results=n_results)
        return results

    def embed_schema_metadata(self, metadata):
        # metadata: output from SchemaParser.extract_metadata()
        docs = []
        for model, info in metadata.get("models", {}).items():
            text = f"Model: {model}. Columns: {', '.join(info.get('columns', []))}. "
            if "description" in info:
                text += f"Description: {info['description']}"
            docs.append({"id": f"model_{model}", "text": text})
        for doc_name, doc_text in metadata.get("docs", {}).items():
            docs.append({"id": f"doc_{doc_name}", "text": doc_text})
        self.add_documents(docs) 