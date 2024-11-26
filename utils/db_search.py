from deprecated import deprecated
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import pymongo.collection
import numpy as np
from numpy.linalg import norm
import faiss


def faiss_similarity_search(collection: pymongo.collection.Collection, query: str, embedding: OpenAIEmbeddings, embedding_key: str = "embedding", k: int = 4, threshold: float = 0.10, include_score: bool = False) -> list[dict]:
    """
    Perform similarity search using FAISS library on a MongoDB collection.

    Args:
    - collection: The MongoDB collection to search.
    - query: The query string for similarity search.
    - embedding: The OpenAI embeddings model to generate embeddings.
    - embedding_key: The key in the MongoDB documents that contains the embeddings.
    - k: The number of top-k results to return.
    - threshold: The minimum similarity score threshold for results.
    - include_score: Whether to include the similarity score in the results.

    Returns:
    - A list of dictionaries, each containing a MongoDB document and its similarity score.
    """
    def build_faiss_index(embeddings: np.ndarray, d: int):
        """Build a FAISS index for fast similarity search."""
        # Create a FAISS index (L2 by default, adjust to cosine if needed)
        index = faiss.IndexFlatL2(d)  # d is the dimension of embeddings
        index.add(embeddings)         # Add embeddings to the index
        return index

    # Get all items and their embeddings
    items = list(collection.find({}))
    embeddings = np.array([item[embedding_key] for item in items])

    # Precompute the query embedding
    query_embedding = np.array(embedding.embed_query(query))

    # Build FAISS index
    d = len(query_embedding)  # Dimension of embeddings
    index = build_faiss_index(embeddings, d)

    # Search the FAISS index for top-k results
    query_embedding = query_embedding.reshape(1, -1)  # Reshape for FAISS
    distances, indices = index.search(query_embedding, k)

    # Gather the top-k items based on FAISS index results
    top_k_items = []
    for i, idx in enumerate(indices[0]):
        item = items[idx]
        item['score'] = 1 - distances[0][i] / 2  # Convert L2 back to cosine similarity
        if item['score'] >= threshold:
            top_k_items.append(item)

    # Optionally, remove embedding and scores from result
    for item in top_k_items:
        del item[embedding_key]
        if not include_score:
            del item['score']

    return top_k_items


def atlas_similarity_search(collection:pymongo.collection.Collection, query:str, embedding:OpenAIEmbeddings, k:int=4, threshold:float=0.10) -> list[dict]:
    """
    Perform similarity search using MongoDB Atlas Vector Search on a MongoDB collection.

    Args:
    - collection: The MongoDB collection to search.
    - query: The query string for similarity search.
    - embedding: The OpenAI embeddings model to generate embeddings.
    - k: The number of top-k results to return.
    - threshold: The minimum similarity score threshold for results.

    Returns:
    - A list of dictionaries, each containing a MongoDB document and its similarity score.
    """
    vector_store = MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=embedding,
        index_name="vector_index",
        relevance_score_fn="cosine",
        text_key="answer"
    )

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": k, "score_threshold": threshold},
    )

    return retriever.invoke(query)


@deprecated("use tools.mongodb_search.similarity_search function instead.")
def similarity_search_old(collection:pymongo.collection.Collection, query:str, embedding:OpenAIEmbeddings, k:int=4, threshold:float=0.10, include_score:bool=False) -> list[dict]:
    items = list(collection.find({}))
    for item in items:
        emb = item['embedding']

        a = emb
        b = embedding.embed_query(query)

        cosine = np.dot(a,b)/(norm(a)*norm(b))
        
        item['score']=cosine

    filtered_items = filter(lambda d: d['score']>=threshold, items)
    
    sorted_items = sorted(filtered_items, reverse=True, key=lambda d: d['score'])

    sorted_items = sorted_items[:k]
    
    for item in sorted_items:
        del item['embedding']
        if not include_score: del item['score'] 

    return sorted_items