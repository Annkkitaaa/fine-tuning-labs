from typing import List, Dict, Optional
import numpy as np
import nltk
from nltk.corpus import wordnet
from googletrans import Translator
import random

nltk.download('wordnet')

class DataAugmenter:
    def __init__(self):
        self.translator = Translator()
        
    def synonym_replacement(
        self,
        text: str,
        n_replacements: int = 1,
        pos_tag: Optional[str] = None
    ) -> str:
        words = text.split()
        new_words = words.copy()
        
        word_indices = list(range(len(words)))
        random.shuffle(word_indices)
        
        replacements_made = 0
        for idx in word_indices:
            if replacements_made >= n_replacements:
                break
                
            word = words[idx]
            synonyms = []
            
            for syn in wordnet.synsets(word):
                if pos_tag and syn.pos() != pos_tag:
                    continue
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.append(lemma.name())
            
            if synonyms:
                new_words[idx] = random.choice(synonyms)
                replacements_made += 1
        
        return ' '.join(new_words)
    
    def back_translation(
        self,
        text: str,
        intermediate_lang: str = 'fr'
    ) -> str:
        try:
            intermediate = self.translator.translate(text, dest=intermediate_lang)
            back_translated = self.translator.translate(intermediate.text, dest='en')
            return back_translated.text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text
    
    def random_insertion(
        self,
        text: str,
        n_insertions: int = 1
    ) -> str:
        words = text.split()
        new_words = words.copy()
        
        for _ in range(n_insertions):
            word = random.choice(words)
            synonyms = []
            
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.append(lemma.name())
            
            if synonyms:
                random_synonym = random.choice(synonyms)
                random_idx = random.randint(0, len(new_words))
                new_words.insert(random_idx, random_synonym)
        
        return ' '.join(new_words)
    
    def random_swap(
        self,
        text: str,
        n_swaps: int = 1
    ) -> str:
        words = text.split()
        new_words = words.copy()
        
        for _ in range(n_swaps):
            if len(new_words) >= 2:
                idx1, idx2 = random.sample(range(len(new_words)), 2)
                new_words[idx1], new_words[idx2] = new_words[idx2], new_words[idx1]
        
        return ' '.join(new_words)