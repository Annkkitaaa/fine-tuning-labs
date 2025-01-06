from typing import List, Dict, Union, Optional
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class DataPreprocessor:
    def __init__(self):
        self.scalers: Dict[str, Union[StandardScaler, MinMaxScaler]] = {}
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.tfidf_vectorizer = TfidfVectorizer()
        
    def preprocess_numerical(
        self,
        data: Union[np.ndarray, pd.DataFrame],
        columns: List[str],
        scaler_type: str = 'standard'
    ) -> np.ndarray:
        for col in columns:
            if col not in self.scalers:
                self.scalers[col] = StandardScaler() if scaler_type == 'standard' else MinMaxScaler()
            
            if isinstance(data, pd.DataFrame):
                data[col] = self.scalers[col].fit_transform(data[col].values.reshape(-1, 1))
            else:
                col_idx = columns.index(col)
                data[:, col_idx] = self.scalers[col].fit_transform(data[:, col_idx].reshape(-1, 1)).ravel()
        
        return data
    
    def preprocess_categorical(
        self,
        data: Union[np.ndarray, pd.DataFrame],
        columns: List[str]
    ) -> np.ndarray:
        for col in columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            
            if isinstance(data, pd.DataFrame):
                data[col] = self.label_encoders[col].fit_transform(data[col])
            else:
                col_idx = columns.index(col)
                data[:, col_idx] = self.label_encoders[col].fit_transform(data[:, col_idx])
        
        return data
    
    def preprocess_text(
        self,
        texts: List[str],
        remove_stopwords: bool = True,
        lowercase: bool = True
    ) -> np.ndarray:
        processed_texts = []
        stop_words = set(stopwords.words('english')) if remove_stopwords else set()
        
        for text in texts:
            if lowercase:
                text = text.lower()
            
            tokens = word_tokenize(text)
            if remove_stopwords:
                tokens = [t for t in tokens if t not in stop_words]
            
            processed_texts.append(' '.join(tokens))
        
        return self.tfidf_vectorizer.fit_transform(processed_texts)
