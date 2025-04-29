from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import numpy as np

class DocumentSearch:
    def __init__(self, csv_path='cleaned_url_data.csv'):
        self.df = pd.read_csv(csv_path)
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self._build_tfidf_matrix()

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        return text

    def _build_tfidf_matrix(self):
        blobs = zip(self.df["Abstract"], self.df["Title"], self.df["KMeansTags"])
        blobs_to_search = [
            f"Title: {self.clean_text(title)} Abstract: {self.clean_text(abstract)}  Tags: {self.clean_text(tags)}"
            for abstract, title, tags in blobs
        ]
        return self.tfidf_vectorizer.fit_transform(blobs_to_search)

    def search(self, querry, num_results):
        tag_boost = 0.1
        cleaned_querry = self.clean_text(querry)
        query_vector = self.tfidf_vectorizer.transform([cleaned_querry])

        # Calculate cosine similarity between the user query and all documents
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        results = []

        # Add a bonus if tags match search
        for i, tags in enumerate(self.df["KMeansTags"]):
            tags = self.clean_text(tags).split(' ')
            if set(querry.split(' ')) & set(tags):
                cosine_similarities[i] += tag_boost  

        # Get the index of the most similar document
        most_similar_document_index = cosine_similarities.argsort()
        # reverse array
        most_similar_document_index = most_similar_document_index[::-1]

        for idx in range(num_results):
            doc_index = most_similar_document_index[idx]
            result = {
                "url": self.df["URL"][doc_index],
                "title": self.df["Title"][doc_index],
                "authors": self.df["Authors"][doc_index],
                "tags": self.df["KMeansTags"][doc_index],
                "abstract": self.df["Abstract"][doc_index],
                "similarity": cosine_similarities[doc_index]
            }
            results.append(result)
        

        return results