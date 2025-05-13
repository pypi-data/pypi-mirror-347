from abc import ABC, abstractmethod
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from sentence_transformers import CrossEncoder
from MetaRagTool import Constants


class MyReranker(ABC):

    def __init__(self, model_name: str, verbose=False):
        self.verbose = verbose
        self.model_name = model_name

    @abstractmethod
    def get_scores(self, query:str, chunks: list):
        pass


    def apply_rerank_raw_texts(self, query: str, chunks: list):
        scores = self.get_scores(query=query, chunks=chunks)
        sorted_chunks = [x for _, x in sorted(zip(scores, chunks), reverse=True)]
        return sorted_chunks

    def apply_rerank_MyChunks(self, query: str, chunks: list):
        chunk_texts = [chunk.Text for chunk in chunks]
        scores = self.get_scores(query=query, chunks=chunk_texts)
        sorted_chunks = [x for _, x in sorted(zip(scores, chunks), key=lambda pair: pair[0], reverse=True)]
        return sorted_chunks

class CrossEncoderReranker(MyReranker):
    MODEL_NSME_ms_marco_MiniLM_L_6_v2_Local = "D:\\Library\\MSc Ai\\Thesis\\Persian RAG\\Models\\rerankers\\crossEncoders\\ms-marco-MiniLM-L6-v2"
    MODEL_NSME_ms_marco_MiniLM_L_6_v2_HF="cross-encoder/ms-marco-MiniLM-L-6-v2"
    def __init__(self, model_name: str =None, verbose=False):
        if model_name is None:
            model_name = CrossEncoderReranker.MODEL_NSME_ms_marco_MiniLM_L_6_v2_Local if Constants.local_mode else CrossEncoderReranker.MODEL_NSME_ms_marco_MiniLM_L_6_v2_HF

        super().__init__(model_name, verbose)
        self.model = CrossEncoder(model_name)

    def get_scores(self, query: str, chunks: list):
        sentence_pairs = [[query, doc] for doc in chunks]
        scores = self.model.predict(sentence_pairs)
        return scores


class JinaRerankerV2(MyReranker):
    def __init__(self, model_name: str = "jinaai/jina-reranker-v2-base-multilingual", verbose=False):
        super().__init__(model_name, verbose)

        # Load the Jina Reranker v2 model and tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype="auto",
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def get_scores(self, query: str, chunks: list):
        # Create sentence pairs for the model
        sentence_pairs = [[query, doc] for doc in chunks]

        # Tokenize the input
        inputs = self.tokenizer(sentence_pairs, padding=True, truncation=True, return_tensors="pt", max_length=1024)

        # Get the model's predictions
        with torch.no_grad():
            scores = self.model(**inputs).logits

        # Return the scores for each document
        return scores.float().numpy().tolist()

