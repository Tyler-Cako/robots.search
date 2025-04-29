from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class DocumentSearch:
    def __init__(self, csv_path='cleaned_url_data.csv'):
        self.df = pd.read_csv(csv_path)
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self._build_tfidf_matrix()
        self._preprocess()

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        return text

    def _str_to_list(self, s, delimiter=','):
        authors = s.split(delimiter)
        authors = [author.strip() for author in authors]
        return authors

    def _preprocess(self):
        self.df.loc[:,"Authors"] = [self._str_to_list(authors) for authors in self.df["Authors"]]
        self.df.loc[:,"KMeansTags"] = [self._str_to_list(tags[2:-2], delimiter="', '") for tags in self.df["KMeansTags"]] 

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


class Recommender:
    def __init__(self, csv_path='cleaned_url_data.csv'):
        self.df = pd.read_csv(csv_path, dtype={"Authors": str, "KMeansTags": object})
        self._preprocess()

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        return text

    def _str_to_list(self, s, delimiter=','):
        authors = s.split(delimiter)
        authors = [author.strip() for author in authors]
        return authors

    def _preprocess(self):
        self.df.loc[:,"Authors"] = [self._str_to_list(authors) for authors in self.df["Authors"]]
        self.df.loc[:,"KMeansTags"] = [self._str_to_list(tags[2:-2], delimiter="', '") for tags in self.df["KMeansTags"]]    
        

    def find_similar(self, ref_idx=0, n=10):
        paper_count = self.df.shape[0]

        assert ref_idx < paper_count
        assert n <= paper_count

        ref_authors = set(self.df["Authors"][ref_idx])
        ref_kw = set(self.df["KMeansTags"][ref_idx])
        
        similarities = []
        for paper in range(paper_count):
            authors_set = set(self.df["Authors"][paper])
            kw_set = set(self.df["KMeansTags"][paper])
            
            authors_intersection = authors_set.intersection(ref_authors)
            authors_union = authors_set.union(ref_authors)

            kw_intersection = kw_set.intersection(ref_kw)
            kw_union = kw_set.union(ref_kw)

            similarity_score = len(authors_intersection)/len(authors_union) + len(kw_intersection)/len(kw_union)
            similarities.append(similarity_score)

        similarity_tups = list(zip(range(paper_count), similarities))
        similarity_tups = [tup for tup in similarity_tups if tup[0] != ref_idx and tup[1] != 2]
        similarity_tups.sort(key=lambda tup: tup[1], reverse=True)
        top_matches = similarity_tups[:n]

        results = []
        for idx, score in top_matches:
            result = {
                "url": self.df["URL"][idx],
                "title": self.df["Title"][idx],
                "authors": self.df["Authors"][idx],
                "tags": self.df["KMeansTags"][idx],
                "abstract": self.df["Abstract"][idx],
                "similarity": round(score, 4)
            }
            results.append(result)

        return results